from typing import List
import re
from selenium import webdriver
from evictions.scraper.basepage import BasePage
from evictions.resources.locators import Locators
from evictions.resources.zips import ST_PETE_ZIPS


class RecordPage(BasePage):
    """Navigates a page on the CCMSPA web site containing the record of a single eviction."""

    def __init__(
        self,
        driver: webdriver.Chrome,
    ):
        super().__init__(driver)
        self.record_data = self.extract_record_data()

    def extract_record_data(self) -> List[dict]:
        """Reads through the record page's text, searching for bits of data
        to store and return. Currently stores 5 data points for each eviction:

        1. case_type
        2. date_filed
        3. case_number
        4. defendant zip code
        5. is_in_st_pete

        Returns:
            List[dict]: One record with the data from one eviction
        """

        self.wait_for_presence(Locators.CASE_DETAIL_CLASS)
        record_rows = self.driver.find_elements(*Locators.RECORD_ROW_XPATH)
        case_type, date_filed, case_number, defendant_zip_code = (
            "",
            "",
            "",
            "",
        )
        is_in_st_pete = False
        # iterate through the rows of the page's internal table
        for index, row in enumerate(record_rows):

            cell_text = row.text
            # print(f"Row {index}: {cell_text}")
            if cell_text.strip().lower().startswith("case type:"):
                case_type = re.search(":(.*)", cell_text).group(1)
                print(f"Case type: {case_type}")
            if cell_text.strip().lower().startswith("date filed:"):
                date_filed = re.search(":(.*)", cell_text).group(1)
                print(f"Date Filed: {date_filed}")
            if cell_text.strip().lower().startswith("uniform case number:"):
                case_number = re.search(":(.*)", cell_text).group(1)
            if cell_text.strip().lower().startswith(
                "defendant"
            ) or cell_text.strip().lower().startswith("defendant"):
                print("found defendant")
                defendant_zip_code = ""
                offset: int = 1
                # inner loop
                while defendant_zip_code == "":
                    next_row = record_rows[index + offset]
                    print(next_row.text)
                    zip_codes = re.findall(r"\d{5}", next_row.text)
                    if len(zip_codes) >= 1:
                        print(zip_codes)
                        defendant_zip_code = zip_codes[-1]
                    else:
                        offset += 1
                is_in_st_pete: bool = (
                    defendant_zip_code.strip() in ST_PETE_ZIPS
                )
        return [
            {
                "case_type": case_type,
                "date_filed": date_filed,
                "case_number": case_number,
                "defendant_zip_code": defendant_zip_code,
                "is_in_st_pete": is_in_st_pete,
            }
        ]
