import tweepy
import requests
import time
import logging
import schedule
import warnings
warnings.simplefilter("ignore", UserWarning)

logger = logging.getLogger('Logging')
logger.setLevel(10)

fh = logging.FileHandler('tweet.log')
logger.addHandler(fh)
formatter = logging.Formatter("%(asctime)s:%(lineno)d:%(levelname)s:%(message)s")
fh.setFormatter(formatter)
logger.info('Started.')

# Twitter API info
bt = ''
ck = ''
cs = ''
at = ''
ats = ''

client = tweepy.Client(bearer_token=bt, consumer_key=ck, consumer_secret=cs, access_token=at, access_token_secret=ats)

def translate_text(text):
    API_KEY = '' # Enter Deepl API Key

    source_lang = 'EN'
    target_lang = 'JA'

    params = {
                'auth_key' : API_KEY,
                'text' : text,
                'source_lang' : source_lang,
                "target_lang": target_lang
            }

    request = requests.post("https://api-free.deepl.com/v2/translate", data=params)
    result = request.json()

    translated_text = result['translations'][0]['text']
    
    return translated_text

def translate_tweets(user_id, last_tweet_id):

    UsersTweets = client.get_users_tweets(user_id, exclude='retweets', since_id=last_tweet_id, max_results=50)
    
    try:
        num_tw = len(UsersTweets[0])
        print(f'Number of Tweets: {num_tw}')

    except TypeError:
        logging.error('')

    else:
    
        for n in reversed(range(num_tw)):
            tw_id = UsersTweets[0][n]['id']
            if tw_id > last_tweet_id:
                pass
            tw = client.get_tweet(tw_id)
            original_txt = tw[0]['text']

            translated_text = translate_text(original_txt)
            print(f'=======================================')
            print(f'tweet id: {tw_id}')
            print(f'translated text: {translated_text}')

            logger.info(translated_text)

            time.sleep(5)

            last_tweet_id = tw_id

def main():
    user_id = 1652541
    last_tweet_id = 1617834670451826690
    schedule.every(5).minutes.do(translate_tweets(user_id, last_tweet_id))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
