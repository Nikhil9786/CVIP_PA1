"""
Character Detection

The goal of this task is to experiment with template matching techniques. Specifically, the task is to find ALL of
the coordinates where a specific character appears using template matching.

There are 3 sub tasks:
1. Detect character 'a'.
2. Detect character 'b'.
3. Detect character 'c'.

You need to customize your own templates. The templates containing character 'a', 'b' and 'c' should be named as
'a.jpg', 'b.jpg', 'c.jpg' and stored in './data/' folder.

Please complete all the functions that are labelled with '# TODO'. Whem implementing the functions,
comment the lines 'raise NotImplementedError' instead of deleting them. The functions defined in utils.py
and the functions you implement in task1.py are of great help.

Do NOT modify the code provided.
Do NOT use any API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import any library (function, module, etc.).
"""


import argparse
import json
import os
import cv2
import numpy as np
import utils
from task1 import read_image , normalize  # you could modify this line
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow, Circle



def parse_args():
    parser = argparse.ArgumentParser(description="cse 473/573 project 1.")
    parser.add_argument(
        "--img_path", type=str, default="./data/proj1-task2-png.png",
        help="path to the image used for character detection (do not change this arg)")
    parser.add_argument(
        "--template_path", type=str, default="./data/a.jpg",
        choices=["./data/a.jpg", "./data/b.jpg", "./data/c.jpg"],
        help="path to the template image")
    parser.add_argument(
        "--result_saving_directory", dest="rs_directory", type=str, default="./results/",
        help="directory to which results are saved (do not change this arg)")
    args = parser.parse_args()
    return args


def detect(img, template):
    """Detect a given character, i.e., the character in the template image.

    Args:
        img: nested list (int), image that contains character to be detected.
        template: nested list (int), template image.

    Returns:
        coordinates: list (tuple), a list whose elements are coordinates where the character appears.
            format of the tuple: (x (int), y (int)), x and y are integers.
            x: row that the character appears (starts from 0).
            y: column that the character appears (starts from 0).
    """
    # TODO: implement this function.
    widthim, heightim = (np.asarray(img)).shape
    widthtemp, heighttemp = (np.asarray(template)).shape
    template = np.asarray(template)
    some_list = list()
    pad_img = utils.zero_pad(img,widthtemp+1,heighttemp+1)
    
    for i in range(widthim):
        for j in range(heightim):
            img_crop = np.asarray(utils.crop(pad_img,i+widthtemp+1,i+widthtemp+widthtemp+1,j+heighttemp+1,j+heighttemp+heighttemp+1))
#            print(i+widthtemp+1, j+heighttemp+1)
            tatti = 0
            for k in range(len(template[0])):
                for l in range(len(template[1])):
                    tatti += ((img_crop[k][l] - template[k][l])**2)
#            print(tatti)
#            if tatti < 0.156:
            some_list.append(tatti)
#    coordinates = some_list
    normed_coor = (normalize(some_list)).reshape(widthim, heightim)
    print(normed_coor.shape)
    coordinates = list()
    
    for x in range(widthim):
        for y in range(heightim):
#            print(normed_coor[x][y])
            if normed_coor[x][y] < 0.01:
                coordinates.append((x,y))

#    raise NotImplementedError
    return coordinates


def save_results(coordinates, template, template_name, rs_directory):
    results = {}
    results["coordinates"] = sorted(coordinates, key=lambda x: x[0])
    results["templat_size"] = (len(template), len(template[0]))
    with open(os.path.join(rs_directory, template_name), "w") as file:
        json.dump(results, file)


def main():
    args = parse_args()

    img = read_image(args.img_path)
    template = read_image(args.template_path)

    coordinates = detect(img, template)
    print(coordinates)
#    print(coordinates)
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    for i in coordinates:
        ax.add_patch(Circle((i[1], i[0]), radius=1, color='red'))
        plt.show(fig)

    template_name = "{}.json".format(os.path.splitext(os.path.split(args.template_path)[1])[0])
    save_results(coordinates, template, template_name, args.rs_directory)
    

if __name__ == "__main__":
    main()
