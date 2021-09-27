import requests
from bs4 import BeautifulSoup
import pandas as pd
from fyslLogger import fyslLogger
from fyslConfig import fyslConfig
from abc import ABC, abstractmethod
from typing import List
import re
from math import ceil


class webScraping(ABC):
    """This class grasps information from MIT webpage"""

    def __init__(self):
        self.logger = fyslLogger(self.__class__.__name__).logger
        self.urls = fyslConfig().url_config

    def read_all_html_into_soup(self, url) -> BeautifulSoup:
        data = requests.get(url)
        soup = BeautifulSoup(data.text, "html.parser")
        self.logger.info(f"read html into soup for {url}-> Done")
        return soup

    def get_item_number_from_str(self, input_str: str) -> int:
        num = re.search(r"\d*", input_str)
        return int(num.group(0))

    @abstractmethod
    def get_item_list_from_soup(self) -> List:
        pass

    @abstractmethod
    def get_total_number_of_items(self) -> int:
        pass

    @abstractmethod
    def get_info_from_item(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_df_for_one_page(self) -> pd.DataFrame:
        pass


class ws37express(webScraping):
    def __init__(self):
        super().__init__()
        self.url_page1 = self.urls["37express"]
        self.url_per_page_base = self.url_page1[:-1]
        self.soup_page_1 = self.read_all_html_into_soup(self.url_page1)
        self.total_num_of_items = self.get_total_number_of_items()
        self.num_items_per_page = self.get_num_items_per_page()
        self.num_of_pages = ceil(self.total_num_of_items / self.num_items_per_page)

    def get_item_list_from_soup(self, page_number: int) -> List:
        soup = self.read_all_html_into_soup(
            url=f"{self.url_per_page_base}{page_number}"
        )
        div = soup.find("div", {"id": "product-list-container"})
        ul = div.find("ul", {"class": "d-flex flex-wrap justify-content-start"})
        li = ul.find_all("li", {"class": "card rounded-0 mb-4"})
        self.logger.info(f"get item list for page_number {page_number} -> Done")
        return li

    def get_num_items_per_page(self) -> int:
        num_items_per_page = len(self.get_item_list_from_soup(page_number=1))
        self.logger.info(f"num_items_per_page = {num_items_per_page}")
        return num_items_per_page

    def get_total_number_of_items(self) -> int:
        div = self.soup_page_1.find("div", {"id": "shipping-second"})
        div_2 = div.find("div", {"class": "price-filter d-flex"})
        num_items_str = div_2.text.strip()
        total_item_number = self.get_item_number_from_str(num_items_str)
        self.logger.info(f"total_item_number = {total_item_number}")
        return total_item_number

    def get_info_from_item(self, li) -> pd.DataFrame:
        # get title
        h4 = li.find("h4", {"id": "name_cn"})
        title = h4.text.strip()

        # get price
        div = li.find("div", {"class": "content position-relative"})
        div_2 = div.find("div", {"class": "shipping-price px-2"})
        amount = div_2.find("span", {"id": "amount"})
        orig_price = div_2.find("span", {"id": "original_price"})
        selling_price = amount.text.strip()
        if orig_price:
            original_price = orig_price.text.strip()
        else:
            original_price = selling_price
        d = {
            "title": [title],
            "selling_price": [selling_price],
            "original_price": [original_price],
        }
        df = pd.DataFrame(data=d)
        return df

    def get_df_for_one_page(self, page_number: int) -> pd.DataFrame:
        dfs = []
        item_lists = self.get_item_list_from_soup(page_number)

        for item in item_lists:
            df = self.get_info_from_item(item)
            dfs.append(df)
        df_merge = pd.concat(dfs)
        return df_merge.reset_index(drop=True)

    def run(self) -> pd.DataFrame:
        dfs = []
        for i in range(1, self.num_of_pages + 1):
            dfs.append(ws37.get_df_for_one_page(i))
        return pd.concat(dfs, ignore_index=True)


if __name__ == "__main__":
    ws37 = ws37express()
    df = ws37.run()
    df.to_excel(r"./data/37_express_pricing.xlsx")
