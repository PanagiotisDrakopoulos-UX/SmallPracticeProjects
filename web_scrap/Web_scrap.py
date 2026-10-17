#Page Scraper
#Create an application which connects to a site and pulls out all links, or images, and saves them to a list. 
#Optional: Organize the indexed content and don’t allow duplicates. Have it put the results into an easily searchable index file.


import requests
import bs4
import openpyxl


wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Προϊόντα Σκλαβενίτης"

ws.append(["Αρ.", "Τίτλος Προϊόντος", "Τιμή"])

counter = 1  
page = 1

while True:
    url = f"https://www.sklavenitis.gr/galata-rofimata-chymoi-psygeioy/galata-psygeioy/?pg={page}"  
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    titles = soup.select("h4.product__title a")
    prices = soup.select(".priceWrp .price")
    
    if not titles:
        print("Τέλος.")
        break
    for title, price_elem in zip(titles, prices):
        clean_title = title.get_text(strip=True)
        clean_price = price_elem.get("data-price")
        
        if clean_title and clean_price:
            ws.append([counter, clean_title, f"{clean_price}€"])
            counter += 1        
    page += 1
 
file_name = "sklavenitis_products.xlsx"
wb.save(file_name)
print(f"Η αποθήκευση ολοκληρώθηκε επιτυχώς στο αρχείο: {file_name}")