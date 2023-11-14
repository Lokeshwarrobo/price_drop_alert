import requests
import json
import re
import csv
from bs4 import BeautifulSoup
from Mail import send_mail
import schedule
import time


def get_response(url):
    header = get_headers(url)
    try:
        response = requests.get(url, headers=header)
        check_prices(response)
    except Exception as e:
        print("Error Occurred : ", e)


def get_price(response):
    pattern = r"https?://(www\.)?([a-zA-Z0-9.-]+)(?:\.\w+).*"
    match = re.match(pattern, response.url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if match:
        domain = match.group(2)
        if domain == "flipkart":
            return soup.find("div", {"class": "_30jeq3 _16Jk6d"})
        if domain == "amazon":
            return soup.find("span", {"class": "a-price-whole"})
        if domain == "myntra":
            script_tags = soup.findAll("script", {"type": "application/ld+json"})
            for script_tag in script_tags:
                json_data = json.loads(script_tag.contents[0])
                if '@type' in json_data and json_data['@type'] == 'Product' and 'offers' in json_data:
                    price = json_data['offers']['price']
                    return int(price)
        if "ajio" in domain:
            script_tags = soup.findAll("script", {"type": "application/ld+json"})
            for script_tag in script_tags:
                json_data = json.loads(script_tag.contents[0])
                if '@type' in json_data and json_data['@type'] == 'ProductGroup' and 'offers' in json_data:
                    price = json_data['offers']['price']
                    return int(price)

    else:
        print("url is not correct" + response.url)


def check_prices(response):
    current_price = get_price(response)
    if type(current_price) != int and current_price is not None:
        current_price = current_price.text
        current_price = int(current_price.replace(".", "").replace("₹", ""))

    previous_price = get_previous_price(response)
    if previous_price is not None:
        if int(previous_price) - current_price > 200:
            send_mail("lokeshwar.robo2@gmail.com", current_price)
    else:
        write_current_price(response.url, current_price)


def write_current_price(url, price):
    new_data = []
    data = {'key': url, 'value': price}
    new_data.append(data)
    with open('Giants.csv', mode='a', newline='') as file:
        fieldnames = ['key', 'value']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            csv_writer.writeheader()

        csv_writer.writerows(new_data)


def get_previous_price(response):
    with open('Giants.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        next(csv_reader, None)
        for row in csv_reader:
            if row['key'] == response.url:
                return row['value'].replace(".", "")


def get_headers(url):
    pattern = r"https?://(www\.)?([a-zA-Z0-9.-]+)(?:\.\w+).*"
    match = re.match(pattern, url)
    if match:
        domain = match.group(2)
        if domain == "flipkart":
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.5",
            }
            return header
        if domain == "amazon":
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36."}
            return header
        if domain == "ajio":
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
            return header
        else:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9,te;q=0.8"
            }
            return header

    else:
        print("url is not correct" + url)


links = [
    "https://www.flipkart.com/misfit-boat-t200-runtime-120-mins-6-in-1-trimmer-men/p/itm799721a9f94d9?pid=TMRG2CJSWHVVGAKV&lid=LSTTMRG2CJSWHVVGAKVOYBTGF&marketplace=FLIPKART&q=misfit+trimmer&store=zlw/79s/by3&spotlightTagId=BestsellerId_zlw/79s/by3&srno=s_1_13&otracker=search&otracker1=search&fm=Search&iid=ef252d8e-9128-4a09-8df9-1bfada5dd6a3.TMRG2CJSWHVVGAKV.SEARCH&ppt=sp&ppn=sp&ssid=iy30ig9o3k0000001683369888234&qH=9f193241501a1f50&affid=rohanpouri&affExtParam1=ENKR20230628A500165129&affExtParam2=ENKR20230628A500165129",
    "https://www.flipkart.com/aula-f2023-anti-ghosting-aluminium-body-mobile-holder-membrane-wired-usb-gaming-keyboard/p/itmcecaf9ac9f135?pid=ACCGNHC4CMBPGNNS&lid=LSTACCGNHC4CMBPGNNSZRI4N8&marketplace=FLIPKART&store=6bo%2Fai3%2F3oe&srno=b_1_1&otracker=browse&fm=organic&iid=4b8d7c7b-ff9b-41b4-a2e8-c152d599f4a4.ACCGNHC4CMBPGNNS.SEARCH&ppt=browse&ppn=browse&ssid=3odd5pbzuo0000001699885029828",
    "https://gap.ajio.com/gap-dark-washed-slim-fit-jeans/p/441778169_black",
    "https://www.flipkart.com/bestor-usb-hub-multiport-adapter-macbook-pro-air-m1-4-in-1-4port/p/itm1032b7417e715?pid=USGGHZ6UZ3BUE89V&lid=LSTUSGGHZ6UZ3BUE89V0PPUZ1&marketplace=FLIPKART&fm=productRecommendation%2FcrossSelling&iid=R%3Ac%3Bp%3AACCGNHC4CMBPGNNS%3Bl%3ALSTACCGNHC4CMBPGNNSZRI4N8%3Bpt%3App%3Buid%3A659ce967-822f-11ee-98d9-4ff594af0b77%3B.USGGHZ6UZ3BUE89V&ppt=pp&ppn=pp&ssid=3odd5pbzuo0000001699885029828&otracker=pp_reco_Bought%2BTogether_2_36.productCard.PMU_TAB_Bestor%2BUSB%2BHub%2BMultiport%2BAdapter%2Bfor%2BMacBook%2BPro%2BAir%2BM1%2B4-in-1%2BUSB%2BHub%2B4Port%2BUSB%2BHub_USGGHZ6UZ3BUE89V_productRecommendation%2FcrossSelling_1&otracker1=pp_reco_PINNED_productRecommendation%2FcrossSelling_Bought%2BTogether_GRID_productCard_cc_2_NA_view-all&cid=USGGHZ6UZ3BUE89V",
    "https://www.amazon.in/dp/B0BNDRXDHF/ref=sspa_dk_detail_1?pd_rd_i=B0BNDRXDHF&pd_rd_w=80hAB&content-id=amzn1.sym.0fcdb56a-738b-4621-9da7-d47193883987&pf_rd_p=0fcdb56a-738b-4621-9da7-d47193883987&pf_rd_r=Z23K0TTAFZJS93XZ487V&pd_rd_wg=bAZgB&pd_rd_r=c2543f6b-faf7-49ea-9f67-662b4e2a72cf&s=hpc&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWwy&th=1",
    "https://www.myntra.com/trousers/ivoc/ivoc-men-navy-blue-slim-fit-solid-cargos/11647230/buy",
    ]


def start():
    for link in links:
        get_response(link)


schedule.every().hour.do(start)

while True:
    schedule.run_pending()
    time.sleep(1)
