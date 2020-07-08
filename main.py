#!/usr/bin/python

from PIL import Image
import os
import sys
import getopt, getpass
import re

args = sys.argv[1:]

default_outputs_directory = f"/home/{getpass.getuser()}/watermarker_outputs"
default_image_path = "image.png"
default_logo_path = "logo.png"

logo_file_path = None

# Set default logo place, which is bottom left
bottom = True
left = True

# Save flag
save = False

# percent of original size
height_scale_percent = 6

# percent of distance from sides
distance_from_sides_of_picture_percent = 5
distance_from_up_bottom_of_picture_percent = 5

images = list()


def add_included_images_to_images_list(directory):
    for root, directories, included_files in os.walk(directory):
        for file in included_files:
            if '.png' in file or '.jpg' in file or '.jpeg' in file:
                images.append(os.path.join(root, file))


# Pars arguments
try:
    opts, args = getopt.getopt(args,"hr:i:l:p:d:u:s",["folder=", "image=", "logo=", "percents="])
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
        print('-d <distance from left or right >')
        print('-u <distance from up or bottom>')
        print('-s')
        print('')
        print('Use -s flag to save result')
        print('If you don\'t gave image path and watermark, script consume them by default as image.png and logo.png')
        print('With -p option, declare logo should be how many percents of the main image')
        print('By defalt, this value is 6%')
        print('You can set logo distance from picture sides using -d')
        print('You can set logo distance from up or bottom using -u')
        print('Default value for these are 5%')
        print('Use top, bottom, left and right key words to declare watermark place')
        print('Watermark palce is by default bottom and left')
        sys.exit()
    elif opt in ("-i", "--image"):
        images.append(arg)
    elif opt in ("-l", "--logo"):
        logo_file_path = arg
    elif opt in ("-p", "--percents"):
        height_scale_percent = int(arg)
    elif opt in ("-d"):
        distance_from_sides_of_picture_percent = int(arg)
    elif opt in ("-u"):
        distance_from_up_bottom_of_picture_percent = int(arg)
    elif opt in ("-r"):
        add_included_images_to_images_list(directory=arg)
    elif opt in ("-s"):
        save = True


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
        elif argument == 'folder':
            add_included_images_to_images_list(directory=value)

if not images:
    images.append(default_image_path)

if logo_file_path is None or logo_file_path == '':
    logo_file_path = default_logo_path


def get_absolute_image_name(image_file_path):
    return re.search("\w+\.[a-z]+", image_file_path).group()

def save(img: Image):
    image_filename = get_absolute_image_name(img.filename)
    try:
        os.mkdir(default_outputs_directory)
    except FileExistsError:
        [ os.remove(os.path.join(default_outputs_directory, file)) for file in os.listdir(default_outputs_directory) ]
    print(f"{image_filename}: ", end="")
    try:
        img.save("%s/output_%s" % (default_outputs_directory, image_filename)) 
    except OSError:
        print("\033[91m{}\033[00m".format("Failed"))
    print("\033[92m{}\033[00m" .format("Successfull"))

def add_watermark(image_file_path):

    # Load image and watermark
    img = Image.open(image_file_path)
    logo = Image.open(logo_file_path)
    
    img_width, img_height= img.size
    logo_width, logo_height = logo.size
    
    width_scale_percent = (height_scale_percent * img_height * logo_width) / (img_width * logo_height)

    # Calculate new width and height of logo
    logo_width = int(img_width * width_scale_percent  / 100)
    logo_height = int(img_height * height_scale_percent / 100)

    # Resize logo
    logo = logo.resize((logo_width, logo_height))

    # Calculate distance from image sides
    distance_from_bottom = int(img_height * distance_from_up_bottom_of_picture_percent / 100)
    distance_from_side = int(img_width * distance_from_sides_of_picture_percent / 100)

    if bottom:
        logo_starting_height = img_height - logo_height - distance_from_bottom
        logo_ending_height = img_height - distance_from_bottom
    else:
        logo_starting_height = distance_from_bottom
        logo_ending_height = logo_height + distance_from_bottom

    if left:
        logo_starting_width = distance_from_side
        logo_ending_width = logo_width + distance_from_side
    else:
        logo_starting_width = img_width - logo_width - distance_from_side
        logo_ending_width = img_width - distance_from_side

    # Set watermark palce
    position = (logo_starting_width, logo_starting_height)

    # Add watermark to base image
    img.paste(logo, position, mask=logo)

    img.show()
    
    if save:
        save(img)

if __name__ == '__main__':
    for image in images:
        add_watermark(image)
