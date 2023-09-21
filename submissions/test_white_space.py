from white_space import WhiteSpace
import glob
import base64
#https://opencv.org/
import cv2
from process_segmentation import processComponent
def test_white_space():
    path = './submissions/submission_*/out1R.png'
    id = 0
    correct_detected = 0 
    for filename in glob.glob(path):
        id = id + 1
        #create the specific string
        img_string = ''
        with open(filename, "rb") as img_file:
            img_string = base64.b64encode(img_file.read())
        white_space = WhiteSpace(filename=filename, id=id, img_string=img_string)
        white_space_proportion = white_space.execute_metric()
        # testing
        image = cv2.imread(filename)
        height = image.shape[0]
        width = image.shape[1]
        process_component = processComponent(id)
        processed_components = process_component.execute_combined_segmentation(filename = filename, img_string = img_string)
        areas = 0
        for component in processed_components:
            areas = areas + component[1] * component[3]
        white_space_proportion_test = 1- float(areas/(height * width))
        print(white_space_proportion_test)
        print(white_space_proportion)
        if abs(white_space_proportion_test - white_space_proportion) < 0.001:
            correct_detected = correct_detected + 1
            
        
    
    return (float(correct_detected / id))
    