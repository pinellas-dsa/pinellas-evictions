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

    def extract_record_data(self):
        self.wait_for_presence(Locators.CASE_DETAIL_CLASS)
        record_rows = self.driver.find_elements(*Locators.RECORD_ROW_XPATH)
        case_type, date_filed, case_number, defendent_zip_code = (
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
                "defendent"
            ) or cell_text.strip().lower().startswith("defendant"):
                print("found defendent")
                defendent_zip_code = ""
                offset: int = 1
                # inner loop
                while defendent_zip_code == "":
                    next_row = record_rows[index + offset]
                    print(next_row.text)
                    zip_codes = re.findall(r"\d{5}", next_row.text)
                    if len(zip_codes) >= 1:
                        print(zip_codes)
                        defendent_zip_code = zip_codes[-1]
                    else:
                        offset += 1
                is_in_st_pete: bool = (
                    defendent_zip_code.strip() in ST_PETE_ZIPS
                )
        print(
            {
                "case_type": case_type,
                "date_filed": date_filed,
                "case_number": case_number,
                "defendent_zip_code": defendent_zip_code,
                "is_in_st_pete": is_in_st_pete,
            }
        )
        return [
            {
                "case_type": case_type,
                "date_filed": date_filed,
                "case_number": case_number,
                "defendent_zip_code": defendent_zip_code,
                "is_in_st_pete": is_in_st_pete,
            }
        ]
