#https://opencv.org/
import cv2
# https://numpy.org/
import numpy as np
from metric_utils.text_extraction import extract_text_position
from metric_utils.process_segmentation import processComponent
from metric import Metric
    
class NTTR(Metric):
    """
    Metric: Non-Text and Text Ratio (NTTR)
    """
    
    def __init__(self, id, filename, img_string):
        """
        Initiate the metric calculation
        
        Args:
            id: int. The id of every submission
            filename: str. The filename of the assessed visualisation
            img_string: str. The image string of that visualisation

        """
        self.nttr_img = None
        super().__init__(id, filename, img_string)
    
    def execute_metric(self):
        """
        Execute the metric.

        Returns:
            non_text_text_ratio: float. The ratio of non-text areas and text areas (float)
        """
        #get text
        text_blocks = extract_text_position(filename=self.filename, bias = 10) 
        img = cv2.imread(self.filename) 
        img_shape = img.shape
        
        non_text_coverage = np.zeros((img_shape[0], img_shape[1]), dtype=int)
        text_coverage = np.zeros((img_shape[0], img_shape[1]), dtype=int)
        
        process_component = processComponent(self.id)
        element_blocks = process_component.execute_combined_segmentation(filename=self.filename, img_string=self.img_string)
        visual_block_color = (96, 163, 215)
        text_color = (162, 32, 66)
        white = (255, 255, 255)
        height = len(img[0])
        width = len(img)
        self.nttr_img = [[white] * height] * width
        self.nttr_img = np.array(self.nttr_img)
        
        #make the covered visual blocks areas be 1
        for element_block in element_blocks:
            non_text_coverage[element_block[2]:element_block[2]+element_block[3], element_block[0]:element_block[0]+element_block[1]] = 1
            self.nttr_img[element_block[2]:element_block[2]+element_block[3], element_block[0]:element_block[0]+element_block[1]] = visual_block_color
        # make the text blocks areas be 0
        for text_block in text_blocks:
            non_text_coverage[text_block[2]:text_block[2]+text_block[3], text_block[0]:text_block[0]+text_block[1]] = 0
            text_coverage[text_block[2]:text_block[2]+text_block[3], text_block[0]:text_block[0]+text_block[1]] = 1 
            self.nttr_img[text_block[2]:text_block[2]+text_block[3], text_block[0]:text_block[0]+text_block[1]] = text_color
        
        #calculate
        non_text_proportion = float(np.mean(non_text_coverage))
        text_proportion = float(np.mean(text_coverage))
        non_text_text_ratio = non_text_proportion / text_proportion
        
        self.save_nttr_map()
        return non_text_text_ratio
    
    def save_nttr_map(self):
        """
        Save the nttr distribution map
        """
        dir2save = './submissions/submission_' + str(self.id) + '/RESULTS/nttr_dist.png'
        print('saving images')
        status = cv2.imwrite((dir2save), self.nttr_img)
        
    
