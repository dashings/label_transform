import xml.etree.ElementTree as ET
import os

class_list = ['toilet', 'sink', 'desk', 'orange', 'pink', 'lightblue']

def convert_annotation(corresponding_xml_file, list_file):
    in_file = open(corresponding_xml_file, 'r', encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in class_list or int(difficult) == 1:
            continue
        cls_id = class_list.index(cls)

        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


if __name__ == '__main__':
    # train.txt
    # 文件夹结构  path/to/train/subdirName/img.jpg
    # annotation_root和 image_root两个文件夹下的目录结构要一致，路径可以不一样
    annotation_root = r'C:\Users\yaoji\Desktop\test'
    image_root = r'C:\Users\yaoji\Desktop\test'


    categories = {
        'train': 'train',
        'test:': 'test',
    }

    # .txt存放的路径
    txt_save_path = r'C:\Users\yaoji\Desktop\test'
    trainset_file = open( os.path.join(txt_save_path,'train.txt'), 'w')
    testset_file = open(os.path.join(txt_save_path,'test.txt'), 'w')

    for category in categories:
        image_sets = os.path.join(image_root, categories.get(category))
        annotation_sets = os.path.join(annotation_root, categories.get(category))

        if not os.path.exists(image_sets):
            continue

        if category == 'train':
            in_file = trainset_file
        else:
            in_file = testset_file


        anno_dirs = os.listdir(annotation_sets)
        for sub_dir in anno_dirs:
            image_set_dir = os.path.join(image_sets, sub_dir)
            annotation_set_dir = os.path.join(annotation_sets, sub_dir)

            # in_file = trainset_file

            files = os.listdir(image_set_dir)
            for file in files:
                image_file = os.path.join(image_set_dir, file)
                if os.path.isfile(image_file):
                    file_suffix = os.path.splitext(image_file)[1]
                    if file_suffix == '.jpg' or file_suffix == '.png' or file_suffix == '.bmp':
                        corresponding_xml_file = os.path.splitext(os.path.join(annotation_set_dir, file))[0] + '.xml'
                        if os.path.exists(corresponding_xml_file):
                            in_file.write('%s' % image_file)
                            convert_annotation(corresponding_xml_file, in_file)
                            in_file.write('\n')
                        else:
                            in_file.write('%s/%s' % (image_set_dir, file))
                            in_file.write('\n')

    trainset_file.close()
    testset_file.close()







