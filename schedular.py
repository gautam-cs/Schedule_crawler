from apscheduler.schedulers.blocking import BlockingScheduler

from get_image import Image


def get_memes_imag():
    Image().get_image()


scheduler = BlockingScheduler()
scheduler.add_job(get_memes_imag, 'interval', minutes=0.1)
scheduler.start()
