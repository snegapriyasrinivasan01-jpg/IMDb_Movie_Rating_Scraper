import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def scrape_imdb_top_250():
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")

    print("Initializing Chrome WebDriver...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = "https://www.imdb.com/chart/top/"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        print("Waiting for page to load and scrolling...")
        time.sleep(5)

        # Scroll down to load all 250 items
        driver.execute_script("window.scrollTo(0, 3000);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 6000);")
        time.sleep(3)

        movies = []
        print("Extracting movie data...")
        
        items = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
        print(f"Total items found: {len(items)}")

        for index, item in enumerate(items):
            try:
                # Direct innerText extraction
                full_text = item.text
                lines = [line.strip() for line in full_text.split("\n") if line.strip()]
                
                title = ""
                rank = str(index + 1)
                year = ""
                rating = ""

                # Extract Title
                for line in lines:
                    if len(line) > 0 and (line[0].isdigit() or "." in line[:5]):
                        if "." in line:
                            parts = line.split(".", 1)
                            title = parts[1].strip()
                        else:
                            title = line
                        break
                
                if not title and len(lines) > 0:
                    title = lines[0]

                # Extract Year (4-digit number)
                for line in lines:
                    if line.isdigit() and len(line) == 4 and (line.startswith("19") or line.startswith("20")):
                        year = line
                        break

                # Extract Rating (like 9.3, 8.5 etc)
                for line in lines:
                    try:
                        val = float(line)
                        if 1.0 <= val <= 10.0 and "." in line:
                            rating = line
                            break
                    except ValueError:
                        continue

                movies.append({
                    "Rank": rank,
                    "Title": title,
                    "Year": year,
                    "Rating": rating
                })

            except Exception as e:
                pass

        print(f"Successfully parsed {len(movies)} movies.")

        if movies:
            df = pd.DataFrame(movies)
            output_file = "imdb_top_250.csv"
            df.to_csv(output_file, index=False)
            print(f"Data saved successfully to '{output_file}'[span_0](start_span)[span_0](end_span)[span_1](start_span)[span_1](end_span)!")
        else:
            print("No movies were parsed.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        input("\nScraping mudinthathu! Browser-a close seiya Enter-ai amukkavum...")
        driver.quit()

if __name__ == "__main__":
    scrape_imdb_top_250()