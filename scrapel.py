from bs4 import BeautifulSoup
import time 
import pandas as pd

#Iniciar navegador web
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

#Filas y columnas de la lista
scarped_data = []
def scrape():
    
    soup = BeautifulSoup()
        
    #Encontrar <table>
    bright_star_table = soup.find("table", attrs={"class", "wikitable"})
    
    #Encontrar <tbody>
    table_body = bright_star_table.find('tbody')
    
    #Encontrar <try>
    table_rows = table_body.find_all('tr')
    
    #Obtener información de <td>
    for row in table_rows:
        table_cols = row.find_all('td')
        #print(table_cols)
            
        temp_list = []
            
        # Imprimir solo las columnas de texto usando la propiedad ".text"
        for col_data in table_cols:
            #print(col_data.text)
                
            #Quitar los espacios en blanco usando el método strip()
            data = col_data.text.strip()
            #print(data)
                
            temp_list.append(data)
                
        #Agregar datos a la lista star_data
        scarped_data.append(temp_list)
    
            
        stars_data = []
            
        for i in range(0, len(scarped_data)):
            Star_names = scarped_data[i][1]
            Distance = scarped_data[i][3]
            Mass = scarped_data[i][5]
            Radius = scarped_data[i][6]
            Lum = scarped_data[i][7]
        
            required_data = [Star_names, Distance, Mass, Radius, Lum]
            stars_data.append(required_data)
        
            #Definir el Encabezado
            headers = ['Star_name','Distance','Mass','Radius','Luminosity']
        
            #Define pandas DataFrame
            star_df_1 = pd.DataFrame(stars_data, colums=headers)
        
            #Convierte a csv
            star_df_1.to_csv('scraped_data.csv', index=True, index_label="id")
                                