
#!/bin/bash


:<<CMT
export PATT_SETTING_FILE="patt_setting_gemm_nm"
./run.sh
CMT

rm -rf result
mkdir result

threads=64
remote=lyon3
repetition=3

# Multiple trials based on REP_NUM is used for changing seeds of random number generation in Simulated Annealing
#REP_NUM=(1)
REP_NUM=(1 1 1)

source kernels_info.sh

CC="/home/yukinori/PATT/TACO/src/patt.py"
#CC="/home/yuki/yWork/patt_github_sato_ver/PATT/src/patt.py"

SRC_DIR="/home/yukinori/benchmark/polybench4.2_mainNit/polybench-c-4.2"
POLYBENCH_DIR="${SRC_DIR}/utilities"


export PATT_SETTING_FILE="patt_setting"



#for psize in L XL
for psize in L
do

TEMPNUM=0

for i in "${BENCH_DIR_LIST[@]}"
#for kernel in covariance
do
	TEMP_LIST=(`echo ${i} | tr -s '/' ' '`)
	BENCH_NAME=${TEMP_LIST[((${#TEMP_LIST[*]}-1))]}
	BENCH_DIR=$SRC_DIR/${i}
	kernel=$BENCH_NAME
	echo $BENCH_DIR
	#echo $BENCH_NAME >> $PATT_SETTING_FILE
	#echo  $PATT_SETTING_FILE

	S1=${S1_LIST[${TEMPNUM}]}
	S2=${S2_LIST[${TEMPNUM}]}

	if [ ${psize} = "L" ]; then
	    IT_NUM=${IT_NUM_LIST_L[${TEMPNUM}]}
	    #IT_NUM=${IT_NUM_LIST_XL[${TEMPNUM}]}
	    #BEST_PARA=${BEST_PARA_LIST[${TEMPNUM}]}
	    ENALL32_PARA=${ENALL32_PARA_LIST_L[${TEMPNUM}]}
	    ANALL32_PARA=${ANALL32_PARA_LIST_L[${TEMPNUM}]}
	    LOOP_SIZE=${LOOP_SIZE_LIST_L[${TEMPNUM}]}
	    THIS_DATASET="LARGE_DATASET"
	elif [ ${psize} = "XL" ]; then
	    IT_NUM=${IT_NUM_LIST_XL[${TEMPNUM}]}
	    #BEST_PARA=${BEST_PARA_LIST[${TEMPNUM}]}
	    ENALL32_PARA=${ENALL32_PARA_LIST_XL[${TEMPNUM}]}
	    ANALL32_PARA=${ANALL32_PARA_LIST_XL[${TEMPNUM}]}
	    LOOP_SIZE=${LOOP_SIZE_LIST_XL[${TEMPNUM}]}
	    THIS_DATASET="EXTRALARGE_DATASET"
	fi
	((++TEMPNUM))


	#echo $IT_NUM
	#echo $LOOP_SIZE

	POLYBENCH_OPTION="-DPOLYBENCH_TIME -DDATA_TYPE_IS_DOUBLE -D${THIS_DATASET} -DIT_NUM=${IT_NUM} -DPOLYBENCH_USE_C99_PROTO"
	CC_OPTION="${POLYBENCH_OPTION} -I${POLYBENCH_DIR} -I${BENCH_DIR} -patt-setting=${PATT_SETTING_FILE}"

	SRC1="${BENCH_DIR}/${BENCH_NAME}.c"
	SRC2="${POLYBENCH_DIR}/polybench_original.c"



	mkdir result/${kernel}
	num=0
	#for mode in polly_default_size no_tiling i_patt orio_nm orio_sa
	#for mode in polly_default_size no_tiling manual_size
	#for mode in orio_sa
	for mode in i_patt
	#for mode in s_patt_plus
	#for mode in turbo_tiling
	#for mode in polly_default_size
	do

	    echo "mode=$mode" > ${PATT_SETTING_FILE}
	    echo "kernel_file=$SRC1" >> ${PATT_SETTING_FILE}
	    echo "threads=$threads" >> ${PATT_SETTING_FILE}
	    echo "remote=$remote" >> ${PATT_SETTING_FILE}
	    echo "repetition=$repetition" >> ${PATT_SETTING_FILE}
	    echo "loop_size=$LOOP_SIZE" >> ${PATT_SETTING_FILE}

:<<CMT
			#old setting (memkf03, th14)

			#256KB
	    echo "cSizeL2=262144" >> ${PATT_SETTING_FILE}
			#35MB
	    echo "cSizeLLC=36700160" >> ${PATT_SETTING_FILE}
	    echo "nL2=8" >> ${PATT_SETTING_FILE}
	    echo "nLLC=20" >> ${PATT_SETTING_FILE}
	    echo "lSize=64" >> ${PATT_SETTING_FILE}
	    echo "sizeDataType=8" >> ${PATT_SETTING_FILE}

			#threads=14
	    echo "r=14" >> ${PATT_SETTING_FILE}
	    echo "M=1000" >> ${PATT_SETTING_FILE}
	    echo "N=1200" >> ${PATT_SETTING_FILE}
	    echo "P=1100" >> ${PATT_SETTING_FILE}
	    echo "s1=1" >> ${PATT_SETTING_FILE}
	    echo "s2=1" >> ${PATT_SETTING_FILE}
CMT

			#32KB
	    echo "cSizeL2=32768" >> ${PATT_SETTING_FILE}
			#1MB
	    echo "cSizeLLC=1048576" >> ${PATT_SETTING_FILE}
	    echo "nL2=8" >> ${PATT_SETTING_FILE}
	    #echo "nLLC=20" >> ${PATT_SETTING_FILE}
	    echo "nLLC=16" >> ${PATT_SETTING_FILE}
	    echo "lSize=64" >> ${PATT_SETTING_FILE}
	    echo "sizeDataType=8" >> ${PATT_SETTING_FILE}

	    #echo "r=$threads" >> ${PATT_SETTING_FILE}
	    echo "r=2" >> ${PATT_SETTING_FILE}
	    echo "s1=${S1}" >> ${PATT_SETTING_FILE}
	    echo "s2=${S2}" >> ${PATT_SETTING_FILE}

			#for doubly nested loops default value
	    echo "P=1" >> ${PATT_SETTING_FILE}

			LS_TEMPNUM=0
			MNP=("M" "N" "P")
			for lsize in `echo ${LOOP_SIZE}`
			do
				if [ ${MNP[${LS_TEMPNUM}]} = "M" ]; then
					lsize=`expr ${lsize} / 32`
				fi
				echo "${MNP[${LS_TEMPNUM}]}=${lsize}" >> ${PATT_SETTING_FILE}
				((++LS_TEMPNUM))
			done

 
	    if [ ${mode} = "manual_size" ]; then
		echo "tile_size=16,1172,12" >> ${PATT_SETTING_FILE}
	    fi	
		for rep in `seq 1 ${REP_NUM[${num}]}`
		do
			echo "start ${kernel} ${mode} ${rep}"
			#echo ${CC} ${CC_OPTION} ${SRC1} ${SRC2}
			${CC} ${CC_OPTION} ${SRC1} ${SRC2} &> ./result/${kernel}/${mode}_${rep}
			#./run_${kernel}.sh &> ./result/${kernel}/${mode}_${rep}
			#./extract_data.py ./result/${kernel}/${mode}_${rep}
			#./align_this_time.py ./result/${kernel}/${mode}_${rep}_extracted
		done
		((++num))
	done

done
# mv result result_${psize}
done

#./allcsv.sh


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

