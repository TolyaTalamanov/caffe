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
        return ' '.join(str(x) for x in [self.im_id, self.conf, self.xmin, self.ymin, self.xmax, self.ymax])

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
            dt.append(DTObject(conf, int(xmin), int(ymin), int(xmax), int(ymax)))
        return dt

# gt = read_groundtruth('ground_truth/gt_person.txt')
# dt = read_detections('detections/dt_person.txt')
