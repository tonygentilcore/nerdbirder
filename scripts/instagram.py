import sys

# Monkey-patch multiprocessing prior to importing "instagram_scraper" in order
# to let it run on GAE.
import dummy_multiprocessing
sys.modules['multiprocessing'] = dummy_multiprocessing.DummyProcessing

import instagram_scraper

# Monkey-patch to avoid filesystem writes which aren't allowed on GAE.
import logging
@staticmethod
def get_stdout_logger(level=logging.DEBUG, verbose=0):
    logger = logging.getLogger(__name__)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter( logging.Formatter('%(levelname)s: %(message)s') )
    sh_lvls = [logging.ERROR, logging.WARNING, logging.INFO]
    sh.setLevel(sh_lvls[verbose])
    logger.addHandler(sh)

    return logger
instagram_scraper.InstagramScraper.get_logger = get_stdout_logger

INSTAGRAM_ACCOUNT = 'nerdbirder'

def getFirstHashtag(caption):
    return caption.split('#')[1].split()[0]

def getPostsByEnglishName():
    result = {}
    instagram = instagram_scraper.InstagramScraper()
    posts = instagram.media_gen(INSTAGRAM_ACCOUNT)
    num_posts = 0
    for post in posts:
        caption = post['caption']['text']
        english_name = getFirstHashtag(caption)
        images = post['images']
        likes = post['likes']['count']
        result[english_name] = {
          'likes': likes,
          'num_comments': post['comments']['count'],
          'images': images
        }
        num_posts += 1
        # print('%s %d' % (getFirstHashtag(caption), likes))

    print('%d instagram posts' % num_posts)

    return result
