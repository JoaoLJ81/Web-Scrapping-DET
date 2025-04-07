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

# Caminho dinâmico para o driver
chromedriver_path = os.path.join(os.getcwd(), "driver", "chromedriver.exe")

options = webdriver.ChromeOptions()

# Define o driver a ser utilizado (tem que ser a mesma versão do chrome que estiver instalado na máquina)
# Pede logs mais detalhados
service = Service(
    executable_path=chromedriver_path,
    service_args=['--verbose'],
    log_path='chrome.log'
)

options.add_argument(f"--user-data-dir={profile_path}")  # Pasta base do perfil
options.add_argument(f"--profile-directory={profile_name}") # Subpasta do perfil

options.add_argument("--no-sandbox") # Desativa o sandbox do Chrome (necessário em alguns ambientes restritos)
options.add_argument("--disable-dev-shm-usage") # Previne problemas de memória compartilhada em sistemas Linux/containers
options.add_argument("--remote-debugging-port=9222")  # Força uma porta fixa para depuração (evita conflitos aleatórios)
options.add_argument("--disable-gpu") # Desativa aceleração por GPU (útil para prevenir crashes em máquinas virtuais)
options.add_argument("--disable-software-rasterizer") # Desativa rasterização por software (otimização de performance)
options.add_argument("--disable-features=VizDisplayCompositor") # Desativa feature experimental que pode causar instabilidade
options.add_argument("--no-default-browser-check") # Ignora verificação se Chrome é navegador padrão (ganho de velocidade)
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Esconde o aviso de automação

# Inicialização segura
try:
    # Inicializa o driver usando as opções definidas
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://servicos.mte.gov.br/spme-v2/#/login")
    driver.maximize_window()

    # Aguarda o elemento aparecer na tela
    entrar_gov = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/div/div[1]/div/div/div/div[1]/div/div[3]/button'))
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