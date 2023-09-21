import glob
# https://opencv.org/
import cv2
import statistics

def load_data():
    # the path can be replaced
    path = './submissions/submission_*/annotations/ground_truth.png'
    input = []
    ground_truth = []
    for filename in glob.glob(path):
        images = []
        with open(filename, "rb") as img_file:
            input_name = filename[:-29] + '/RESULTS/left.png'
            images.append([cv2.imread(filename ).flatten().flatten().flatten(),cv2.imread(input_name).flatten().flatten().flatten()])
            # pdb.set_trace()
        for image in images:
            input.append(image[1])
            ground_truth.append(image[0])

    return input, ground_truth

def load_data_uied():
    # the path can be replaced
    path = './submissions/submission_*/annotations/ground_truth.png'
    input = []
    ground_truth = []
    for filename in glob.glob(path):
        images = []
        with open(filename, "rb") as img_file:
            input_name = filename[:-29] + '/RESULTS/left_uied.png'
            images.append([cv2.imread(filename ).flatten().flatten().flatten(),cv2.imread(input_name).flatten().flatten().flatten()])
            # pdb.set_trace()
        for image in images:
            input.append(image[1])
            ground_truth.append(image[0])

    return input, ground_truth

def calculate_confusion_table(input_list, ground_truth_list):
    table_list =[]
    for i in range(len(input_list)):
        input = input_list[i]
        ground_truth = ground_truth_list[i]
        tp = 0
        tn = 0
        fn = 0
        fp = 0
        for j in range(len(input)):
            y_pred = input[j]
            y_true = ground_truth[j]
            if y_true == 0:
                if y_pred == y_true:
                    tp = tp + 1
                else:
                    fn = fn + 1
            if y_true == 255:
                if y_pred == y_true:
                    tn = tn + 1
                else:
                    fp = fp + 1
        table_list.append([tp, tn, fn, fp])
    print(len(input_list))
    return table_list


def calcualte_precision(confusion_table_list):
    precision_list = []
    for table in confusion_table_list:
        precision_single = 0
        if (table[0] + table[3]) != 0:
            precision_single = table[0] / (table[0] + table[3])
        
        precision_list.append(precision_single)

    return statistics.mean(precision_list)

def calcualte_recall(confusion_table_list):
    recall_list = []
    for table in confusion_table_list:
        recall_single = 0
        if (table[0] + table[2]) != 0:
            recall_single = table[0] / (table[0] + table[2])
        recall_list.append(recall_single)

    return statistics.mean(recall_list)



def execute_test_image_segmentation(type = 'combined'):
    input_list=[]
    ground_truth_list = []
    if type == 'combined':
        input_list, ground_truth_list = load_data()
    else:
        input_list, ground_truth_list = load_data_uied()
        
    confusion_table_list = calculate_confusion_table(input_list, ground_truth_list)
    precision = calcualte_precision(confusion_table_list)
    recall = calcualte_recall(confusion_table_list)
    F1_score = 2*(precision * recall) / (precision + recall)
    
    test_description = 'precision:' + str(precision) + ' recall:' + str(recall) + ' F1-score:' + str(F1_score)
    print(test_description)
    return test_description


