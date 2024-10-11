from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up the Chrome driver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL for Books to Scrape
myurl = "http://books.toscrape.com/"
driver.get(myurl)

time.sleep(5)  # Wait for the page to load

# Locate product containers
containers = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

# Check how many containers were found
print(f"Found {len(containers)} product containers.")

# List to store product details
products = []

# Iterate through containers and extract product information
for container in containers:
    try:
        title_element = container.find_element(By.CSS_SELECTOR, "h3 a")
        price_element = container.find_element(By.CSS_SELECTOR, "p.price_color")
        availability_element = container.find_element(By.CSS_SELECTOR, "p.availability")
        
        title = title_element.get_attribute('title')  # Extract title attribute
        price = price_element.text
        availability = availability_element.text.strip()
        
        products.append({"Title": title, "Price": price, "Availability": availability})
        print(f"Title: {title}, Price: {price}, Availability: {availability}")  # Debugging output
    except Exception as e:
        print(f"Error occurred: {e}")

# Create a DataFrame and save to CSV
if products:
    df = pd.DataFrame(products)
    df.to_csv("books_toscrape.csv", index=False)
    print(f"Data has been written to books_toscrape.csv")
else:
    print("No product data was collected.")

driver.quit()
