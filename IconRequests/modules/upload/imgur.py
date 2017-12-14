from base64 import b64encode
from os import path
import requests

from IconRequests.modules.settings import Settings
from .upload import Upload

UPLOAD_URI = "https://api.imgur.com/3/upload"


class Imgur(Upload):
    _instance = None

    def __init__(self):
        super(Imgur, self).__init__()
        self.client_id = Settings.get_default().imgur_client_id

    @staticmethod
    def get_default():
        if Imgur._instance is None:
            Imgur._instance = Imgur()
        return Imgur._instance

    def upload_icon(self, image_path, title=None):
        if path.isfile(image_path):
            with open(image_path, 'rb') as image_obj:
                image_data = b64encode(image_obj.read())
            image_obj.close()

            headers = {
                "Authorization": "Client-ID {0}".format(self.client_id),
                "Accept": "application/json"
            }
            if not title:
                title = path.basename(image_path)

            data = {
                "type": "base64",
                "image": image_data,
                "title": title
            }
            try:
                query = requests.post(UPLOAD_URI, data, headers=headers)
                if query.status_code == 200:
                    return query.json()["data"]["link"]
            except requests.exceptions.ConnectionError:
                pass
        return None
