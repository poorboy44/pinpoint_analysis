# pinpoint_analysis
`$ cat out.txt | sort -k1,1 > out_sorted.txt`  
`$ cat out_sorted.txt | ./data_parser3.py`  
`$ cat data_v3-sorted_dates.csv | sed 's/\[//g' | sed 's/\]//g  > data_4_R.csv`  

NOTE: you may have to use the following command to clean up the code as 'null' may not work in R.  

`$ cat data_v3-sorted_dates.csv | sed 's/\[//g' | sed 's/\]//g' | sed 's/null/NA/g'  > data_4_R.csv`  

Header:  
student_name, vsim_counts, vsim date, vsim score, prepU_counts, prepU_median, prepU_mean, prepU_stdev, prepU_vector (20 values), overall_ml_counts, overall_ml_median, overall_ml_mean, overall_ml_stdev, overall_ml vector (20 values)


