#https://docs.python.org/3/library/argparse.html
from arg_utils import get_args
from result_analysis import ResultAnalysis
from generate_pdf import PDFWriter
from metrics_calculation import metric_calculation
import sys

def main(args):
    try:
        execute_metric = args.metric
        execute_items_numbers = metric_calculation(execute_metric)
        result_analysis = ResultAnalysis(execute_items_numbers)
        result_analysis.execute_result_analysis()
        
        for i in range(1, execute_items_numbers + 1):
            PDF_writer = PDFWriter('submissions', i)
            PDF_writer.generate_pdf()
    except KeyboardInterrupt:
        print("Interrupted by user, stopping app")
        
        sys.exit(0)
        
if __name__=='__main__':
    args = get_args()
    main(args)