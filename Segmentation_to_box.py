import csv
import os
import json
import re
import cv2
from PIL import Image

file = open('annotations.csv')

csv_reader = csv.reader(file)

header = []
header = next(csv_reader)
rows = []
for row in csv_reader:
    rows.append(row)

for i in rows:
    image_file = "D:\git\RealtimeTracker\macaquepose_v1" + os.sep + "v1\images" + os.sep + i[0]
    image = cv2.imread(image_file)
    height, width, _ = image.shape
    text_file = i[0].replace('.jpg', '.txt')

    if os.path.exists(".\labels" + os.sep + text_file):
        os.remove(".\labels" + os.sep + text_file)
    data_file = open(".\labels" + os.sep + text_file, "w")
    indices_seg = [i.start() for i in re.finditer("segment", i[2])]
    print(indices_seg)
    indices_bracket = [i.start() for i in re.finditer("}", i[2])]
    print(indices_bracket)

    for j in range(len(indices_seg)):
        try:
            seg = i[2][indices_seg[j] - 2:indices_bracket[j] + 1]
        except IndexError:
            print("ERROR")
        res = json.loads(seg)
        coordinates = res['segment']
        list_x = []
        list_y = []

        if len(coordinates) == 0:
            continue

        for coordinate in coordinates:
            list_x.append(coordinate[0])
            list_y.append(coordinate[1])
        min_x = min(list_x)
        max_x = max(list_x)
        min_y = min(list_y)
        max_y = max(list_y)

        data_file.write(
            str(0) + " " + str(((min_x + max_x) / 2) / width) + " " + str(
                ((min_y + max_y) / 2) / height) + " " + str((max_x - min_x) / width) + " " + str(
                (max_y - min_y) / height))
        data_file.write("\n")
    data_file.close()

if os.path.exists("data.txt"):
    os.remove("data.txt")
data_file = open("data.txt", "w")
