import os
# import psutil
import traceback
from datetime import datetime

import requests
from lxml import html
import logging

from requests import ConnectTimeout, ReadTimeout

timeout = 60 * 1  # 1 minute

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
        """
        helps in getting random htmls of memes pages and extracting random image from it
        :return:
        """
        try:
            # process = psutil.Process(os.getpid())
            # process.wait(timeout=timeout)
            response = requests.get('https://c.xkcd.com/random/comic/', timeout=timeout)
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
        # except psutil.TimeoutExpired:
        #     logging.error('killing process due to timeout')
        #     process.kill()
        #     raise RuntimeError('Timeout')
        except ConnectTimeout:
            raise ConnectTimeout('Timeout exceeded')
        except ReadTimeout:
            raise ReadTimeout(' timeout error')
        except Exception as err:
            logging.error('image downloading failed after {} retry with error: {}'.format(self.retry, str(err)))
            traceback.print_tb(err.__traceback__)

    @staticmethod
    def store_image(image_name, image_content):
        """
        takes the image data and it stores it in some defined directory
        :param image_name:
        :param image_content:
        :return:
        """
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
