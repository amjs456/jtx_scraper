from playwright.sync_api import sync_playwright, Playwright
import csv
import sys

JTX_URL = "https://www.jointex.co.jp/DFiDtl001Servlet?orderCode="

items=[]

def create_order_codes(csv_file_name):
    with open(csv_file_name, newline='') as f:
        spamreader = csv.reader(f)
        order_codes = []
        for row in spamreader:
            order_codes.append(row[0])
        return order_codes


def run(Playwright, order_codes):
    chromium = Playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()

    item_n = len(order_codes)
    for i, order_code in enumerate(order_codes):
        page.goto(JTX_URL+order_code)
        item_code = maker = url = name = price = is_price_red = None
        is_not_six_digit = False

        if not len(order_code)==6:
            is_not_six_digit = True

        if not page.title()=="エラー画面":
            price = page.locator("div.rBox aside p.txt02").nth(1).inner_html().replace(" ", "").replace("\n", "")[:-1]
            if price.startswith("<font"):
                price=price[21:-7]
                is_price_red = True
            item_code = page.locator("div.info p.txt span").nth(3).inner_html()[7:]
            maker = page.locator("div.info p.txt span").nth(0).inner_html()[6:]
            url = page.url
            name = page.locator("div.info h2").inner_html()

        item_info = [maker, name, price, is_price_red, item_code, url, is_not_six_digit]
        items.append(item_info)
        print(str(i+1)+"/"+str(item_n)+" completed!")
    browser.close()
    return items

def save_excel_file(items, filename):
    pass


with sync_playwright() as playwright:
    csv_file_name = sys.argv[1]
    if not csv_file_name.endswith(".csv"):
        csv_file_name = csv_file_name + ".csv"    
        order_codes=  create_order_codes(csv_file_name)
        items = run(playwright, order_codes)
        print(items)