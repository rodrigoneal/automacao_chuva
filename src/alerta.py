from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


from src.elemento import Elemento


bairros = [
    "Irajá",
    "Madureira",
    "Bangu",
    "Campo Grande",
    "Av. Brasil/Mendanha",
    "Santa Cruz",
]


def pegar_clima() -> List[Elemento]:
    """
    Faz o crawler  no site do alerta rio e pega os dados do local e da chuva.
    Returns:
        List[Elemento]: List com os elementos.
    """
    options = Options()
    options.headless = True
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://alertario.rio.rj.gov.br/tabela-de-dados/")
    frame = driver.find_element(By.XPATH, '//*[@id="post-240"]/div/iframe')
    driver.switch_to.frame(frame)
    tables_rows = driver.find_element(By.XPATH, "/html/body/table[1]").find_elements(
        By.TAG_NAME, "tr"
    )
    elementos = []
    for table in tables_rows:
        try:
            hora = table.find_element(By.XPATH, ".//td[3]").text.strip()
            bairro = table.find_element(By.XPATH, ".//td[2]").text.strip()
            if bairro in bairros:
                local = bairro
                chuva = table.find_element(By.XPATH, ".//td[5]").text.strip()
                elementos.append(Elemento(local, hora, chuva))
        except NoSuchElementException:
            pass
    return elementos
