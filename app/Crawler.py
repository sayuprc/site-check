from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Crawler:

  def __init__(self):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    self.driver = webdriver.Chrome(options=options)

  def get_screenshot(self, url, file_name):
    self.driver.get(url)

    w = self.driver.execute_script('return document.body.scrollWidth;')
    h = self.driver.execute_script('return document.body.scrollHeight;')

    self.driver.set_window_size(w, h)

    self.driver.save_screenshot(file_name)

    self.driver.quit()