#https://scipy.org/
from scipy.stats import pearsonr
#https://pandas.pydata.org/
import pandas as pd
#https://pypi.org/project/chardet/
import chardet
# https://numpy.org/
import numpy as np 
import os
import csv

def caculate_correlation(x,y):
    corr, p_value= pearsonr(x, y)
    return corr, p_value

# take first element for sort
def takeFirst(elem):
    return elem[0]

def get_pearson_value():
    dir_save = './submissions/correlations' 
    command = "mkdir " + dir_save
    if not os.path.exists(dir_save):
        os.system(command)
    command = "./ " + dir_save + '/correlation_value.csv'
    if not os.path.exists(dir_save + '/correlation_value.csv'):
        os.system(command)
    metric_names = ['saliency', 'nttr', 'text_coverage', 'white_space', 'colourfulness', 'text_similarity', 'wave']
    print("start computing Pearsons correlation ...")
    fileName = './submissions/metrics_results.csv'
    human_mark = []
    metric_value = []
    csv_filename = dir_save + '/correlation_value.csv'
    with open(csv_filename, 'w') as csv_file:
        metric_writer = csv.writer(csv_file)
        metric_writer.writerow(['metric name','mark name','r_value', 'p_value'])
        for metric_name in metric_names:
            with open(fileName, 'rb') as f:
                result = chardet.detect(f.read())
            df = pd.read_csv(fileName, encoding=result['encoding'])
            mark_name = ''
            if metric_name == 'white_space':
                mark_name = 'gestalt_mark'
            if metric_name == 'nttr' or metric_name == 'text_coverage':
                mark_name = 'aid_mark'
            if metric_name == 'wave' or metric_name == 'colourfulness':
                mark_name = 'colour_mark'
            if metric_name == 'saliency' or metric_name == 'text_similarity':
                mark_name = 'language mark'
            metric_value = df[metric_name]
            ids = np.array(df['id'])
            metric_list = list(zip(ids,metric_value))
            metric_list.sort(key=takeFirst)
            metric_value = np.array(list(zip(*metric_list))[1])
                
            with open('./human_mark.csv', 'rb') as f:
                result = chardet.detect(f.read())
            mark_df = pd.read_csv('./human_mark.csv', encoding=result['encoding'])
            human_mark = mark_df[mark_name]
            corr, p_value = caculate_correlation(metric_value, human_mark)
            metric_writer.writerow([metric_name, mark_name,  corr, p_value])
            
    
get_pearson_value()

