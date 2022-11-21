from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from services.repositories.BaseRepository import BaseRepository
import re


class JobsBgScraper:

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def scrape_all_jobs(self):
        driver = webdriver.Chrome()
        driver.get("https://www.jobs.bg/front_job_search.php")
        jobs_data = []
        while True:
            self._scroll_to_unscraped_jobs(driver)
            html = driver.page_source
            bs = BeautifulSoup(html, "html.parser")
            jobs = bs.find_all("li", {"class": re.compile("\d")})
            for job in jobs:
                job_data = self._extract_job_data(job)
                jobs_data.append(job_data)

            # TODO: define break condition
            break
        print(jobs_data)
        self.repository.add(jobs_data)

    def _get_page_numbers(self, html):
        regex = r"page-(\d+)"
        page_numbers = {int(x) for x in re.findall(regex, html)}
        return page_numbers

    def _scroll_to_unscraped_jobs(self, driver):
        body = driver.find_element(By.TAG_NAME, "body")
        html = driver.page_source
        initial_page_numbers = self._get_page_numbers(html)
        target_page_numbers = {1, 2, 3}

        if initial_page_numbers != {1, 2}:
            number_of_rendered_pages = 3
            target_page_numbers = {x + number_of_rendered_pages for x in initial_page_numbers}
        current_page_numbers = []
        while current_page_numbers != target_page_numbers:
            body.send_keys(keys.Keys.PAGE_DOWN)
            html = driver.page_source
            current_page_numbers = self._get_page_numbers(html)

    def _extract_job_data(self, job):
        job_data_element = job.find("div", {"class": "left"})
        job_title = job_data_element.a["title"]
        job_link = job_data_element.a["href"]
        job_id = int(job_link.split("/")[-1])
        job_description = job_data_element.find("div", class_="card-info").contents[0]

        company_data_element = job.find("div", {"class": "right"})
        company_link = company_data_element.a["href"]
        company_id = re.findall(r"https:\/\/www.jobs.bg\/company\/(.+)\?job=\d+", company_link)[0]
        company_name = company_data_element.a["title"]

        extracted_data = {
            "job_title": job_title,
            "job_link": job_link,
            "job_id": job_id,
            "job_description": job_description,
            "company_name": company_name,
            "company_id": company_id
        }
        return extracted_data