from playwright.sync_api import sync_playwright, Playwright

JTX_URL = "https://www.jointex.co.jp/DFiDtl001Servlet?orderCode="

order_codes=[
    "832151",
    "349813",
    "483901"
]

items=[]

def run(Playwright, order_codes):
    chromium = Playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()

    item_n = len(order_codes)
    for i, order_code in enumerate(order_codes):
        page.goto(JTX_URL+order_code)
        code = None
        maker = None
        url = None
        name = None
        price = None
        is_price_red = None

        if not page.title()=="エラー画面":
        
            price = page.locator("div.rBox aside p.txt02").nth(1).inner_html().replace(" ", "").replace("\n", "")[:-1]
            if price.startswith("<font"):
                price=price[21:-7]
                is_price_red = True
            code = page.locator("div.info p.txt span").nth(3).inner_html()[7:]
            maker = page.locator("div.info p.txt span").nth(0).inner_html()[6:]
            url = page.url
            name = page.locator("div.info h2").inner_html()

        item_info = [maker, name, price, is_price_red, code, url]
        items.append(item_info)
        print(str(i+1)+"/"+str(item_n)+" completed!")
    browser.close()

with sync_playwright() as playwright:
    run(playwright, order_codes)
    print(items)