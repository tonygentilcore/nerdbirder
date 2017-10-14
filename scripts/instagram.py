import instagram_scraper

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
