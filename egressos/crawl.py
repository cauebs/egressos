import csv
from itertools import count
from sys import argv
from typing import Optional

import requests
from bs4 import BeautifulSoup

URL = "https://egressos.sistemas.ufsc.br/listaEgressos.xhtml"

BASE_FORM_DATA = {
    "AJAXREQUEST": "_viewRoot",
    "javax.faces.ViewState": "j_id1",
    "j_id65": "j_id65",
    "j_id65:j_id84": "j_id65:j_id84",
}

PROGRAM_ID_KEY = "j_id65:selectCursosGraduacao"
PAGE_INDEX_KEY = "j_id65:formadosGraduacaoDataScroller"


def semester_to_year(s):
    y = int(s[:4])
    if s[4] != '1':
        y += 0.5
    return y


def crawl(program_id: Optional[int] = None):
    session = requests.Session()
    session.post(URL)

    form_data = BASE_FORM_DATA.copy()
    if program_id is not None:
        form_data[PROGRAM_ID_KEY] = str(program_id)

    previous = None
    for i in count(1):
        form_data[PAGE_INDEX_KEY] = str(i)
        response = session.post(URL, form_data)
        if response.text == previous:
            break
        print(i)

        soup = BeautifulSoup(response.text, "html5lib")

        for row in soup.find_all("tr", class_="rich-table-row"):
            cells = row.find_all("td")
            entry = [cell.get_text(strip=True) for cell in cells]
            entry[-2] = semester_to_year(entry[-2])
            entry[-1] = semester_to_year(entry[-1])
            yield entry[1:]

        previous = response.text


def run():
    try:
        program_id = int(argv[1])
    except IndexError:
        program_id = None

    with open(f"{program_id}.csv", "w") as f:
        csv.writer(f).writerows(crawl(program_id))
