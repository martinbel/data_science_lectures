import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

depto = 'https://departamento.mercadolibre.com.ar/MLA-762464986-departamento-alquiler-recoletaluminoso-dueno-directo-_JM'

def get_soup(depto):
    r = requests.get(depto)
    soup = BeautifulSoup(r.content)
    return soup

def remove_dots(s):
    return re.sub(r"\.", "", s)

def remove_words(s):
    return re.sub(r'[^0-9]+', '', s)

def get_price(soup):
    precio = soup.select(".price-tag-fraction")[0].text
    return remove_dots(precio)

def get_address(soup):
    return soup.select(".map-address")[0].text

def get_specs(soup):
    specs = soup.select(".specs-item")
    depto = {}
    for e in specs:
        key = e.strong.text
        value = e.span.text
        depto[key] = value
    return depto

def get_depto(depto):
    soup = get_soup(depto)
    price = get_price(soup)
    address = get_address(soup)
    depto = get_specs(soup)
    depto['price'] = price
    depto['address'] = address

    for k in ['Superficie total', 'Superficie cubierta']:
        depto[k] = remove_words(depto[k])
    return depto

def get_dept_links(page):
    pag = get_soup(page)
    soup_links = pag.select("a.item__info-link")
    links = []
    for e in soup_links:
        links.append(e.attrs['href'])
    return links


page = "https://inmuebles.mercadolibre.com.ar/departamentos/capital-federal/departamento-alquiler"

links = get_dept_links(page)
deptos = []
for link in links:
    try:
        deptos.append(get_depto(link))
    except:
        print(link)

pd.set_option('display.max_columns', 100)
pd.DataFrame(deptos)
