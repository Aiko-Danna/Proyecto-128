from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time 
import pandas as pd
import requests

#Iniciar navegador web
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

# Controlador web
browser = webdriver.Chrome("/Users/danna/Downloads/chromedriver_mac_arm64/chromedriver")
browser.get(START_URL)

time.sleep(10)

#Filas y columnas de la lista
scarped_data = []

def scrape():
    for i in range(1,2):
        while True:
            time.sleep(2)
            
            soup = BeautifulSoup(browser.page_source, "html.parser")
            
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))

            if current_page_num < i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            
            # Obtener la etiqueta del hipervínculo
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs" + hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            
            scarped_data.append(temp_list)
            
        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        
        print(f"Extracción de datos de la página {i} completada")
        
# Llamar al método
scrape()


def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list =[]
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        scarped_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
        

star_df_1 = pd.read_csv("updated_scraped_data.csv")

# Llamar al método
for index, row in star_df_1.iterrows():
    print(row['hyperlink'])
    scrape_more_data(row['hyperlink'])
    print(f"La extracción de datos del hipervínvulo {index+1} se ha completado")

print(scarped_data[0:10])

# Remover el carácter '\n' de los datos extraídos
scarpped_data = []

for row in scarped_data:
    replaced = []
    for el in row:
        el = el.replace("\n", "")
        replaced.append(el)
    scarpped_data.append(replaced)

print(scarpped_data)

# Definir los encabezados
headers = ['Star_name','Distance','Mass','Radius','Luminosity','hyperlink']

# Definir el dataframe de Pandas
star_df_1 = pd.DataFrame(scarped_data, columns=headers)

# Convertir a CSV
scarped_data.to_csv('updated_scraped_data.csv',index=True, index_label="id")
