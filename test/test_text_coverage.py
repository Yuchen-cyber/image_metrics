from text_coverage import TextCoverage
from text_extraction import extract_text_position
import glob
import base64
# https://opencv.org/
import cv2

def test_text_coverage():
    path = './submissions/submission_1/out1R*.png'
    id = 0
    correct_detected = 0 
    for filename in glob.glob(path):
        id = id + 1
        #create the specific string
        img_string = ''
        with open(filename, "rb") as img_file:
            img_string = base64.b64encode(img_file.read())
        text_coverage = TextCoverage(filename=filename, id=id, img_string=img_string)
        text_coverage_value = text_coverage.execute_metric()
        # testing
        image = cv2.imread(filename)
        height = image.shape[0]
        width = image.shape[1]
        text_blocks = extract_text_position(filename=filename, bias = 10) 
        areas = 0
        for text_block in text_blocks:
            areas = areas + text_block[1] * text_block[3]
        text_coverage_value_test = float(areas/(height * width))
        print(text_coverage_value_test)
        print(text_coverage_value)
        if abs(text_coverage_value_test - text_coverage_value) < 0.001:
            correct_detected = correct_detected + 1
            
    return (float(correct_detected / id))
    
