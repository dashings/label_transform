#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import argparse
import collections
import datetime
import glob
import json
import os
import os.path as osp
import sys
import numpy as np
import PIL.Image
import labelme
import pycocotools.mask

'''
labelme
1. 同一张图片中如果有多个同类物体的实例目标，应该在实例标签后添加“-1，-2，-3…”等，例如:person-1,person-2,dog
2.标注完后，会在文件夹中生成对应的json文件，然后我们需要将每个图片json转换为coco格式，首先创建一个label.txt，内容如下，其中后面四个为自己的实例分割目标，前面两个是必须的，不可以删掉，只需修改添加自己的实例目标即可：
txt内容：
    __ignore__
    _background_
    plane
    cat
    dog
    person

运行方式：
python labelme2coco.py your-image-and-labelme-json-path your-expected-output-folder --labels the-path-of-labels.txt
其中：
your-image-and-labelme-json-path ：是你刚才标注好的json文件和图片的文件夹；
your-expected-output-folder ：是你要输出的数据集保存的文件夹；
the-path-of-labels.txt ： 是你刚才写的label.txt文件。

'''

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_dir', help='input annotated directory')
    parser.add_argument('output_dir', help='output dataset directory')
    parser.add_argument('--labels', help='labels file', required=True)
    args = parser.parse_args()

    if osp.exists(args.output_dir):
        print('Output directory already exists:', args.output_dir)
        sys.exit(1)
    os.makedirs(args.output_dir)
    os.makedirs(osp.join(args.output_dir, 'JPEGImages'))
    print('Creating dataset:', args.output_dir)

    now = datetime.datetime.now()

    data = dict(
        info=dict(
            description=None,
            url=None,
            version=None,
            year=now.year,
            contributor=None,
            date_created=now.strftime('%Y-%m-%d %H:%M:%S.%f'),
        ),
        licenses=[dict(
            url=None,
            id=0,
            name=None,
        )],
        images=[
            # license, url, file_name, height, width, date_captured, id
        ],
        type='instances',
        annotations=[
            # segmentation, area, iscrowd, image_id, bbox, category_id, id
        ],
        categories=[
            # supercategory, id, name
        ],
    )

    class_name_to_id = {}
    for i, line in enumerate(open(args.labels).readlines()):
        class_id = i - 1  # starts with -1
        class_name = line.strip()
        if class_id == -1:
            assert class_name == '__ignore__'
            continue
        class_name_to_id[class_name] = class_id
        data['categories'].append(dict(
            supercategory=None,
            id=class_id,
            name=class_name,
        ))

    out_ann_file = osp.join(args.output_dir, 'annotations.json')
    label_files = glob.glob(osp.join(args.input_dir, '*.json'))
    for image_id, label_file in enumerate(label_files):
        print('Generating dataset from:', label_file)
        with open(label_file) as f:
            label_data = json.load(f)

        base = osp.splitext(osp.basename(label_file))[0]
        out_img_file = osp.join(
            args.output_dir, 'JPEGImages', base + '.jpg'
        )

        img_file = osp.join(
            osp.dirname(label_file), label_data['imagePath']
        )
        img = np.asarray(PIL.Image.open(img_file))
        PIL.Image.fromarray(img).save(out_img_file)
        data['images'].append(dict(
            license=0,
            url=None,
            file_name=osp.relpath(out_img_file, osp.dirname(out_ann_file)),
            height=img.shape[0],
            width=img.shape[1],
            date_captured=None,
            id=image_id,
        ))

        masks = {}  # for area
        segmentations = collections.defaultdict(list)  # for segmentation
        for shape in label_data['shapes']:
            points = shape['points']
            label = shape['label']
            shape_type = shape.get('shape_type', None)
            mask = labelme.utils.shape_to_mask(
                img.shape[:2], points, shape_type
            )

            if label in masks:
                masks[label] = masks[label] | mask
            else:
                masks[label] = mask

            points = np.asarray(points).flatten().tolist()
            segmentations[label].append(points)

        for label, mask in masks.items():
            cls_name = label.split('-')[0]
            if cls_name not in class_name_to_id:
                continue
            cls_id = class_name_to_id[cls_name]

            mask = np.asfortranarray(mask.astype(np.uint8))
            mask = pycocotools.mask.encode(mask)
            area = float(pycocotools.mask.area(mask))
            bbox = pycocotools.mask.toBbox(mask).flatten().tolist()

            data['annotations'].append(dict(
                id=len(data['annotations']),
                image_id=image_id,
                category_id=cls_id,
                segmentation=segmentations[label],
                area=area,
                bbox=bbox,
                iscrowd=0,
            ))

    with open(out_ann_file, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    main()
