/*
Created on Fri Jun 26 14:13:26 2020
Copyright (C) 2020 Peter Rakyta, Ph.D.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.

@author: Peter Rakyta, Ph.D.
*/
/*! \file N_Qubit_Decomposition.cpp
    \brief Base class to determine the decomposition of a unitary into a sequence of two-qubit and one-qubit gate gates.
    This class contains the non-template implementation of the decomposition class
*/

#include "N_Qubit_Decomposition_Base.h"
#include "N_Qubit_Decomposition_Cost_Function.h"
#include "Adam.h"

#include <fstream>


#ifdef __DFE__
#include "common_DFE.h"
#endif


static double adam_time = 0;
static double bfgs_time = 0;
static double pure_DFE_time = 0;


/**
@brief Nullary constructor of the class.
@return An instance of the class
*/
N_Qubit_Decomposition_Base::N_Qubit_Decomposition_Base() {

    // logical value. Set true if finding the minimum number of gate layers is required (default), or false when the maximal number of two-qubit gates is used (ideal for general unitaries).
    optimize_layer_num  = false;

    // A string describing the type of the class
    type = N_QUBIT_DECOMPOSITION_CLASS;

    // The global minimum of the optimization problem
    global_target_minimum = 0;

    // logical variable indicating whether adaptive learning reate is used in the ADAM algorithm
    adaptive_eta = true;

    // parameter to contron the radius of parameter randomization around the curren tminimum
    radius = 1.0;
    randomization_rate = 0.3;

    // The chosen variant of the cost function
    cost_fnc = FROBENIUS_NORM;


    prev_cost_fnv_val = 0.0;
    //
    correction1_scale = 1/1.7;
    correction2_scale = 1/2.0;  

    iteration_threshold_of_randomization = 2500000;

    // number of utilized accelerators
    accelerator_num = 0;

    // unique id indentifying the instance of the class
    std::uniform_int_distribution<> distrib_int(0, INT_MAX);  
    int id = distrib_int(gen);

}

/**
@brief Constructor of the class.
@param Umtx_in The unitary matrix to be decomposed
@param qbit_num_in The number of qubits spanning the unitary Umtx
@param optimize_layer_num_in Optional logical value. If true, then the optimization tries to determine the lowest number of the layers needed for the decomposition. If False (default), the optimization is performed for the maximal number of layers.
@param initial_guess_in Enumeration element indicating the method to guess initial values for the optimization. Possible values: 'zeros=0' ,'random=1', 'close_to_zero=2'
@return An instance of the class
*/
N_Qubit_Decomposition_Base::N_Qubit_Decomposition_Base( Matrix Umtx_in, int qbit_num_in, bool optimize_layer_num_in, guess_type initial_guess_in= CLOSE_TO_ZERO, int accelerator_num_in ) : Decomposition_Base(Umtx_in, qbit_num_in, initial_guess_in) {

    // logical value. Set true if finding the minimum number of gate layers is required (default), or false when the maximal number of two-qubit gates is used (ideal for general unitaries).
    optimize_layer_num  = optimize_layer_num_in;

    // A string describing the type of the class
    type = N_QUBIT_DECOMPOSITION_CLASS;

    // The global minimum of the optimization problem
    global_target_minimum = 0;

    // number of iteratrion loops in the optimization
    iteration_loops[2] = 3;

    // filling in numbers that were not given in the input
    for ( std::map<int,int>::iterator it = max_layer_num_def.begin(); it!=max_layer_num_def.end(); it++) {
        if ( max_layer_num.count( it->first ) == 0 ) {
            max_layer_num.insert( std::pair<int, int>(it->first,  it->second) );
        }
    }

    // logical variable indicating whether adaptive learning reate is used in the ADAM algorithm
    adaptive_eta = true;

    // parameter to contron the radius of parameter randomization around the curren tminimum
    radius = 1.0;
    randomization_rate = 0.3;

    // The chosen variant of the cost function
    cost_fnc = FROBENIUS_NORM;

    prev_cost_fnv_val = 0.0;
    //
    correction1_scale = 1/1.7;
    correction2_scale = 1/2.0; 

    iteration_threshold_of_randomization = 2500000;


    // unique id indentifying the instance of the class
    std::uniform_int_distribution<> distrib_int(0, INT_MAX);  
    id = distrib_int(gen);


#ifdef __DFE__

    // number of utilized accelerators
    accelerator_num = accelerator_num_in;
#else
    accelerator_num = 0;
#endif

}



/**
@brief Destructor of the class
*/
N_Qubit_Decomposition_Base::~N_Qubit_Decomposition_Base() {


#ifdef __DFE__
    unload_dfe_lib();//releive_DFE();
#endif      


}


/**
@brief Call to add further layer to the gate structure used in the subdecomposition.
*/
void 
N_Qubit_Decomposition_Base::add_finalyzing_layer() {


    // creating block of gates
    Gates_block* block = new Gates_block( qbit_num );

    // adding U3 gate to the block
    bool Theta = true;
    bool Phi = false;
    bool Lambda = true;

    for (int qbit=0; qbit<qbit_num; qbit++) {
        block->add_u3(qbit, Theta, Phi, Lambda);
    }

    // adding the opeartion block to the gates
    add_gate( block );

}




