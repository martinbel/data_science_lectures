import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

pd.set_option('display.max_columns', 100)

depto = 'https://departamento.mercadolibre.com.ar/MLA-762464986-departamento-alquiler-recoletaluminoso-dueno-directo-_JM'

def get_soup(depto):
    r = requests.get(depto)
    soup = BeautifulSoup(r.content)
    return soup

def remove_dots(s):
    s = re.sub(r"\.", "", s)
    if len(s) > 0:
        return int(s)
    else:
        return s

def remove_words(s):
    s = re.sub(r'[^0-9]+', '', s)
    if len(s) > 0:
        return int(s)
    else:
        return s

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

def get_neiborhood(soup):
    return soup.select(".map-location")[0].text

def get_depto(depto):
    drop_words_vars = ['Superficie total', 'Superficie cubierta']
    soup = get_soup(depto)
    price = get_price(soup)
    address = get_address(soup)
    depto = get_specs(soup)
    
    depto['price'] = price
    depto['address'] = address
    depto['neighborhood'] = get_neiborhood(soup)
    
    for key in drop_words_vars:
        depto[key] = remove_words(depto.get(key, ''))

    return depto


def flatten(l):
    return [item for sublist in l for item in sublist]


def get_dept_links(page):
    pag = get_soup(page)
    soup_links = pag.select("a.item__info-link")

    links = []
    for e in soup_links:
        links.append(e.attrs['href'])
    
    return links


def get_links_from_pages(base_page):
    pag = get_soup(base_page)
    q_results = remove_words(pag.select(".quantity-results")[0].text)
    pages = ["{}_Desde_{}".format(base_page, i) for i in range(51, q_results, 50)]
    
    alllinks = [get_dept_links(page) for page in pages]
    links = flatten(alllinks)
    return links


if __name__ == '__main__':
    # Iterate over the list of apartments
    groups = ['sin-dormitorios', '1-dormitorio', 
                  '2-dormitorio', '3-dormitorio', 
                  'mas-de-4-dormitorios']

    base_pages = ['https://inmuebles.mercadolibre.com.ar/departamentos/alquiler/{}/capital-federal'.format(g) for g in groups] 

    # Generate a list with each element to scrape
    links = flatten([get_links_from_pages(base_page) for base_page in base_pages])

    deptos = []
    for i, link in enumerate(links):
        if (i % 100) == 0:
            print("Iter: {}".format(i))
        try:
            deptos.append(get_depto(link))
        except:
            print(link)


    # Save a pandas data.frame with results
    df = pd.DataFrame(deptos)
    print(df.shape)
    df.to_csv('deptos.csv', index=False)
    print("Saved csv file")

