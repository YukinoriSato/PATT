/**
 * This version is stamped on May 10, 2016
 *
 * Contact:
 *   Louis-Noel Pouchet <pouchet.ohio-state.edu>
 *   Tomofumi Yuki <tomofumi.yuki.fr>
 *
 * Web address: http://polybench.sourceforge.net
 */
#ifndef _FDTD_2D_H
# define _FDTD_2D_H

/* Default to LARGE_DATASET. */
/*
# if !defined(MINI_DATASET) && !defined(SMALL_DATASET) && !defined(MEDIUM_DATASET) && !defined(LARGE_DATASET) && !defined(EXTRALARGE_DATASET)
#  define LARGE_DATASET
# endif
*/

# if !defined(TMAX) && !defined(NX) && !defined(NY)
/* Define sample dataset sizes. */
#  ifdef MINI_DATASET
//#   define TMAX 20
#   define TMAX 1
#   define NX 20
#   define NY 30
#   define NZ 30
#  endif

#  ifdef SMALL_DATASET
//#   define TMAX 40
#   define TMAX 1
#   define NX 60
#   define NY 80
#   define NZ 80
#  endif

#  ifdef MEDIUM_DATASET
//#   define TMAX 100
#   define TMAX 1
#   define NX 100
#   define NY 140
#   define NZ 140
#  endif

#  ifdef LARGE_DATASET
//#   define TMAX 60
#   define TMAX 1
#   define NX 260
#   define NY 260
#   define NZ 260
#  endif

#  ifdef EXTRALARGE_DATASET
//#   define TMAX 100
#   define TMAX 1
#   define NX 520
#   define NY 520
#   define NZ 520
#  endif

//yAdd
#  ifdef XXLARGE_DATASET
//#   define TMAX 100
#   define TMAX 1
#   define NX 1040
#   define NY 1040
#   define NZ 1040
#  endif


#endif /* !(TMAX NX NY) */

# define _PB_TMAX POLYBENCH_LOOP_BOUND(TMAX,tmax)
# define _PB_NX POLYBENCH_LOOP_BOUND(NX,nx)
# define _PB_NY POLYBENCH_LOOP_BOUND(NY,ny)
# define _PB_NZ POLYBENCH_LOOP_BOUND(NZ,nz)


/* Default data type */
# if !defined(DATA_TYPE_IS_INT) && !defined(DATA_TYPE_IS_FLOAT) && !defined(DATA_TYPE_IS_DOUBLE)
#  define DATA_TYPE_IS_DOUBLE
# endif

#ifdef DATA_TYPE_IS_INT
#  define DATA_TYPE int
#  define DATA_PRINTF_MODIFIER "%d "
#endif

#ifdef DATA_TYPE_IS_FLOAT
#  define DATA_TYPE float
#  define DATA_PRINTF_MODIFIER "%0.2f "
#  define SCALAR_VAL(x) x##f
#  define SQRT_FUN(x) sqrtf(x)
#  define EXP_FUN(x) expf(x)
#  define POW_FUN(x,y) powf(x,y)
# endif

#ifdef DATA_TYPE_IS_DOUBLE
#  define DATA_TYPE double
#  define DATA_PRINTF_MODIFIER "%0.2lf "
#  define SCALAR_VAL(x) x
#  define SQRT_FUN(x) sqrt(x)
#  define EXP_FUN(x) exp(x)
#  define POW_FUN(x,y) pow(x,y)
# endif

#endif /* !_FDTD_2D_H */
