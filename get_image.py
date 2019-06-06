import os
import traceback
from datetime import datetime

import requests
from lxml import html
import logging

log_folder = '{}/logs'.format(os.getcwd())
if not os.path.exists(log_folder):
    os.mkdir(log_folder)
logging.basicConfig(filename='{log_folder}/Image_{date}.log'.format(log_folder=log_folder, date=datetime.now().date()),
                    level=logging.DEBUG)


class Image:
    """
    this class crawls random images from xkcd website after some given time
    """

    def __init__(self):
        self.retry = 1
        pass

    def get_image(self):
        try:
            response = requests.get('https://c.xkcd.com/random/comic/')
            tree = html.fromstring(response.content)
            image_src = tree.xpath('//*[@id="comic"]/img/@src')
            image_name = image_src[0].split('/')[-1]
            image_url = 'http:{}'.format(image_src[0])
            image_response = requests.get(image_url)

            if image_response.status_code in [200]:
                image_content = image_response.content
                Image().store_image(image_name, image_content)
            elif self.retry <= 3:
                self.retry += 1
                logging.info('retrying {} times'.format(self.retry))
                self.get_image()
        except Exception as err:
            logging.error('image downloading failed after {} retry with error: {}'.format(self.retry, str(err)))
            traceback.print_tb(err.__traceback__)

    @staticmethod
    def store_image(image_name, image_content):
        dir_path = os.getcwd()
        base_folder = '{}/Images'.format(dir_path)
        if not os.path.exists(base_folder):
            os.mkdir(base_folder)
        image_path = '{}/{}'.format(base_folder, image_name)
        with open(image_path, 'wb') as file:
            logging.info('writing image in file {}'.format(image_name))
            file.write(image_content)


if __name__ == "__main__":
    Image().get_image()
