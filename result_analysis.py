from linear_regression import draw_linear_graph
from extract_dominant_color import execute_dominant_colour
from pearson_correlation import get_pearson_value
from draw_result import ( draw_all, 
                         draw_single)
class ResultAnalysis:
    
    def __init__ (self,execute_number=18):
        self.execute_number = execute_number
        
    def execute_result_analysis(self):
        draw_linear_graph()
        get_pearson_value()
        execute_dominant_colour(self.execute_number)
        draw_all(self.execute_number)
        draw_single(self.execute_number)
        