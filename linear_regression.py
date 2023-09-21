# https://numpy.org/
import numpy as np
# https://matplotlib.org/
import matplotlib.pyplot as plt
# https://scikit-learn.org/stable/
from sklearn.linear_model import LinearRegression
#https://pandas.pydata.org/
import pandas as pd
#https://pypi.org/project/chardet/
import chardet
import os

# take first element for sort
def takeFirst(elem):
    return elem[0]
def draw_linear_graph():
    metric_names = ['saliency', 'nttr', 'text_coverage', 'white_space', 'colourfulness', 'text_similarity', 'wave']
    lm = LinearRegression()
    fileName = './submissions/metrics_results.csv'
    dir_save = './submissions/correlations' 
    command = "mkdir " + dir_save
    if not os.path.exists(dir_save):
        os.system(command)
    for metric_name in metric_names:
        with open(fileName, 'rb') as f:
            result = chardet.detect(f.read())
        df = pd.read_csv(fileName, encoding=result['encoding'])
        X_train = df[metric_name]
        mark_name = ''
        if metric_name == 'white_space':
            mark_name = 'gestalt_mark'
        if metric_name == 'nttr' or metric_name == 'text_coverage':
            mark_name = 'aid_mark'
        if metric_name == 'wave' or metric_name == 'colourfulness':
            mark_name = 'colour_mark'
        if metric_name == 'saliency' or metric_name == 'text_similarity':
            mark_name = 'language mark'
        ids = np.array(df['id'])
        metric_list = list(zip(ids,X_train))
        metric_list.sort(key=takeFirst)
        X_train = np.array(list(zip(*metric_list))[1]).reshape(-1, 1)
            
        with open('./human_mark.csv', 'rb') as f:
            result = chardet.detect(f.read())
        mark_df = pd.read_csv('./human_mark.csv', encoding=result['encoding'])
        y_train = np.array(mark_df[mark_name])
        lm.fit(X_train,y_train)
        if metric_name != "nttr" and metric_name != 'colourfulness':
            plt.xlim(0, 1) # non-text and texct ratio are not range from 0 to 1 

        # Plot the data and the regression line
        plt.scatter(X_train, y_train)
        plt.plot(X_train, lm.coef_[0]*X_train + lm.intercept_, color='red', label='Slope:' + str(round(lm.coef_[0],2)) + " Intercept:" + str(round(lm.intercept_)))
        plt.xlabel(metric_name.replace('_', ' '))
        plt.ylabel(mark_name.replace('_', ' '))
        plt.legend(loc="upper left")
        plt.ylim(0, 10)
        plt.grid(True, alpha=0.3, linestyle="--")
        saved_file_name = metric_name + '_similarity'
        command = dir_save + '/' + saved_file_name
        plt.savefig(command)
        plt.clf()