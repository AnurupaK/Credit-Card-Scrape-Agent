from crewai import Crew, Process
from .tasks import credit_card_task  
from .agents import credit_card_miner
from modules.credit_card_links import ExtractLinks

# Class to handle scraping and processing of credit card information in batches
class CardScrape:
    def __init__(self, all_links, start_batch_size=0, stop_batch_size=5):
        self.all_links = all_links
        self.start = start_batch_size
        self.stop = stop_batch_size

    # Run scraping in batches
    def _run_batch(self, urls):
        results = {}
        for url in urls:
            task = credit_card_task(url)
            crew = Crew(
                agents=[credit_card_miner],
                tasks=[task],
                process=Process.sequential,
            )
            result = crew.kickoff()
            results[url] = result
        return results

    # Execute the scraping for a given batch
    def execute(self):
        total_links = len(self.all_links)
        print(f'🔗 Total links available: {total_links}')

        batch = self.all_links[self.start:self.stop]
        if not batch:
            print(f"🚫 No more links to process between {self.start} and {self.stop}.")
            return {}

        print(f"\n🔍 Running batch from index {self.start} to {self.stop - 1} ({len(batch)} links)\n")
        batch_results = self._run_batch(batch)

        return batch_results

if __name__ == "__main__":
    batch_size = 5
    start = 0
    stop = batch_size

    extractor = ExtractLinks(url='https://www.sbicard.com/en/personal/credit-cards.page')
    all_links = extractor.do_extraction()

    if not all_links:
        print("❌ No links found. Exiting.")
        exit()

    while True:
        scraper = CardScrape(
            all_links=all_links,
            start_batch_size=start,
            stop_batch_size=stop
        )
        data = scraper.execute()

        if not data:
            print("🛑 Ending batch loop — no more data.")
            break

        cont = input("\nDo you want to run the next batch? (y/n): ").lower()
        if cont != 'y':
            break
        else:
            start += batch_size
            stop += batch_size
