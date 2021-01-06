import requests


def get_meme(tag: str):

    tag = tag.replace(" ", "+")

    URL = f"https://api.giphy.com/v1/gifs/random?api_key=0UTRbFtkMxAplrohufYco5IY74U8hOes&tag={tag}&rating=pg-13"
    response = requests.get(URL)
    r = response.json()
    meme = r['data']['image_original_url']

    return meme
