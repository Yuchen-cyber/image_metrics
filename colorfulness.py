from metric import Metric
# Third-party modules
# https://numpy.org/
import numpy as np
# https://pillow.readthedocs.io/en/stable/
from PIL import Image
from io import BytesIO
import base64


class Colorfulness(Metric):
    """
    Metric: Colorfulness.
    """
    
    def __init__(self, id, filename, img_string):
        """
        Initiate the metric calculation
        
        Args:
            id: int. The id of every submission
            filename: str. The filename of the assessed visualisation
            img_string: str. The image string of that visualisation

        """
        self._CF_COEF= 0.3 # a magic coefficient for computing colorfulness
        super().__init__(id, filename, img_string)
    
    
    def execute_metric(self) :
        #    the code below is written based on the aim project:https://github.com/aalto-ui/aim
        #     aim licence: MIT License


        #     Copyright (c) 2018-present, User Interfaces group, Aalto University, Finland

        #     Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
        #     to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
        #     and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

        #     The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

        #     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        #     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
        #     DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
        #     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        """
        Execute the metric.

        Returns:
            colorfulness: float. Colourfulness Value

        """

        print('start calculating wave for ' + self.filename)
         # Create PIL image
        img= Image.open(BytesIO(base64.b64decode(self.img_string)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb = img.convert("RGB")

        # Get NumPy array
        img_rgb_nparray = np.array(img_rgb).astype(float)

        # Get RGB
        red = img_rgb_nparray[:, :, 0]
        green = img_rgb_nparray[:, :, 1]
        blue = img_rgb_nparray[:, :, 2]

        # Compute Red-Green and Yellow-Blue
        rg = red - green
        yb = 0.5 * (red + green) - blue

        # Compute metrics based on Hassler and Süsstrunk's paper
        rgyb_avg = float(np.sqrt(np.mean(rg) ** 2 + np.mean(yb) ** 2))
        rgyb_std = float(np.sqrt(np.std(rg) ** 2 + np.std(yb) ** 2))
        colorfulness = float(rgyb_std + self._CF_COEF * rgyb_avg)
        print('stop calculating colourfulness for ' + self.filename)

        return colorfulness
    