/**
@brief Calculate the error of the decomposition according to the spectral norm of \f$ U-U_{approx} \f$, where \f$ U_{approx} \f$ is the unitary produced by the decomposing quantum cirquit.
@param decomposed_matrix The decomposed matrix, i.e. the result of the decomposing gate structure applied on the initial unitary.
@return Returns with the calculated spectral norm.
*/
void
N_Qubit_Decomposition_Base::calc_decomposition_error(Matrix& decomposed_matrix ) {

	// (U-U_{approx}) (U-U_{approx})^\dagger = 2*I - U*U_{approx}^\dagger - U_{approx}*U^\dagger
	// U*U_{approx}^\dagger = decomposed_matrix_copy
	
 	Matrix A(matrix_size, matrix_size);
	QGD_Complex16* A_data = A.get_data();
	QGD_Complex16* decomposed_data = decomposed_matrix.get_data();
	QGD_Complex16 phase;
	phase.real = decomposed_matrix[0].real/(std::sqrt(decomposed_matrix[0].real*decomposed_matrix[0].real + decomposed_matrix[0].imag*decomposed_matrix[0].imag));
	phase.imag = -decomposed_matrix[0].imag/(std::sqrt(decomposed_matrix[0].real*decomposed_matrix[0].real + decomposed_matrix[0].imag*decomposed_matrix[0].imag));

	for (int idx=0; idx<matrix_size; idx++ ) {
		for (int jdx=0; jdx<matrix_size; jdx++ ) {
			
			if (idx==jdx) {
				QGD_Complex16 mtx_val = mult(phase, decomposed_data[idx*matrix_size+jdx]);
				A_data[idx*matrix_size+jdx].real = 2.0 - 2*mtx_val.real;
				A_data[idx*matrix_size+jdx].imag = 0;
			}
			else {
				QGD_Complex16 mtx_val_ij = mult(phase, decomposed_data[idx*matrix_size+jdx]);
				QGD_Complex16 mtx_val_ji = mult(phase, decomposed_data[jdx*matrix_size+idx]);
				A_data[idx*matrix_size+jdx].real = - mtx_val_ij.real - mtx_val_ji.real;
				A_data[idx*matrix_size+jdx].imag = - mtx_val_ij.imag + mtx_val_ji.imag;
			}

		}
	}


	Matrix alpha(matrix_size, 1);
	Matrix beta(matrix_size, 1);
	Matrix B = create_identity(matrix_size);

	// solve the generalized eigenvalue problem of I- 1/2
	LAPACKE_zggev( CblasRowMajor, 'N', 'N',
                          matrix_size, A.get_data(), matrix_size, B.get_data(),
                          matrix_size, alpha.get_data(),
                          beta.get_data(), NULL, matrix_size, NULL,
                          matrix_size );

	// determine the largest eigenvalue
	double eigval_max = 0;
	for (int idx=0; idx<matrix_size; idx++) {
		double eigval_abs = std::sqrt((alpha[idx].real*alpha[idx].real + alpha[idx].imag*alpha[idx].imag) / (beta[idx].real*beta[idx].real + beta[idx].imag*beta[idx].imag));
		if ( eigval_max < eigval_abs ) eigval_max = eigval_abs;		
	}

	// the norm is the square root of the largest einegvalue.
	decomposition_error = std::sqrt(eigval_max);


}



/**
@brief final optimization procedure improving the accuracy of the decompositin when all the qubits were already disentangled.
*/
void  N_Qubit_Decomposition_Base::final_optimization() {

	//The stringstream input to store the output messages.
	std::stringstream sstream;
	sstream << "***************************************************************" << std::endl;
	sstream << "Final fine tuning of the parameters in the " << qbit_num << "-qubit decomposition" << std::endl;
	sstream << "***************************************************************" << std::endl;
	print(sstream, 1);	    	

         


        //# setting the global minimum
        global_target_minimum = 0;


        if ( optimized_parameters_mtx.size() == 0 ) {
            solve_optimization_problem(NULL, 0);
        }
        else {
            current_minimum = optimization_problem(optimized_parameters_mtx.get_data());
            if ( check_optimization_solution() ) return;

            solve_optimization_problem(optimized_parameters_mtx.get_data(), parameter_num);
        }
}


/**
@brief Call to solve layer by layer the optimization problem via calling one of the implemented algorithms. The optimalized parameters are stored in attribute optimized_parameters.
@param num_of_parameters Number of parameters to be optimized
@param solution_guess_gsl A GNU Scientific Library vector containing the solution guess.
*/
void N_Qubit_Decomposition_Base::solve_layer_optimization_problem( int num_of_parameters, gsl_vector *solution_guess_gsl) {


    switch ( alg ) {
        case ADAM:
            solve_layer_optimization_problem_ADAM( num_of_parameters, solution_guess_gsl);
            return;
        case BFGS:
            solve_layer_optimization_problem_BFGS( num_of_parameters, solution_guess_gsl);
            return;
        case BFGS2:
            solve_layer_optimization_problem_BFGS2( num_of_parameters, solution_guess_gsl);
            return;
        default:
            std::string error("N_Qubit_Decomposition_Base::solve_layer_optimization_problem: unimplemented optimization algorithm");
            throw error;
    }


}


