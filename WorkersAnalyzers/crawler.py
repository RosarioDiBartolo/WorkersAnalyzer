import os
import time
from datetime import datetime

import requests
import bs4



base = 'https://sportellodipendenti.policlinico.unict.it/gp4web'
mese = "DICEMBRE"
anno = "2024"
mail = 'silvana.mangione@policlinico.unict.it'
dashboard_suf = '/common/Main.do'
login_suf = '/restrict/index.do?MVTD=Login'
login_url =  base  + login_suf
dashboard =  base + dashboard_suf

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://sportellodipendenti.policlinico.unict.it/gp4web/common/Main.do?',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

print(dashboard)


today = datetime.now()
today_year = today.year
today_month = today.month


def validDate(date: datetime) -> bool:
    return date.year > today_year or date.month > today_month


def login(username, password):
    with requests.session() as session:
        #set browser headers
        session.headers.update( headers)
        #The requests must follow this exact order
        session.get(dashboard)

        #The requests must follow this exact order
        session.get(
            login_url
        )

        old = session.cookies.get("JSESSIONID")

        data = {
            'j_username': username,
            'j_password': password,
            'Login': '  Login  ',
        }


        #The requests must follow this exact order
        log = session.post(
            'https://sportellodipendenti.policlinico.unict.it/gp4web/restrict/j_security_check',
            data = data,
        )

        new = session.cookies.get("JSESSIONID")



        if old == new:
            raise Exception(f"Login was not successfull... {username} and {password}")


        home = session.get(dashboard)

        soup = bs4.BeautifulSoup(home.text, "html.parser")

        user = soup.select_one(".AFCHeaderWelcome b").text.split()[0]
        print(user, username)
        if username != user:
            raise Exception(f"Login failed...")
    return session

def crawl(session, anno, mese, username):
    anno = str(anno)
    if not validDate(datetime(day=0, month=mese, year=anno ) ):
        raise Exception(f"Invalid date...")

    conferma = session.post(    'https://sportellodipendenti.policlinico.unict.it/gp4web/ss/CedolinoRichiestaConferma.do?ccsForm=Appoggio:Edit',data = {
        'anno': anno,
        'par': mese[:3],
        'ci': username,
        'CODICE_MENSILITA': mese[:3],
        'INVIO_TELEMATICO': '1',
        'E_MAIL': mail,
        'Button_Update': 'Conferma Richiesta',
    }
     )


    for i in range(3):
        cedolini = session.get("https://sportellodipendenti.policlinico.unict.it/gp4web/ss/CedolinoRichiesta.do?")
        s = bs4.BeautifulSoup(cedolini.text, "html.parser")
        interested_link = s.select("a.AFCLink")[1]
        words = interested_link.get('title').split()
        month = words[1]
        year = words[3]
        if mese == month and year == anno:
            print("Cedolino Richiesta trovato")
            return session.post("https://sportellodipendenti.policlinico.unict.it/gp4web/ss/UploadDownload",
                                data={"dataSource": "jdbc/gp4web", "functionName": "verify_ci",
                                      "p1": "\'CEDOLINO_RICHIESTO\'", "p2": username})

        time.sleep(10)

    raise Exception(f"Nessun file trovati per il seguente anno e mese: {anno}-{mese}           {words}")



if __name__ == '__main__':
    session = login("30105", "cespiti")
    print(session)
