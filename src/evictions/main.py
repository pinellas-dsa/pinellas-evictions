import datetime
from pathlib import Path
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from evictions.utils.io_utils import load_query
from evictions.scraper.homepage import HomePage
from evictions.scraper.searchpage import SearchPage
from evictions.scraper.tablepage import TablePage
from evictions.utils.date_utils import find_last_day_of_month


# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)


if __name__ == "__main__":
    query_path = Path.cwd() / "src" / "evictions" / "query.yaml"
    query = load_query(query_path)
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    HomePage(driver)
    # loop through months in range
    months_of_data = []
    for month_num in range(1, 2):  # 12):
        last_day_of_month = find_last_day_of_month(query["year"], month_num)
        start_date = datetime.date(query["year"], month_num, 1)
        end_date = datetime.date(query["year"], month_num, last_day_of_month)
        start_date_str = start_date.strftime("%m/%d/%Y")
        end_date_str = end_date.strftime("%m/%d/%Y")
        # get month of data
        SearchPage(driver, start_date_str, end_date_str, query["case_type"])
        current_month_data = TablePage(driver).data_df
        months_of_data.append(current_month_data)

    year_of_data = pd.concat(months_of_data)
    year_of_data.to_csv("evictions.csv")
    driver.quit()
