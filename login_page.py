from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://github.com/'

        # Get the login button on the main page
        self.btn_login = (
            By.XPATH,
            #"//a[contains(@href, '/login') and (normalize-space(text())='Sign in' or contains(@href, '/login') and normalize-space(text())='Entrar')]"
            "//a[@href='/login']"
        )

        # Get the fields on the login page
        self.username = (By.ID, 'login_field')
        self.password = (By.ID, 'password')
        self.btn_submit_credentials = (By.NAME, 'commit')

        # Get the side menu and the 'Your profile' button
        self.btn_profile_menu = (
            By.XPATH,
            "//button[contains(@aria-label, 'user navigation') or contains(@aria-label, 'navegação do usuário')]"
            #"//button[contains(@aria-label, 'Open user navigation menu')]"
            #"//button[contains(@aria-label, normalize-space()='user navigation') or contains(@aria-label, 'navegação do usuário')]"
        )
        self.btn_your_profile = (By.XPATH, "//a[normalize-space()='Your profile' or normalize-space()='Seu perfil']")


        # Get the user data
        self.user_name = (By.XPATH, "//span[contains(@itemprop, 'name')]")
        self.user_additional_name = (By.XPATH, "//span[contains(@itemprop, 'additionalName')]")
        self.user_title = (By.XPATH, "//div[contains(@class, 'user-profile-bio")
        self.user_followers = (By.XPATH, "//a[contains(@href,'followers')]/span")
        self.user_following = (By.XPATH, "//a[contains(@href,'following')]/span")

    def open(self):
        self.driver.get(self.url)
        print(f'Site {self.url} acessado com sucesso')

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.btn_login)
            ).click()
            print('Botão "Fazer login" clicado com sucesso.')
        except Exception as e:
            print('Erro ao tentar clicar no botão de login:', e)


    def login(self, username, password):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.username)
            ).send_keys(username)
            self.driver.find_element(*self.password).send_keys(password)

            time.sleep(1)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.btn_submit_credentials)
            ).click()
        except Exception as e:
            print('Falha ao fazer login: ', e)

    def access_profile(self):
        try:
            time.sleep(3)
            menu_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.btn_profile_menu)
            )

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of(menu_btn)
            )

            try:
                menu_btn.click()
            except:
                # Try access the side menu with javascript
                self.driver.execute_script("arguments[0].click();", menu_btn)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.btn_your_profile)
            ).click()

            name = self._get_text_safe(self.user_name)
            username = self._get_text_safe(self.user_additional_name)
            title = self._get_text_safe(self.user_title)
            followers = self._get_text_safe(self.user_followers)
            following = self._get_text_safe(self.user_following)

            return {
                'Nome': name,
                'Username': username,
                'Titulo': title,
                'Seguidores': followers,
                'Seguindo': following
            }
        except Exception as e:
            print(f'Falha ao acessar perfil: {e}')
            return None

    def _get_text_safe(self, locator):
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(locator)
            )
            text = element.text.strip()
            return text if text else "(vazio)"
        except:
            return "(não encontrado)"

