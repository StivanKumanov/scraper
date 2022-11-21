from services.JobsBgScraper import JobsBgScraper
from data.repositories.CSVRepository import CSVRepository

repo = CSVRepository()
s = JobsBgScraper(repo)
s.scrape_all_jobs()
