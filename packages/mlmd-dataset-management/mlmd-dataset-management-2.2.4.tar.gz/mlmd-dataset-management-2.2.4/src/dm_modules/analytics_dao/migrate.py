from dm_modules.analytics_dao.groundtruth_dao import insert_groundtruth
import dataset_manager as dm

dataset_name = "test_moap_ir_hotspot_det_0"
model_id = "moap-ir-hotspot-det"
ds = dm.get_dataset(dataset_name)
gen = ds.get_filelist(get_annotation=True)
for item in gen:
    data = {
        "dataset_id": dataset_name,
        "document_id": item[0],
        "model_id": model_id,
        "gt": item[1]
    }
    insert_groundtruth(data)
    print(data)