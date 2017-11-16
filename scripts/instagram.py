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
    user_details = instagram.get_user_details(INSTAGRAM_ACCOUNT)
    posts = instagram.query_media_gen(user_details)
    num_posts = 0
    for post in posts:
        caption = post['edge_media_to_caption']['edges'][0]['node']['text']
        english_name = getFirstHashtag(caption)
        likes = post['edge_media_preview_like']['count']
        comments = post['edge_media_to_comment']['count']
        thumbnail = post['thumbnail_resources'][0]
        result[english_name] = {
          'likes': likes,
          'num_comments': comments,
          'images': {
              'thumbnail': {
                  'url': thumbnail['src'],
                  'width': thumbnail['config_width'],
                  'height': thumbnail['config_height']
              }
          }
        }
        num_posts += 1
        # print('%s %d' % (getFirstHashtag(caption), likes))

    print('%d instagram posts' % num_posts)

    return result
