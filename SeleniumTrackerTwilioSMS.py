from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def send_sms(message, to_number):
    account_sid = ''
    auth_token = ''
    from_number = ''

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )


def check_discount():
    print("Running discount tracker...")
    print("Loading website...")

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Set path to chromedriver as per your system
    driver_path = "./chromedriver.exe"

    # Create a webdriver instance
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Load the website
    driver.get("https://magicpin.in/Bangalore/Nallurhalli/Restaurant/Chowki-Multicuisine-Restaurant/store/1539938/")

    print("Waiting for voucher price element...")

    try:
        # Wait for the voucher price element to be present
        voucher_price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.voucher-final-price"))
        )
        voucher_price_text = voucher_price_element.text.strip('₹').strip()

        # Extract the numeric part of the voucher price text
        voucher_price_numeric = ''.join(filter(str.isdigit, voucher_price_text))

        if voucher_price_numeric:
            voucher_price = int(voucher_price_numeric)
            print("Voucher price:", voucher_price)

            if voucher_price <= 200:
                print("Voucher price is 200 or below. Alert!")
                send_sms(f"Voucher price is Rs. {voucher_price}. Grab the deal now! Link: https://bit.ly/chowki-mp",
                         "{NO_WITH_EXTENSION}")  # Update with your desired phone number

                send_sms(f"Voucher price is Rs. {voucher_price}. Grab the deal now! Link: https://bit.ly/chowki-mp",
                         "{NO_WITH_EXTENSION}")  # Update with your desired phone number

            else:
                print("Voucher price is above 200.")
        else:
            print("Unable to parse voucher price.")

    except Exception as e:
        print("Error:", e)

    finally:
        # Quit the webdriver
        driver.quit()


check_discount()
