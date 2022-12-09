import datetime
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from evictions.utils.date_utils import find_last_day_of_month
from evictions.resources.zips import ST_PETE_ZIPS
from evictions.resources.locators import Locators

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


def select_search_by_date_button(cdriver: webdriver.Chrome, search_by: str):
    cdriver.get(Locators.CCMPSA_HOMEPAGE_URL)
    time.sleep(1)  # wait one second
    cdriver.find_element(*Locators.ALL_CASE_RECORDS_LINK).click()
    radio_list = driver.find_elements(By.NAME, "SearchBy")

    for rbutton in radio_list:
        rbutton_t = rbutton.get_attribute("id")
        if rbutton_t == search_by:
            rbutton.click()
            # print("Is Selected : ", rbutton.is_selected())
            break


def select_start_end_dates(cdriver: webdriver.Chrome, start_date, end_date):
    cdriver.find_element(By.ID, "DateFiledOnAfter").send_keys(start_date)
    cdriver.find_element(By.ID, "DateFiledOnBefore").send_keys(end_date)


def select_case_type(
    cdriver: webdriver.Chrome, dropdown_id: str, case_type: str
):
    dropdown = Select(cdriver.find_element(By.ID, dropdown_id))
    dropdown.select_by_visible_text(case_type)


def click_search_submit(cdriver: webdriver.Chrome):
    cdriver.find_element(By.ID, "SearchSubmit").click()


def select_cases(
    driver: webdriver.Chrome,
    year: int,
    search_by,
    case_type="DELINQUENT TENANT/EVICTION/UNLAWFUL DETAINER",
):
    months_of_data = []
    for month_num in range(1, 2):  # 12):
        last_day_of_month = find_last_day_of_month(year, month_num)
        start_date = datetime.date(year, month_num, 1)
        end_date = datetime.date(year, month_num, last_day_of_month)
        start_date_str = start_date.strftime("%m/%d/%Y")
        end_date_str = end_date.strftime("%m/%d/%Y")
        select_search_by_date_button(driver, search_by=search_by)
        select_start_end_dates(driver, start_date_str, end_date_str)
        select_case_type(driver, "selCaseTypeGroups", case_type)
        click_search_submit(driver)
        month_of_data = obtain_details_from_eviction_filings(driver)
        months_of_data.append(month_of_data)
        time.sleep(1)  # TODO: Delete this line
    year_of_data = pd.concat(months_of_data)
    year_of_data.to_csv("evictions.csv")


def extract_zip_code(cdriver):
    rows = cdriver.find_elements(By.XPATH, "//table/tbody/tr")
    for index, row in enumerate(rows):
        case_type, date_filed, case_number, defendent_zip_code = "", "", "", ""
        is_in_st_pete = False
        cell_text = row.text
        print(f"Row {index}: {cell_text}")
        if cell_text.strip().lower().startswith("case type:"):
            case_type = re.search(":(.*)", cell_text).group(1)
        if cell_text.strip().lower().startswith("date filed:"):
            date_filed = re.search(":(.*)", cell_text).group(1)
        if cell_text.strip().lower().startswith("uniform case number:"):
            case_number = re.search(":(.*)", cell_text).group(1)
        if cell_text.strip().lower().startswith(
            "defendent"
        ) or cell_text.strip().lower().startswith("defendant"):
            print("found defendent")
            defendent_zip_code = ""
            offset: int = 1
            while defendent_zip_code == "":
                next_row = rows[index + offset]
                print(next_row.text)
                zip_codes = re.findall(r"\d{5}", next_row.text)
                if len(zip_codes) >= 1:
                    print(zip_codes)
                    defendent_zip_code = zip_codes[-1]
                else:
                    offset += 1
            if defendent_zip_code in ST_PETE_ZIPS:
                is_in_st_pete = True
            else:
                is_in_st_pete = False
    return [
        {
            "case_type": case_type,
            "date_filed": date_filed,
            "case_number": case_number,
            "defendent_zip_code": defendent_zip_code,
            "is_in_st_pete": is_in_st_pete,
        }
    ]


def obtain_details_from_eviction_filings(cdriver: webdriver.Chrome):
    time.sleep(1)
    print("checking")
    list_of_rows = cdriver.find_elements(By.CSS_SELECTOR, "a[href*='CaseID']")
    print(len(list_of_rows))
    eviction_list = []
    for index in range(len(list_of_rows)):
        row = cdriver.find_elements(By.CSS_SELECTOR, "a[href*='CaseID']")[
            index
        ]
        row.click()
        row_data = extract_zip_code(cdriver)
        eviction_level_data = pd.DataFrame.from_records(row_data)
        eviction_list.append(eviction_level_data)
        time.sleep(1)
        driver.back()
    month_of_data = pd.concat(eviction_list)

    return month_of_data


select_cases(driver, 2022, "DateFiled")
time.sleep(10)
# driver.quit()
