import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By

token = '1977078501:AAEx0ccKV8NwG_HZ6PTsVYBhgKjHCyzeaYE'
bot = telebot.TeleBot(token)

def link(domen, page, driver, links):
    url = (f'{domen}?PAGEN_1={page}')
    driver.get(url)

    items = driver.find_elements(By.CLASS_NAME, "col-lg-3")
    for item in items:
        link = item.find_element(By.CLASS_NAME, "dark_link").get_attribute('href')
        links.append(link)

@bot.message_handler(commands=['start'])
def parsing(message):
    domen = 'https://autorx.ru/catalog/Vneshniyvid/Spoylery/'
    pages = 8

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    bot.send_message(message.chat.id, 'Процесс пошёл')

    links = []
    for page in range(1, pages + 1):
       link(domen, page, driver, links)

    for url in links:
        driver.get(url)

        title = driver.find_element(By.ID, 'pagetitle').text
        price = driver.find_element(By.XPATH, "//div[@class='price font-bold font_mxs']//span[@class='values_wrapper']").text
        article = driver.find_element(By.CLASS_NAME, 'code_in__value').text

        bot.send_message(message.chat.id, f'Название: {title}, цена: {price}, код товара: {article}, ссылка: {url}')

bot.polling()