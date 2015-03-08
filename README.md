# pinpoint_analysis
$ cat out.txt | sort -k1,1 > out_sorted.txt  
$ cat out_sorted.txt | ./data_parser3.py
$ cat data_v3-sorted_dates.csv | sed 's/\[//g' | sed 's/\]//g
