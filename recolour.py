#!/usr/local/bin/python3

# -*- coding: utf-8 -*-
# @Author: tintinux
# @Date:   2017-11-09 10:46:34
# @Last Modified time: 2017-11-09 11:26:02

import argparse
import cv2
import numpy as np


parse = argparse.ArgumentParser()
parse.add_argument("-i", "--image", required=True,
                   help="Path to the image to be scanned")
parse.add_argument("-p", "--primary", required=True,
                   help="The new background colour as hex without '#'")
parse.add_argument("-s", "--secondary", required=True,
                   help="The new foreground colour as hex without '#'")
args = vars(parse.parse_args())


def hex_to_bgr(value):
    lv = len(value)
    rgb = [int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)]
    return rgb[::-1]  # reverse the rgb value


def filename_no_ext(file_name):
    return file_name.split('.')[0]


def binary_image(img):
    #cv2.rectangle(img, (0, 1000), (1300, 440), (0, 0, 0), -1)
    _, new_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return new_img


def recolor_image(img, primary_colour, secondary_colour):
    colour_img_shape = (img.shape[0], img.shape[1], 3)
    new_img = np.zeros(colour_img_shape)
    new_img[img == 255] = primary_colour
    new_img[img == 0] = secondary_colour
    return new_img


def main():
    file_name = filename_no_ext(args["image"])
    input_img = cv2.imread(args["image"], 0)
    primary_colour = hex_to_bgr(args["primary"])
    secondary_colour = hex_to_bgr(args["secondary"])
    bin_img = binary_image(input_img)

    output_img = recolor_image(bin_img, primary_colour, secondary_colour)

    cv2.imwrite(file_name + "_transformed.jpg", output_img)


if __name__ == '__main__':
    main()
