from metric_algorithm.colorfulness import Colorfulness
#https://opencv.org/
import cv2
import base64
def execute_test_colourfulness():
    #create the specific string
    original_img_string = ''
    with open('./test/test_image.png', "rb") as img_file:
        original_img_string = base64.b64encode(img_file.read())
    colorfulness = Colorfulness(1,'./test/test_image.png', original_img_string )
    original_img = cv2.imread('./test/test_image.png')
    gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('./test/test_image_gray.png', gray_img)
    original_colourfulness = colorfulness.execute_metric()
    #create the specific string
    gray_img_string = ''
    with open('./test/test_image_gray.png', "rb") as img_file:
        gray_img_string = base64.b64encode(img_file.read())
    colorfulness_gray = Colorfulness(2,'./test/test_image_gray.png', gray_img_string )
    gray_colourfulness = colorfulness_gray.execute_metric()
    status = original_colourfulness > gray_colourfulness
    print(gray_colourfulness)
    print(original_colourfulness)
    if status:
        return 'test passed'
    else:
        return 'test not passed'
    
        