import os

import requests


class HttpManager(object):
    @staticmethod
    def upload_plugin(store_path, file_path, data):
        values = {**data, **{"action": "uploadPlugin"}}
        files = {file_path.split("/")[-1]: open(file_path, 'rb')}
        r = requests.post(store_path, files=files, data=values)
        print(r.status_code)
        print(r.text)
