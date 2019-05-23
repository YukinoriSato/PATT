#!/bin/bash



rm -rf result
mkdir result

for kernel in gemm atax
do
	mkdir result/${kernel}
	echo "start ${kernel} exhaustive"
	export PATT_SETTING_FILE="patt_setting_${kernel}_exha"
	./run_${kernel}.sh &> ./result/${kernel}/exha
	#./run_${kernel}.sh
done


#-----------------------------------------------------
:<<CMT

export PATT_SETTING_FILE="patt_setting_gemm_ipatt"
./run.sh &> ./ntimes_result_gemm/result_i_patt
./extract_data.py ./ntimes_result_gemm/result_i_patt

export PATT_SETTING_FILE="patt_setting_gemm_nm"
./run.sh &> ./ntimes_result_gemm/result_nm
./extract_data.py ./ntimes_result_gemm/result_nm

export PATT_SETTING_FILE="patt_setting_gemm_sa"
for i in `seq 1 1`
do
echo ${i}
./run.sh &> ./ntimes_result_gemm/result_sa_${i}
./extract_data.py ./ntimes_result_gemm/result_sa_${i}
done

#-----------------------------------------------------
rm -rf ./ntimes_result_atax
mkdir ntimes_result_atax

export PATT_SETTING_FILE="patt_setting_atax_ipatt"
./atax_run.sh &> ./ntimes_result_atax/result_i_patt
./extract_data.py ./ntimes_result_atax/result_i_patt
./align_this_time.py ./ntimes_result_atax/result_i_patt_extracted

export PATT_SETTING_FILE="patt_setting_atax_nm"
./atax_run.sh &> ./ntimes_result_atax/result_nm
./extract_data.py ./ntimes_result_atax/result_nm
./align_this_time.py ./ntimes_result_atax/result_nm_extracted

export PATT_SETTING_FILE="patt_setting_atax_sa"
for i in `seq 1 1`
do
echo ${i}
./atax_run.sh &> ./ntimes_result_atax/result_sa_${i}
./extract_data.py ./ntimes_result_atax/result_sa_${i}
./align_this_time.py ./ntimes_result_atax/result_sa_${i}_extracted
done

#-----------------------------------------------------
#for i in `seq 1 100`
#do
#grep "final_best_perf_cost:" ./ntimes_result/result_${i} >> ./ntimes_result/ntimes_all
#done

CMT

