from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as keys
from time import sleep
from openpyxl import Workbook


browser = webdriver.Chrome()
#link para o linkedIn
browser.get('https://www.linkedin.com/login/pt')
sleep(2)
email = input('Qual é seu E-mail: ')
browser.find_element(By.XPATH, '//*[@id="username"]').send_keys(email)
senha = input('Qual é sua Senha: ')
browser.find_element(By.XPATH, '//*[@id="password"]').send_keys(senha)
btn_enter = browser.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
sleep(2)
btn_enter.click()
sleep(4)
x = input("Pausa, fazer a verificação")
browser.find_element(By.XPATH, '//*[@id="global-nav"]/div/nav/ul/li[3]/a').click()
sleep(8)
browser.find_element(By.XPATH, '/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]').send_keys('estagio ti', keys.ENTER)
sleep(4)
ul_element = browser.find_element(By.CSS_SELECTOR, "main div.jobs-search-results-list")
sleep(5)


def scroll_list(pixels):
    browser.execute_script(f"arguments[0].scrollTop += {pixels};", ul_element)
    sleep(2)


titulo_da_vaga = []
links = []
descricoes = []

for i in range(1, 26):
    scroll_list(100)
    nome_vaga_link = browser.find_element(By.XPATH, f"/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[{i}]/div/div")
    nome_vaga_link.click()
    link_vaga = browser.find_elements(By.XPATH, f"//main//div/div//ul//li[{i}]//a[@data-control-id]")  
    descricoes_vagas = browser.find_elements(By.XPATH, "//*[@id='job-details']/div")
    for texto in descricoes_vagas:
        descricoes.append(texto.text)
        break
    for link in link_vaga:
        links.append(link.get_attribute("href"))
        break
    print(f"Descrições > {len(descricoes)}")
    print(f"Links das vagas > {len(links)}")
    titulo_da_vaga.append(nome_vaga_link)
    print(f"Titulo_da_vaga > {len(titulo_da_vaga)}")
    if len(titulo_da_vaga) >= 25:
        print(f'chegamos ao numero esperado de {len(titulo_da_vaga)}')
        break


spreadsheet = Workbook()

sheet = spreadsheet.active

sheet['A1'] = "NOME DA VAGA"
sheet['B1'] = "LINK DA VAGA"
sheet['C1'] = "DESCRIÇÃO DA VAGA"
ponto = 0
next_line = sheet.max_row + 1


for link in titulo_da_vaga:
    text = link.text
    
    sheet[f'A{next_line}'] = text
    sheet[f'B{next_line}'] = links[ponto]
    sheet[f'C{next_line}'] = descricoes[ponto]

    ponto +=1
    next_line += 1
        
spreadsheet.save("vagas_links_estagio_ti(2).xlsx")
print("planilha criada")

print("Encerrando busca")
sleep(3)
browser.quit()