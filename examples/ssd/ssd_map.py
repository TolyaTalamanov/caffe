from __future__ import division
import time
import matplotlib.pyplot as plt
from itertools import chain
from itertools import compress
from collections import defaultdict
import os
import numpy as np
from xml.dom import minidom

import argparse
class BoundingBox(object):
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.checked = False

    def area(self):
        return (self.xmax - self.xmin) * (self.ymax -self.ymin)

class Object(object):
    def parse(self, line):
        words = line.split()
        self.image_name = words[0]
        self.confidence = float(words[1])
        self.rect = BoundingBox(int(words[2]), int(words[3]), int(words[4]), int(words[5]))

    def __init__(self, line):
        self.parse(line)

    def __lt__(self, other):
        return self.confidence >= other.confidence

    def __eq__(self, other):
        return self.image_name == other.image_name

class GTruth(object):
    def __init__(self, line):
        words = line.split()
        self.image_id = words[0]
        self.rect     = BoundingBox(int(words[1]), int(words[2]), int(words[3]), int(words[4]))

def IoU(bounding_box, ground_truth):
    return  round(intersection(bounding_box, ground_truth) / ground_truth.area(), 2)

def intersection(a, b):
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

def main(args):
    sum_ap = 0
    num_class = 0
    dt_folder = args.detections
    gt_dict = {}
    gt_folder = args.groundtruth

    gt_files = os.listdir(gt_folder)
    for gt_file in gt_files:
        gt_dict[gt_file[len('gt_') :]] = open(os.path.join(gt_folder, gt_file))

    dt_files = os.listdir(dt_folder)
    for dt_file in dt_files:
        num_class +=1 
        dt_objects = []
        detections_file = open(os.path.join(dt_folder, dt_file))

        for line in detections_file.readlines():
            obj = Object(line)
            dt_objects.append(obj)

        dt_objects.sort()

        gt_object = []
        grount_truth_f = gt_dict[dt_file[len('dt_') : ]]

        for line in grount_truth_f.readlines():
            gt = GTruth(line)
            gt_object.append(gt)

        img_id_to_truth_bndb = defaultdict(list)

        for gt in gt_object:
            img_id_to_truth_bndb[gt.image_id].append(gt.rect)

        tp = np.zeros(len(dt_objects), dtype=int)
        fp = np.zeros(len(dt_objects), dtype=int)

        for i, aeroplane in enumerate(dt_objects):
            iou_max = 0.50
            iou_max_idx = -1

            key = aeroplane.image_name

            if not key in img_id_to_truth_bndb:
                fp[i] = 1
                continue

            for j, gt in enumerate(img_id_to_truth_bndb[key]):
                if gt.checked:
                    continue
                cur_iou = IoU(gt, aeroplane.rect)
                if (cur_iou >= iou_max):
                    iou_max = cur_iou
                    iou_max_idx = j 

            if (iou_max_idx >= 0 and (not img_id_to_truth_bndb[key][iou_max_idx].checked)):
                tp[i] = 1
                img_id_to_truth_bndb[key][iou_max_idx].checked = True
            else:
                fp[i] = 1

        tp = list(np.cumsum(tp))
        fp = list(np.cumsum(fp))
        recall = [x / len(gt_object) for x in tp]
        precision = [tp[i] / (fp[i] + tp[i]) for i in range(len(tp))]

        ap = 0.0
        t = 0.0
        step = 0.1
        kpoints = 11
        while t <= 1.0:
            pr = max(chain(compress(precision,
                [recall[i] >= t for i in range(len(recall))]), [0.0]))
            ap += pr / kpoints
            t += step

        print dt_file[len('dt_') :] + ' = ' + str(ap)
        sum_ap += ap

    print 'mAp = ' + str(sum_ap / num_class)

def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--groundtruth', help = 'groundtruth')
    parser.add_argument('-d', '--detections', help = 'detections')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_args())
