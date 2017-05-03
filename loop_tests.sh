#!/bin/bash

#for numtrain in `seq 50 200 5000`;
#do
	for i in {1..50}
	do
		#filename="results_"$numtrain"_$1"
		filename="bayes_only_500_200_200"
		echo $filename
		#python run.py classifiers.classifiers.support_vec_machine $filename 1 1 1 1 $numtrain $1 0 0  
		python run.py classifiers.classifiers.support_vec_machine $filename 1 1 1 1 500 200 0 1  
	done
#done
