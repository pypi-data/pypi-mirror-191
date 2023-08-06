import requests
import io
from PIL import Image
from neurocore_worker.transliter import translit_car_number
from traceback import format_exc


class NeuroCoreWorker:
    def __init__(self, api_login, api_password,
                 plate_frame_size: tuple = None):
        self.api_login = api_login
        self.api_password = api_password
        self.plate_frame_size = plate_frame_size

    def get_car_number(self, photo):
        photo = self.cut_photo(photo, self.plate_frame_size)
        response = self.make_request_for_plate(
            url='https://dispatcher.ml.neuro-vision.tech/1.4/predict/'
                'car_plate_gpu',
            photo=photo,
            login=self.api_login,
            password=self.api_password
        )
        if 'error' in response:
            return response
        number = self.parse_recognition_result(response.json())
        if 'error' in number:
            return number
        number = translit_car_number(number)
        return {'number': number, 'photo': photo}

    def make_request_for_plate(self, url, photo, login, password, timeout=5):
        try:
            response = requests.post(
                url,
                files={'images': ('image.jpg', photo, 'image/jpeg')},
                auth=(login, password),
                timeout=timeout)
        except requests.exceptions.ReadTimeout:
            response = {'error': 'Neurocore service read time out',
                        'info': f'Neurocore service read time out for {timeout} sec.'}
        except requests.exceptions.ConnectionError:
            response = {'error': 'Neurocore service is not avialable',
                        'info': format_exc()}
        return response

    def parse_recognition_result(self, response):
        try:
            if response['results'][0]['status'] == 'Success':
                return response['results'][0]['plate']
            else:
                return {'error': 'NeuroCore error',
                        'info': response['results'][0]['status']}
        except:
            return {'error': 'Response parsing error', 'info': format_exc(),
                    'source': response}

    def cut_photo(self, photo, size):
        if not size:
            return photo
        img = Image.open(io.BytesIO(photo))
        # left, upper, right, lower
        # 2592*1944
        im_r = img.crop(size)
        img_byte_arr = io.BytesIO()
        im_r.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr
