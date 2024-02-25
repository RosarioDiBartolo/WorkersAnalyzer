import os
import requests
import bs4
base = 'https://sportellodipendenti.policlinico.unict.it/gp4web'

dashboard_suf = '/common/Main.do'
login_suf = '/restrict/index.do?MVTD=Login'
login =  base  + login_suf
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

def log_in(username, password):
    with requests.session() as session:

        #set browser headers
        session.headers.update( headers)

        #The requests must follow this exact order
        session.get(dashboard)


        #The requests must follow this exact order
        response = session.get(
            login
         )

        oldJSESSIONID = session.cookies.get_dict('JSESSIONID')


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


        if session.cookies.get('JSESSIONID') == oldJSESSIONID:
            print("Login failed")
        else:
            print("Login was succesfull")

        home = session.get(dashboard)

        s = bs4.BeautifulSoup(home.text, 'html.parser')
        print(s.select("tr.AFCHeaderTR > td:nth-child(3) font") )
        print( session.cookies)

    return session

log_in("30105", "cesti")