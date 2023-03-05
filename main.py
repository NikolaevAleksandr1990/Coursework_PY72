import time
import os.path
import requests
from tqdm import tqdm
import json
import os


class BackupCopyPhoto:
    def __init__(self, toke: str):
        self.token = toke

    @staticmethod
    def catch_json(num, id_number):
        """Метод получения JSON - файла, для дальнейшей работы с ним"""
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': id_number,
            'album_id': 'profile',
            'rev': '1',
            'extended': '1',
            'photo_sizes': '0',
            'count': num,
            'access_token': token,
            'v': '5.131'
        }
        res = requests.get(url, params=params)

        return res.json()

    def loader_large_photo(self, num):
        """Метод скачивания фотографии самого большого размер и сохранение данных в JSON"""
        _get_j_file = self.catch_json(numb, id_vk)
        name_photo = str(_get_j_file['response']['items'][num]
                         ['likes']['count']) + '.jpg'
        way_to_photo = 'Photos/' + name_photo

        if not os.path.exists(name_photo):
            url_upload = str(_get_j_file['response']['items']
                             [num]['sizes'][-1]['url'])
            img_data = requests.get(url_upload).content

            with open(way_to_photo, 'wb') as photo:
                photo.write(img_data)
            dictionary = {
                "file_name": str(_get_j_file['response']['items'][num]
                                 ['likes']['count']) + '.jpg',
                "size": str(_get_j_file['response']['items']
                            [num]['sizes'][-1]['type'])
                         }

            return [way_to_photo, dictionary]

        else:
            name_photo = str(_get_j_file['response']['items'][num]
                             ['likes']['count']) + '.jpg' \
                         + '_' + str(time.ctime
                                     (int(self.catch_json(
                                         numb, id_vk)['response']
                                          ['items'][num]['likes']
                                          ['date'])))
            way_to_photo = 'Photos/' + name_photo
            url_upload = str(_get_j_file['response']['items'][num]
                             ['sizes'][-1]['url'])
            img_data = requests.get(url_upload).content

            with open(way_to_photo, 'wb') as photo:
                photo.write(img_data)
            dictionary = {
                "file_name": str(_get_j_file['response']['items'][num]
                                 ['likes']['count']) + '.jpg',
                "size": str(_get_j_file['response']['items']
                            [num]['sizes'][-1]['type'])
            }

            return [way_to_photo, dictionary]


class YaUploader:

    def __init__(self, toke: str):
        self.token = toke

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, file_path):
        """Метод получения cсылки для загрузки на яндекс диск"""
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)

        return response.json()

    def create_folder(self, path):
        """Метод создания новой папки на яндекс диске"""
        href = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        headers['Accept'] = 'application/json'
        params = {'path': path}
        response = requests.put(href, headers=headers, params=params)

        return response.json()

    def upload(self, filepath: str, filename: str):
        """Метод загружает файлы на яндекс диск"""
        result_url = self._get_upload_link(file_path=filepath).get('href', '')
        response = requests.put(result_url, data=open(filename, 'rb'))
        response.raise_for_status()


if __name__ == '__main__':
    with open('tk.txt', 'r') as file_tk:
        token = file_tk.read().strip()
    with open('tkYandex.txt', 'r') as file_tkY:
        token_Ya = file_tkY.read().strip()
    with open('number_of _photos.txt', 'r') as file_num:
        numb = file_num.read().strip()
    with open('ID_VK.txt', 'r') as file_id:
        id_vk = file_id.read().strip()

    name_Folder = 'Photos'
    if not os.path.exists(name_Folder):
        os.makedirs(name_Folder)

    vk_id = BackupCopyPhoto(token)
    uploader = YaUploader(token_Ya)
    uploader.create_folder(name_Folder)
    list_photo = []

    for i in tqdm(range(len(vk_id.catch_json(numb, id_vk)
                            ['response']['items']))):
        result = vk_id.loader_large_photo(i)
        path_to_file = result[0]
        file_name = path_to_file
        list_photo.append(result[1])
        uploader.upload(path_to_file, file_name)
        time.sleep(0.33)

    dict_jso = {'file_photo': list_photo}
    with open('photos.json', 'a', encoding='utf-8') as outfile:
        json.dump(dict_jso, outfile,  ensure_ascii=False, indent=2)

    print('Success')
