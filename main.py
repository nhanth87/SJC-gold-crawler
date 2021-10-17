import csv

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

#config Y-M-D
FROM_DATE = "2019-01-01"
TO_DATE = "2021-10-16"
url = 'https://giavangonline.com/goldhistory.php?date='

#100 requests/s
limit = 100
from_date = datetime.strptime(FROM_DATE, "%Y-%m-%d")
to_date = datetime.strptime(TO_DATE, "%Y-%m-%d")


def crawler(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def write_to_csv(row):
    with open('gold_price.csv', mode='a') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        employee_writer.writerow(row)

def write_header_to_csv(row):
    with open('gold_price.csv', mode='w') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        employee_writer.writerow(row)

if __name__ == '__main__':
    links = ""
    delta = timedelta(days=1)
    g_data_col = ['date', 'SJC Eximbank', 'SJC HCM', 'SJC Hanoi', 'SJC Danang', 'SJC Nhatrang', 'SJC Cantho']

    #main code
    write_header_to_csv(g_data_col)
    counter = 0

    while from_date <= to_date:
        g_date = from_date.strftime("%Y-%m-%d")
        try:
            soup = crawler('https://giavangonline.com/goldhistory.php?date={0}'.format(g_date))

            links = soup.find(id='sjcexchange')
            links = links.find("table", attrs={"class":"home"})

            content_count = 0
            exim = ""
            hcm = ""
            hanoi = ""
            danang = ""
            nhatrang = ""
            cantho = ""
            for content in links.contents:
                if content_count == 3: #exim
                    exim = content.contents[1].text
                elif content_count == 4: #hcm
                    hcm = content.contents[1].text

                elif content_count == 5: #hanoi
                    hanoi = content.contents[1].text

                elif content_count == 6:  # danang
                    danang = content.contents[1].text

                elif content_count == 7:  # nha trang
                    nhatrang = content.contents[1].text

                elif content_count == 8:  # can tho
                    cantho = content.contents[1].text

                content_count += 1
            #end for

            #append to list
            row = [datetime.strftime(from_date, "%Y-%m-%d"), exim, hcm, hanoi, danang, nhatrang, cantho]
            print(row)
            write_to_csv(row)

        except:
            pass



        counter += 1
        from_date += delta


        if counter % 101 == 0:
            time.sleep(2)

    #end while

