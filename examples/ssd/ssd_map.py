from __future__ import division
import xml.etree.ElementTree as ET
import argparse
class BoundingBox(object):
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
    def area(self):
        return (self.xmax - self.xmin) * (self.ymax -self.ymin)

class Object(object):
    def parse(self, line):
        words = line.split()
        self.image_name = words[0] + ".xml"
        self.confidence = float(words[1])
        self.rect       = BoundingBox(int(words[2]), int(words[3]), int(words[4]), int(words[5]))

    def __init__(self, line):
        self.parse(line)

    def __lt__(self, other):
        return self.confidence >= other.confidence

    def __eq__(self, other):
        return self.image_name == other.image_name

def average_precision():
    return 0

def IoU(bounding_box, ground_truth):
    return  round(intersection(bounding_box, ground_truth) / ground_truth.area(), 2)

def intersection(a, b):  # returns None if rectangles don't intersect
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if (dx>=0) and (dy>=0):
        return dx*dy
    else:
        return 0

def search_label(name, root):
    for obj in root.iter('object'):
        if obj[0].text != name:
            print(obj[0].text + " != " + name)
            return False
    return True

class_file = "/home/tolik/data/VOCdevkit/results/VOC2007/SSD_300x300_score/Main_from_cluster/comp4_det_test_aeroplane.txt"
file = open(class_file, 'r')

aeroplan_objects = []
for line in file.readlines():
    obj = Object(line)
    if obj in aeroplan_objects:
        if aeroplan_objects[aeroplan_objects.index(obj)].confidence < obj.confidence:
            aeroplan_objects[aeroplan_objects.index(obj)] = obj
    else:
        aeroplan_objects.append(obj)

aeroplan_objects.sort()

TP = 0
FP = 0
path_to_anotation = "/home/tolik/data/VOCdevkit/VOC2007/Annotations"

print len(aeroplan_objects)
precision = []
for obj in aeroplan_objects:
    anotation = ET.parse(path_to_anotation + "/" + obj.image_name)
    root = anotation.getroot()
    for bndbox in root.iter('bndbox'):
        xmin = float(bndbox[0].text)
        ymin = float(bndbox[1].text)
        xmax = float(bndbox[2].text)
        ymax = float(bndbox[3].text)
        # print obj.image_name, xmin, ymin, xmax, ymax
        break
    if not search_label("aeroplane", root):
        FP += 1
        prec = TP / (TP + FP)
        precision.append(prec)
        print '============='
        print obj.image_name
        print TP
        print FP
        print prec
        print '=============\n'
        continue

    iou = IoU(obj.rect, BoundingBox(xmin, ymin, xmax, ymax))
    if (iou >= 0.50):
        TP += 1
    else:
        FP += 1
    prec = TP / (TP + FP)
    precision.append(prec)
    print '\n'
    print '============='
    print TP
    print FP
    print prec
    print '=============\n'

print "average_precision:"
print round(sum(precision) / len(precision),2)

    # print IoU(obj.rect, BoundingBox(xmin, ymin, xmax, ymax))
    # print xmin, ymin, xmax, ymax


# def parse_args():
    # '''parse args'''
    # parser = argparse.ArgumentParser()
    # parser.add_argument('ground_truth', help='ground_truth')
    # parser.add_argument('class_file',   help='class_file')
    # return parser.parse_args()

# if __name__ == '__main__':
    # main(parse_args())
