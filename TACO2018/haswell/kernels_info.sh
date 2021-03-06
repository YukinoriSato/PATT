#!/bin/bash

#on/off switch

#for 64th eNall32 and aNall32 and IT_NUM

#exp_gemm=true
# 12 benchmarks
exp_gemm=true
:<<CMT
exp_gemver=true
exp_gesummv=true
exp_mvt=true
exp_syrk=true
exp_syr2k=true
exp_2mm=true
exp_3mm=true
exp_atax=true
exp_correlation=true
exp_covariance=true
exp_jacobi2d=true

CMT

#exp_gemm=true


<<EOF




# more applications
exp_himeno=true
exp_fdtd3d=true


EOF


:<<CMT
exp_atax=true
#exp_doitgen=true
#exp_deriche=true
exp_gemm=true
exp_2mm=true
exp_3mm=true
#exp_covariance=true
#exp_correlation=true
exp_syrk=true
exp_syr2k=true

CMT


#--------------------------detail settings----------------------------------
if test ${exp_gemm} ; then
BENCH_DIR_LIST+=("linear-algebra/blas/gemm")
#LOOP_DEPENDENCE_LIST+=("false")
LOOP_DEPENDENCE_LIST+=("true")
LOOP_SIZE_LIST_L+=("1000 1200 1100")
LOOP_SIZE_LIST_XL+=("2000 2300 2600")
LOOP_SIZE_LIST_XXL+=("4000 4600 5200")
IT_NUM_LIST_L+=("100")
#IT_NUM_LIST_L+=("20")
IT_NUM_LIST_XL+=("20")
IT_NUM_LIST_XXL+=("2")
ENALL32_PARA_LIST_L+=("17,32,32")
ENALL32_PARA_LIST_XL+=("32,32,32")
ENALL32_PARA_LIST_XXL+=("64,32,32")
ANALL32_PARA_LIST_L+=("16,32,32")
#ANALL32_PARA_LIST_L+=("16,264,40")
ANALL32_PARA_LIST_XL+=("32,32,32")
ANALL32_PARA_LIST_XXL+=("32,32,32")
S1_LIST+=("1")
S2_LIST+=("1")
fi
if test ${exp_gemver} ; then
BENCH_DIR_LIST+=("linear-algebra/blas/gemver")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("2000 2000")
LOOP_SIZE_LIST_XL+=("4000 4000")
LOOP_SIZE_LIST_XXL+=("12000 12000")
IT_NUM_LIST_L+=("1800")
IT_NUM_LIST_XL+=("400")
IT_NUM_LIST_XXL+=("50")
ENALL32_PARA_LIST_L+=("8,32")
ENALL32_PARA_LIST_XL+=("8,32")
ENALL32_PARA_LIST_XXL+=("8,32")
ANALL32_PARA_LIST_L+=("16,32")
ANALL32_PARA_LIST_XL+=("68,32")
ANALL32_PARA_LIST_XXL+=("8,32")
S1_LIST+=("2")
S2_LIST+=("2")
#S2_LIST+=("1")
fi
if test ${exp_gesummv} ; then
BENCH_DIR_LIST+=("linear-algebra/blas/gesummv")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("1300 1300")
LOOP_SIZE_LIST_XL+=("2800 2800")
LOOP_SIZE_LIST_XXL+=("8400 8400")
IT_NUM_LIST_L+=("10000")
IT_NUM_LIST_XL+=("1800")
IT_NUM_LIST_XXL+=("180")
ENALL32_PARA_LIST_L+=("8,32")
ENALL32_PARA_LIST_XL+=("4,32")
ENALL32_PARA_LIST_XXL+=("48,32")
ANALL32_PARA_LIST_L+=("4,32")
ANALL32_PARA_LIST_XL+=("4,32")
ANALL32_PARA_LIST_XXL+=("4,32")
S1_LIST+=("1")
S2_LIST+=("1")
fi
if test ${exp_mvt} ; then
BENCH_DIR_LIST+=("linear-algebra/kernels/mvt")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("2000 2000")
LOOP_SIZE_LIST_XL+=("4000 4000")
LOOP_SIZE_LIST_XXL+=("12000 12000")
IT_NUM_LIST_L+=("4000")
IT_NUM_LIST_XL+=("1000")
IT_NUM_LIST_XXL+=("100")
ENALL32_PARA_LIST_L+=("8,32")
ENALL32_PARA_LIST_XL+=("8,32")
ENALL32_PARA_LIST_XXL+=("56,32")
ANALL32_PARA_LIST_L+=("8,32")
ANALL32_PARA_LIST_XL+=("68,32")
ANALL32_PARA_LIST_XXL+=("248,32")
S1_LIST+=("1")
S2_LIST+=("1")
fi
if test ${exp_doitgen} ; then
BENCH_DIR_LIST+=("linear-algebra/kernels/doitgen")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("150 140")
LOOP_SIZE_LIST_XL+=("250 220")
LOOP_SIZE_LIST_XXL+=("500 440")
IT_NUM_LIST_L+=("2")
IT_NUM_LIST_XL+=("1")
IT_NUM_LIST_XXL+=("1")
fi
if test ${exp_deriche} ; then
BENCH_DIR_LIST+=("medley/deriche")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("2160 2160")
LOOP_SIZE_LIST_XL+=("4320 4320")
LOOP_SIZE_LIST_XXL+=("8640 8640")
IT_NUM_LIST_L+=("5")
IT_NUM_LIST_XL+=("1")
IT_NUM_LIST_XXL+=("1")
fi

