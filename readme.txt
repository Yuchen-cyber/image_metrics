**This project is made possible through a grant from Newcastle University's Research, Police, Intelligence, and Ethics Team, with permissions granted for its use from April 1, 2021, to May 1, 2023. Consequently, we are unable to publicly display the images associated with this project due to confidentiality agreements. However, you can gain insight into the project's functionality and purpose by reviewing the provided code.**


B.1 Installation
Installing Python: You can install Python here: https://www.python.org/downloads/. The programming Language should be Python 3.7 or higher.
Before installing the third-party packages, it is better to have a virtual environment in-
stalled.
B.1.1 Conda Environment
To not affect your current environment, you can set up a virtual environment to install the
necessary packages because some packages will change other packages versions, for example,
PaddleOCR will change the OpenCV version to 4.6 because PaddleOCR is only compatible with
OpenCV 4.6. So Virtual Environment is not mandatory, but it is highly recommended.
B.1.1.1 Installing Conda
The recommended virtual is Conda, Follow these steps to install Conda through Anaconda or
Miniconda:
1. Choose your preferred distribution:
For Anaconda, visit the official download page:
https://www.anaconda.com/products/distribution
For Miniconda, visit the official download page:
https://docs.conda.io/en/latest/miniconda.html
2. Select the installer for your operating system (Windows, macOS, or Linux) and download
it.
3. Run the installer and follow the on-screen instructions:
Windows: Double-click the downloaded .exe file and follow the installation wizard.
macOS: Double-click the downloaded .pkg file and follow the installation wizard.
Linux: Open a terminal, navigate to the directory where the downloaded .sh file is
located, and run the following command:
bash Miniconda3-latest-Linux-x86_64.sh
Replace Miniconda3-latest-Linux-x86 64.sh with the actual filename of the down-
loaded installer.
B.1.2 Activating Conda Environment
After installing the virtual environments, you need to activate it to install the necessary third-party packages. Follow these steps to activate a Conda environment:
1. Open a terminal (Command Prompt or PowerShell for Windows users).
2. To set up a new environment, type in the terminal, replacing my env with the name of
your environment, the recommended name for my env is auto grader:
conda create --name my_env
3. To activate the environment, use the following command:
conda activate my_env



B.1.3 Installing Third-Party Packages
To facilitate users, we put all needed third-party packages versions into a file called require-
ments.txt. Because the virtual environment is Conda, so environment.yaml is also created to
be compatible with the Conda environment. This file could simplify the process of installing the
Third-party packages by typing one line for all packages instead of one line only for one package.
Use this command line to install all third-party packages:
conda env create -f environment.yaml

If you can not install some of the third-party packages, try to install them manually using 'pip install'
The name for the new environment is metric-env, so you need to activate the environment you have created just now, using this line:
conda activate metric-env

When all these are done, please read B.2 to see how to run this program.

B.2 Getting Started
To run the assessment code, please type in the terminal:
python3 main.py
To run the testing code, please type in the terminal:
python3 test.py
, but please note to run the testing code, you need to first run the assessment code to generate
the testing data.
