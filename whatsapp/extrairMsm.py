import time

from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ExtrairMsm():

    def __init__(self):
        pass

    def conexao(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://web.whatsapp.com/')
        WebDriverWait(self.driver, 10000000000000).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[4]/header/div[1]/div')))
        return True

    def receberMensagem(self):
        conect=WebDriverWait(self.driver, 10000000000000).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[4]/header/div[1]/div')))


        if conect:
            while True:

                container=WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g0rxnol2._3fGK2')))
                users=container.find_elements(By.CSS_SELECTOR, 'div.lhggkp7q.ln8gz9je.rx9719la')
                for user in users:
                    try:
                        if 'não' in user.find_element(By.CLASS_NAME, 'aumms1qt').get_attribute('aria-label'):
                            msm=user.find_element(By.CLASS_NAME, 'vQ0w7').text
                            remetente=user.find_element(By.CLASS_NAME, '_21S-L').text
                            user.click()
                            WebDriverWait(self.driver, 100).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'kiiy14zj')))
                            menu=self.driver.find_element(By.CLASS_NAME, 'kiiy14zj')
                            menu.click()
                            WebDriverWait(self.driver, 100).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.iWqod._1MZM5._2BNs3' )))
                            time.sleep(0.1)

                            sair_conversa=self.driver.find_elements(By.CSS_SELECTOR, 'li.jScby.Iaqxu.FCS6Q')
                            for sair in sair_conversa:
                                if 'Fechar conversa' in sair.text:
                                    sair.click()
                                    break



                            return remetente, msm
                    except:
                        pass
                return False

    def formatar_numero_telefone(self, numero):
        numero = numero.replace('-', '').replace('+', '').replace(' ', '')  # Remove hífen, sinal de mais e espaços
        if not numero.startswith('55'):
            numero = '55' + numero  # Adiciona "55" no início se necessário
        return numero




                        



