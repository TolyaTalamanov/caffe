import argparse
import os
from xml.dom import minidom

def main(args):
    classes = open(args.classes).read().split()
    class_dict = {}
    for class_name in classes:
        class_dict[class_name] = open('gt_' + class_name + '.txt', 'w')

    annotation_folder = args.annotations
    onlyfiles = [os.path.join(annotation_folder, f) for f in os.listdir(annotation_folder) if os.path.isfile(os.path.join(annotation_folder, f))]

    for f in onlyfiles:
        xmldoc = minidom.parse(f)
        itemlist = xmldoc.getElementsByTagName('object')
        for item in itemlist:
            name = (item.getElementsByTagName('name')[0]).firstChild.data
            bndbox = item.getElementsByTagName('bndbox')
            os.path.basename(f)
            for bb in bndbox:
                xmin = (bb.getElementsByTagName('xmin')[0]).firstChild.data
                ymin = (bb.getElementsByTagName('ymin')[0]).firstChild.data
                xmax = (bb.getElementsByTagName('xmax')[0]).firstChild.data
                ymax = (bb.getElementsByTagName('ymax')[0]).firstChild.data
                class_dict[name].write(str(os.path.splitext(os.path.basename(f))[0]) + ' ' + (xmin.split('.')[0]) + ' ' + (ymin.split('.')[0]) + ' ' + (xmax.split('.')[0]) + ' ' + (ymax.split('.')[0]) + '\n')

def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--annotations', help = 'annotations')
    parser.add_argument('-c', '--classes', help = 'classes')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_args())

