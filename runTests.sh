#!/bin/bash

for num_train in `seq 50 200 5000`;
do
	filename="results_$num_train_$1"
	echo $filename
	python3 run.py classifiers.classifiers.support_vec_machine $filename 0 0 0 1 $num_train $1 0 0  
done