/**
@brief Call to solve layer by layer the optimization problem via ADAM algorithm. (optimal for larger problems) The optimalized parameters are stored in attribute optimized_parameters.
@param num_of_parameters Number of parameters to be optimized
@param solution_guess_gsl A GNU Scientific Library vector containing the solution guess.
*/
void N_Qubit_Decomposition_Base::solve_layer_optimization_problem_ADAM( int num_of_parameters, gsl_vector *solution_guess_gsl) {

#ifdef __DFE__
        if ( qbit_num >= 5 ) {
            upload_Umtx_to_DFE();
        }
#endif



        if (gates.size() == 0 ) {
            return;
        }


        if (solution_guess_gsl == NULL) {
            solution_guess_gsl = gsl_vector_alloc(num_of_parameters);
        }
//memset( solution_guess_gsl->data, 0.0, solution_guess_gsl->size*sizeof(double) );

        if (optimized_parameters_mtx.size() == 0) {
            optimized_parameters_mtx = Matrix_real(1, num_of_parameters);
            memcpy(optimized_parameters_mtx.get_data(), solution_guess_gsl->data, num_of_parameters*sizeof(double) );
        }


        int random_shift_count = 0;
        int sub_iter_idx = 0;
        double current_minimum_hold = current_minimum;
    

        tbb::tick_count adam_start = tbb::tick_count::now();
        adam_time = 0.0;
pure_DFE_time = 0.0;
        Adam optimizer;
        optimizer.initialize_moment_and_variance( num_of_parameters );



        // the array storing the optimized parameters
        gsl_vector* grad_gsl = gsl_vector_alloc(num_of_parameters);
        gsl_vector* solution_guess_tmp = gsl_vector_alloc(num_of_parameters);
        memcpy(solution_guess_tmp->data, solution_guess_gsl->data, num_of_parameters*sizeof(double) );

        Matrix_real solution_guess_tmp_mtx = Matrix_real( solution_guess_tmp->data, num_of_parameters, 1 );
        Matrix_real grad_mtx = Matrix_real( grad_gsl->data, num_of_parameters, 1 );
        //solution_guess_tmp_mtx.print_matrix();


        double f0 = DBL_MAX;
        std::stringstream sstream;
        sstream << "iter_max: " << iter_max << ", randomization threshold: " << iteration_threshold_of_randomization << ", randomization radius: " << radius << std::endl;
        print(sstream, 2); 

        int ADAM_status = 0;

        int randomization_successful = 0;

        for ( int iter_idx=0; iter_idx<iter_max; iter_idx++ ) {

            


            optimization_problem_combined( solution_guess_tmp, (void*)(this), &f0, grad_gsl );

            prev_cost_fnv_val = f0;
  
            if (sub_iter_idx == 1 ) {
                current_minimum_hold = f0;   
               
                if ( adaptive_eta )  { 
                    optimizer.eta = optimizer.eta > 1e-3 ? optimizer.eta : 1e-3; 
                    //std::cout << "reset learning rate to " << optimizer.eta << std::endl;
                }                 

            }


            if (current_minimum_hold*0.95 > f0 || (current_minimum_hold*0.97 > f0 && f0 < 1e-3) ||  (current_minimum_hold*0.99 > f0 && f0 < 1e-4) ) {
                sub_iter_idx = 0;
                current_minimum_hold = f0;        
            }
    
    
            if (current_minimum > f0 ) {
                current_minimum = f0;
                memcpy( optimized_parameters_mtx.get_data(),  solution_guess_tmp->data, num_of_parameters*sizeof(double) );
                //double new_eta = 1e-3 * f0 * f0;
                
                if ( adaptive_eta )  {
                    double new_eta = 1e-3 * f0;
                    optimizer.eta = new_eta > 1e-6 ? new_eta : 1e-6;
                    optimizer.eta = new_eta < 1e-1 ? new_eta : 1e-1;
                }
                
                randomization_successful = 1;
            }
    

            if ( iter_idx % 5000 == 0 ) {

                Matrix matrix_new = get_transformed_matrix( optimized_parameters_mtx, gates.begin(), gates.size(), Umtx );

                std::stringstream sstream;
                sstream << "ADAM: processed iterations " << (double)iter_idx/iter_max*100 << "\%, current minimum:" << current_minimum << ", pure cost function:" << get_cost_function(matrix_new) << std::endl;
                print(sstream, 0);   
                std::string filename("initial_circuit_iteration.binary");
                export_gate_list_to_binary(optimized_parameters_mtx, this, filename, verbose);

            }

//std::cout << grad_norm  << std::endl;
            if (f0 < optimization_tolerance || random_shift_count > random_shift_count_max ) {
                break;
            }



                // calculate the gradient norm
                double norm = 0.0;
                for ( int grad_idx=0; grad_idx<num_of_parameters; grad_idx++ ) {
                    norm += grad_gsl->data[grad_idx]*grad_gsl->data[grad_idx];
                }
                norm = std::sqrt(norm);
                
//grad_mtx.print_matrix();
/*
            if ( ADAM_status == 0 && norm > 0.01 && optimizer.eta < 1e-4) {

                std::uniform_real_distribution<> distrib_prob(0.0, 1.0);
                if ( distrib_prob(gen) < 0.05 ) {
                    optimizer.eta = optimizer.eta*10;
                    std::cout << "Increasing learning rate at " << f0 << " to " << optimizer.eta << std::endl;
                }

            }
*/
/*

            if ( ADAM_status == 1 && norm > 0.01 ) {
                optimizer.eta = optimizer.eta > 1e-5 ? optimizer.eta/10 : 1e-6;
                std::cout << "Decreasing learning rate at " << f0 << " to " << optimizer.eta << std::endl;
                ADAM_status = 0;
            }

  */       

            if ( sub_iter_idx> iteration_threshold_of_randomization || ADAM_status != 0 ) {

                //random_shift_count++;
                sub_iter_idx = 0;
                random_shift_count++;
                current_minimum_hold = current_minimum;   


                
                std::stringstream sstream;
                if ( ADAM_status == 0 ) {
                    sstream << "ADAM: initiate randomization at " << f0 << ", gradient norm " << norm << std::endl;
                }
                else {
                    sstream << "ADAM: leaving local minimum " << f0 << ", gradient norm " << norm << " eta: " << optimizer.eta << std::endl;
                }
                print(sstream, 0);   
                    
                randomize_parameters(optimized_parameters_mtx, solution_guess_tmp, randomization_successful, f0 );
                randomization_successful = 0;
        
                optimizer.reset();
                optimizer.initialize_moment_and_variance( num_of_parameters );   

                ADAM_status = 0;   

                //optimizer.eta = 1e-3;
        
            }

            else {
                ADAM_status = optimizer.update(solution_guess_tmp_mtx, grad_mtx, f0);
            }

            sub_iter_idx++;

        }


        sstream.str("");
        sstream << "obtained minimum: " << current_minimum << std::endl;


        gsl_vector_free(grad_gsl);
        gsl_vector_free(solution_guess_tmp);
        tbb::tick_count adam_end = tbb::tick_count::now();
        adam_time  = adam_time + (adam_end-adam_start).seconds();
        sstream << "adam time: " << adam_time << ", pure DFE time:  " << pure_DFE_time << " " << f0 << std::endl;
        
        print(sstream, 0); 

}



/**
@brief Call to solve layer by layer the optimization problem via BBFG algorithm. (optimal for smaller problems) The optimalized parameters are stored in attribute optimized_parameters.
@param num_of_parameters Number of parameters to be optimized
@param solution_guess_gsl A GNU Scientific Library vector containing the solution guess.
*/
void N_Qubit_Decomposition_Base::solve_layer_optimization_problem_BFGS( int num_of_parameters, gsl_vector *solution_guess_gsl) {


#ifdef __DFE__
        if ( qbit_num >= 5 ) {
            upload_Umtx_to_DFE();
        }
#endif

        if (gates.size() == 0 ) {
            return;
        }


        if (solution_guess_gsl == NULL) {
            solution_guess_gsl = gsl_vector_alloc(num_of_parameters);
        }


        if (optimized_parameters_mtx.size() == 0) {
            optimized_parameters_mtx = Matrix_real(1, num_of_parameters);
            memcpy(optimized_parameters_mtx.get_data(), solution_guess_gsl->data, num_of_parameters*sizeof(double) );
        }

        // maximal number of iteration loops
        int iteration_loops_max;
        try {
            iteration_loops_max = std::max(iteration_loops[qbit_num], 1);
        }
        catch (...) {
            iteration_loops_max = 1;
        }

        // random generator of real numbers   
        std::uniform_real_distribution<> distrib_real(0.0, 2*M_PI);


        // do the optimization loops
        for (int idx=0; idx<iteration_loops_max; idx++) {

            int iter = 0;
            int status;

            const gsl_multimin_fdfminimizer_type *T;
            gsl_multimin_fdfminimizer *s;

            N_Qubit_Decomposition_Base* par = this;


            gsl_multimin_function_fdf my_func;


            my_func.n = num_of_parameters;
            my_func.f = optimization_problem;
            my_func.df = optimization_problem_grad;
            my_func.fdf = optimization_problem_combined;
            my_func.params = par;


            T = gsl_multimin_fdfminimizer_vector_bfgs2;
            s = gsl_multimin_fdfminimizer_alloc (T, num_of_parameters);

            gsl_multimin_fdfminimizer_set(s, &my_func, solution_guess_gsl, 0.01, 0.1);

            do {
                iter++;
                gsl_set_error_handler_off();
                status = gsl_multimin_fdfminimizer_iterate (s);

                if (status) {
                  break;
                }

                status = gsl_multimin_test_gradient (s->gradient, gradient_threshold);

            } while (status == GSL_CONTINUE && iter < iter_max);

            if (current_minimum > s->f) {
                current_minimum = s->f;
                memcpy( optimized_parameters_mtx.get_data(), s->x->data, num_of_parameters*sizeof(double) );
                gsl_multimin_fdfminimizer_free (s);

                for ( int jdx=0; jdx<num_of_parameters; jdx++) {
                    solution_guess_gsl->data[jdx] = solution_guess_gsl->data[jdx] + distrib_real(gen)/100;
                }
            }
            else {
                for ( int jdx=0; jdx<num_of_parameters; jdx++) {
                    solution_guess_gsl->data[jdx] = solution_guess_gsl->data[jdx] + distrib_real(gen);
                }
                gsl_multimin_fdfminimizer_free (s);
            }

#ifdef __MPI__        
            MPI_Bcast( (void*)solution_guess_gsl->data, num_of_parameters, MPI_DOUBLE, 0, MPI_COMM_WORLD);
#endif



        }


}



