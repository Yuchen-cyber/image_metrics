#Library
#https://numpy.org/
import numpy as np
#https://pandas.pydata.org/
import pandas as pd
#https://matplotlib.org/
import matplotlib.pyplot as plt
#https://pypi.org/project/chardet/
import chardet
import os

def draw_all(execute_number):
    metric_names = ['saliency', 'nttr', 'text_coverage', 'white_space', 'colourfulness', 'text_similarity', 'wave']
    fileName = './submissions/metrics_results.csv'
    x = [id for id in range(execute_number)]
    y = []
    dir_save = './submissions/frequencies' 
    command = "mkdir " + dir_save
    if not os.path.exists(dir_save):
        os.system(command)
        
    for metric_name in metric_names:
        with open(fileName, 'rb') as f:
            result = chardet.detect(f.read())
            df = pd.read_csv(fileName, encoding=result['encoding'])
            y = df[metric_name]

       
        
        # Plot the histogram.
        hist, bins = np.histogram(y)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        average_value = np.mean(y)
        # the line below is written based on:https://stackoverflow.com/questions/3866520/plot-a-histogram-such-that-bar-heights-sum-to-1-probability
        plt.bar(bins[:-1], hist.astype(np.float32) / hist.sum(), width=(bins[1]-bins[0]), alpha=0.6, color='b')
        lines = ax.plot([average_value, average_value], [0.4, 0.6], color = 'r', label="average value")
        saved_file_name = metric_name + '.png'
        command = dir_save + '/' + saved_file_name
        title = 'The average ' +  metric_name.replace('_', ' ') + ' metric value:' + str(round(average_value,2))
        plt.xlabel(metric_name.replace('_', ' '))  
         # Drawing a graph              
        plt.grid(True, alpha=0.3, linestyle="--")  
        plt.ylabel('Frequency') 
        plt.title(label=title,color="r")
        plt.legend(loc="upper left")
        # Set the range of x-axis
        if metric_name != "nttr" and metric_name != 'colourfulness':
            plt.xlim(0, 1) # non-text and texct ratio are not range from 0 to 1

        plt.ylim(0, 1)
        plt.savefig(command)
        plt.clf()

# take first element for sort
def takeFirst(elem):
    return elem[0]

def draw_single(execute_number):
    metric_names = ['saliency', 'nttr', 'text_coverage', 'white_space', 'colourfulness', 'text_similarity', 'wave']
    fileName = './submissions/metrics_results.csv'
    x = [id for id in range(18)]
    y = []
    dir_save = './submissions/submission_' 
        
    for metric_name in metric_names:
        lines = []
        with open(fileName, 'rb') as f:
            result = chardet.detect(f.read())
            df = pd.read_csv(fileName, encoding=result['encoding'])
            y = df[metric_name]
            
        ids = np.array(df['id'])
        metric_list = list(zip(ids,y))
        metric_list.sort(key=takeFirst)
        sorted_y = np.array(list(zip(*metric_list))[1])

        

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        average_value = np.mean(sorted_y)
        
        

        for i in range(1, execute_number + 1):
            # Plot the histogram.
            hist, bins = np.histogram(y)
            # the line below is written based on:https://stackoverflow.com/questions/3866520/plot-a-histogram-such-that-bar-heights-sum-to-1-probability
            plt.bar(bins[:-1], hist.astype(np.float32) / hist.sum(), width=(bins[1]-bins[0]), alpha=0.6, color='b')
            index = i - 1
            value = round(sorted_y[index],2)
            lines = ax.plot([average_value, average_value], [0.4, 0.6], color = 'r', label="average value")
            lines.append(ax.plot([value, value], [0.6, 0.8], color = 'g', label="your value"))
            saved_file_name = metric_name + '_result.png'
            command = dir_save  + str(i) + '/RESULTS/' +saved_file_name
            title = 'Your image ' +  metric_name.replace('_', ' ') + ' metric:' + str(value)
            plt.title(label=title,color="g")
            plt.legend(loc="upper left")
            # Drawing a graph
            plt.xlabel(metric_name)    
            plt.ylabel('Frequency')                
            plt.grid(True, alpha=0.3, linestyle="--")
             # Set the range of x-axis
            if metric_name != "nttr" and metric_name != 'colourfulness':
                plt.xlim(0, 1) # non-text and texct ratio are not range from 0 to 1

            plt.ylim(0, 1)
            plt.savefig(command)
            ax.clear()
        
        plt.clf()
        