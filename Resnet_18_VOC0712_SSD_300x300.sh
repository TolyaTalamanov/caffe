#!/bin/bash                                                                                         
#SBATCH --time=3000   
cp -r ~/lmdb /tmp
cd /common/home/itlab_sparse_mini/dnn-object-detectors-comp/ssd-detector/caffe 
python examples/ssd/ssd_pascal_resnet_18.py
