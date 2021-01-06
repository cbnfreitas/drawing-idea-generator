import time
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup

MAX_RESULTS = 100
GOOGLE_URL = "https://www.google.com.br"

# Initial version
# SAO_JOSE_DOS_CAMPOS = "uule=w+CAIQICItU2FvIEpvc2UgZG9zIENhbXBvcyxTdGF0ZSBvZiBTYW8gUGF1bG8sQnJhemls&cr=countryBR"

# SAO_JOSE_DOS_CAMPOS = "ie=UTF-8&oe=UTF-8&ip=0.0.0.0&noj=1&nomo=1&nota=1&igu=1&tci=g:1001772,p:30000&glp=1&uule=w+CAIQICItU2FvIEpvc2UgZG9zIENhbXBvcyxTdGF0ZSBvZiBTYW8gUGF1bG8sQnJhemls&cr=countryBR"
# BRASIL = "hl=pt-BR&lr=lang_pt-BR"

SAO_JOSE_DOS_CAMPOS = "gl=br&ie=UTF-8&oe=UTF-8&hl=pt-BR&ip=0.0.0.0&noj=1&nomo=1&nota=1&igu=1&tci=g:1001772,p:30000&glp=1&uule=w+CAIQICItU2FvIEpvc2UgZG9zIENhbXBvcyxTdGF0ZSBvZiBTYW8gUGF1bG8sQnJhemls"
BRASIL = "gl=br"

#    hl=pt-BR&gl=br

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def scraper(terms: str, url_to_find: str, isCity: bool):

    terms_plus = terms.replace(" ", "+")

    if isCity:
        GEO = SAO_JOSE_DOS_CAMPOS
    else:
        GEO = BRASIL

    url = f"{GOOGLE_URL}/search?q={terms_plus}&num={MAX_RESULTS}&{GEO}"

    print(url)

    start = time.time()
    time.sleep(10.0)
    response = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(response.content, "lxml", from_encoding="UTF-8")

    h3s = soup.find_all('h3')
    links = [h3.parent['href'] if h3.parent.has_attr(
        'href') else 'Vídeos'for h3 in h3s]
    # end = time.time()

    # h3s = soup.find_all('h3')
    # if len(h3s) < MAX_RESULTS + 1:
    #     print(
    #         f'Foram encontrados { len(h3s) - 1 } resultados para essa pesquisa.')

    url_to_find = url_to_find.replace("https://", "")
    url_to_find = url_to_find.replace("http://", "")
    url_to_find = url_to_find.replace("www.", "")
    url_to_find = url_to_find.lower()
    url_to_find = url_to_find.replace(" ", "")
    if len(url_to_find) == 0:
        url_to_find = 'asasdasdjjntikeire'

    links = []
    index = 1
    for h3 in h3s:
        h3parent = h3.parent
        if h3parent.has_attr('href'):
            link = h3parent['href']
            link = unquote(link)
            link = link.lower()

            # print(link)

            found = link.count(url_to_find) > 0

            if index <= 10 or found:
                links.append({"index": index, "link": link})

            if found:
                print(f"Encontrei {url_to_find} na posição {index}")
                end = time.time()
                print(f"Total elapsed time: {end - start}")
                return {"contains": True, "rank": index, "links": links}

            index = index+1
        # else:
            # print('Outros')

    print(f"Não encontrei {url_to_find} nos resultados.")
    end = time.time()
    print(f"Total elapsed time: {end - start}")
    return {"contains": False, "rank": None, "links": links}