/**
@brief Call to solve layer by layer the optimization problem via BFGS algorithm. The optimalized parameters are stored in attribute optimized_parameters.
@param num_of_parameters Number of parameters to be optimized
@param solution_guess_gsl A GNU Scientific Library vector containing the solution guess.
*/
void N_Qubit_Decomposition_Base::solve_layer_optimization_problem_BFGS2( int num_of_parameters, gsl_vector *solution_guess_gsl) {


#ifdef __DFE__
        if ( qbit_num >= 5 ) {
            upload_Umtx_to_DFE();
        }
#endif


        if (gates.size() == 0 ) {
            return;
        }


        if (solution_guess_gsl == NULL) {
            solution_guess_gsl = gsl_vector_alloc(num_of_parameters);
        }


        if (optimized_parameters_mtx.size() == 0) {
            optimized_parameters_mtx = Matrix_real(1, num_of_parameters);
            memcpy(optimized_parameters_mtx.get_data(), solution_guess_gsl->data, num_of_parameters*sizeof(double) );
        }

        // maximal number of iteration loops
        int iteration_loops_max;
        try {
            iteration_loops_max = std::max(iteration_loops[qbit_num], 1);
        }
        catch (...) {
            iteration_loops_max = 1;
        }


        int random_shift_count = 0;
        int sub_iter_idx = 0;
        double current_minimum_hold = current_minimum;


tbb::tick_count bfgs_start = tbb::tick_count::now();
bfgs_time = 0.0;


        // random generator of real numbers   
        std::uniform_real_distribution<> distrib_real(0.0, 2*M_PI);

        // random generator of integers   
        std::uniform_int_distribution<> distrib_int(0, 5000);  

        // do the optimization loops
        for (int idx=0; idx<iteration_loops_max; idx++) {

            int iter_idx = 0;
            int status = GSL_CONTINUE;

            const gsl_multimin_fdfminimizer_type *T;
            gsl_multimin_fdfminimizer *s;

            N_Qubit_Decomposition_Base* par = this;


            gsl_multimin_function_fdf my_func;


            my_func.n = num_of_parameters;
            my_func.f = optimization_problem;
            my_func.df = optimization_problem_grad;
            my_func.fdf = optimization_problem_combined;
            my_func.params = par;


            T = gsl_multimin_fdfminimizer_vector_bfgs2;
            s = gsl_multimin_fdfminimizer_alloc (T, num_of_parameters);

            gsl_multimin_fdfminimizer_set(s, &my_func, solution_guess_gsl, 0.01, 0.1);

            do {
                gsl_set_error_handler_off();
                
                if ( sub_iter_idx > iteration_threshold_of_randomization || status != GSL_CONTINUE ) {

                    std::stringstream sstream;
                    sstream << "BFGS2: initiate randomization at " << s->f << std::endl;
                    print(sstream, 2); 
                    
                    sub_iter_idx = 0;
                    random_shift_count++;
                    current_minimum_hold = current_minimum;        

                    int factor = distrib_int(gen) % 10 + 1;
             
                    for ( int jdx=0; jdx<num_of_parameters; jdx++) {
                        solution_guess_gsl->data[jdx] = optimized_parameters_mtx[jdx] + distrib_real(gen)*2*M_PI*std::sqrt(s->f)/factor;
                    } 

#ifdef __MPI__        
                    MPI_Bcast( (void*)solution_guess_gsl->data, num_of_parameters, MPI_DOUBLE, 0, MPI_COMM_WORLD);
#endif
                    
                    status = 0;    
                    
                    gsl_multimin_fdfminimizer_free (s);                     
                    s = gsl_multimin_fdfminimizer_alloc (T, num_of_parameters);  
                    gsl_multimin_fdfminimizer_set(s, &my_func, solution_guess_gsl, 0.01, 0.1);                             
        
                }
                else {
                    status = gsl_multimin_fdfminimizer_iterate (s);
                }
                                
/*
                if (status) {
                  break;
                }
*/
                status = gsl_multimin_test_gradient (s->gradient, gradient_threshold);
                
                
                if (sub_iter_idx == 1 ) {
                     current_minimum_hold = s->f;    
                }


                if (current_minimum_hold*0.95 > s->f || (current_minimum_hold*0.97 > s->f && s->f < 1e-3) ||  (current_minimum_hold*0.99 > s->f && s->f < 1e-4) ) {
                     sub_iter_idx = 0;
                     current_minimum_hold = s->f;        
                }
    
    
                if (current_minimum > s->f ) {
                     current_minimum = s->f;
                     memcpy( optimized_parameters_mtx.get_data(),  s->x->data, num_of_parameters*sizeof(double) );
                }
    

                if ( iter_idx % 5000 == 0 ) {
                     std::stringstream sstream;
                     sstream << "BFGS2: processed iterations " << (double)iter_idx/iter_max*100 << "\%, current minimum:" << current_minimum << std::endl;
                     print(sstream, 2);  

                     std::string filename("initial_circuit_iteration.binary");
                     export_gate_list_to_binary(optimized_parameters_mtx, this, filename, verbose);
                }


                if (s->f < optimization_tolerance || random_shift_count > random_shift_count_max ) {
                    break;
                }


                sub_iter_idx++;
                iter_idx++;

            } while (iter_idx < iter_max && s->f > optimization_tolerance);

            if (current_minimum > s->f) {
                current_minimum = s->f;
                memcpy( optimized_parameters_mtx.get_data(), s->x->data, num_of_parameters*sizeof(double) );                

                for ( int jdx=0; jdx<num_of_parameters; jdx++) {
                    solution_guess_gsl->data[jdx] = optimized_parameters_mtx[jdx] + distrib_real(gen)*2*M_PI/100;
                }
            }
            else {
                for ( int jdx=0; jdx<num_of_parameters; jdx++) {
                    solution_guess_gsl->data[jdx] = optimized_parameters_mtx[jdx] + distrib_real(gen)*2*M_PI;
                }
            }

#ifdef __MPI__        
            MPI_Bcast( (void*)solution_guess_gsl->data, num_of_parameters, MPI_DOUBLE, 0, MPI_COMM_WORLD);
#endif
            
            gsl_multimin_fdfminimizer_free (s);
            
            if (current_minimum < optimization_tolerance ) {
                break;
            }



        }

tbb::tick_count bfgs_end = tbb::tick_count::now();
bfgs_time  = bfgs_time + (bfgs_end-bfgs_start).seconds();
std::cout << "bfgs2 time: " << bfgs_time << " " << current_minimum << std::endl;
std::cout << "cost function of the imported circuit: " << optimization_problem( optimized_parameters_mtx ) << std::endl;

}


