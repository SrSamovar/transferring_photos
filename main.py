import requests
from datetime import datetime
from tqdm import tqdm
import json


vk_id = int(input('Введите vk_id: '))
vk_token = str(input('Введите vk_token: '))
y_token = str(input('Введите y_token: '))


class vk():
    url_vk = 'https://api.vk.com/method'
    url_y = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, vk_token, vk_id, y_token ):
        self.vk_token = vk_token
        self.vk_id = vk_id
        self.y_token = y_token

    

    def get_photos(self, count=5):
        url_vk = 'https://api.vk.com/method'
        params = {
            'access_token': self.vk_token,
            'owner_id': self.vk_id,
            'album_id': 'profile',
            'rev': 0, 
            'extended': 1,
            'photo_sizes': 0,
            'count': count,
            'v': '5.199'
        }    
        response = requests.get(f'{url_vk}/photos.get', params=params )
        info = response.json()
        photos = info['response']['items']
        photo_info = []
        json_info = []
        for photo in photos:
            max_photo_size = max(photo['sizes'], key=lambda x: x['width'] * x['height'])
            likes = photo['likes']['count']
            date = datetime.utcfromtimestamp(photo["date"]).strftime('%Y-%m-%d_%H-%M-%S')
            photo_info.append({'url': max_photo_size['url'], 'likes': likes, 'date': date})
            json_info.append({'file_name': f'{likes}.jpg', 'size': max_photo_size['type']})
            with open('photos_info.json', 'w', ) as f:
                json.dump(json_info, f, sort_keys=True, indent=4)
        return photo_info
    

    def put_image(self):
        url_y = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Authorization': f'OAuth {self.y_token}'
        }
        params = {
            'path': 'image'
        }
        response = requests.put(url_y, params=params, headers=headers)
        info = response.json()
        return info
    

    def post_photos(self, photos):
        url_y = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        for photo in tqdm(photos, desc='Uploading photos'):
            file_name = f"{photo['likes']}_{photo['date']}.jpg"
            headers = {
                'Authorization': self.y_token
            }
            params = {
                'path': f'image/{file_name}',
                'url': photo['url']
            }
            response = requests.post(url_y, params=params, headers=headers)
            info = response.json()
        return f"Фотографии загружены на ваш Яндекс Диск. Файл с фотографиями сохранен под названием 'photos_info.json'."
    
    



if __name__ == "__main__":
    vk_client = vk(vk_token, vk_id, y_token)
    image = vk_client.put_image()
    photos = vk_client.get_photos()
    post = vk_client.post_photos(photos)
    print(image, post)