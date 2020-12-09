import concurrent.futures
from web_scraper.scrapper_support import SuggestionUpdater

def start_threads(self):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executer:
        suggestion_workers = {executer.submit(self.update_suggestions_workers): worker for worker in range(10)}

def update_suggestions_workers(self):
    suggestionUpdater = SuggestionUpdater()
    suggestionUpdater.start_up()
