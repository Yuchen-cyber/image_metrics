from text_extraction import extract_text_position
# https://opencv.org/
import cv2
# https://numpy.org/
import numpy as np
from metric import Metric
   
class TextCoverage(Metric):
    """
    Metric: Text Coverage
    """
    
    def __init__(self, id, filename, img_string):
        """
        Initiate the metric calculation
        
        Args:
            id: int. The id of every submission
            filename: str. The filename of the assessed visualisation
            img_string: str. The image string of that visualisation

        """
        self.text_blocks_img = None
        super().__init__(id, filename, img_string)
    
    def execute_metric(self):
        """
        Execute the metric.

        Returns:
            text_proportion: float.  Text areas proportion in a visualisation
        """  
        text_blocks = extract_text_position(filename=self.filename, bias = 10) 
        img = cv2.imread(self.filename) 
        img_shape = img.shape
        text_coverage = np.zeros((img_shape[0], img_shape[1]), dtype=int)
        black = (0,0,0)
        white = (255,255,255)
        height = len(img[0])
        width = len(img)
        self.text_blocks_img = [[white] * height] * width
        self.text_blocks_img = np.array(self.text_blocks_img)
        
        for text_block in text_blocks:
            text_coverage[text_block[2]:text_block[2]+text_block[3], text_block[0]:text_block[0]+text_block[1]] = 1
            self.text_blocks_img[text_block[2]:text_block[2]+text_block[3], text_block[0]:text_block[0]+text_block[1]] = black
            
         
        text_proportion = float(np.mean(text_coverage))
        self.save_text_blocks_img()
        return text_proportion
    
    def save_text_blocks_img(self):
        """
        Save the images that all text areas are black while other areas are white
        """
        dir2save = './submissions/submission_' + str(self.id) + '/RESULTS/text_blocks_black.png'
        status = cv2.imwrite(dir2save, self.text_blocks_img) 
        