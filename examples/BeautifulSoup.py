import requests
from bs4 import BeautifulSoup

# example of post url
url = 'https://www.instagram.com/p/B-uyBVRpWe2/'


def get_post_description(post_url):
    html = requests.get(post_url).text

    # parsing html with beautiful soup in order to get post description
    parser = BeautifulSoup(html, 'html.parser')
    full_text = parser.title.text.strip()

    return full_text[full_text.index(':') + 2:]


if __name__ == '__main__':
    print(get_post_description(url))