if test ${exp_2mm} ; then
BENCH_DIR_LIST+=("linear-algebra/kernels/2mm")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("800 900 900")
LOOP_SIZE_LIST_XL+=("1600 1800 1800")
LOOP_SIZE_LIST_XXL+=("3200 3600 3600")
IT_NUM_LIST_L+=("80")
IT_NUM_LIST_XL+=("10")
IT_NUM_LIST_XXL+=("2")
ENALL32_PARA_LIST_L+=("8,32,32")
ENALL32_PARA_LIST_XL+=("15,32,32")
ENALL32_PARA_LIST_XXL+=("25,32,32")
ANALL32_PARA_LIST_L+=("16,32,32")
ANALL32_PARA_LIST_XL+=("28,32,32")
ANALL32_PARA_LIST_XXL+=("28,32,32")
S1_LIST+=("1")
S2_LIST+=("1")
fi
if test ${exp_3mm} ; then
BENCH_DIR_LIST+=("linear-algebra/kernels/3mm")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("800 900 900")
LOOP_SIZE_LIST_XL+=("1600 1800 1800")
LOOP_SIZE_LIST_XXL+=("3200 3600 3600")
IT_NUM_LIST_L+=("60")
IT_NUM_LIST_XL+=("8")
IT_NUM_LIST_XXL+=("1")
ENALL32_PARA_LIST_L+=("8,32,32")
ENALL32_PARA_LIST_XL+=("30,32,32")
ENALL32_PARA_LIST_XXL+=("30,32,32")
ANALL32_PARA_LIST_L+=("16,32,32")
ANALL32_PARA_LIST_XL+=("32,32,32")
ANALL32_PARA_LIST_XXL+=("20,32,32")
S1_LIST+=("1")
S2_LIST+=("1")
fi
if test ${exp_syrk} ; then
BENCH_DIR_LIST+=("linear-algebra/blas/syrk")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("1200 1000 1200")
LOOP_SIZE_LIST_XL+=("2600 2000 2600")
LOOP_SIZE_LIST_XXL+=("5200 4000 5200")
IT_NUM_LIST_L+=("150")
IT_NUM_LIST_XL+=("18")
IT_NUM_LIST_XXL+=("2")
ENALL32_PARA_LIST_L+=("2,32,32")
ENALL32_PARA_LIST_XL+=("5,32,32")
ENALL32_PARA_LIST_XXL+=("14,32,32")
ANALL32_PARA_LIST_L+=("2,32,32")
ANALL32_PARA_LIST_XL+=("3,32,32")
ANALL32_PARA_LIST_XXL+=("4,32,32")
S1_LIST+=("1")
S2_LIST+=("1")
fi
if test ${exp_syr2k} ; then
BENCH_DIR_LIST+=("linear-algebra/blas/syr2k")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("1200 1000 1200")
LOOP_SIZE_LIST_XL+=("2600 2000 2600")
LOOP_SIZE_LIST_XXL+=("5200 4000 5200")
IT_NUM_LIST_L+=("100")
IT_NUM_LIST_XL+=("10")
IT_NUM_LIST_XXL+=("1")
ENALL32_PARA_LIST_L+=("3,32,32")
ENALL32_PARA_LIST_XL+=("7,32,32")
ENALL32_PARA_LIST_XXL+=("6,32,32")
ANALL32_PARA_LIST_L+=("2,32,32")
ANALL32_PARA_LIST_XL+=("3,32,32")
ANALL32_PARA_LIST_XXL+=("8,32,32")
S1_LIST+=("2")
S2_LIST+=("1")
fi
if test ${exp_atax}; then
BENCH_DIR_LIST+=("linear-algebra/kernels/atax")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("1900 2100")
LOOP_SIZE_LIST_XL+=("1800 2200")
LOOP_SIZE_LIST_XXL+=("5400 6600")
IT_NUM_LIST_L+=("4000")
IT_NUM_LIST_XL+=("4000")
IT_NUM_LIST_XXL+=("400")
ENALL32_PARA_LIST_L+=("4,32")
ENALL32_PARA_LIST_XL+=("8,32")
ENALL32_PARA_LIST_XXL+=("8,32")
ANALL32_PARA_LIST_L+=("8,32")
ANALL32_PARA_LIST_XL+=("16,32")
ANALL32_PARA_LIST_XXL+=("32,32")
S1_LIST+=("1")
S2_LIST+=("1")
fi
if test ${exp_covariance} ; then
BENCH_DIR_LIST+=("datamining/covariance")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("1200 1200 1400")
LOOP_SIZE_LIST_XL+=("2600 2600 3000")
LOOP_SIZE_LIST_XXL+=("5200 5200 6000")
IT_NUM_LIST_L+=("180")
IT_NUM_LIST_XL+=("18")
IT_NUM_LIST_XXL+=("2")
ENALL32_PARA_LIST_L+=("8,32,32")
ENALL32_PARA_LIST_XL+=("18,32,32")
ENALL32_PARA_LIST_XXL+=("37,32,32")
ANALL32_PARA_LIST_L+=("8,32,32")
ANALL32_PARA_LIST_XL+=("20,32,32")
ANALL32_PARA_LIST_XXL+=("20,32,32")
S1_LIST+=("1")
S2_LIST+=("1")
fi
if test ${exp_correlation} ; then
BENCH_DIR_LIST+=("datamining/correlation")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("1200 1200 1400")
LOOP_SIZE_LIST_XL+=("2600 2600 3000")
LOOP_SIZE_LIST_XXL+=("5200 5200 6000")
IT_NUM_LIST_L+=("50")
IT_NUM_LIST_XL+=("8")
IT_NUM_LIST_XXL+=("2")
ENALL32_PARA_LIST_L+=("8,32,32")
ENALL32_PARA_LIST_XL+=("18,32,32")
ENALL32_PARA_LIST_XXL+=("24,32,32")
ANALL32_PARA_LIST_L+=("8,32,32")
ANALL32_PARA_LIST_XL+=("20,32,32")
ANALL32_PARA_LIST_XXL+=("20,32,32")
S1_LIST+=("1")
S2_LIST+=("1")
fi
if test ${exp_jacobi2d} ; then
BENCH_DIR_LIST+=("stencils/jacobi-2d")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("1300 1300")
LOOP_SIZE_LIST_XL+=("2800 2800")
LOOP_SIZE_LIST_XXL+=("8400 8400")
IT_NUM_LIST_L+=("4000")
IT_NUM_LIST_XL+=("600")
IT_NUM_LIST_XXL+=("60")
ENALL32_PARA_LIST_L+=("17,32")
ENALL32_PARA_LIST_XL+=("10,32")
ENALL32_PARA_LIST_XXL+=("36,32")
ANALL32_PARA_LIST_L+=("16,32")
ANALL32_PARA_LIST_XL+=("12,32")
ANALL32_PARA_LIST_XXL+=("48,32")
S1_LIST+=("0")
S2_LIST+=("0")
fi
if test ${exp_gemm2} ; then
BENCH_DIR_LIST+=("linear-algebra/blas/gemm2")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("1000 1200 1100")
LOOP_SIZE_LIST_XL+=("2000 2300 2600")
LOOP_SIZE_LIST_XXL+=("4000 4600 5200")
IT_NUM_LIST_L+=("50")
IT_NUM_LIST_XL+=("7")
IT_NUM_LIST_XXL+=("1")
ENALL32_PARA_LIST_L+=("8,32,32")
ENALL32_PARA_LIST_XL+=("19,32,32")
ENALL32_PARA_LIST_XXL+=("36,32,32")
ANALL32_PARA_LIST_L+=("16,32,32")
ANALL32_PARA_LIST_XL+=("32,32,32")
ANALL32_PARA_LIST_XXL+=("32,32,32")
fi
if test ${exp_himeno} ; then
BENCH_DIR_LIST+=("himeno")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("257 257 513")
LOOP_SIZE_LIST_XL+=("513 513 1025")
LOOP_SIZE_LIST_XXL+=("513 513 1025")
IT_NUM_LIST_L+=("70")
IT_NUM_LIST_XL+=("1")
IT_NUM_LIST_XXL+=("1")
ENALL32_PARA_LIST_L+=("2,32,32")
ENALL32_PARA_LIST_XL+=("1,32,32")
ENALL32_PARA_LIST_XXL+=("1,32,32")
ANALL32_PARA_LIST_L+=("1,32,32")
ANALL32_PARA_LIST_XL+=("1,32,32")
ANALL32_PARA_LIST_XXL+=("1,32,32")
fi
if test ${exp_fdtd3d} ; then
BENCH_DIR_LIST+=("stencils/fdtd-3d")
LOOP_DEPENDENCE_LIST+=("false")
LOOP_SIZE_LIST_L+=("260 260 260")
LOOP_SIZE_LIST_XL+=("520 520 520")
LOOP_SIZE_LIST_XXL+=("1040 1040 1040")
IT_NUM_LIST_L+=("10")
IT_NUM_LIST_XL+=("1")
IT_NUM_LIST_XXL+=("1")
ENALL32_PARA_LIST_L+=("1,32,32")
ENALL32_PARA_LIST_XL+=("1,32,32")
ENALL32_PARA_LIST_XXL+=("1,32,32")
ANALL32_PARA_LIST_L+=("1,32,32")
ANALL32_PARA_LIST_XL+=("1,32,32")
ANALL32_PARA_LIST_XXL+=("1,32,32")
fi


