import pandas as pd
import redis
import json
class Extractors:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def load_data(self):
        self.data = pd.read_csv(self.file_path)

    def transform_data(self):
        self.data = self.data[['Employee_Name', 'EmpID', 'MarriedID', 'MaritalStatusID', 'GenderID']]
        return self.data

    def get_metadata(self):
        metadata = {}
        headers = dict(self.data.dtypes)
        # todo : Hard coding for the demo need to set them in the config file other than data types
        metadata["name"] = "Annual sales "
        metadata["field_names"] = {key: str(value) for key, value in headers.items()}
        metadata["trans_comments"] = "Reduced the data set to only few columns"
        metadata["source"] = "xyz1.com"
        json_data = json.dumps(metadata)
        self.r.set('meta_data', json_data)
        return metadata

transformer = Extractors("../data/HRDataset.csv")
transformer.load_data()
transformer.transform_data()
metadata = transformer.get_metadata()
print(metadata)
