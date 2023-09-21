import argparse

__all__ = ['get_args']

def get_args():
    parser = argparse.ArgumentParser(description = 'Automated_Grader')
    parser.add_argument('--metric', default='all', type=str, help='Command for determining which metric file to execute(default is all metrics)')
    parser.add_argument('--marked', default='true', type=str, help='Command for determining which report to generate(default is true)')
    args = parser.parse_args()
    return args