/**
@brief ?????????????
*/
void N_Qubit_Decomposition_Base::randomize_parameters( Matrix_real& input, gsl_vector* output, const int randomization_succesful, const double& f0  ) {

    // random generator of real numbers   
    std::uniform_real_distribution<> distrib_prob(0.0, 1.0);
    std::uniform_real_distribution<> distrib_real(-2*M_PI, 2*M_PI);


    const int num_of_parameters = input.size();

    if (randomization_probs.size() != num_of_parameters) {
        randomization_probs = Matrix_real(1, num_of_parameters);
        for ( int idx=0; idx<num_of_parameters; idx++ ) {
            randomization_probs[idx] = randomization_rate;
        }
        
        randomized_probs = matrix_base<int>(1, num_of_parameters);
    }
/*
    else {

        if ( randomization_succesful ) {
            for ( int jdx=0; jdx<num_of_parameters; jdx++) {
                if ( randomized_probs[jdx] == 1 ) {
                    randomization_probs[jdx] = randomization_probs[jdx] + 1.0/50;
                    randomization_probs[jdx] = randomization_probs[jdx] < 1.0 ? randomization_probs[jdx] : 1.0;
                }
                else {
                    randomization_probs[jdx] = randomization_probs[jdx] - 1.0/50;
                    randomization_probs[jdx] = randomization_probs[jdx] > 0.0 ? randomization_probs[jdx] : 0.01;
                }
            }
        }
        else {
            for ( int jdx=0; jdx<num_of_parameters; jdx++) {
                if ( randomized_probs[jdx] == 1 ) {
                    randomization_probs[jdx] = randomization_probs[jdx] - 1.0/50;
                    randomization_probs[jdx] = randomization_probs[jdx] > 0.0 ? randomization_probs[jdx] : 0.01;
                }
                else {
                    randomization_probs[jdx] = randomization_probs[jdx] + 1.0/50;
                    randomization_probs[jdx] = randomization_probs[jdx] < 1.0 ? randomization_probs[jdx] : 1.0;
                }                
            }
        }


    }
*/
    int changed_parameters = 0;
    for ( int jdx=0; jdx<num_of_parameters; jdx++) {
        if ( distrib_prob(gen) <= randomization_probs[jdx] ) {
            output->data[jdx] = input[jdx] + distrib_real(gen)*std::sqrt(f0)*radius;

            randomized_probs[jdx] = 1;
            changed_parameters++;
        }
        else {
            output->data[jdx] = input[jdx];
            randomized_probs[jdx] = 0;
        }
    }

#ifdef __MPI__  
        MPI_Bcast( (void*)output->data, num_of_parameters, MPI_DOUBLE, 0, MPI_COMM_WORLD);

   
if ( current_rank == 0 ) { 
#endif
    std::cout << "Randomized parameters: " << changed_parameters << " from " <<  num_of_parameters << std::endl;
#ifdef __MPI__  
}
#endif


}


/**
// @brief The optimization problem of the final optimization
// @param parameters An array of the free parameters to be optimized. (The number of teh free paramaters should be equal to the number of parameters in one sub-layer)
// @return Returns with the cost function. (zero if the qubits are desintangled.)
*/
double N_Qubit_Decomposition_Base::optimization_problem( double* parameters ) {

    // get the transformed matrix with the gates in the list
    Matrix_real parameters_mtx(parameters, 1, parameter_num );
    Matrix matrix_new = get_transformed_matrix( parameters_mtx, gates.begin(), gates.size(), Umtx );


    if ( cost_fnc == FROBENIUS_NORM ) {
        return get_cost_function(matrix_new);
    }
    else if ( cost_fnc == FROBENIUS_NORM_CORRECTION1 ) {
        Matrix_real&& ret = get_cost_function_with_correction(matrix_new, qbit_num);
        return ret[0] - std::sqrt(prev_cost_fnv_val)*ret[1]*correction1_scale;
    }
    else if ( cost_fnc == FROBENIUS_NORM_CORRECTION2 ) {
        Matrix_real&& ret = get_cost_function_with_correction2(matrix_new, qbit_num);
        return ret[0] - std::sqrt(prev_cost_fnv_val)*(ret[1]*correction1_scale + ret[2]*correction2_scale);
    }
    else {
        std::string err("N_Qubit_Decomposition_Base::optimization_problem: Cost function variant not implmented.");
        throw err;
    }


}


