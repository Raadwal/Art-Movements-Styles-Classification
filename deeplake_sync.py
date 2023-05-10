import deeplake
from concurrent.futures import ThreadPoolExecutor

token = ""

data_directory_train = r'Organized Images\train'
data_directory_dev = r'Organized Images\dev'
data_directory_val = r'Organized Images\val'
data_directory_test = r'Organized Images\test'

deeplake_path_train = 'hub://um_project/art-train'
deeplake_path_dev = 'hub://um_project/art-dev'
deeplake_path_val = 'hub://um_project/art-val'
deeplake_path_test = 'hub://um_project/art-test'

ds = deeplake.ingest_classification(data_directory_train, deeplake_path_train, token = token)
ds = deeplake.ingest_classification(data_directory_dev, deeplake_path_dev, token = token)
ds = deeplake.ingest_classification(data_directory_val, deeplake_path_val, token = token)
ds = deeplake.ingest_classification(data_directory_test, deeplake_path_test, token = token)