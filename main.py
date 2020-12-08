import feedparser
import os
import base64
import re

from datetime import datetime
from github import Github, GithubException


RSS_URL = 'https://vico.dev/rss'
POSTS_LIMIT = 3
DATETIME_FORMAT = '%a, %d %b %Y %H:%M:%S %Z'  # e.g. Thu, 29 Oct 2020 16:10:42 GMT

START_BLOG_SECTION = '<!--START_SECTION:blog-->'
END_BLOG_SECTION = '<!--END_SECTION:blog-->'

github_repo = os.getenv('GITHUB_REPOSITORY') 
github_token = os.getenv('USER_GITHUB_TOKEN')

blog_pattern = f'{START_BLOG_SECTION}[\\s\\S]+{END_BLOG_SECTION}'
commit_message = '[update] Blog Posts'

def get_last_posts():
  news_feed = feedparser.parse(RSS_URL)
  posts_block = ''

  for i in range(POSTS_LIMIT):
    post = news_feed.entries[i]
    post_date = datetime.strptime(f'{post.published}', DATETIME_FORMAT).strftime('%d %b %Y')
    posts_block += f'  - [{post.title}]({post.link}) - *{post_date}* \n'
  return posts_block

def decode_readme(data) -> str:
  decoded_bytes = base64.b64decode(data)
  return str(decoded_bytes, 'utf-8')

def generate_new_readme(old_readme: str):
  new_posts_block = f'{START_BLOG_SECTION}\n{get_last_posts()}{END_BLOG_SECTION}'
  return re.sub(blog_pattern, new_posts_block, old_readme)

if __name__ == '__main__':
    github = Github(github_token)
    try:
        repo = github.get_repo(github_repo)
    except GithubException:
        print('Github Authentication Error')
        sys.exit(1)
    readme_content = repo.get_readme()
    old_readme = decode_readme(readme_content.content)
    new_readme = generate_new_readme(old_readme)
    if new_readme != old_readme:
        repo.update_file(
          path=readme_content.path, message=commit_message, 
          content=new_readme, sha=readme_content.sha
        )