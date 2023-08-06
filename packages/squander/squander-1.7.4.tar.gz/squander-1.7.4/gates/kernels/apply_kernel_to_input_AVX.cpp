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
/*! \file apply_kerel_to_input_AVX.cpp
    \brief ????????????????
*/


#include "apply_kernel_to_input_AVX.h"
#include <immintrin.h>


/**
@brief AVX kernel to apply single qubit gate kernel on an input matrix
@param A matrix on which the householder transformation is applied. (The output is returned via this matrix)
@param v A matrix instance of the reflection vector
*/
void
apply_kernel_to_input_AVX(Matrix& u3_1qbit, Matrix& input, const bool& deriv, const int& target_qbit, const int& control_qbit, const int& matrix_size) {


    int index_step_target = 1 << target_qbit;
    int current_idx = 0;
    int current_idx_pair = current_idx+index_step_target;


    // load elements of the U3 unitary into 256bit registers (4 registers)
    __m128d* u3_1qubit_tmp  = (__m128d*)&u3_1qbit[0];
    __m256d u3_1qbit_00_vec = _mm256_broadcast_pd( u3_1qubit_tmp );

    u3_1qubit_tmp = (__m128d*)&u3_1qbit[1];
    __m256d u3_1qbit_01_vec = _mm256_broadcast_pd( u3_1qubit_tmp );

    u3_1qubit_tmp = (__m128d*)&u3_1qbit[2];
    __m256d u3_1qbit_10_vec = _mm256_broadcast_pd( u3_1qubit_tmp );

    u3_1qubit_tmp = (__m128d*)&u3_1qbit[3];
    __m256d u3_1qbit_11_vec = _mm256_broadcast_pd( u3_1qubit_tmp );



    while ( current_idx_pair < matrix_size ) {

        for(int idx=0; idx<index_step_target; idx++) {  
        //tbb::parallel_for(0, index_step_target, 1, [&](int idx) {  

            int current_idx_loc = current_idx + idx;
            int current_idx_pair_loc = current_idx_pair + idx;

            int row_offset = current_idx_loc*input.stride;
            int row_offset_pair = current_idx_pair_loc*input.stride;

           if ( control_qbit<0 || ((current_idx_loc >> control_qbit) & 1) ) {


                double* element      = (double*)input.get_data() + 2*row_offset;
                double* element_pair = (double*)input.get_data() + 2*row_offset_pair;


                __m256d neg = _mm256_setr_pd(1.0, -1.0, 1.0, -1.0); // 5th register


                for ( int col_idx=0; col_idx<2*(input.cols-1); col_idx=col_idx+4) {

                    // extract successive elements from arrays element, element_pair
                    __m256d element_vec      = _mm256_loadu_pd( element+col_idx ); // 6th register
                    __m256d element_pair_vec = _mm256_loadu_pd( element_pair+col_idx ); // 7th register

                    //// u3_1qbit_00*element_vec ////

                    // 1 calculate the multiplications  u3_1qbit_00*element_vec
                    __m256d vec3 = _mm256_mul_pd(u3_1qbit_00_vec, element_vec); // 8th register

                    // 2 Switch the real and imaginary elements of element_vec
                    __m256d element_vec_permuted = _mm256_permute_pd(element_vec, 0x5);   // 9th register

                    // 3 Negate the imaginary elements of element_vec_permuted
                    element_vec_permuted = _mm256_mul_pd(element_vec_permuted, neg);

                    // 4 Multiply elements of u3_1qbit_00*element_vec_permuted
                    __m256d vec4 = _mm256_mul_pd(u3_1qbit_00_vec, element_vec_permuted); 

                    // 5 Horizontally subtract the elements in vec3 and vec4
                    vec3  = _mm256_hsub_pd(vec3, vec4); 


                    //// u3_1qbit_01*element_vec_pair ////

                    // 1 calculate the multiplications  u3_1qbit_01*element_pair_vec
                    __m256d vec5 = _mm256_mul_pd(u3_1qbit_01_vec, element_pair_vec); // 10th register

                    // 2 Switch the real and imaginary elements of element_vec
                    __m256d element_pair_vec_permuted = _mm256_permute_pd(element_pair_vec, 0x5);   // 11th register

                    // 3 Negate the imaginary elements of element_vec_permuted
                    element_pair_vec_permuted = _mm256_mul_pd(element_pair_vec_permuted, neg);

                    // 4 Multiply elements of u3_1qbit_01*element_vec_pair_permuted
                    vec4 = _mm256_mul_pd(u3_1qbit_01_vec, element_pair_vec_permuted); 

                    // 5 Horizontally subtract the elements in vec5 and vec4
                    vec5  = _mm256_hsub_pd(vec5, vec4); 

                    //// u3_1qbit_00*element_vec + u3_1qbit_01*element_vec_pair ////
                    vec3 = _mm256_add_pd(vec3, vec5);


                    // 6 store the transformed elements in vec3
                    _mm256_storeu_pd(element+col_idx, vec3);


                    //// u3_1qbit_10*element_vec ////

                    // 1 calculate the multiplications  u3_1qbit_10*element_vec
                    vec3 = _mm256_mul_pd(u3_1qbit_10_vec, element_vec); 

                    // 4 Multiply elements of u3_1qbit_10*element_vec_permuted
                    vec4 = _mm256_mul_pd(u3_1qbit_10_vec, element_vec_permuted); 

                    // 5 Horizontally subtract the elements in vec3 and vec4
                    vec3  = _mm256_hsub_pd(vec3, vec4); 


                    //// u3_1qbit_01*element_vec_pair ////

                    // 1 calculate the multiplications  u3_1qbit_01*element_pair_vec
                    vec5 = _mm256_mul_pd(u3_1qbit_11_vec, element_pair_vec); 

                    // 4 Multiply elements of u3_1qbit_01*element_vec_pair_permuted
                    vec4 = _mm256_mul_pd(u3_1qbit_11_vec, element_pair_vec_permuted); 

                    // 5 Horizontally subtract the elements in vec5 and vec4
                    vec5  = _mm256_hsub_pd(vec5, vec4); 

                    //// u3_1qbit_10*element_vec + u3_1qbit_11*element_vec_pair ////
                    vec3 = _mm256_add_pd(vec3, vec5);

                    // 6 store the transformed elements in vec3
                    _mm256_storeu_pd(element_pair+col_idx, vec3);

                }   

                if (input.cols % 2 == 1) {     

                    int col_idx = input.cols-1;       

                    int index      = row_offset+col_idx;
                    int index_pair = row_offset_pair+col_idx;                

                    QGD_Complex16 element      = input[index];
                    QGD_Complex16 element_pair = input[index_pair];              

                    QGD_Complex16 tmp1 = mult(u3_1qbit[0], element);
                    QGD_Complex16 tmp2 = mult(u3_1qbit[1], element_pair);
 
                    input[index].real = tmp1.real + tmp2.real;
                    input[index].imag = tmp1.imag + tmp2.imag;

                    tmp1 = mult(u3_1qbit[2], element);
                    tmp2 = mult(u3_1qbit[3], element_pair);

                    input[index_pair].real = tmp1.real + tmp2.real;
                    input[index_pair].imag = tmp1.imag + tmp2.imag;


                }

            }
            else if (deriv) {
                // when calculating derivatives, the constant element should be zeros
                memset( input.get_data()+row_offset, 0.0, input.cols*sizeof(QGD_Complex16));
                memset( input.get_data()+row_offset_pair, 0.0, input.cols*sizeof(QGD_Complex16));
            }
            else {
                // leave the state as it is
                continue; 
            }


//std::cout << current_idx_target << " " << current_idx_target_pair << std::endl;

        
        //});
        }


        current_idx = current_idx + (index_step_target << 1);
        current_idx_pair = current_idx_pair + (index_step_target << 1);


    }




}

