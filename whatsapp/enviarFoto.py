from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from banco_de_dados import IaraDB
iaraDB=IaraDB()
from selenium.webdriver.support import expected_conditions as EC
import time

class EnviarFoto:
    def __init__(self):
        self.driver = webdriver.Chrome('../chomedriver.exe')

    # Espera até que um elemento seja localizado no DOM dentro de um determinado tempo limite
    def wait_for_element(self, xpath, timeout):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def conexao(self, numero):
        self.driver.get(f'https://web.whatsapp.com/send?phone={numero}')
        WebDriverWait(self.driver, 10000000000000).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[4]/header/div[1]/div')))
        return True

    # Clica em um elemento localizado por XPath
    def click_element(self, xpath):
        element = self.wait_for_element(xpath, 10)
        element.click()

    # Envia teclas para um elemento localizado por XPath
    def send_keys_to_element(self, xpath, keys):
        element = self.wait_for_element(xpath, 10)
        element.send_keys(keys)

    # Exemplo de uso dos métodos acima
    def enviar_foto(self, caminho, numero):

        self.conexao(numero)

        footer_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div'
        input_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input'
        enviar_xpath = '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div'

        element = self.wait_for_element(footer_xpath, 20)
        self.click_element(footer_xpath)

        self.send_keys_to_element(input_xpath, caminho)
        time.sleep(0.6)

        self.click_element(enviar_xpath)
        time.sleep(3)

        mensagem = 'foto enviada'

    def send_menu(self, numero):

        try:
            self.enviar_foto('../arquivos/refeitorio/cardapio.png', numero)


        except:
            pass

    def enviar_horario(self, turma, numero):
        try:

            self.enviar_foto(f'../arquivos/horario/horario_aula/{turma}.png', numero)

        except:
            pass


