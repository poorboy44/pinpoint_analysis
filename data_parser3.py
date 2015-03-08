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
    test_score = float(rec[4])
    return current_student, class_name, current_date, test_type, test_score

def define_globals():
    prev_student = -1
    #fileName = "data_v2-sorted_dates.csv"
    fileName = "data_v3-sorted_dates.csv"
    now = datetime.now()
    d_list = {'ml':[], 'best':[], 'overall_ml':[]}
    return prev_student, now, d_list, fileName

def evaluate_vector(test_score,count,lst):
    # keeps the vectors length at v_len
    # starts counting the number of test taken at or beyond 20.
    v_len=20
    if count > v_len:
        lst[v_len - 1] = lst[v_len - 1]+1
    elif count == v_len:
        lst.append(1)
    else:
        lst.append(test_score)
    return lst

def increment_counts(data,d_list,student):
    singl_d = OrderedDict()
    outer_counter = 0
    for vsim in data.iteritems():
        outer_counter+=1
        rank = vsim[0]
        vsim_date_obj = vsim[1][0]
        vsim_date_str = vsim[1][1]

        # check if the vsim can be converted to int
        if vsim[1][2] != None:
            vsim_test_score = float(vsim[1][2])
        else:
            vsim_test_score = vsim[1][2]

        # increment test counts and appends values to the test_vectors
        ml_count_on_date = vsim[1][3]
        oml_count_on_date = vsim[1][4]
        singl_d[rank] = [vsim_date_str,vsim_test_score,ml_count_on_date,[],oml_count_on_date,[]]

        inner_ml_counter = 0
        for ml in d_list['ml']:
            inner_ml_counter+=1
            ml_date_obj = ml[0]

            # compare dates
            if ml_date_obj <= vsim_date_obj:

                # incredment ml count
                singl_d[rank][2] += 1
                singl_d[rank][3]=evaluate_vector(ml[2],singl_d[rank][2],singl_d[rank][3])

        inner_oml_counter = 0
        for oml in d_list['overall_ml']:
            inner_oml_counter += 1
            oml_date_obj = oml[0]

            # compare dates
            if oml_date_obj <= vsim_date_obj:

                # incredment overall_ml count
                singl_d[rank][4] += 1
                # append test score
                singl_d[rank][5]=evaluate_vector(oml[2],singl_d[rank][4],singl_d[rank][5])
                #singl_d[rank][5].append(oml[2])
    # add null values for those students that have not yet taken 20+ exams
    for rank in singl_d:
        length1 = len(singl_d[rank][3])
        length2 = len(singl_d[rank][5])
        if length1 < 20:
            singl_d[rank][3].extend([None]*(20-length1))
        if length2 < 20:
            singl_d[rank][5].extend([None]*(20-length2))

    printable={"scores":singl_d,"student":student}
    return printable

def median(lst):
    lst = [ x for x in lst if x is not None]
    lst = sorted(lst)
    n = len(lst)
    if n < 1:
        return None
    if n %2 == 1:
        return lst[((n+1)/2)-1]
    if len(lst) %2 == 0:
        return float(sum(lst[(n/2)-1:(n/2)+1]))/2.0

def mean(lst):
    lst = [ x for x in lst if x is not None]
    n = float(len(lst))
    if n < 1:
        return None
    else:
        return round(sum(lst)/n,4)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    data = [ x for x in data if x is not None]
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    """Calculates the population standard deviation."""
    data = [ x for x in data if x is not None]
    n = len(data)
    if n < 2:
        return None
    ss = _ss(data)
    pvar = ss/n # the population variance
    return round(pvar**0.5,4)

def print_results(results,f):

    for score in results["scores"].iteritems():
        student = results["student"]
        vsim_count = score[0]
        vsim_date = score[1][0]
        vsim_score = score[1][1]
        prepU_exam_count = score[1][2]
        prepU_vector = score[1][3]
        prepU_median = median(prepU_vector)
        prepU_mean = mean(prepU_vector)
        prepU_stdev = pstdev(prepU_vector)
        overall_ml_count = score[1][4]
        overall_ml_vector = score[1][5]
        overall_ml_median = median(overall_ml_vector)
        overall_ml_mean = mean(overall_ml_vector)
        overall_ml_stdev = pstdev(overall_ml_vector)
        f.write(json.dumps(
            [results["student"],
                vsim_count,
                vsim_date,
                vsim_score,
                prepU_exam_count,
                prepU_median,
                prepU_mean,
                prepU_stdev,
                prepU_vector,
                overall_ml_count,
                overall_ml_median,
                overall_ml_mean,
                overall_ml_stdev,
                overall_ml_vector])+'\n')

def process_data(d_list,now,prev_student):
    # add date student has not taken vsim
    if len(d_list['best']) == 0:
        d_list['best'] = [(now,datetime.strftime(now,"%Y-%m-%d %H:%M:%S"),None,0,0)]

    # order dates
    d_list['best'] = sorted(d_list['best'],key = operator.itemgetter(0))

    # create an ordered dict of vsim counts by date
    data = OrderedDict(zip(range(0,len(d_list['best'])),d_list['best']))

    # increment ml counts per dated vsim attempt
    results = increment_counts(data,d_list,prev_student)

    # print results
    print_results(results,f)

    # reset counts for each new student
    return {'ml':[], 'best':[], 'overall_ml':[]}



if __name__ == '__main__':
    #define globals
    prev_student, now, d_list, fileName = define_globals()
    sys.stderr.write("Header:\nstudent_name, vsim_counts, vsim date, vsim score, prepU_counts, prepU_median, prepU_mean, prepU_stdev, prepU_vector (20 values), overall_ml_counts, overall_ml_median, overall_ml_mean, overall_ml_stdev, overall_ml vector (20 values)\n\n")

    with open(fileName,"wb") as f:
        for line in sys.stdin:
            # parse line
            current_student, current_class, current_date, test_type, test_score = split_data(line)

            # check new student
            if current_student != prev_student and prev_student != -1:
                d_list=process_data(d_list,now,prev_student)

            # append [current_date, date_string, test_score,count] based on test_type, ml_count, overall_ml_count
            d_list[test_type].append([current_date,str(current_date),test_score,0,0])
            #print d_list

            # set prev student
            prev_student = copy.deepcopy(current_student)

        # add the last student 
        process_data(d_list,now,prev_student)
    sys.stderr.write("Reults saved: {}\n\n".format(fileName))
