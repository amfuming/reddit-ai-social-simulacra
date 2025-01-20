import logging
import random
import time
from utils.helper import load_accounts, get_reddit_client, subreddit_valid, get_random_post, save_comment
from utils.constant import generate_comment
from utils.vote import vote_comment

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

with open("accounts.json") as f:
    accounts = load_accounts()

def generate_comments():
    account = random.choice(accounts)
    logger.info(f"Select Comment Account : {account['username']}")

    reddit = get_reddit_client(account)

    if not reddit:
        logger.error(f"Skipping account {account['username']} due to failed authentication.")
    
    logger.info(f"Logged in as: {reddit.user.me()}")

    subreddit = random.choice(account["subreddits"])

    if not subreddit_valid(reddit, subreddit):
        logger.error(f"Skipping comment: Subreddit '{subreddit}' is invalid or inaccessible.")

    comment_data = get_random_post()
    submission = reddit.submission(id=comment_data["post_id"])    
    comment_content = generate_comment(account["prompt"], submission.selftext)
    
    try:
        create_comment(submission, comment_content, account, comment_data["post_id"])
          
    except Exception as e:
         logger.error(f"Error commenting on post: {e}")

def create_comment(submission, content, account, post_id):
    try:
        comment = submission.reply(content)
        save_comment(account["username"], comment.id, post_id)
        vote_comment(comment)
        time.sleep(random.randint(10 * 60, 11 * 60))

    except Exception as e:
                logger.error(f"Error commenting on post: {e}")