:<<CMT
BENCH_DIR_LIST+=("${SRC_DIR}/linear-algebra/solvers/lu")

BENCH_DIR_LIST+=("${SRC_DIR}/stencils/adi")
BENCH_DIR_LIST+=("${SRC_DIR}/stencils/seidel-2d")

BENCH_DIR_LIST+=("${SRC_DIR}/linear-algebra/kernels/bicg")
BENCH_DIR_LIST+=("${SRC_DIR}/linear-algebra/solvers/durbin")
BENCH_DIR_LIST+=("${SRC_DIR}/stencils/fdtd-2d")
BENCH_DIR_LIST+=("${SRC_DIR}/stencils/heat-3d")
BENCH_DIR_LIST+=("${SRC_DIR}/stencils/jacobi-1d")
BENCH_DIR_LIST+=("${SRC_DIR}/stencils/jacobi-2d")
BENCH_DIR_LIST+=("${SRC_DIR}/linear-algebra/solvers/trisolv")
BENCH_DIR_LIST+=("${SRC_DIR}/linear-algebra/blas/symm")
BENCH_DIR_LIST+=("${SRC_DIR}/linear-algebra/blas/trmm")
BENCH_DIR_LIST+=("${SRC_DIR}/linear-algebra/solvers/ludcmp")
BENCH_DIR_LIST+=("${SRC_DIR}/medley/nussinov")
BENCH_DIR_LIST+=("${SRC_DIR}/linear-algebra/solvers/cholesky")

BENCH_DIR_LIST+=("${SRC_DIR}/linear-algebra/solvers/gramschmidt")
BENCH_DIR_LIST+=("${SRC_DIR}/medley/floyd-warshall")
CMT


