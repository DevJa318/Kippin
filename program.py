from bs4 import BeautifulSoup
import requests
import os

lista_do_popow = ['https://rs.maszyna.pl/~boberov/Kippin2/']
katalog_pobierania = "C:\\Twoj_katalog"

def wykaz_linkow_z_podstrony(url):
    """
    znajduje wszystkie linki z podanego linku
    """
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
     
    return soup.findAll('a')

def pobieranie_pliku(i):
    res = requests.get(i)
    plik = open(os.path.join(katalog_pobierania, i[31:]), 'wb')
    for chunk in res.iter_content(100000):
        plik.write(chunk)
    plik.close()

def pobierz_linki_i_pliki(znaczniki):
    pelne_linki = []
    for i in znaczniki[5:]:
        pelne_linki.append(url+i.get_text())
    
    for i in pelne_linki:
        if i.endswith('/'):
            res = requests.get(i)
            if res.text.startswith('<!DOCTYPE'):
                 lista_do_popow.append(i)
            else:
                pobieranie_pliku(i[:-1])
                print(i)
        else:
            pobieranie_pliku(i)

while lista_do_popow:
    url = lista_do_popow.pop()
    a = wykaz_linkow_z_podstrony(url)
    b = pobierz_linki_i_pliki(a)
    os.makedirs(katalog_pobierania + url[31:],exist_ok = True)

