import time
from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from banco_de_dados import IaraDB
iaraDB=IaraDB()

class EnviarMsm:
    def  __init__(self):
        pass

    def conexao(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://web.whatsapp.com/')
        WebDriverWait(self.driver, 10000000000000).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[4]/header/div[1]/div')))
        return True

    def enviarMensagem(self, numero, msm):
        try:
            link = f'https://web.whatsapp.com/send?phone={numero}&text={msm}'
            self.driver.get(link)
            envio=WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))
            envio.click()
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'kiiy14zj')))
            menu = self.driver.find_element(By.CLASS_NAME, 'kiiy14zj')
            menu.click()
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.iWqod._1MZM5._2BNs3')))
            time.sleep(0.1)

            sair_conversa = self.driver.find_elements(By.CSS_SELECTOR, 'li.jScby.Iaqxu.FCS6Q')
            for sair in sair_conversa:
                if 'Fechar conversa' in sair.text:
                    sair.click()
                    break
        except:
            pass







