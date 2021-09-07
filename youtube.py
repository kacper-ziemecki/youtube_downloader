from selenium import webdriver
import re
import pyautogui
import time


def wczytajLinkiJakoListe(nazwaPliku):
  plik = open(nazwaPliku, 'r')
  listaJakoPlik = plik.readlines()
  return listaJakoPlik

def otworzStroneInternetowa(url):
  strona = webdriver.Firefox()
  strona.get(url) 
  return strona

def wczytajWszystkieHref(listaWzorcow):
  listaWszystkichHref = []

  for element in listaWzorcow:
    wzorzec = r"href=\".*\"" 
    pasowanie = re.findall(wzorzec, element)
    if(pasowanie):
      for element in pasowanie:
        if(element not in listaWszystkichHref):
          listaWszystkichHref.append(element)

  return listaWszystkichHref

def wczytajUrl(listaHrefow):
  listaUrl = []
  for element in listaHrefow:
    urlElementu = element[7 : len(element) - 1] # href="/watch?v=XRVA5PMSKKE" --> watch?v=XRVA5PMSKKE
    if(len(urlElementu) == 19 and urlElementu[0 : 8] == 'watch?v='):
      listaUrl.append(urlElementu)

  dokonczonaListaUrl = []
  for element in listaUrl:
    dokonczonyElement = "https://www.youtube.com/" + element 
    dokonczonaListaUrl.append(dokonczonyElement)

  return dokonczonaListaUrl

def dodajNowaLiniaDoListy(lista):
  poprawionaLista = []
  for element in lista:
    poprawionyElement = element + '\n'
    poprawionaLista.append(poprawionyElement)

  return poprawionaLista

def napiszWszystkieNapisyZListy(lista):
  for napis in lista:
    for element in napis:
      time.sleep(0.02)
      pyautogui.typewrite(element)

def zakonczProgramy():
  pyautogui.moveTo(1920, -150, 0.5) # zamykanie yt downloader 
  pyautogui.click() 

  pyautogui.moveTo(1340, 17, 0.5) # zamykanie firefox
  pyautogui.click() 

def pliknijPrzyciskDownload():
  pyautogui.moveTo(1450, 120, 0.5) 
  pyautogui.click() 

def zakonczProgramyWOdpowiednimMomencie():
  ScreenShoot = pyautogui.screenshot()
  koordynatyDoPoprawnegoScreena = ()
  ScreenShoot.crop()

def pobierzFilmiki(listaUrl):
    pyautogui.press("winleft")
    time.sleep(1)
    pyautogui.typewrite("Youtube Multi Downloader")
    time.sleep(2)
    pyautogui.moveTo(62, 150, 2)
    pyautogui.click()
    time.sleep(1)
    listaUrl = dodajNowaLiniaDoListy(listaUrl) 
    listaUrl = listaUrl[0]
    napiszWszystkieNapisyZListy(listaUrl)
    input("\anaciśnij ENTER jeśli wpisałeś ścieżkę docelową")
    pliknijPrzyciskDownload()
    #zakonczProgramyWOdpowiednimMomencie()

def wczytajUrlFilmikowZeStrony(strona):
  elementyKlasyJakoKlasa = strona.find_elements_by_class_name("style-scope ytd-video-renderer")
  elementyIdJakoKlasa = strona.find_elements_by_id("video-title")
  elementyAJakoKlasa = strona.find_elements_by_tag_name('a')

  elementyKlasy = [element.get_attribute("outerHTML") for element in elementyKlasyJakoKlasa]
  elementyId = [element.get_attribute("outerHTML") for element in elementyIdJakoKlasa]
  elementyA = [element.get_attribute("outerHTML") for element in elementyAJakoKlasa]

  listaHref = []

  hrefElementowKlasy = wczytajWszystkieHref(elementyKlasy)
  for element in hrefElementowKlasy:
    listaHref.append(element)

  hrefElementowId = wczytajWszystkieHref(elementyId)
  for element in hrefElementowId:
    listaHref.append(element)

  hrefElementowA = wczytajWszystkieHref(elementyA)
  for element in hrefElementowA:
    listaHref.append(element)

  listaUrl = wczytajUrl(listaHref)

  pobierzFilmiki(listaUrl)

def main():
  listaStronInternetowych = wczytajLinkiJakoListe('kanaly.txt')
  for stronaInternetowa in listaStronInternetowych:
    stronaJakoKlasa = otworzStroneInternetowa(stronaInternetowa)
    wczytajUrlFilmikowZeStrony(stronaJakoKlasa)
    input("\nnaciśnij ENTER jeśli wszystkie filmiki pobrały się")
  
main()