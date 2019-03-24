import numpy as np
import matplotlib.pyplot as plt

class GTObject(object):
    def __init__(self, img_id, xmin, ymin, xmax, ymax):
        self.img_id = img_id
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
    def __str__(self):
        return ' '.join(str(x) for x in [self.img_id, self.xmin, self.ymin, self.xmax, self.ymax])

class DTObject(object):
    def __init__(self, img_id, conf, xmin, ymin, xmax, ymax):
        self.img_id = img_id
        self.conf = conf
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
    def __str__(self):
        return ' '.join(str(x) for x in [self.img_id, self.conf, self.xmin, self.ymin, self.xmax, self.ymax])

def read_groundtruth(path_to_ants):
    gt = []
    with open(path_to_ants, 'r') as f:
        for line in f:
            img_id, xmin, ymin, xmax, ymax = line.split() 
            gt.append(GTObject(img_id, int(xmin), int(ymin), int(xmax), int(ymax)))
        return gt

def read_detections(path_to_detections):
    dt = []
    with open(path_to_detections, 'r') as f:
        for line in f:
            img_id, conf, xmin, ymin, xmax, ymax = line.split() 
            dt.append(DTObject(img_id, float(conf), int(xmin), int(ymin), int(xmax), int(ymax)))
        return dt

gts = read_groundtruth('ground_truth/gt_cat.txt')
dts = read_detections('detections/dt_cat.txt')

# number of objects of this class in the annotations
total_class_casses = len(dts)

precision = []
recall = []
tp = 0

dts.sort(key=lambda x: x.conf, reverse=True)
id_to_gts = {}

for gt in gts:
    if gt.img_id in id_to_gts:
        id_to_gts[gt.img_id].append(gt)
    else:
        id_to_gts[gt.img_id] = [ gt ]

for i, dt in enumerate(dts, 1):
    if dt.img_id in id_to_gts:
        max_iou = IoU(dt, gt)
        idx_max_iou = 0
        for j, gt in enumerate(id_to_gts[dt.img_id]):
            iou = IoU(dt, gt)
            if iou > max_iou:
                max_iou = iou
                idx_max_iou = j
        if max_iou > 0.5:
            tp += 1
            del it_to_gst[dt.img_id][idx_max_iou]

    precision.append(tp / i)
    recall.append(tp / total_class_casses)

plt.plot(precision, recall)
plot.show()
