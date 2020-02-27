#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
time:
"""

import os, sys
import glob
from PIL import Image


src_img_dir = r"C:\Users\yaoji\Desktop\test\train"   # VEDAI 图像存储位置
xmlSaveDir = r"C:\Users\yaoji\Desktop\test\train"  # VEDAI 图像生成的xml文件存放位置

xmlMoveTo_xmlSaveDir = False # if False : xmlSaveDir = src_img_dir

subdirs = os.listdir(src_img_dir)
for sub_dir in subdirs:
    image_set = os.path.join(src_img_dir, sub_dir)
    img_Lists = glob.glob(image_set + '/*.jpg')

    for img in img_Lists:
        corresponding_xml_file = img.split(".")[0] + '.xml'
        if not os.path.exists(corresponding_xml_file):
            im = Image.open(img)
            width, height = im.size

            if xmlMoveTo_xmlSaveDir :
                xml_file = open((xmlSaveDir + '/' + os.path.basename(corresponding_xml_file)), 'w')
            else:
                xml_file = open(corresponding_xml_file, 'w')

            xml_file.write('<annotation>\n')
            xml_file.write('    <folder>VOC2007</folder>\n')
            xml_file.write('    <filename>' + os.path.basename(img) + '</filename>\n')
            xml_file.write('    <path>' + img + '</path>\n')
            xml_file.write('    <source>\n')
            xml_file.write('        <database>' + "Unknow" + '</database>\n')
            xml_file.write('    </source>\n')
            xml_file.write('    <size>\n')
            xml_file.write('        <width>' + str(width) + '</width>\n')
            xml_file.write('        <height>' + str(height) + '</height>\n')
            xml_file.write('        <depth>3</depth>\n')
            xml_file.write('    </size>\n')
            xml_file.write('    <segmented>0</segmented>\n')
            xml_file.write('</annotation>')







#
#     img_basenames = []  # e.g. 100.jpg
#     for item in img_Lists:
#         img_basenames.append(os.path.basename(item))
#
#
#
# img_names = []  # e.g. 100
# for item in img_basenames:
#     temp1, temp2 = os.path.splitext(item)
#     img_names.append(temp1)
#
# for img in img_names:
#     im = Image.open((src_img_dir + '/' + img + '.jpg'))
#     width, height = im.size
#     # write in xml file
#     # os.mknod(src_xml_dir + '/' + img + '.xml')
#     xml_file = open((xml_save_dir + '/' + img + '.xml'), 'w')
#     xml_file.write('<annotation>\n')
#     xml_file.write('    <folder>VOC2007</folder>\n')
#     xml_file.write('    <filename>' + str(img) + '.jpg' + '</filename>\n')
#     xml_file.write('    <path>' + xml_save_dir + '/' + str(img) + '.jpg' + '</path>\n')
#     xml_file.write('    <source>\n')
#     xml_file.write('        <database>' + "Unknow" + '</database>\n')
#     xml_file.write('    </source>\n')
#     xml_file.write('    <size>\n')
#     xml_file.write('        <width>' + str(width) + '</width>\n')
#     xml_file.write('        <height>' + str(height) + '</height>\n')
#     xml_file.write('        <depth>3</depth>\n')
#     xml_file.write('    </size>\n')
#     xml_file.write('    <segmented>0</segmented>\n')
#     xml_file.write('</annotation>')