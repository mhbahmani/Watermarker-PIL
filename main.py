#!/usr/bin/python

from PIL import Image
import sys, getopt
import re

args = sys.argv[1:]
image_file_path = logo_file_path = None

# Set default logo place, which is bottom left
bottom = True
left = True

# percent of original size
height_scale_percent = 6

# percent of distance from sides
distance_from_sides_of_picture_percent = 5
distance_from_up_bottom_of_picture_percent = 5

# Pars arguments
try:
    opts, args = getopt.getopt(args,"hi:l:p:r:u:",["image=", "logo=", "percents="])
except getopt.GetoptError:
    print('Use `python main.py -h` to see how this code has to used.')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print('$ python main.py')
        print('Options:')
        print('-i <image path>')
        print('-l <watermark path>')
        print('-p <watermark scale percents>')
        print('-r <distance from left or right >')
        print('-u <distance from up or bottom>')
        print('')
        print('If you don\'t gave image path and watermark, script consume them by default as image.jpg and logo.png')
        print('With -p option, declare logo should be how many percents of the main image')
        print('By defalt, this value is 6%')
        print('You can set logo distance from picture sides using -r')
        print('You can set logo distance from up or bottom using -u')
        print('Default value for these are 5%')
        print('Use top, bottom, left and right key words to declare watermark place')
        print('Watermark palce is by default bottom and left')
        sys.exit()
    elif opt in ("-i", "--image"):
        image_file_path = arg
    elif opt in ("-l", "--logo"):
        logo_file_path = arg
    elif opt in ("-p", "--percents"):
        height_scale_percent = int(arg)
    elif opt in ("-r"):
        distance_from_sides_of_picture_percent = int(arg)
    elif opt in ("-u"):
        distance_from_up_bottom_of_picture_percent = int(arg)


for arg in args:
    if arg == 'right':
        left = False
        continue
    elif arg == 'top':
        bottom = False
        continue

    arg = re.split("=", arg)
    if len(arg) == 2:
        argument, value = arg
        if argument == 'image':
            image_file_path = value
        elif argument == 'logo':
            logo_file_path = value
        elif argument == 'percents':
            height_scale_percent = value

if image_file_path is None or image_file_path is '':
    print('You didn\'t give image file path. I consume it as image.jpg')
    image_file_path = "image.jpg"

if logo_file_path is None or logo_file_path is '':
    print('You didn\'t give logo file path. I consume it as logo.png')
    logo_file_path = "logo.png"




im = Image.open('image.png')
logo = Image.open('logo.png')

box = (500, 500, 800, 800)
region = im.crop(box)

im.paste(region, box)

im.show()


