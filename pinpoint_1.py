"""
This script processes the results.json file into a pipe delimieted list 
appropraite for input into pythom modeling scripts
"""

import pandas as pd
import sys
from pymongo import MongoClient
import numpy as np

#set up client connection
client = MongoClient()
db = client.pinpoint
result=db.result

# #create empty data frame
# d=pd.DataFrame()

# #iterate through data and append to data frame
# line_num=0
# for rec in result.find():
# 	line_num+=1
# 	#if line_num>10:
# 	#	break
# 	try:
# 		d=d.append(rec, ignore_index=True)
# 	except:
# 		sys.stderr.write( "Error on line:{}\n".format(line_num))
# 		continue
# d.to_csv('data.csv')

line_num=0
error_num=0
with open('out.txt', 'w') as out:
	for rec in result.find():
		line_num+=1
		try:
			student = rec['student']['first_name'] + " " + rec['student']['last_name']
			student = student.strip('|') 
			classname= rec['class']['name']
			dt = rec['result_date']
			if 'ml' in rec.keys():
				ml = rec['ml']
				out.write("{}|{}|{}|ml|{}\n".format(student, classname, dt, ml))
			elif 'best' in rec.keys():
				best = rec['best']
				out.write("{}|{}|{}|best|{}\n".format(student, classname, dt, best))
		except:
			error_num+=1
			sys.stderr.write( "Error on line:{}\n".format(line_num))
			continue
	sys.stderr.write("DONE\n")
	sys.stderr.write("Total errors:{}".format(error_num))




