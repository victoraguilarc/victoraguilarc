import feedparser
import os
import base64
import re

from datetime import datetime
from github import Github, GithubException

RSS_URL = 'htpps://vico.dev/rss'
POST_LIMIT = 3
TIME_FORMAT = '%a, %d %b %Y %H:%M:%S %Z'  # e.g. Thu, 29 Oct 2020 16:10:42 GMT

START_BLOG_SECTION = '<!--START_SECTION:blog-->'
END_BLOG_SECTION = '<!--END_SECTION:blog-->'

# github_repo = os.getenv('GITHUB_REPOSITORY') 
# github_token = os.getenv('USER_GITHUB_TOKEN')

github_repo = 'victoraguilarc/victoraguilarc' 
github_token = 'dca33446fa5f04b43c8608e977c5f798336840b1'

blog_pattern = f'{START_BLOG_SECTION}[\\s\\S]+{END_BLOG_SECTION}'
commit_message = '[update] Blog Posts'


def decode_readme(data) -> str:
  decoded_bytes = base64.b64decode(data)
  return str(decoded_bytes, 'utf-8')


if __name__ == '__main__':
  github = Github(github_token)
  try:
    repo = github.get_repo(github_repo)
  except GithubException:
    print('Github Authentication Error')
    sys.exit(1)
  
  readme_content = repo.get_readme()
  old_readme = decode_readme(readme_content.content)
  