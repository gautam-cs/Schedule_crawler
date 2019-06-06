from apscheduler.schedulers.blocking import BlockingScheduler

from get_image import Image


def get_memes_imag():
    """
    it calls the method defined for scrabing image from given website
    :return:
    """
    Image().get_image()


scheduler = BlockingScheduler()
scheduler.add_job(get_memes_imag, 'interval', minutes=0.2)
scheduler.start()
