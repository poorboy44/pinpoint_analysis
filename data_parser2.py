#!/usr/bin/env python
import sys
import json
from datetime import datetime
from collections import OrderedDict
import copy
import operator
from itertools import chain

def split_data(line):
    rec = line.strip().split("|")
    current_student = rec[0]
    class_name = rec[1]
    current_date = datetime.strptime(rec[2],"%Y-%m-%d %H:%M:%S")
    test_type = rec[3]
    test_score = rec[4]
    return current_student, class_name, current_date, test_type, test_score

def define_globals():
    prev_student = -1
    fileName = "data_v2-sorted_dates.csv"
    now = datetime.now()
    d_list = {'ml':[], 'best':[]}
    return prev_student, now, d_list, fileName

def increment_counts(data,d_list,student):
    d = OrderedDict()
    for vsim in data.iteritems():
        rank = vsim[0]
        vsim_date_obj = vsim[1][0]
        vsim_date_str = vsim[1][1]
        vsim_test_score = int(vsim[1][2])
        ml_count_on_date = vsim[1][3]
        d[rank]=[vsim_date_str,vsim_test_score,ml_count_on_date]
        for ml in d_list['ml']:
            ml_date_obj = ml[0]
            # compare dates
            if ml_date_obj <= vsim_date_obj:
                #print "data[rank]: {}".format(data[rank])
                d[rank][2] += 1
    printable={"scores":d,"student":student}
    return printable


if __name__ == '__main__':
    sys.stderr.write("Header:\nstudent name, # of previous vsim attempts, vsim date, vsim score, # of previous prepU attempts\n\n")

    #define globals
    prev_student, now, d_list, fileName = define_globals()

    with open(fileName,"wb") as f:
        for line in sys.stdin:

            # parse line
            current_student, current_class, current_date, test_type, test_score = split_data(line)

            # check new student
            if current_student != prev_student and prev_student != -1:

                # add date if empty
                if len(d_list['best']) == 0:
                    d_list['best'] = [(now,datetime.strftime(now,"%Y-%m-%d %H:%M:%S"),0,0)]

                # order dates
                d_list['best'] = sorted(d_list['best'],key = operator.itemgetter(0))

                # create an ordered dict of vsim counts by date
                data = OrderedDict(zip(range(0,len(d_list['best'])),d_list['best']))

                # increment ml counts per dated vsim attempt
                results = increment_counts(data,d_list,prev_student)

                # print results
                for score in results["scores"].iteritems():
                    #print json.dumps([results["student"],score[0],score[1][0],score[1][1],score[1][2]])
                    f.write(json.dumps([results["student"],score[0],score[1][0],score[1][1],score[1][2]])+'\n')

                # reset counts for each new student
                d_list = {'ml':[], 'best':[]}

            # append values based on test_type
            d_list[test_type].append([current_date,str(current_date),test_score,0])
            #print d_list

            # set prev student
            prev_student = copy.deepcopy(current_student)

sys.stderr.write("Reults saved: {}\n\n".format(fileName))
