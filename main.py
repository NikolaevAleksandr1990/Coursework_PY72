import time
import os.path
import requests
from tqdm import tqdm
import json


class BackupCopyPhoto:
    def __init__(self, toke: str):
        self.token = toke

    @staticmethod
    def catch_json():
        """Метод получения JSON - файла, для дальнейшей работы с ним"""
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': '362712',   # Введите ID пользователя, фотографии которого вы хотите сохранить
            'album_id': 'profile',
            'rev': '1',
            'extended': '1',
            'photo_sizes': '0',
            'count': '5',   # Количество сохраняемых фотографи
            'access_token': token,
            'v': '5.131'
        }
        res = requests.get(url, params=params)
        return res.json()

    def loader_large_photo(self, num):
        """Метод скачивания фотографии самого большого размер и сохранение данных в JSON"""
        name_photo = str(self.catch_json()['response']['items'][num]
                         ['likes']['count']) + '.jpg'
        way_to_photo = 'Photos/' + name_photo
        if not os.path.exists(name_photo):
            url_upload = str(self.catch_json()['response']['items']
                             [num]['sizes'][-1]['url'])
            img_data = requests.get(url_upload).content
            with tqdm.wrapattr(open(way_to_photo, 'wb'), "write",
                               miniters=0.01) as photo:
                photo.write(img_data)
            dictionary = {
                "file_name": str(self.catch_json()['response']['items'][num]
                                 ['likes']['count']) + '.jpg',
                "size": str(self.catch_json()['response']['items'][num]
                            ['sizes'][-1]['type'])
            }
            with open('photos.json', 'a', encoding='utf-8') as outfile:
                json.dump(dictionary, outfile,  ensure_ascii=False, indent=2)
            return way_to_photo
        else:
            name_photo = str(self.catch_json()['response']['items'][num]
                             ['likes']['count']) + '.jpg' \
                         + '_' + str(time.ctime(int(self.catch_json()[
                            'response']['items'][num]['likes']['date'])))
            way_to_photo = 'Photos/' + name_photo
            url_upload = str(self.catch_json()['response']['items'][num]
                             ['sizes'][-1]['url'])
            img_data = requests.get(url_upload).content
            with tqdm.wrapattr(open(way_to_photo, 'wb'), "write",
                               miniters=1) as photo:
                photo.write(img_data)
            dictionary = {
                 "file_name": str(self.catch_json()['response']['items'][num]
                                  ['likes']['count']) + '.jpg',
                 "size": str(self.catch_json()['response']['items']
                             [num]['sizes'][-1]['type'])
            }
            with open('photos.json', 'a', encoding='utf-8') as outfile:
                json.dump(dictionary, outfile,  ensure_ascii=False, indent=2)
            return way_to_photo


class YaUploader:

    def __init__(self, toke: str):
        self.token = toke

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, file_path):
        """Метод cсылку для загрузки на яндекс диск"""
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path: str, filename: str):
        """Метод загружает файлы на яндекс диск"""
        result = self._get_upload_link(file_path=file_path).get('href', '')
        response = requests.put(result, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Success')


if __name__ == '__main__':
    with open('tk.txt', 'r') as file_tk:
        token = file_tk.read().strip()
    with open('tkYandex.txt', 'r') as file_tkY:
        token_Ya = file_tkY.read().strip()
    vk_id = BackupCopyPhoto(token)
    uploader = YaUploader(token_Ya)
    for i in range(len(vk_id.catch_json()['response']['items'])):
        path_to_file = vk_id.loader_large_photo(i)
        file_ = path_to_file
        uploader.upload(path_to_file, file_)
        time.sleep(0.33)
