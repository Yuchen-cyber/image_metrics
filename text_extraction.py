# https://opencv.org/
import cv2
# https://github.com/PaddlePaddle/PaddleOCR
from paddleocr import PaddleOCR
from process_utils import (
    check_intersect
)
# https://numpy.org/
import numpy as np

def text_recognition(filename):
    # only extract text without text positions
    img = cv2.imread(filename)
    texts = []
    paddle_model = PaddleOCR(
            use_angle_cls=True, lang="en", show_log=True
        )
    paddle_result = paddle_model.ocr(img, cls=True)[0]
    for line in paddle_result:
        
        texts.append(line[1][0]) 

    
    return texts

def extract_text_position(filename, bias):
    # only extract text positions without text contents
    img = cv2.imread(filename)
    text_blocks = []
    paddle_model = PaddleOCR(
            use_angle_cls=True, lang="en", show_log=True
        )
    paddle_result = paddle_model.ocr(img, cls=True)[0]
    for line in paddle_result:
        shape = {
            'top_left':line[0][0],
            'top_right':line[0][1],
            'bottom_right':line[0][2],
            'bottom_left':line[0][3]
        }
        
        text_blocks.append([int(shape['top_left'][0]), int(shape['top_right'][0]) - int(shape['top_left'][0]), int(shape['top_left'][1]), int(shape['bottom_left'][1]- shape['top_left'][1])])
    
        
    text_blocks = check_intersect(sliced_img_list = text_blocks,bias = bias, isText = True)
    text_blocks = check_intersect(sliced_img_list = text_blocks,bias = 0, isText = True)
    
    return text_blocks

def save_text_segmentation_img(filename):
    text_blocks = extract_text_position(filename=filename, bias = 10) 
    img = cv2.imread(filename) 
    dir2save = filename[:-10]
    for sliced_img in text_blocks:
        if sliced_img[3] > 10:
            cv2.rectangle(img, (sliced_img[0],sliced_img[2]), (sliced_img[0] + sliced_img[1], sliced_img[2] + sliced_img[3]), (36, 255,12), 2)
        
    cv2.imwrite((dir2save + '/RESULTS/text_blocks.png'), img)
    
    

def save_text_left_img(filename):
    img = cv2.imread(filename)
    dir2save = filename[:-10]
    text_blocks = extract_text_position(filename=filename, bias = 5)  
    black = (0,0,0)
    white = (255,255,255)
    height = len(img[0])
    width = len(img)
    text = [[white] * height] * width
    text = np.array(text)
    # change the text areas to blacks
    for text_block in text_blocks:
        text[text_block[2]:text_block[2]+text_block[3], text_block[0]:text_block[0]+text_block[1]] = black
    cv2.imwrite((dir2save + '/RESULTS/text_blocks_black.png'), text)