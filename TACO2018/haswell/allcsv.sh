#!/bin/bash

rm -f alldata.csv

ALLFILE=`ls *_extracted_aligned`

echo ${ALLFILE} >> alldata.csv
paste -d"," ${ALLFILE} >> alldata.csv



:<<CMT
for i in `ls *_extracted_aligned`
do
	echo ${i} >> alldata.csv
	cat ${i} >> alldata.csv
done
CMT




