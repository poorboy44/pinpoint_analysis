#!/usr/bin/env python
import sys
import json
from datetime import datetime
import copy



#map(sum,zip([1,2],[0,5])) 

def split_data(line):
    # split line
    rec = line.strip().split("|")
    current_student = rec[0]
    class_name = rec[1]
    current_date = datetime.strptime(rec[2],"%Y-%m-%d %H:%M:%S")
    test_type = rec[3]
    test_score = rec[4]
    return current_student, class_name, current_date, test_type, test_score

def define_globals():
    prev_student = -1
    now = datetime.now()
    d_list = {'ml':[], 'best':[]}
    return prev_student, now, d_list

def increment_counts(data,d_list,student):
    d = {date:[data[date],0] for date in data}
    for vsim_date in d:
        for ml_date in d_list['ml']:
            if ml_date <= vsim_date:
                d[vsim_date][1]+=1

    # dates >> strings
    printable = {"scores":{}}
    date_list = d.keys()
    date_list.sort()
    for item in date_list:
        printable["scores"][str(item)] = d[item]

    printable["student"] = student

    return printable

if __name__ == '__main__':

    #define globals
    prev_student, now, d_list = define_globals()

    for line in sys.stdin:

        # parse line
        current_student, current_class, current_date, test_type, test_score = split_data(line)

        # check to see if we have a new student
        if current_student != prev_student and prev_student != -1:
            if len(d_list['best']) == 0:
                d_list['best'] = [now]

            # order dates
            d_list['best'].sort()
            d_list['ml'].sort()

            # create a dict of vsim counts
            data=dict(zip(d_list['best'],range(0,len(d_list['best']))))

            #print increment_counts(data,d_list,current_student)
            print json.dumps(increment_counts(data,d_list,prev_student))

            # reset counts for each new student
            d_list = {'ml':[], 'best':[]}

        # append values based on test_type
        d_list[test_type].append(current_date)

        # set prev student
        prev_student = copy.deepcopy(current_student)
