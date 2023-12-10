import json

coco_annotations_file = './in.json' # INPUT FILE IN COCO FORMAT
fairmot_annotations_file = './annotations.json' # OUTPUT FILE ON MOT FORMAT


def coco_to_mot(coco_annotations, fairmot_annotations):
    with open(coco_annotations, 'r') as f:
        coco_data = json.load(f)

    fairmot_data = []

    for image_info in coco_data['images']:
        image_id = image_info['id']
        file_name = image_info['file_name']

        annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] == image_id]

        frame_info = {
            "frame_id": image_id,
            "file_name": file_name,
            "height": image_info['height'],
            "width": image_info['width'],
            "ann": []
        }

        for ann in annotations:
            bbox = ann['bbox']
            track_id = ann.get('track_id', ann['id'])  # Assuming track_id is available, otherwise use annotation id

            frame_info['ann'].append({
                "track_id": track_id,
                "bbox": [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]]
                # Convert COCO format to FairMOT format
            })

        fairmot_data.append(frame_info)

    with open(fairmot_annotations, 'w') as f:
        json.dump(fairmot_data, f)


coco_to_mot(coco_annotations_file, fairmot_annotations_file)
