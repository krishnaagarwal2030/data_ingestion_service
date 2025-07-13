import unittest
import sys
import datetime
sys.path.append('../')
from data_ingestion_app.core_modules import collect_data, transform_data, store_data

class TestDataIngestion(unittest.TestCase):

    def test_transform_data(self):
        sample_input = "[{key: value}]"
        expected_output = {"data": "[{key: value}]", "ingested_at": datetime.datetime.utcnow(), "source":"sample_url"}
        respone, actual_output = transform_data(input_data=sample_input, data_source="sample_url")
        self.assertEqual(expected_output["data"], actual_output["data"])
        assert isinstance(expected_output["ingested_at"], datetime.datetime) #checking if output is of datetime object
        self.assertEqual(expected_output["source"], actual_output["source"])

    def test_collect_data(self):
        data_source = "https://jsonplaceholder.typicode.com/posts"
        self.assertEqual((408, None), collect_data(data_source, timeout=0.001))
        self.assertEqual(200, collect_data(data_source)[0])

    def test_store_data(self):
        sample_input = {"key": "value"}
        self.assertEqual(200, store_data(data=sample_input))


if __name__ == '__main__':
    unittest.main()
