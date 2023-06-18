import re
import requests
from bs4 import BeautifulSoup


def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Telegram message sent successfully.")
    else:
        print("Failed to send Telegram message. Response content:", response.content)


def check_discount(html_content, url):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find voucher price button
    voucher_price_button = soup.select_one('.voucher-price-button')
    if voucher_price_button:
        voucher_price_text = voucher_price_button.get_text(strip=True)
        voucher_price_match = re.search(r'₹(\d+)', voucher_price_text)
        if voucher_price_match:
            voucher_price = int(voucher_price_match.group(1))
            print("Voucher price:", voucher_price)

            # Find save text
            save_text = soup.select_one('.saveText')
            if save_text:
                save_percent_match = re.search(r'Save (\d+)', save_text.get_text(strip=True))
                if save_percent_match:
                    save_percent = int(save_percent_match.group(1))
                    print("Save percentage:", save_percent)

                    if voucher_price <= 200 and save_percent >= 60:
                        message = f"Alert! Voucher price is ₹{voucher_price} and save percentage is {save_percent}%. URL: {url}"
                        send_telegram_message("{token}", "{chat_id}", message)
                else:
                    print("Save percentage not found.")
            else:
                print("Save text not found.")
        else:
            print("Voucher price not found.")
    else:
        print("Voucher price button not found.")


html = '<div><article class="merchant-voucher-single   "><div><div class="voucher-description"><div class="voucher-text">Get Rs. 500 off on your bill</div></div><div class="voucher-add-tnc"><div class="voucher-counter-holder"><div class="voucher-counter"><button class="voucher-price-button ">Get it for ₹200</button></div></div></div></div><div></div><div class="voucher-details"><div class="voucher-detailed-info reverse"><p class="refundable-status">Refundable</p><section class="details-holder"><article class="valid-days"><div><p class="heading-text"> Valid on: </p><span> All Days  </span></div></article><div class="more-info-holder"><div class="more-info">.<p>Details</p></div></div></section></div><section class="savePercentHolder"><div><img alt="wallet icon" class="icon err-handled" src="https://static.magicpin.com/samara/static/images/merchant/wallet-new.svg"><span class="saveText">Save 60 %</span></div></section></div></article></div>'
url = "https://magicpin.in/Bangalore/Nallurhalli/Restaurant/Chowki-Multicuisine-Restaurant/store/1539938/vouchers/"

check_discount(html, url)
