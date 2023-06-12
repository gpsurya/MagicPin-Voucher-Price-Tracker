import re
import requests


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


def check_discount(html_content):
    # Extract the voucher price using regex pattern
    pattern = r'<p[^>]*?class="voucher-final-price "[^>]*?>(.*?)<\/p>'
    voucher_price_match = re.search(pattern, html_content)

    if voucher_price_match:
        voucher_price_text = voucher_price_match.group(1).strip('₹')
        print("Voucher price found.")

        # Extract the numeric part of the voucher price text
        voucher_price_numeric = ''.join(filter(str.isdigit, voucher_price_text))

        if voucher_price_numeric:
            voucher_price = int(voucher_price_numeric)
            print("Current voucher price:", voucher_price)

            if voucher_price <= 200:
                print("Voucher price is 200 or below. Alert!")
                send_telegram_message("{BOT_API_CODE_HERE}", "{@CHANNEL_NAME}",
                                      f"Alert! Current voucher price is {voucher_price}. Link: https://bit.ly/chowki-mp")
            else:
                print("Voucher price is above 200.")
        else:
            print("Unable to parse voucher price.")
    else:
        print("Voucher price not found.")


html = '<a class="merchant-voucher merchant-sub-content rel-handled" href="https://magicpin.in/Bangalore/Nallurhalli/Restaurant/Chowki-Multicuisine-Restaurant/store/1539938/vouchers/?selected_voucher_roa_id=1713621"><section class="voucher-details-holder"><h5 class="desc">Get Rs. 500 off on your bill</h5><div class="voucher-price"><p class="voucher-price-holder"><span class="voucher-high-price"> </span><span class="voucher-low-price">₹500</span></p><div class="tagline"><p><img alt="save percent" class="usable-wallet err-handled" src="https://static.magicpin.com/samara/static/images/savepercent.svg"><p class="max-usable-points">SAVE 55%</p></p></div></div></section><div class="voucher-info"><section class="detailedInfo"><p class="refundable-status refundable">Refundable .</p><div class="voucherTnc"><p class="heading-text"> Valid on: </p><span> All Days . </span></div></section><p class="voucher-final-price ">Get it for ₹225 </p></div></a>'

check_discount(html)
