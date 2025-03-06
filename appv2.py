import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from yt_downloader import download_audio  # Importa a função do módulo yt_downloader
import os

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")

wait = WebDriverWait(driver, 100)
print('Abrindo o Whatsapp.....')

try:
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Scan this QR code to link a device!']"))
    )
    time.sleep(1)
    print("Escaneie o QR Code para fazer login no WhatsApp Web.")
except Exception as e:
    print(f"Erro ao carregar o WhatsApp Web: {e}")
    driver.quit()
    exit()

time.sleep(9)
contact_name = input("Digite o nome do contato ou grupo de onde buscar os links: ").strip()

try:
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='3']"))
    )
    search_box.click()
    search_box.send_keys(contact_name)
    print(f"Buscando pelo contato/grupo '{contact_name}'...")
except Exception as e:
    print(f"Erro ao localizar a barra de pesquisa: {e}")
    driver.quit()
    exit()

max_retries = 5
retry_delay = 5

retry_count = 0
contact_found = False

while retry_count < max_retries and not contact_found:
    try:
        contact = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//span[@title='{contact_name}']"))
        )
        contact.click()
        print(f"Conversa com '{contact_name}' aberta.")
        contact_found = True
    except Exception as e:
        retry_count += 1
        print(f"Tentativa {retry_count} falhou ao abrir a conversa com '{contact_name}': {e}")
        if retry_count < max_retries:
            print(f"Aguardando {retry_delay} segundos antes de tentar novamente...")
            time.sleep(retry_delay)
        else:
            print(f"Erro persistente: não foi possível abrir a conversa com '{contact_name}' após {max_retries} tentativas.")
            driver.quit()
            exit()

print('Carregando mensagens....')
print("Se quer esperar mais mensagens carregarem, aperte 'Enter' quando quiser prosseguir.")
input('')
print('Prosseguindo...')

try:
    messages = driver.find_elements(By.XPATH, "//a[@href]")
    links = [msg.get_attribute("href") for msg in messages]
    print(f"Links encontrados na conversa '{contact_name}':")
    for link in links:
        print(link)
except Exception as e:
    print(f"Erro ao buscar links na conversa: {e}")

print(f"Essas são as Urls: {links}. Para continuar, aperte Enter")
while True:
    link = input(">> ")
    if not link:
        break
    links.append(link)

if not links:
    print("Nenhuma URL fornecida. Encerrando o programa.")
    exit()

print("Aperte 'Enter' para fazer o download:")
destination = './downloads'

for link in links:
    download_audio(link)  # Usa a função yt_dlp para baixar o áudio

folder_path = "./downloads"

if not os.path.isdir(folder_path):
    print(f"Pasta '{folder_path}' não encontrada!")
    driver.quit()
    exit()

# files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]

# clip_icon = driver.find_element(By.CSS_SELECTOR, "span[data-icon='plus']")

# for file_path in files:
#     if os.path.isfile(file_path):
#         absolute_file_path = os.path.abspath(file_path)
#         print(f"Enviando arquivo: {file_path}")
#         clip_icon.click()
#         time.sleep(1)

#         file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
#         time.sleep(1)
#         file_input.send_keys(absolute_file_path)
#         time.sleep(1)

#         send_button = driver.find_element(By.CSS_SELECTOR, "span[data-icon='send']")
#         send_button.click()
#         time.sleep(5)

# print("Todos os arquivos foram enviados.")

profile_button = driver.find_element(By.XPATH, "//span[@data-icon='menu']")
profile_button.click()

time.sleep(1)

logout_button = driver.find_element(By.XPATH, "//div[@aria-label='Log out']")
logout_button.click()

time.sleep(1)

second_button = driver.find_element(By.XPATH, "(//div[@aria-label='Log out?']//button)[last()]")
second_button.click()

time.sleep(8)

driver.quit()
