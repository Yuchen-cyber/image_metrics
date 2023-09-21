from metric import Metric
# Third-party modules
# https://numpy.org/
import numpy as np
#https://opencv.org/
import cv2
# https://matplotlib.org/
import matplotlib.pyplot as plt


class WAVE(Metric):
    """
    Metric: Average WAVE score (Weighted Affective Valence Estimates).
    """

    def __init__(self, id, filename, img_string):
        #    the code below is written modified based on the aim project:https://github.com/aalto-ui/aim
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
        Initiate the metric calculation
        
        Args:
            id: int. The id of every submission
            filename: str. The filename of the assessed visualisation
            img_string: str. The image string of that visualisation

        """
        self._WAVE_COLORS = {
            (235, 45, 92): {
                "Level": "Saturated",
                "Hue": "Red",
                "Abbreviation": "SR",
                "Score": 0.5488069414316703,
            },
            (242, 149, 185): {
                "Level": "Light",
                "Hue": "Red",
                "Abbreviation": "LR",
                "Score": 0.4577006507592191,
            },
            (204, 119, 141): {
                "Level": "Muted",
                "Hue": "Red",
                "Abbreviation": "MR",
                "Score": 0.4859002169197397,
            },
            (162, 32, 66): {
                "Level": "Dark",
                "Hue": "Red",
                "Abbreviation": "DR",
                "Score": 0.8481561822125814,
            },
            (243, 145, 51): {
                "Level": "Saturated",
                "Hue": "Orange",
                "Abbreviation": "SO",
                "Score": 0.7114967462039046,
            },
            (251, 200, 166): {
                "Level": "Light",
                "Hue": "Orange",
                "Abbreviation": "LO",
                "Score": 0.3741865509761389,
            },
            (208, 154, 119): {
                "Level": "Muted",
                "Hue": "Orange",
                "Abbreviation": "MO",
                "Score": 0.39154013015184386,
            },
            (159, 90, 48): {
                "Level": "Dark",
                "Hue": "Orange",
                "Abbreviation": "DO",
                "Score": 0.18329718004338397,
            },
            (253, 228, 51): {
                "Level": "Saturated",
                "Hue": "Yellow",
                "Abbreviation": "SY",
                "Score": 0.7201735357917572,
            },
            (252, 232, 158): {
                "Level": "Light",
                "Hue": "Yellow",
                "Abbreviation": "LY",
                "Score": 0.5140997830802604,
            },
            (218, 198, 118): {
                "Level": "Muted",
                "Hue": "Yellow",
                "Abbreviation": "MY",
                "Score": 0.49132321041214755,
            },
            (162, 149, 59): {
                "Level": "Dark",
                "Hue": "Yellow",
                "Abbreviation": "DY",
                "Score": 0.0,
            },
            (179, 208, 68): {
                "Level": "Saturated",
                "Hue": "cHartreuse",
                "Abbreviation": "SH",
                "Score": 0.4652928416485901,
            },
            (224, 231, 153): {
                "Level": "Light",
                "Hue": "cHartreuse",
                "Abbreviation": "LH",
                "Score": 0.2928416485900217,
            },
            (177, 200, 101): {
                "Level": "Muted",
                "Hue": "cHartreuse",
                "Abbreviation": "MH",
                "Score": 0.33731019522776573,
            },
            (126, 152, 68): {
                "Level": "Dark",
                "Hue": "cHartreuse",
                "Abbreviation": "DH",
                "Score": 0.3579175704989154,
            },
            (101, 190, 131): {
                "Level": "Saturated",
                "Hue": "Green",
                "Abbreviation": "SG",
                "Score": 0.648590021691974,
            },
            (193, 224, 196): {
                "Level": "Light",
                "Hue": "Green",
                "Abbreviation": "LG",
                "Score": 0.46095444685466386,
            },
            (129, 199, 144): {
                "Level": "Muted",
                "Hue": "Green",
                "Abbreviation": "MG",
                "Score": 0.5726681127982647,
            },
            (37, 152, 114): {
                "Level": "Dark",
                "Hue": "Green",
                "Abbreviation": "DG",
                "Score": 0.7125813449023862,
            },
            (86, 197, 208): {
                "Level": "Saturated",
                "Hue": "Cyan",
                "Abbreviation": "SC",
                "Score": 0.8297180043383949,
            },
            (164, 219, 228): {
                "Level": "Light",
                "Hue": "Cyan",
                "Abbreviation": "LC",
                "Score": 0.7028199566160521,
            },
            (133, 204, 208): {
                "Level": "Muted",
                "Hue": "Cyan",
                "Abbreviation": "MC",
                "Score": 0.5932754880694144,
            },
            (24, 155, 154): {
                "Level": "Dark",
                "Hue": "Cyan",
                "Abbreviation": "DC",
                "Score": 0.6377440347071583,
            },
            (96, 163, 215): {
                "Level": "Saturated",
                "Hue": "Blue",
                "Abbreviation": "SB",
                "Score": 1.0,
            },
            (170, 194, 228): {
                "Level": "Light",
                "Hue": "Blue",
                "Abbreviation": "LB",
                "Score": 0.7537960954446855,
            },
            (124, 159, 201): {
                "Level": "Muted",
                "Hue": "Blue",
                "Abbreviation": "MB",
                "Score": 0.8318872017353579,
            },
            (59, 125, 181): {
                "Level": "Dark",
                "Hue": "Blue",
                "Abbreviation": "DB",
                "Score": 0.7396963123644252,
            },
            (156, 78, 155): {
                "Level": "Saturated",
                "Hue": "Purple",
                "Abbreviation": "SP",
                "Score": 0.6843817787418656,
            },
            (184, 158, 199): {
                "Level": "Light",
                "Hue": "Purple",
                "Abbreviation": "LP",
                "Score": 0.63882863340564,
            },
            (162, 115, 167): {
                "Level": "Muted",
                "Hue": "Purple",
                "Abbreviation": "MP",
                "Score": 0.7451193058568331,
            },
            (115, 56, 145): {
                "Level": "Dark",
                "Hue": "Purple",
                "Abbreviation": "DP",
                "Score": 0.8080260303687636,
            },
        }
        self._MATCH_COLORS = list(self._WAVE_COLORS.keys())
        self._NUM_MATCH_COLORS = len(self._MATCH_COLORS)
        super().__init__(id, filename, img_string)
        
    def execute_metric(self):
        #    the code below is written modified based on the aim project:https://github.com/aalto-ui/aim
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
            wave_mean: float. Average WAVE score across pixels
        """
        print('start calculating WAVE for ' + self.filename)
        # Get NumPy array
        img_rgb_nparray  = cv2.imread(self.filename)

        ax1, ax2, _ = img_rgb_nparray.shape

        # Repeated values for every possible match color (self._MATCH_COLORS)
        repeated_img_nparray = np.tile(
            img_rgb_nparray, self._NUM_MATCH_COLORS
        ).reshape(ax1, ax2, self._NUM_MATCH_COLORS, 3)
        # Find colors most closely matching self._MATCH_COLORS across pixels.
        l2_norms = (
            (repeated_img_nparray - np.array(self._MATCH_COLORS)) ** 2
        ).sum(axis=3)
        match_indices = l2_norms.argmin(axis=2).flatten()

        # Mean over matched colors (size of the image) weight values. Some
        # colors are closer to self._MATCH_COLORS than the others, but when we
        # compute the average, there is no difference.
        wave_values= [
            self._WAVE_COLORS[self._MATCH_COLORS[i]]["Score"]
            for i in match_indices
        ]
        wave_mean= float(np.mean(wave_values))
        print('stop calculating colourfulness')
        return wave_mean
    
    def draw_wave_preference(self):
        """
        draw and save the wave preference graph
        """
        color_number = ['R', 'O', 'Y', 'H', 'G', 'C', 'B', 'P']
        saturated_list = []
        light_list = []
        muted_list = []
        dark_list = []

        
        for colour_number in self._WAVE_COLORS:
            colour = self._WAVE_COLORS[colour_number]
            level = colour['Level']
            colour_value = (colour_number, colour["Score"])
            if level == 'Saturated':
                saturated_list.append(colour_value)
            if level == 'Light':
                light_list.append(colour_value)
            if level == 'Muted':
                muted_list.append(colour_value)
            if level == 'Dark':
                dark_list.append(colour_value)

        for i in range(len(saturated_list)):
            pair = saturated_list[i]
            y = pair[1]
            c = pair[0]
            plt.scatter(color_number[i], y, color='#%02x%02x%02x'%c, marker='p', zorder=2)
        for i in range(len(light_list)):
            pair = light_list[i]
            y = pair[1]
            c = pair[0]
            plt.scatter(color_number[i], y, color='#%02x%02x%02x'%c, marker='>', zorder=2)
        for i in range(len(muted_list)):
            pair = muted_list[i]
            y = pair[1]
            c = pair[0]
            plt.scatter(color_number[i], y, color='#%02x%02x%02x'%c, marker='D',  zorder=2)
        for i in range(len(dark_list)):
            pair = dark_list[i]
            y = pair[1]
            c = pair[0]
            plt.scatter(color_number[i], y, color='#%02x%02x%02x'%c, marker='s', zorder=2)
        plt.plot(color_number, list(list(zip(*saturated_list))[1]), color = 'black', marker='p', label="saturated",zorder=1)
        plt.plot(color_number, list(list(zip(*light_list))[1]), color = 'black', marker='>', label='light', zorder=1)
        plt.plot(color_number, list(list(zip(*muted_list))[1]), color = 'black', marker='D',label='muted',zorder=1)
        plt.plot(color_number, list(list(zip(*dark_list))[1]), color = 'black', marker='s', label='dark',zorder=1)
        plt.legend(loc="lower right")
        plt.xlabel('HUE')
        plt.ylabel('WAVE Value')
        dir_save = './submissions/' 
        saved_file_name = 'wave_preference'
        command = dir_save + '/' + saved_file_name
        plt.savefig(command)
    
    