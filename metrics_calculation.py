import os
import csv
from text_similarirty import TextSimilarity
from white_space import WhiteSpace
from text_coverage import TextCoverage
from NTTR import NTTR
from saliency import Saliency
from colorfulness import Colorfulness
from WAVE import WAVE
import base64
import glob


def metric_calculation(execute_metric):
    # create the folders
    dir2save = 'submissions'
    command = "./" + dir2save + "/metrics_results.csv"
    if not os.path.exists(dir2save):
        os.system(command)
    print("start metric evaluation...")
    path = './submissions/submission_*/out1R.png'
    
    number = 0

    with open('./submissions/metrics_results.csv', 'w') as csvfile:
        metric_writer = csv.writer(csvfile)
        if execute_metric == 'all':
            metric_writer.writerow(['id', 'colourfulness', 'wave', 'saliency', 'text_similarity', 'white_space', 'text_coverage', 'nttr'])
        for filename in glob.glob(path):
            number = number + 1
            id = filename[-12:-10].replace('_', '')
            # create the file for each result
            dir_svae_each = './submissions/submission_' + str(id) + '/RESULTS'
            command = "mkdir " + dir_svae_each
            if not os.path.exists(dir_svae_each):
                os.system(command)
            # create the csv file for each result 
            command = "./ " + dir_svae_each + '/metrics_results.csv'
            if not os.path.exists(dir_svae_each + '/metrics_results.csv'):
                os.system(command)
                
                
            print("start metric evaluation...")
                
            
            #create the specific string
            img_string = ''
            with open(filename, "rb") as img_file:
                img_string = base64.b64encode(img_file.read())
                
            # write the results for each submission
            csv_single_file = dir_svae_each + '/metrics_results.csv'  
            with open(csv_single_file, 'w') as csvfile_each:
                metric_writer_each = csv.writer(csvfile_each)
                
                text_similarity_value = 0
                white_space_prroportion = 0
                text_coverage_value = 0
                nttr_value = 0
                saliency_value = 0
                colourfulness_value = 0
                wave_value = 0
                
                if execute_metric == 'all':
                    metric_writer_each.writerow(['colourfulness', 'wave', 'saliency', 'text_similarity', 'white_space', 'text_coverage', 'nttr'])
                # text similarity
                if execute_metric == 'all' or execute_metric == 'text similarity':
                    text_similarity = TextSimilarity(filename=filename, img_string = img_string, id = id)
                    text_similarity_value = text_similarity.execute_metric()
                # white space
                if execute_metric == 'all' or execute_metric == 'white space':
                    white_space = WhiteSpace(filename=filename, img_string = img_string, id = id)
                    white_space_prroportion = white_space.execute_metric()

                # text coverage
                if execute_metric == 'all' or execute_metric == 'text coverage':
                    text_coverage = TextCoverage(filename=filename, img_string = img_string, id = id)
                    text_coverage_value = text_coverage.execute_metric()

                # nttr
                if execute_metric == 'all' or execute_metric == 'nttr':
                    nttr = NTTR(filename=filename, img_string = img_string, id = id)
                    nttr_value = nttr.execute_metric()

                # saliency
                if execute_metric == 'all' or execute_metric == 'saliency':
                    saliency = Saliency(filename=filename, img_string = img_string, id = id)
                    saliency_value = saliency.execute_metric()

                # colourfulness
                if execute_metric == 'all' or execute_metric == 'colourfulness':
                    colourfulness = Colorfulness(filename=filename, img_string = img_string, id = id)
                    colourfulness_value = colourfulness.execute_metric()
                # wave
                if execute_metric == 'all' or execute_metric == 'wave':
                    wave = WAVE(filename=filename, img_string = img_string, id = id)
                    wave_value = wave.execute_metric()

                # write values
                if execute_metric == 'all':
                    metric_writer_each.writerow([colourfulness_value,wave_value, saliency_value, text_similarity_value, white_space_prroportion, text_coverage_value, nttr_value])
            
            
            if execute_metric == 'all':
                metric_writer.writerow([id, colourfulness_value,wave_value, saliency_value, text_similarity_value, white_space_prroportion, text_coverage_value, nttr_value])
            
    csvfile.close()
    return number
        

        

    

        