/**
// @brief The optimization problem of the final optimization
// @param parameters An array of the free parameters to be optimized. (The number of teh free paramaters should be equal to the number of parameters in one sub-layer)
// @return Returns with the cost function. (zero if the qubits are desintangled.)
*/
double N_Qubit_Decomposition_Base::optimization_problem( Matrix_real& parameters ) {

    // get the transformed matrix with the gates in the list
    if ( parameters.size() != parameter_num ) {
        std::stringstream sstream;
	sstream << "N_Qubit_Decomposition_Base::optimization_problem: Number of free paramaters should be " << parameter_num << ", but got " << parameters.size() << std::endl;
        print(sstream, 0);	  
        exit(-1);
    }


    Matrix matrix_new = get_transformed_matrix( parameters, gates.begin(), gates.size(), Umtx );
//matrix_new.print_matrix();

    if ( cost_fnc == FROBENIUS_NORM ) {
        return get_cost_function(matrix_new);
    }
    else if ( cost_fnc == FROBENIUS_NORM_CORRECTION1 ) {
        Matrix_real&& ret = get_cost_function_with_correction(matrix_new, qbit_num);
        return ret[0] - std::sqrt(prev_cost_fnv_val)*ret[1]*correction1_scale;
    }
    else if ( cost_fnc == FROBENIUS_NORM_CORRECTION2 ) {
        Matrix_real&& ret = get_cost_function_with_correction2(matrix_new, qbit_num);
        return ret[0] - std::sqrt(prev_cost_fnv_val)*(ret[1]*correction1_scale + ret[2]*correction2_scale);
    }
    else {
        std::string err("N_Qubit_Decomposition_Base::optimization_problem: Cost function variant not implmented.");
        throw err;
    }

}


/**
// @brief The optimization problem of the final optimization
@param parameters A GNU Scientific Library containing the parameters to be optimized.
@param void_instance A void pointer pointing to the instance of the current class.
@return Returns with the cost function. (zero if the qubits are desintangled.)
*/
double N_Qubit_Decomposition_Base::optimization_problem( const gsl_vector* parameters, void* void_instance ) {

    N_Qubit_Decomposition_Base* instance = reinterpret_cast<N_Qubit_Decomposition_Base*>(void_instance);
    std::vector<Gate*> gates_loc = instance->get_gates();

    // get the transformed matrix with the gates in the list
    Matrix Umtx_loc = instance->get_Umtx();
    Matrix_real parameters_mtx(parameters->data, 1, instance->get_parameter_num() );
    Matrix matrix_new = instance->get_transformed_matrix( parameters_mtx, gates_loc.begin(), gates_loc.size(), Umtx_loc );

  
    cost_function_type cost_fnc = instance->get_cost_function_variant();



    if ( cost_fnc == FROBENIUS_NORM ) {
        return get_cost_function(matrix_new);
    }
    else if ( cost_fnc == FROBENIUS_NORM_CORRECTION1 ) {
        double correction1_scale    = instance->get_correction1_scale();
        Matrix_real&& ret = get_cost_function_with_correction(matrix_new, instance->get_qbit_num());
        return ret[0] - std::sqrt(instance->get_previous_cost_function_value())*ret[1]*correction1_scale;
    }
    else if ( cost_fnc == FROBENIUS_NORM_CORRECTION2 ) {
        double correction1_scale    = instance->get_correction1_scale();
        double correction2_scale    = instance->get_correction2_scale();            
        Matrix_real&& ret = get_cost_function_with_correction2(matrix_new, instance->get_qbit_num());
        return ret[0] - std::sqrt(instance->get_previous_cost_function_value())*(ret[1]*correction1_scale + ret[2]*correction2_scale);
    }
    else {
        std::string err("N_Qubit_Decomposition_Base::optimization_problem: Cost function variant not implmented.");
        throw err;
    }


}


/**
@brief Calculate the approximate derivative (f-f0)/(x-x0) of the cost function with respect to the free parameters.
@param parameters A GNU Scientific Library vector containing the free parameters to be optimized.
@param void_instance A void pointer pointing to the instance of the current class.
@param grad A GNU Scientific Library vector containing the calculated gradient components.
*/
void N_Qubit_Decomposition_Base::optimization_problem_grad( const gsl_vector* parameters, void* void_instance, gsl_vector* grad ) {

    // The function value at x0
    double f0;

    // calculate the approximate gradient
    optimization_problem_combined( parameters, void_instance, &f0, grad);

}


