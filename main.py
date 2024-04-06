from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    import re

    import requests
    from bs4 import BeautifulSoup

    pattern = re.compile('"([^"]*)"')

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=chrome_options)


    url = "https://animefire.plus/animes/seikon-no-qwaser/1"


    driver.get(url)

    video_element = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]/div/div/div[2]/div[3]/video")


    caminho_completo = video_element.get_attribute("outerHTML")
    caminho_cortado = caminho_completo.split(' ')

    driver.quit()
    for item in caminho_cortado:
        if 'src' in item:
            match = pattern.search(item)
            if match:
                link_api = match.group(1)
            break 

    url = link_api
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    str_soup = str(soup)
    soup_cortado = str_soup.split('{')
    lista_link_video = soup_cortado[3][6:]
    lista_link_video_cortado = lista_link_video.split(',')
    link_do_video_quebrado = lista_link_video_cortado[0][1:-1]


    url_video = link_do_video_quebrado


    chrome_options = Options()
    chrome_options.add_argument("--headless")
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=chrome_options)
    url_video = link_do_video_quebrado
    driver.get(url_video)
    current_url = driver.current_url
    driver.quit()

    return current_url


app.run()



if __name__ == '__main__':
    app.run()