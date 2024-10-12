import logging
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

logging.basicConfig(filename='parser.txt', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

geckodriver_path = r'C:/Users/maxim/Desktop/python/pars/geckodriver.exe'
firefox_path = r'C:/Program Files/Mozilla Firefox/firefox.exe'

if not os.path.exists(geckodriver_path):
    logging.error(f"GeckoDriver not found at: {geckodriver_path}")
    exit(1)

if not os.path.exists(firefox_path):
    logging.error(f"Firefox not found at: {firefox_path}")
    exit(1)

service = Service(geckodriver_path)
options = Options()
options.binary_location = firefox_path

try:
    driver = webdriver.Firefox(service=service, options=options)
    logging.info("Browser launched successfully.")
except Exception as e:
    logging.error(f"Error launching browser: {e}")
    exit(1)

def scroll_page():
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        logging.info("Page scrolled down successfully.")
    except Exception as e:
        logging.error(f"Error scrolling page: {e}")

def parse_and_save():
    try:
        url = 'https://freelancehunt.com/ua/projects/skill/python/22.html'
        driver.get(url)
        logging.info(f"Opened page: {url}")

        time.sleep(5)
        for i in range(3):
            logging.info(f"Scrolling page: {i+1}/3")
            scroll_page()

        html_content = driver.page_source

        with open('page.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info("HTML code of the page saved to 'page.html'.")

        soup = BeautifulSoup(html_content, 'html.parser')
        data = []

        for item in soup.find_all('td', class_='left'):
            title = item.find('h2').get_text(strip=True) if item.find('h2') else 'No title'
            description = item.find('p').get_text(strip=True) if item.find('p') else 'Description not available'
                      
            link_tag = item.find('a', class_='biggest visitable')
            link = link_tag['href'] if link_tag and link_tag.has_attr('href') else 'Link not available'

            data.append({
                'Title': title,
                'Description': description,
                'Link': link,
            })

        logging.info(f"Found elements: {len(data)}")

        if not data:
            logging.warning("No data found. Check selectors and page structure.")
            return

        file_path = os.path.join(os.getcwd(), 'parsed_data.txt')

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"\n\n++++++++++++ Data updated: {time.ctime()} ++++++++++++\n")
            for entry in data:
                file.write(f"\n{entry['Title']}\n")
                file.write(f"\n{entry['Description']}\n")
                file.write(f"\n{entry['Link']}\n")
        logging.info(f"Data successfully written to file '{file_path}'.")

    except Exception as e:
        logging.error(f"Error during parsing and saving data: {e}")

try:
    while True:
        logging.info("Starting parsing...")
        parse_and_save()
        logging.info("Parsing finished. Waiting 60 seconds.")
        time.sleep(60*5)
except KeyboardInterrupt:
    logging.info("Program stopped by user.")
finally:
    driver.quit()
    logging.info("Browser closed.")
