import random
import logging
import time

from utils.helper import load_accounts, get_reddit_client, subreddit_valid, save_post, get_flairs
from utils.constant import generate_post_content, generate_post_title
from utils.vote import vote_post

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

with open("accounts.json") as f:
    accounts = load_accounts()

def generate_posts():
    account = random.choice(accounts)
    logger.info(f"Select Account : {account['username']}")
    
    reddit = get_reddit_client(account)
    
    if not reddit:
        logger.error(f"Skipping account {account['username']} due to failed authentication.")
    
    subreddit = random.choice(account["subreddits"])

    logger.info(f"Logged in as: Username:{reddit.user.me()}, Subreddit:{subreddit}")

    if not subreddit_valid(reddit, subreddit):
        logger.error(f"Skipping post: Subreddit '{subreddit}' is invalid or inaccessible.")

    post_content= generate_post_content(account["prompt"], subreddit) 
    post_title= generate_post_title(post_content)

    try:
        create_post(reddit, account, subreddit, post_title, post_content)
        
    except Exception as e:
        print(f"Error creating post: {e}")

def create_post(reddit, account, subreddit_name, title, content):
    try:
        subreddit = reddit.subreddit(subreddit_name)
     
        post = subreddit.submit(title = title, selftext = content)
        save_post(post.id ,account["username"], subreddit_name, title)
        vote_post(post)
        time.sleep(random.randint(100, 200))

    except Exception as e:
        logger.error(f"Error posting to subreddit: {e}")