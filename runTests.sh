#!/bin/bash

for numtrain in `seq 450 1 5000`;
do
	filename="results_"$numtrain"_$1"
	echo $filename
	python run.py classifiers.classifiers.support_vec_machine $filename 0 0 0 1 $numtrain $1 0 0  
done
