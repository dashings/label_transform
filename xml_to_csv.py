# coding:utf-8
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
 
 
def xml_to_csv(anno_root_path):
    xml_list = []

    #支持多个子文件夹
    anno_dirs = os.listdir(anno_root_path)
    for sub_dir in anno_dirs:
        annotation_set_dir = os.path.join(anno_root_path, sub_dir)

        for xml_file in glob.glob(annotation_set_dir + '/*.xml'):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for member in root.findall('object'):
                #注：这里filename的组成改用“子文件夹名+文件名”的形式
                value = (sub_dir + '\\' + root.find('filename').text,
                         int(root.find('size')[0].text),
                         int(root.find('size')[1].text),
                         member[0].text,
                         int(member[4][0].text),
                         int(member[4][1].text),
                         int(member[4][2].text),
                         int(member[4][3].text)
                         )
                xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df
 
 
def main():
    #xml_path = os.path.join(os.getcwd(), 'annotations')
    xml_path = r'D:\data\apidataset'
    xml_df = xml_to_csv(xml_path)


    save_path = r'D:\data\apitestdata\data'
    csv_name = 'raccoon_labels.csv'

    csv_save_path = os.path.join(save_path, csv_name)
    xml_df.to_csv(csv_save_path, index=None)

    print('Successfully converted xml to csv.')
 
 
main()