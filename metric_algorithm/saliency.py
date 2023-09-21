# import the necessary packages
#https://opencv.org/
import cv2 as cv
# https://pillow.readthedocs.io/en/stable/
from PIL import Image as im
# https://numpy.org/
import numpy as np
from metric import Metric
# the code below is written based on: https://pyimagesearch.com/2018/07/16/opencv-saliency-detection/

class Saliency(Metric):
    """
    Metric: Saliency
    """
    def __init__(self, id, filename, img_string):
        """
        Initiate the metric calculation
        
        Args:
            id: int. The id of every submission
            filename: str. The filename of the assessed visualisation
            img_string: str. The image string of that visualisation

        """
        self.saliency_map = None
        super().__init__(id, filename, img_string)

    def execute_metric(self):
        """
        Execute the metric.

        Returns:
            saliency_ratio: float.  Average Saliency across pixels
        """
        print('start calculating saliency for ' + self.filename)
        self.image = cv.imread(self.filename)
        
        self.lum = cv.imread(self.filename,cv.IMREAD_GRAYSCALE)
 
		
        saliency = cv.saliency.StaticSaliencyFineGrained_create()
	
		
        (success, self.saliency_map) = saliency.computeSaliency(self.image)

		
        self.saliency_map = (self.saliency_map * 255).astype(np.uint8)


		
        saliency_pixel = np.count_nonzero(self.saliency_map >= 64)
		
        saliencyMap_shape = self.saliency_map.shape
		
        all_saliency_pixel = saliencyMap_shape[0] * saliencyMap_shape[1]
		
        saliency_ratio = saliency_pixel/all_saliency_pixel


        self.saliency_map = im.fromarray(self.saliency_map)

		
        
        print('stop calculating saliency')
        self.draw_saliency_map()
        return saliency_ratio
    
    def draw_saliency_map(self):
        """
        Save the saliency map
        """
        dir_save = './submissions/submission_' + str(self.id) + '/RESULTS/saliency.png'
        self.saliency_map.save(dir_save)

        