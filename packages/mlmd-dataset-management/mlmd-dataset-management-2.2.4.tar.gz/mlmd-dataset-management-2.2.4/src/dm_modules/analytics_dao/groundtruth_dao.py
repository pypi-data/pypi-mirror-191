from dm_modules.analytics_dao.db import get_connection, get_collection_name

db_client = get_connection()

def insert_groundtruth(groundtruth_data):
    collection_name = get_collection_name("groundtruth", None)
    from dm_modules.analytics_dao.groundtruth_scheme import parse_data
    document_id, decorated_data = parse_data(groundtruth_data)
    return db_client.collection(collection_name).document(document_id).set(decorated_data, merge=True)

def get_groundtruth_gen(dataset_id):
    collection_name = get_collection_name("groundtruth", None)
    if not collection_name:
        return None
    return db_client.collection(collection_name).where(u'dataset_id', u'==', dataset_id).stream()

# dataset_name = "test_moap_ir_hotspot_det_0"
# gen = get_groundtruth_gen(dataset_name)
# for item in gen:
#     print(item.to_dict())