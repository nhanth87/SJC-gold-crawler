import csv

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

#config Y-M-D
FROM_DATE = "2019-01-01"
TO_DATE = "2021-10-15"
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

def split_buy_sell_g_price(price):
    buy, sell = price.split(" / ", 1)
    return buy, sell

if __name__ == '__main__':
    links = ""
    delta = timedelta(days=1)
    g_data_col = ['date', 'Exim_buy','Exim_sell', 'Hcm_buy', 'Hcm_sell', 'Hanoi_buy', 'Hanoi_sell', 'Danang_buy', 'Danang_sell',
                  'Nhatrang_buy', 'Nhatrang_sell', 'Cantho_buy', 'Cantho_sell']

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
            exim_buy = "0"
            exim_sell = "0"

            hcm_buy = "0"
            hcm_sell = "0"

            hanoi_buy = "0"
            hanoi_sell = "0"

            danang_buy = "0"
            danang_sell = "0"

            nhatrang_buy = "0"
            nhatrang_sell = "0"

            cantho_buy = "0"
            cantho_sell = "0"

            for content in links.contents:
                if content_count == 3: #exim
                    exim_buy, exim_sell = split_buy_sell_g_price(content.contents[1].text)
                elif content_count == 4: #hcm
                    hcm_buy, hcm_sell = split_buy_sell_g_price(content.contents[1].text)

                elif content_count == 5: #hanoi
                    hanoi_buy, hanoi_sell = split_buy_sell_g_price(content.contents[1].text)

                elif content_count == 6:  # danang
                    danang_buy, danang_sell = split_buy_sell_g_price(content.contents[1].text)

                elif content_count == 7:  # nha trang
                    nhatrang_buy, nhatrang_sell = split_buy_sell_g_price(content.contents[1].text)

                elif content_count == 8:  # can tho
                    cantho_buy, cantho_sell = split_buy_sell_g_price(content.contents[1].text)

                content_count += 1
            #end for

            #append to list
            row = [datetime.strftime(from_date, "%Y-%m-%d"), exim_buy, exim_sell, hcm_buy, hcm_sell,
                   hanoi_buy, hanoi_sell, danang_buy, danang_sell, nhatrang_buy, nhatrang_sell, cantho_buy, cantho_sell]
            print(row)
            write_to_csv(row)

        except:
            pass



        counter += 1
        from_date += delta


        if counter % 101 == 0:
            time.sleep(2)

    #end while