/**
@brief Call to calculate both the cost function and the its gradient components.
@param parameters A GNU Scientific Library vector containing the free parameters to be optimized.
@param void_instance A void pointer pointing to the instance of the current class.
@param f0 The value of the cost function at x0.
@param grad A GNU Scientific Library vector containing the calculated gradient components.
*/
void N_Qubit_Decomposition_Base::optimization_problem_combined( const gsl_vector* parameters, void* void_instance, double* f0, gsl_vector* grad ) {

    N_Qubit_Decomposition_Base* instance = reinterpret_cast<N_Qubit_Decomposition_Base*>(void_instance);

    // the number of free parameters
    int parameter_num_loc = instance->get_parameter_num();

    // the variant of the cost function
    cost_function_type cost_fnc = instance->get_cost_function_variant();

    // value of the cost function from the previous iteration to weigth the correction to the trace
    double prev_cost_fnv_val = instance->get_previous_cost_function_value();
    double correction1_scale    = instance->get_correction1_scale();
    double correction2_scale    = instance->get_correction2_scale();    

    int qbit_num = instance->get_qbit_num();

#ifdef __DFE__

///////////////////////////////////////
//std::cout << "number of qubits: " << instance->qbit_num << std::endl;
//tbb::tick_count t0_DFE = tbb::tick_count::now();/////////////////////////////////    
if ( instance->qbit_num >= 5 && instance->get_accelerator_num() > 0 ) {
    Matrix_real parameters_mtx(parameters->data, 1, parameters->size);

    int gatesNum, redundantGateSets, gateSetNum;
    DFEgate_kernel_type* DFEgates = instance->convert_to_DFE_gates_with_derivates( parameters_mtx, gatesNum, gateSetNum, redundantGateSets );

    Matrix&& Umtx_loc = instance->get_Umtx();   
    Matrix_real trace_DFE_mtx(gateSetNum, 3);


#ifdef __MPI__
    // the number of decomposing layers are divided between the MPI processes

    int mpi_gateSetNum = gateSetNum / instance->world_size;
    int mpi_starting_gateSetIdx = gateSetNum/instance->world_size * instance->current_rank;

    Matrix_real mpi_trace_DFE_mtx(mpi_gateSetNum, 3);

    lock_lib();
    calcqgdKernelDFE( Umtx_loc.rows, Umtx_loc.cols, DFEgates+mpi_starting_gateSetIdx*gatesNum, gatesNum, mpi_gateSetNum, mpi_trace_DFE_mtx.get_data() );
    unlock_lib();

    int bytes = mpi_trace_DFE_mtx.size()*sizeof(double);
    MPI_Allgather(mpi_trace_DFE_mtx.get_data(), bytes, MPI_BYTE, trace_DFE_mtx.get_data(), bytes, MPI_BYTE, MPI_COMM_WORLD);

#else

    lock_lib();
    calcqgdKernelDFE( Umtx_loc.rows, Umtx_loc.cols, DFEgates, gatesNum, gateSetNum, trace_DFE_mtx.get_data() );
    unlock_lib();

#endif  

    std::stringstream sstream;
    sstream << *f0 << " " << 1.0 - trace_DFE_mtx[0]/Umtx_loc.cols << " " << trace_DFE_mtx[1]/Umtx_loc.cols << " " << trace_DFE_mtx[2]/Umtx_loc.cols << std::endl;
    instance->print(sstream, 5);	
    
  
    if ( cost_fnc == FROBENIUS_NORM ) {
        *f0 = 1-trace_DFE_mtx[0]/Umtx_loc.cols;
    }
    else if ( cost_fnc == FROBENIUS_NORM_CORRECTION1 ) {
        *f0 = 1 - (trace_DFE_mtx[0] + std::sqrt(prev_cost_fnv_val)*trace_DFE_mtx[1]*correction1_scale)/Umtx_loc.cols;
    }
    else if ( cost_fnc == FROBENIUS_NORM_CORRECTION2 ) {
        *f0 = 1 - (trace_DFE_mtx[0] + std::sqrt(prev_cost_fnv_val)*(trace_DFE_mtx[1]*correction1_scale + trace_DFE_mtx[2]*correction2_scale))/Umtx_loc.cols;
    }
    else {
        std::string err("N_Qubit_Decomposition_Base::optimization_problem_combined: Cost function variant not implmented.");
        throw err;
    }

    //double f0_DFE = *f0;

    //Matrix_real grad_components_DFE_mtx(1, parameter_num_loc);
    for (int idx=0; idx<parameter_num_loc; idx++) {

        if ( cost_fnc == FROBENIUS_NORM ) {
            gsl_vector_set(grad, idx, -trace_DFE_mtx[3*(idx+1)]/Umtx_loc.cols);
        }
        else if ( cost_fnc == FROBENIUS_NORM_CORRECTION1 ) {
            gsl_vector_set(grad, idx, -(trace_DFE_mtx[3*(idx+1)] + std::sqrt(prev_cost_fnv_val)*trace_DFE_mtx[3*(idx+1)+1]*correction1_scale)/Umtx_loc.cols);
        }
        else if ( cost_fnc == FROBENIUS_NORM_CORRECTION2 ) {
            gsl_vector_set(grad, idx, -(trace_DFE_mtx[3*(idx+1)] + std::sqrt(prev_cost_fnv_val)*(trace_DFE_mtx[3*(idx+1)+1]*correction1_scale + trace_DFE_mtx[3*(idx+1)+2]*correction2_scale))/Umtx_loc.cols );
        }
        else {
            std::string err("N_Qubit_Decomposition_Base::optimization_problem_combined: Cost function variant not implmented.");
            throw err;
        }

        //grad_components_DFE_mtx[idx] = gsl_vector_get( grad, idx );


    }

    delete[] DFEgates;

//tbb::tick_count t1_DFE = tbb::tick_count::now();/////////////////////////////////
//std::cout << "uploaded data to DFE: " << (int)(gatesNum*gateSetNum*sizeof(DFEgate_kernel_type)) << " bytes" << std::endl;
//std::cout << "time elapsed DFE: " << (t1_DFE-t0_DFE).seconds() << ", expected time: " << (((double)Umtx_loc.rows*(double)Umtx_loc.cols*gatesNum*gateSetNum/get_chained_gates_num()/4 + 4578*3*get_chained_gates_num()))/350000000 + 0.001<< std::endl;

///////////////////////////////////////
}
else {

#endif

#ifdef __DFE__
tbb::tick_count t0_CPU = tbb::tick_count::now();/////////////////////////////////
#endif

    Matrix_real cost_function_terms;

    // vector containing gradients of the transformed matrix
    std::vector<Matrix> Umtx_deriv;

    tbb::parallel_invoke(
        [&]{
            *f0 = instance->optimization_problem(parameters, reinterpret_cast<void*>(instance)); 
        },
        [&]{
            Matrix Umtx_loc = instance->get_Umtx();
            Matrix_real parameters_mtx(parameters->data, 1, parameters->size);
            Umtx_deriv = instance->apply_derivate_to( parameters_mtx, Umtx_loc );
        });


    tbb::parallel_for( tbb::blocked_range<int>(0,parameter_num_loc,2), [&](tbb::blocked_range<int> r) {
        for (int idx=r.begin(); idx<r.end(); ++idx) { 

            double grad_comp;
            if ( cost_fnc == FROBENIUS_NORM ) {
                grad_comp = (get_cost_function(Umtx_deriv[idx]) - 1.0);
            }
            else if ( cost_fnc == FROBENIUS_NORM_CORRECTION1 ) {
                Matrix_real deriv_tmp = get_cost_function_with_correction( Umtx_deriv[idx], qbit_num );
                grad_comp = (deriv_tmp[0] - std::sqrt(prev_cost_fnv_val)*deriv_tmp[1]*correction1_scale - 1.0);
            }
            else if ( cost_fnc == FROBENIUS_NORM_CORRECTION2 ) {
                Matrix_real deriv_tmp = get_cost_function_with_correction2( Umtx_deriv[idx], qbit_num );
                grad_comp = (deriv_tmp[0] - std::sqrt(prev_cost_fnv_val)*(deriv_tmp[1]*correction1_scale + deriv_tmp[2]*correction2_scale) - 1.0);
            }
            else {
                std::string err("N_Qubit_Decomposition_Base::optimization_problem_combined: Cost function variant not implmented.");
                throw err;
            }
            
//            grad->data[idx] = grad_comp;
            gsl_vector_set(grad, idx, grad_comp);



        }
    });

#ifdef __DFE__
}

/*
tbb::tick_count t1_CPU = tbb::tick_count::now();/////////////////////////////////
std::cout << "time elapsed CPU: " << (t1_CPU-t0_CPU).seconds() << " number of parameters: " << parameter_num_loc << std::endl;
std::cout << "cost function CPU: " << *f0 << " and DFE: " << f0_DFE << std::endl;

for ( int idx=0; idx<parameter_num_loc; idx++ ) {

    double diff = std::sqrt((grad_components_DFE_mtx[idx]-gsl_vector_get(grad, idx))*(grad_components_DFE_mtx[idx]-gsl_vector_get(grad, idx)));
    if ( diff > 1e-5 ) {
        std::cout << "DFE and CPU cost functions differs at index " << idx << " " <<  grad_components_DFE_mtx[idx] << " and " <<  gsl_vector_get(grad, idx) << std::endl;
        
    }   

}



std::cout << "N_Qubit_Decomposition_Base::optimization_problem_combined" << std::endl;
std::string error("N_Qubit_Decomposition_Base::optimization_problem_combined");
        throw error;
*/
#endif

/*

    // adjust gradient components corresponding to adaptive gates
    for (int idx=3*qbit_num; idx<parameter_num_loc; idx=idx+7 ) {
        double grad_comp = gsl_vector_get(grad, idx);
        grad_comp = grad_comp * std::sin( parameters->data[idx])*0.5*M_PI;
        gsl_vector_set(grad, idx, grad_comp);
    }
*/

}



