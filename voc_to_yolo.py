import xml.etree.ElementTree as ET
from os import getcwd, path


sets=[('2012', 'train')]
# sets=[('2012', 'train'), ('2012', 'val')]

classes = ["cola","milk tea","ice tea","beer","shampoo","toothpaste","soap","pear","apple","orange"]
# wd = getcwd()
vocPath = getcwd()


def convert_annotation(year, image_id, list_file, voc_path):
    in_file = open(path.join(voc_path ,'VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id)))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


for year, image_set in sets:
    image_ids = open(path.join(vocPath,'VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set))).read().strip().split()
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg'%(vocPath, year, image_id))
        convert_annotation(year, image_id, list_file, vocPath)
        list_file.write('\n')
    list_file.close()