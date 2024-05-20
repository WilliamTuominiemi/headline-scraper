import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

driver.get("https://yle.fi/t/18-204933/fi")

try:
    consent_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@name='accept-necessary-consents']")
        )
    )
    consent_button.click()
except Exception as e:
    print("No consent button found or an error occurred:", e)

try:
    while True:
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[text()='Näytä lisää']]")
            )
        )

        show_more_button.click()

        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        show_more_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[.//span[text()='Näytä lisää']]")
            )
        )
        if not show_more_button.is_displayed():
            break

except Exception as e:
    print("An error occurred:", e)

soup = BeautifulSoup(driver.page_source, "html.parser")

links = soup.find_all("a", class_="underlay-link")

with open("data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(["Link Text", "Link Href", "Date"])

    for link in links:
        ancestor_div = link.find_parent("h3").find_parent("div")
        time_tag = ancestor_div.find("time")
        date = time_tag.text if time_tag else "No date found"

        writer.writerow([link.text, link["href"], date])

driver.quit()
