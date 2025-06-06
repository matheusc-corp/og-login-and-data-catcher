'''
Faz um projetinho aí em Python com selenium, qualquer coisa,
a ideia é fazer um login em um site a sua escolha, coletar
qualquer informação (mínimo 3 dados) e lançar em um Excel
'''

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from login_page import LoginPage
import time
import pandas as pd

if __name__ == '__main__':

    options = Options()
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-infobars')
    #options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=options)

    try:
        login_page = LoginPage(driver)
        login_page.open()

        login_page.login('username', 'password')

        dados = login_page.access_profile()

        if dados:
            df = pd.DataFrame([dados])
            df.to_excel('perfil_github.xlsx', index=False)
            print('Dados salvos com sucesso em perfil_github.xlsx')
        else:
            print('Falha na coleta de dados do perfil')

        time.sleep(5)

    finally:
        driver.quit()
