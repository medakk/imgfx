#!/usr/bin/python3
# Takes an image and creates a triangle effect

from scipy import misc,ndimage
import numpy as np
import matplotlib.pyplot as plt
import logging
import argparse
from sys import stderr,exit

#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_negative(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

parser = argparse.ArgumentParser()
parser.add_argument("src",
                    help="Path to source image file")
parser.add_argument("-b", "--block-size", type=check_negative,
                    help="Size of a block in pixels")
parser.add_argument("-o", "--output", type=str,
                    help="Path to output image file")
parser.add_argument("--no-preview", action="store_true",
                    help="Disables preview. This option is ignored if -o is not used")
args = parser.parse_args()

# open the image file specified by the path
img = None
try:
    img = misc.imread(args.src)
except Exception as e:
    print("Unable to open file: {}".format(args.src), file=stderr)
    exit(1)

height,width,colors = img.shape
logging.info("%sx%s, %s Colors", width,height,colors)

block_size = width//10 # a default value
# figure out block size
if args.block_size:
    block_size = args.block_size

for j in range(0, height, block_size):
    for i in range(0, width, block_size):
        # |\
        # | \
        # |  \
        # |___\
        rgb_sum = [0,0,0]
        px_count = 0
        for x in range(block_size):
            if j+x>=height:
                break
            if i+x>width:
                px_count += width-i
            else:
                px_count += x
            sub_sum = [np.sum(img[j+x,i:i+x,k]) for k in range(3)]
            rgb_sum = [rgb_sum[k]+sub_sum[k] for k in range(3)]

        rgb = [c/px_count for c in rgb_sum]

        for x in range(block_size):
            for k in range(3):
                if j+x>=height:
                    break
                img[j+x,i:i+x,k] = rgb[k]

        # \---|
        #  \  |
        #   \ |
        #    \|
        rgb_sum = [0,0,0]
        px_count = 0
        for x in range(block_size):
            if j+x>=height:
                break
            if i+block_size>width:
                px_count += max(width-x-i,0)
            else:
                px_count += block_size-x
            sub_sum = [np.sum(img[j+x,i+x:i+block_size,k]) for k in range(3)]
            rgb_sum = [rgb_sum[k]+sub_sum[k] for k in range(3)]

        rgb = [c/px_count for c in rgb_sum]

        for x in range(block_size):
            for k in range(3):
                if j+x>=height:
                    break
                img[j+x,i+x:i+block_size,k] = rgb[k]

if args.output:
    misc.imsave(args.output, img)
    if not args.no_preview:
        plt.imshow(img)
        plt.show()
else:
    plt.imshow(img)
    plt.show()
