import glob
# https://opencv.org/
import cv2
from test_segmentation import calculate_confusion_table,calcualte_precision, calcualte_recall

def load_data_text():
    path = './submissions/submission_*/annotations/text_ground_truth.png'
    input = []
    ground_truth = []
    for filename in glob.glob(path):
        images = []
        with open(filename, "rb") as img_file:
            print('filename', filename)
            input_name = filename.replace('/annotations/text_ground_truth.png', '') + '/RESULTS/text_blocks_black.png'
            print('input_name', input_name)
            images.append([cv2.imread(filename ).flatten().flatten().flatten(), cv2.imread(input_name).flatten().flatten().flatten()])
            # pdb.set_trace()
        for image in images:
            input.append(image[1])
            ground_truth.append(image[0])
    return input, ground_truth

def execute_test_text_detection():    
    # calculate the confidence
    input_list, ground_truth_list = load_data_text()
    confusion_table_list = calculate_confusion_table(input_list, ground_truth_list)
    precision = calcualte_precision(confusion_table_list)
    recall = calcualte_recall(confusion_table_list)
    F1_score = 2*(precision * recall) / (precision + recall)
    
    test_description = 'precision:' + str(precision) + ' recall:' + str(recall) + ' F1-score:' + str(F1_score)
    print(test_description)
    return test_description

