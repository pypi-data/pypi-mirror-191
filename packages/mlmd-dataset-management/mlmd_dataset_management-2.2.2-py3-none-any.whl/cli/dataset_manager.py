import json

def print_prediction(execution_id):
    from modules.analytics_dao.prediction_dao import get_prediction_gen
    gen = get_prediction_gen(execution_id)
    for doc in gen:
        print(doc.to_dict())

def parse_r_detection_label(label, dtype="array_of_objects", filtering_labels=None, filtering_indexes=None):
    try:
        if not label:
            return False
        data = label.split(":")
        if len(data) == 3:
            predictions = json.loads(data[1])
            labels = json.loads(data[2])
        else:
            predictions = json.loads(data[0])
            labels = None
        if len(predictions) <= 0:
            return False
        if dtype == "array_of_objects":
            ret = []
            for idx, prediction in enumerate(predictions):
                if (not filtering_labels or label in filtering_labels) and \
                    (not filtering_indexes or idx in filtering_indexes):
                    label = labels[int(prediction[1])] if labels is not None else str(prediction[1])
                    label = label + " - {}".format(prediction[2])
                    ret.append({
                        "parent_index": int(prediction[0]),
                        "label_index": prediction[1],
                        "label": label,
                        "score": prediction[2],
                        "coord": prediction[3:]
                    })
        else:
            ret = {"label_indexes":[],"scores":[],"coords":[], "parent_indexes":[], "label":[]}
            for idx, prediction in enumerate(predictions):
                label = labels[int(prediction[1])] if labels is not None else str(prediction[1])
                label = label + " - {}".format(prediction[2])
                if (not filtering_labels or label in filtering_labels) and \
                    (not filtering_indexes or idx in filtering_indexes):
                    ret["parent_indexes"].append(int(prediction[0]))
                    ret["label_indexes"].append(prediction[1])
                    ret["label"].append(label)
                    ret["scores"].append(prediction[2])
                    ret["coords"].append(prediction[3:])
        return ret
    except Exception as e:
        print(e)
        return False

def main():
    import sys
    import os
    arg1 = sys.argv[1]
    if arg1 == "get-prediction":
        execution_id = sys.argv[2]
        print_prediction(execution_id)
        return
    if arg1 == "get-execution":
        from modules.analytics_dao.moap_execution_dao import get_moap_execution
        execution_id = sys.argv[2]
        exe = get_moap_execution(execution_id)
        print(exe)
        return
    if arg1 == "get-dataset":
        dataset_name = sys.argv[2]
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        pretty_json = json.dumps(str(ds), indent=4)
        print(pretty_json)
        return
    if arg1 == "get-samples":
        dataset_name = sys.argv[2]
        number_of_samples = int(sys.argv[3])
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        filelist = ds.get_filelist(get_annotation=True)
        ret = []
        for sample in filelist:
            if len(ret) >= number_of_samples:
                break
            ret.append(sample)
        pretty_json = json.dumps(ret, indent=4)
        print(pretty_json)
        return
    if arg1 == "list-datasets":
        from dataset_manager.dataset_manager import list_datasets
        datasets =list_datasets()
        pretty_json = json.dumps(datasets, indent=4)
        print(pretty_json)
        return
    if arg1 == "download-dataset":
        dataset_name = sys.argv[2]
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        ds.download_to_dir(".")
        return
    if arg1 == "download-images":
        dataset_name = sys.argv[2]
        filelist = sys.argv[3].split(",")
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        ds.download_to_dir(".", filelist=filelist)
        return
    if arg1 == "decorate-with-gt":
        import os
        import numpy as np
        from dataset_management.utils import get_random_color
        from PIL import Image, ImageDraw
        dataset_name = sys.argv[2]
        try:
            output_dir = sys.argv[3]
        except:
            output_dir = "."
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        curr_files = os.listdir(".")
        g = ds.get_filelist(get_annotation=True)
        os.makedirs(output_dir, exist_ok=True)
        color = get_random_color()
        for file_name, annotation in g:
            if file_name not in curr_files:
                continue
            source_img = Image.open(file_name).convert("RGB")
            draw = ImageDraw.Draw(source_img)
            parsed_annotations = parse_r_detection_label(annotation)
            print(file_name, " => ",parsed_annotations)
            if not parsed_annotations:
                continue
            for ann in parsed_annotations:
                coord = np.asarray(ann['coord']) * [source_img.width, source_img.height, source_img.width, source_img.height]
                draw.rectangle(((coord[0], coord[1]), (coord[2], coord[3])), width=3, outline="red")
                draw.text((coord[0] + 10, coord[1]), ann['label'], fill="red")
            source_img.save(os.path.join(output_dir, file_name), "JPEG")
        return
    if arg1 == "decorate-with-execution":
        import os
        import numpy as np
        from dataset_management.utils import get_random_color
        from PIL import Image, ImageDraw
        dataset_name = sys.argv[2]
        execution_id = sys.argv[3]
        try:
            output_dir = sys.argv[4]
        except:
            output_dir = "."
        
        curr_files = os.listdir(".")
        os.makedirs(output_dir, exist_ok=True)

        from modules.analytics_dao.prediction_dao import get_prediction_gen
        g = get_prediction_gen(execution_id)
        for item in g:
            item = item.to_dict()
            file_name = item['document_id']
            if file_name not in curr_files:
                continue
            source_img = Image.open(file_name).convert("RGB")
            draw = ImageDraw.Draw(source_img)

            for k, annotation in item.items():
                if "_output" in k:
                    color = get_random_color()
                    parsed_annotations = parse_r_detection_label(annotation)
                    print(file_name, " => ",parsed_annotations)
                    if not parsed_annotations:
                        continue
                    for ann in parsed_annotations:
                        coord = np.asarray(ann['coord']) * [source_img.width, source_img.height, source_img.width, source_img.height]
                        draw.rectangle(((coord[0], coord[1]), (coord[2], coord[3])), width=3, outline=color)
                        draw.text((coord[0] + 10, coord[1]), ann['label'], fill=color)
            source_img.save(os.path.join(output_dir, file_name), "JPEG")
        return
    print("Unsupport command: {}".format(arg1))

if __name__ == "__main__":
    main()