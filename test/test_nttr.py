
from metric_algorithm.NTTR import NTTR
from metric_utils.text_extraction import extract_text_position
from metric_utils.process_segmentation import processComponent
import glob
import base64

def test_nttr():
    path = './submissions/submission_1/out1R*.png'
    id = 0
    correct_detected = 0 
    for filename in glob.glob(path):
        id = id + 1
        #create the specific string
        img_string = ''
        with open(filename, "rb") as img_file:
            img_string = base64.b64encode(img_file.read())
        nttr = NTTR(filename=filename, id=id, img_string=img_string)
        nttr_value = nttr.execute_metric()
        # testing

        text_blocks = extract_text_position(filename=filename, bias = 10) 
        process_component = processComponent(id)
        processed_components = process_component.execute_combined_segmentation(filename = filename, img_string = img_string)
        text_areas = 0
        non_text_areas = 0
        for component in processed_components:
            non_text_areas = non_text_areas + component[1] * component[3]
        for text_block in text_blocks:
            text_areas = text_areas + text_block[1] * text_block[3]
            
        nttr_value_test = float((non_text_areas - text_areas)/(text_areas))
        print(nttr_value_test)
        print(nttr_value)
        if abs(nttr_value_test - nttr_value) < 0.001:
            correct_detected = correct_detected + 1
            
    return (float(correct_detected / id))
    