/**
@brief Call to calculate both the cost function and the its gradient components.
@param parameters The parameters for which the cost fuction shoule be calculated
@param f0 The value of the cost function at x0.
@param grad An array storing the calculated gradient components
*/
void N_Qubit_Decomposition_Base::optimization_problem_combined( const Matrix_real& parameters, double* f0, Matrix_real& grad ) {

#ifdef __DFE__

    lock_lib();

    if ( get_accelerator_num() > 0 && get_initialize_id() != id ) {
        std::string err("The uploaded unitary to the DFE might not be identical to the unitary stored by this specific class instance. Please upload the unitary to DFE by the Upload_Umtx_to_DFE() method.");
        throw err;
    }

#endif

    // create GSL wrappers around the pointers
    gsl_block block_tmp;
    block_tmp.data = parameters.get_data();
    block_tmp.size = parameters.size(); 

    gsl_vector parameters_gsl;
    parameters_gsl.data = parameters.get_data();
    parameters_gsl.size = parameters.size();
    parameters_gsl.stride = 1;   
    parameters_gsl.block = &block_tmp; 
    parameters_gsl.owner = 0; 
    
    
    gsl_block block_tmp2;
    block_tmp.data = grad.get_data();
    block_tmp.size = grad.size();        

    gsl_vector grad_gsl;
    grad_gsl.data = grad.get_data();
    grad_gsl.size = grad.size();
    grad_gsl.stride = 1;   
    grad_gsl.block = &block_tmp2; 
    grad_gsl.owner = 0;    

    // call the method to calculate the cost function and the gradients
    optimization_problem_combined( &parameters_gsl, this, f0, &grad_gsl );

#ifdef __DFE__
    unlock_lib();
#endif

}


/**
@brief Call to get the variant of the cost function used in the calculations
*/
cost_function_type 
N_Qubit_Decomposition_Base::get_cost_function_variant() {

    return cost_fnc;

}


/**
@brief Call to set the variant of the cost function used in the calculations
@param variant The variant of the cost function from the enumaration cost_function_type
*/
void 
N_Qubit_Decomposition_Base::set_cost_function_variant( cost_function_type variant  ) {

    cost_fnc = variant;

    std::stringstream sstream;
    sstream << "N_Qubit_Decomposition_Base::set_cost_function_variant: Cost function variant set to " << cost_fnc << std::endl;
    print(sstream, 2);	


}



/**
@brief ?????????????
*/
void N_Qubit_Decomposition_Base::set_iter_max( int iter_max_in  ) {

    iter_max = iter_max_in;
    
}



/**
@brief ?????????????
*/
void N_Qubit_Decomposition_Base::set_random_shift_count_max( int random_shift_count_max_in  ) {

    random_shift_count_max = random_shift_count_max_in;

}


/**
@brief ?????????????
*/
void N_Qubit_Decomposition_Base::set_optimizer( optimization_aglorithms alg_in ) {

    alg = alg_in;

    switch ( alg ) {
        case ADAM:
            iter_max = 1e5;
            random_shift_count_max = 100;
            gradient_threshold = 1e-8;
            max_iterations = 1;
            return;

        case BFGS:
            iter_max = 100;
            gradient_threshold = 1e-1;
            random_shift_count_max = 1;  
            max_iterations = 1e8; 
            return;

        case BFGS2:
            iter_max = 1e5;
            random_shift_count_max = 100;
            gradient_threshold = 1e-8;
            max_iterations = 1;
            return;

        default:
            std::string error("N_Qubit_Decomposition_Base::solve_layer_optimization_problem: unimplemented optimization algorithm");
            throw error;
    }



}



/**
@brief ?????????????
*/
void 
N_Qubit_Decomposition_Base::set_adaptive_eta( bool adaptive_eta_in  ) {

    adaptive_eta = adaptive_eta_in;

}



/**
@brief ?????????????
*/
void 
N_Qubit_Decomposition_Base::set_randomized_radius( double radius_in  ) {

    radius = radius_in;

}


/**
@brief ???????????
*/
double 
N_Qubit_Decomposition_Base::get_previous_cost_function_value() {

    return prev_cost_fnv_val;

}



/**
@brief ???????????
*/
double 
N_Qubit_Decomposition_Base::get_correction1_scale() {

    return correction1_scale;

}


/**
@brief ??????????????
@param ?????????
*/
void 
N_Qubit_Decomposition_Base::get_correction1_scale( const double& scale ) {


    correction1_scale = scale;

}




/**
@brief ???????????
*/
double 
N_Qubit_Decomposition_Base::get_correction2_scale() {

    return correction2_scale;

}


/**
@brief ??????????????
@param ?????????
*/
void 
N_Qubit_Decomposition_Base::get_correction2_scale( const double& scale ) {


    correction2_scale = scale;

}




/**
@brief ???????????
*/
long 
N_Qubit_Decomposition_Base::get_iteration_threshold_of_randomization() {

    return iteration_threshold_of_randomization;

}


/**
@brief ??????????????
@param ?????????
*/
void 
N_Qubit_Decomposition_Base::set_iteration_threshold_of_randomization( const unsigned long long& threshold ) {


    iteration_threshold_of_randomization = threshold;

}


#ifdef __DFE__

void 
N_Qubit_Decomposition_Base::upload_Umtx_to_DFE() {

    lock_lib();

    if ( get_initialize_id() != id ) {
        // initialize DFE library
        init_dfe_lib( accelerator_num, qbit_num, id );
    }

    uploadMatrix2DFE( Umtx );


    unlock_lib();

}


/**
@brief Get the number of accelerators to be reserved on DFEs on users demand. 
*/
int 
N_Qubit_Decomposition_Base::get_accelerator_num() {

    return accelerator_num;

}


#endif

