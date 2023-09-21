from model import Segmentation
#https://opencv.org/
import cv2
from metric_utils.text_extraction import extract_text_position
from metric_utils.process_utils import (
    check_intersect, 
)



class processComponent():
    # Private constants
    _CANNY_EDGE_DETECTION_MATLAB_LOW_THRESHOLD: float = 0.1
    _CANNY_EDGE_DETECTION_MATLAB_HIGH_THRESHOLD: float = 0.2
    _CANNY_EDGE_DETECTION_PYTHON_MIN_THRESHOLD: int = 0
    _CANNY_EDGE_DETECTION_PYTHON_MAX_THRESHOLD: int = 255
    _GAUSSIAN_KERNEL_SIZE =  (0, 0)
    _GAUSSIAN_KERNEL_STANDARD_DEVIATION: int = 2
    
    def __init__(self, id):
        self.img = None
        self.dir2save = ''
        self.image_string = ''
        self.id = id
        
        
    def load_img(self, filename):
        self.img = cv2.imread(filename)
        self.dir2save = './submissions/submission_' + str(self.id) + '/RESULTS'
        
        
    
    def calculate_relation(self, a, b):
        minX = a[0]
        maxX = a[0] + a[1]
        minY = a[2]
        maxY = a[2] + a[3]
        area = a[1] * a[3]
        
        minX_2 = b[0]
        maxX_2 = b[0] + b[1]
        minY_2 = b[2]
        maxY_2 = b[2] + b[3]
        area_2 = b[1] * b[3]
        # compute the width and height of the intersection are
        inter_width = max(0, (min(maxX, maxX_2) - max(minX, minX_2) ))
        inter_height = max(0,(min(maxY, maxY_2) - max(minY, minY_2) ))
        inter_area = inter_width * inter_height
        if inter_area > 0:
            if inter_area / area == 1:
                return 0
            if inter_area / area_2 ==1:
                return 1
            
            return 2
            
        return 3
    
    def generate_countours_array(self,filename):
        """
        the code below is written based on the aim project:https://github.com/aalto-ui/aim
        aim licence: MIT License


        Copyright (c) 2018-present, User Interfaces group, Aalto University, Finland

        Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
        to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
        and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
        DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        """ 
        

        # Create PIL image
        img = cv2.imread(filename)

        # Convert image from ??? (should be RGBA) to L (grayscale) color space
        img_l = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Gaussian filter parameters
        ksize = self._GAUSSIAN_KERNEL_SIZE
        sigma = self._GAUSSIAN_KERNEL_STANDARD_DEVIATION

        # Smooth image
        img_blurred_nparray= cv2.GaussianBlur(
            src=img_l, ksize=ksize, sigmaX=sigma, sigmaY=sigma
        )
        # Canny edge detection parameters
        low_threshold = (
            self._CANNY_EDGE_DETECTION_PYTHON_MAX_THRESHOLD
            * self._CANNY_EDGE_DETECTION_MATLAB_LOW_THRESHOLD
        )  # 50 or 28.05 [0, 255] for mobile and desktop GUIs, respectively
        high_threshold = (

            self._CANNY_EDGE_DETECTION_PYTHON_MAX_THRESHOLD
            * self._CANNY_EDGE_DETECTION_MATLAB_HIGH_THRESHOLD

        ) 

        # Detect edges
        img_contours_nparray = cv2.Canny(
            image=img_blurred_nparray,
            threshold1=low_threshold,
            threshold2=high_threshold,
        )
        return img_contours_nparray

    
    def combine_segmentation(self,filename, input_components):
        countours_array = self.generate_countours_array(filename=filename)
        sliced_img_list = []
        
        cnts = cv2.findContours(countours_array, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])
        
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            sliced = True
            if sliced == True:
                if(w > 30 and h > 100) or (h > 30 and w > 100):
                    sliced_img_list.append([x,w,y,h])
                        
        input_list = input_components + sliced_img_list
        sliced_img_list_after = check_intersect(input_list)

        return sliced_img_list_after
        

    def remove_child(self,components):
        #remove the child components, only take the components that is parent
        processed_segments = []
        segments = components['segments']
        for segment in segments:
            is_child = False
            for segment_b in segments:
                segment_position = segment['position']
                segment_position_detial = [segment_position['column_min'], (segment_position['column_max'] - segment_position['column_min']), segment_position['row_min'], (segment_position['row_max'] - segment_position['row_min'])]
                if segment != segment_b:
                    segment_b_position = segment_b['position']
                    segment_b_position_detial = [segment_b_position['column_min'], (segment_b_position['column_max'] - segment_b_position['column_min']), segment_b_position['row_min'], (segment_b_position['row_max'] - segment_b_position['row_min'])]
                    relation = self.calculate_relation(segment_position_detial, segment_b_position_detial)
                    if relation == 0 :
                        is_child = True
                        
            if not is_child:
                processed_segments.append(segment_position_detial)
                
        # the return value is the components which are not children
        return processed_segments
    
    
    def save_remove_child_img(self, processed_segments):
        img_copy = self.img.copy()
        ROI_number = 0
        for segment in processed_segments:
            print('segment', segment)
            ROI = img_copy[segment[2]:segment[2]+segment[3], segment[0]:segment[0]+segment[1]]
            # cv2.imwrite((self.dir2save + '/ROI_{}.png').format(ROI_number), ROI)
            cv2.rectangle(self.img, (segment[0],segment[2]), (segment[0] + segment[1], segment[2] + segment[3]), (36, 255,12), 2)
            ROI_number += 1
            
        cv2.imwrite((self.dir2save + '/index_bbox.png'), self.img)
        
    def save_countours_sliced_img(self, filename):
        self.load_img(filename)
        img_copy = self.img.copy()
        ROI_number = 0  
        # the input_components is an empty sets to indicate that the only used algorithm is segmenting the images only based on countours
        processed_segments_after = self.combine_segmentation(filename=filename, input_components=[])
        for segment in processed_segments_after:
            ROI = img_copy[segment[2]:segment[2]+segment[3], segment[0]:segment[0]+segment[1]]
            # you can comment the line below if you do not want the segmented blocks images
            # cv2.imwrite((self.dir2save + '/ROI_{}.png').format(ROI_number), ROI)
            cv2.rectangle(self.img, (segment[0],segment[2]), (segment[0] + segment[1], segment[2] + segment[3]), (255, 0, 0), 2)
            ROI_number += 1
            
        cv2.imwrite((self.dir2save + '/output_non_text.png'), self.img)

        
    
            
    def get_components(self, image_string):
        # get the components from uied
        segmentation = Segmentation()
        return segmentation.execute(image_string)
    
    
    def execute_combined_segmentation(self, filename, img_string):
        print('start of the execution')
        self.load_img(filename)
        components = self.get_components(img_string)
        processed_segments = self.remove_child(components=components)    
        text_blocks = extract_text_position(filename=filename, bias = 5) 
        processed_segments_after = processed_segments + text_blocks
        processed_segments_after = check_intersect(sliced_img_list = processed_segments_after)
        processed_segments_final = self.combine_segmentation( filename=filename, input_components=processed_segments_after)
        if len(processed_segments_final) != 1:
            processed_segments_after = processed_segments_final
        # you can comment the line below if you do not want save the images
        # self.save_remove_child_img(processed_segments_after)
        print('end of the execution')
        return processed_segments_after


           



        

    

        