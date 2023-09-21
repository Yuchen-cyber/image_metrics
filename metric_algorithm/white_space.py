#https://opencv.org/
import cv2
# https://numpy.org/
import numpy as np
from metric_utils.process_segmentation import processComponent
from metric import Metric
class WhiteSpace(Metric):
    """
    Metric: White Space
    """
    def __init__(self, id, filename, img_string):
        """
        Initiate the metric calculation
        
        Args:
            id: int. The id of every submission
            filename: str. The filename of the assessed visualisation
            img_string: str. The image string of that visualisation

        """
        self.left_img = None
        super().__init__(id, filename, img_string)

    def execute_metric(self):
        """
        Execute the metric.

        Returns:
            white_space_proportion: float.  White space proportion in a visualisation
        """  
        image = cv2.imread(self.filename)
        height = image.shape[0]
        width = image.shape[1]
        process_component = processComponent(self.id)
        processed_components = process_component.execute_combined_segmentation(filename = self.filename, img_string = self.img_string)
        
        whiteSpaceList = np.ones((height, width), dtype=int)
        black = (0,0,0)
        white = (255,255,255)
        height = len(image[0])
        width = len(image)
        self.left_img = [[white] * height] * width
        self.left_img = np.array(self.left_img)
        
        for component in processed_components:
            self.left_img[component[2]:component[2]+component[3], component[0]:component[0]+component[1]] = black
            whiteSpaceList[component[2]:component[2]+component[3], component[0]:component[0]+component[1]] = 0
        
        white_space_proportion = float(np.mean(whiteSpaceList))
        self.save_left_img()
        return white_space_proportion
    
    def save_left_img(self):
        """
        Save the images that all visual blocks areas are black while other areas are white
        """
        dir2save = './submissions/submission_' + str(self.id) + '/RESULTS/left.png'
        status = cv2.imwrite(dir2save, self.left_img)