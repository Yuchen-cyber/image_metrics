import os
import sys
from test_segmentation import execute_test_image_segmentation
from test_text_detection import execute_test_text_detection
from test_text_similarity import execute_test_text_similarity
from test_text_recognition import execute_test_text_recognition
from test_WAVE import execute_test_WAVE
from test_colourfulness import execute_test_colourfulness
from test_white_space import test_white_space
from test_nttr import test_nttr
from test_text_coverage import test_text_coverage


dir2save = "test"
command = "mkdir " + dir2save
os.system(command)
command = "./" + dir2save + "/test_result.txt"
os.system(command)
file_write = open(command,"w")
file_write.write("These are the results:\n")

def main():
    try:
        print("start metric testing...")
        test_segmentation_result = execute_test_image_segmentation()
        test_text_detection_result = execute_test_text_detection()
        test_text_similarity_result = execute_test_text_similarity()
        test_text_recognition_result = execute_test_text_recognition()
        test_wave_result = execute_test_WAVE()
        test_colourfulness_result = execute_test_colourfulness()
        test_white_space_result = test_white_space()
        test_nttr_result = test_nttr()
        test_text_coverage_value = test_text_coverage()
        
        file_write = open("./" + dir2save + "/test_result.txt","w")
        file_write.write('segmentation testing result:\n' + test_segmentation_result)
        file_write.write('\ntext detection testing result:\n' + test_text_detection_result)
        file_write.write('\ntext similarity testing result:\n' + test_text_similarity_result)
        file_write.write('\ntext recognition testing result:\n' + test_text_recognition_result)
        file_write.write('\nWAVE testing result:\n' + test_wave_result)
        file_write.write('\ncolourfulness testing result:\n' + test_colourfulness_result)
        file_write.write('\nwhite space proportiontesting results:\n' + test_white_space_result)
        file_write.write('\nnttr testing results:\n' + test_nttr_result)
        file_write.write('\ntext coverage testing results:\n' + test_text_coverage_value)
        file_write.close()

    except KeyboardInterrupt:
        print("Interrupted by user, stopping app")
        
        sys.exit(0)

main()
        