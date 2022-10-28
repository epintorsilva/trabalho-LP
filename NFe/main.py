from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.usuario)

@main.route('/emissao-nota')
@login_required
def emissao_nota():
    return render_template('emissao_nota.html')

@main.route('/emissao-nota', methods=['POST'])
@login_required
def emissao_nota_post():
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("http://www.python.org")
    position = driver.get_window_position()
    driver.minimize_window()
    driver.set_window_position(position['x'], position['y'])
    time.sleep(5)
    assert "Python" in driver.title
    elem = driver.find_element(By.NAME, "q")
    elem.clear()
    elem.send_keys("pycon")
    time.sleep(5)
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    return render_template('emissao_realizada.html')