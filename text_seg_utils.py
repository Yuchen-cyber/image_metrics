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
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Text segmentation utility functions.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Third-party modules
import cv2
import numpy as np

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2021-08-05"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Text segmentation utility functions
# ----------------------------------------------------------------------------


class Text:
    def __init__(self, id, content, location):
        self.id = id
        self.content = content
        self.location = location

        self.width = self.location["right"] - self.location["left"]
        self.height = self.location["bottom"] - self.location["top"]
        self.area = self.width * self.height
        self.word_width = self.width / len(self.content)

    def visualize_element(self, img, color, line, show=False):
        loc = self.location
        cv2.rectangle(
            img,
            (loc["left"], loc["top"]),
            (loc["right"], loc["bottom"]),
            color,
            line,
        )
        if show:
            cv2.imshow("text", img)
            cv2.waitKey()
            cv2.destroyWindow("text")


def visualize_texts(
    org_img, texts, color=(0, 0, 255), line=2, show=False, write_path=None
):
    img = org_img.copy()
    for text in texts:
        text.visualize_element(img, color=color, line=line)

    if show:
        cv2.imshow("Texts", img)
        cv2.waitKey(0)
        cv2.destroyWindow("Texts")

    if write_path is not None:
        cv2.imwrite(write_path, img)


def text2json(texts, img_shape):
    output = {"img_shape": img_shape, "texts": []}
    for text in texts:
        c = {"id": text.id, "content": text.content}
        loc = text.location
        c["column_min"], c["row_min"], c["column_max"], c["row_max"] = (
            loc["left"],
            loc["top"],
            loc["right"],
            loc["bottom"],
        )
        c["width"] = text.width
        c["height"] = text.height
        output["texts"].append(c)
    return output


def text_cvt_orc_format_paddle(paddle_result):
    texts = []
    for i, line in enumerate(paddle_result[0]):
        points = np.array(line[0])
        location = {
            "left": int(min(points[:, 0])),
            "top": int(min(points[:, 1])),
            "right": int(max(points[:, 0])),
            "bottom": int(max(points[:, 1])),
        }
        content = line[1][0]
        texts.append(Text(i, content, location))
    return texts
