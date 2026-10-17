# Webscrape product prices from an online store automatically and email them as an Excel report


from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import bs4
import openpyxl
import requests
import smtplib


def export_data():
  wb = openpyxl.Workbook()
  ws = wb.active
  ws.title = "Προϊόντα Σκλαβενίτης"
  ws.append(["Αρ.", "Τίτλος Προϊόντος", "Τιμή"])
  counter = 1
  page = 1
  while True:
    url = f"https://www.sklavenitis.gr/chartika-panes-servietes/vrefikes-paidikes-panes-moromantila/?pg={page}"
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    titles = soup.select("h4.product__title a")
    prices = soup.select(".priceWrp .price")

    if not titles:
      print("Τέλος συλλογής δεδομένων.")
      break
    for title, price_elem in zip(titles, prices):
      clean_title = title.get_text(strip=True)
      clean_price = price_elem.get("data-price")

      if clean_title and clean_price:
        ws.append([counter, clean_title, f"{clean_price}€"])
        counter += 1
    page += 1

  file_name = "prices_products.xlsx"
  wb.save(file_name)
  print(f"Το αρχείο '{file_name}' δημιουργήθηκε με επιτυχία.")
  return file_name


def send_email(filename):
  current_date = datetime.now().strftime("%d/%m/%Y")
  subject = f"Αναφορά τιμών για βρεφικές πάνες ({current_date})"

  smtp_object = smtplib.SMTP("smtp.gmail.com", 587)
  smtp_object.starttls()

  email = "YOUR_EMAIL@gmail.com"
  password = "YOUR_APP_PASSWORD"

  smtp_object.login(email, password)
  from_address = email
  to_address = "RECEIVER_EMAIL@gmail.com"

  msg = MIMEMultipart()
  msg["From"] = from_address
  msg["To"] = to_address
  msg["Subject"] = subject
  body = "Συνημμένο θα βρείτε το αρχείο με τις τιμές."
  msg.attach(MIMEText(body, "plain"))

  try:
    with open(filename, "rb") as attachment:
      part = MIMEBase("application", "octet-stream")
      part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
    msg.attach(part)
  except FileNotFoundError:
    print(
        f"Το αρχείο '{filename}' δεν βρέθηκε. Το email θα σταλεί χωρίς"
        " συνημμένο."
    )


  smtp_object.sendmail(from_address, to_address, msg.as_string())
  smtp_object.quit()
  print("Το email στάλθηκε με επιτυχία!")



if __name__ == "__main__":
  
  excel_file = export_data()
  send_email(excel_file)