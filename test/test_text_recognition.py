from  text_extraction import text_recognition
from test_segmentation import calcualte_precision, calcualte_recall

def test_OUT_1R():
    confusion_table_list = []
    for i in range(1,19):
        tp = 0
        tn = 0 
        fp = 0
        fn = 0
        target_text_list= load_ground_truth(i)
        ground_truth_texts = load_target(i)
        print(ground_truth_texts)
        print(target_text_list)
        #calculate the ture positives and false negatives
        for text in ground_truth_texts:
            if text in target_text_list:
                tp = tp + 1
                target_text_list.remove(text)
            else:
                fn = fn + 1
        #calcualte the false positives and true negatives
        fp = fp + len(target_text_list)


        confusion_table_list.append([tp, tn, fn, fp])  

    return confusion_table_list 
    
def load_ground_truth(id):
    ground_truth_filename = './submissions/submission_' + str(id) + '/annotations/gt.txt'
    ground_truth_texts = []
    with open(ground_truth_filename) as f:
        lines = f.readlines()
        for line in lines:
            text = line.replace('\n', '')
            ground_truth_texts.append(text)

    return ground_truth_texts

def load_target(id):
    target_filename = ''

    target_filename = './submissions/submission_' + str(id) + '/out1R.png'

    texts = text_recognition(target_filename)
   
    
    return texts
    

    
def execute_test_text_recognition():
    confusion_table_list = test_OUT_1R()
    precision = calcualte_precision(confusion_table_list=confusion_table_list)
    recall = calcualte_recall(confusion_table_list=confusion_table_list)
    F1_score = 2*(precision * recall) / (precision + recall)
    
    test_description = 'precision:' + str(precision) + ' recall:' + str(recall) + ' F1-score:' + str(F1_score)
    return test_description

