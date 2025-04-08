from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

# Caminho para o perfil do chrome que possui o Certificado Digital
profile_path = r"C:\\Users\\jvbra\\AppData\\Local\\Google\\Chrome\\User Data\\"
profile_name = "Profile 3"
path_folder_down = os.path.join(os.getcwd(), "arquivos")

# Caminho dinâmico para o driver
chromedriver_path = os.path.join(os.getcwd(), "driver", "chromedriver.exe")

# Define o driver a ser utilizado (tem que ser a mesma versão do chrome que estiver instalado na máquina)
# Pede logs mais detalhados
service = Service(
    executable_path=chromedriver_path,
    service_args=['--verbose'],
    log_path='chrome.log'
)


prefs = {
        "savefile.default_directory": f'{path_folder_down}',
        "download.default_directory": f'{path_folder_down}',
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "download.extensions_to_open": "applications/pdf",
        "plugins.always_open_pdf_externally": True,
        "safebrowsing.enabled": True
    }

chrome_options = webdriver.ChromeOptions()

# Por enquanto o uso de um perfil específico, que possui o Certificado Digital, não faz muita diferença
# pois o CAPTCHA está antes da confirmação do Certificado.
chrome_options.add_argument(f"--user-data-dir={profile_path}")  # Pasta base do perfil
chrome_options.add_argument(f"--profile-directory={profile_name}") # Subpasta do perfil

chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']) # Esconde o aviso de automação
chrome_options.add_argument('--kiosk-printing') # Auxilia a salvar documentos de acordo com as prefs
chrome_options.add_argument("--start-maximized") # Inicializa a janela do chrome já maximizada
chrome_options.add_argument("--no-sandbox") # Desativa o sandbox do Chrome (necessário em alguns ambientes restritos)
chrome_options.add_argument("--disable-dev-shm-usage") # Previne problemas de memória compartilhada em sistemas Linux/containers
chrome_options.add_argument("--remote-debugging-port=9222")  # Força uma porta fixa para depuração (evita conflitos aleatórios)
chrome_options.add_argument("--disable-gpu") # Desativa aceleração por GPU (útil para prevenir crashes em máquinas virtuais)
chrome_options.add_argument("--disable-software-rasterizer") # Desativa rasterização por software (otimização de performance)
chrome_options.add_argument("--disable-features=VizDisplayCompositor") # Desativa feature experimental que pode causar instabilidade
chrome_options.add_argument("--no-default-browser-check") # Ignora verificação se Chrome é navegador padrão (ganho de velocidade)


# Inicialização segura
try:
    # Inicializa o driver usando as opções definidas
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://det.sit.trabalho.gov.br/")

    # Aguarda o elemento aparecer na tela
    entrar_gov = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="botao"]'))
    )

    # Click no botão "Entrar com gov.br"
    entrar_gov.click()

    login_certificado_digital = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="login-certificate"]'))
    )

    login_certificado_digital.click()

    # Pausa para resolver CAPTCHA manualmente
    try:
        # Click em OK na escolha do certificado.
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()
    except TimeoutException:
        input("Resolva o CAPTCHA manualmente e pressione Enter.")

    time.sleep(5)

except Exception as e:
    print(f"Erro crítico: {str(e)}")
finally:
    if 'driver' in locals():
        driver.quit()