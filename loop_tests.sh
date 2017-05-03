#!/bin/bash

for numtrain in `seq 50 200 5000`;
do
	for i in {1..50}
	do
		filename="results_"$numtrain"_$1"
		echo $filename
		python run.py classifiers.classifiers.support_vec_machine $filename 1 1 1 1 $numtrain $1 0 0  
	done
done
