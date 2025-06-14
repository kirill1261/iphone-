from apscheduler.schedulers.background import BackgroundScheduler
from scrap import PriceScraper
from db_setup import PriceTracker

class PriceMonitor:
    def __init__(self):
        self.tracker = PriceTracker()
        self.scheduler = BackgroundScheduler()
        self.stores = {
            'rozetka': 'https://rozetka.com.ua/iphones/',
            'comfy': 'https://comfy.ua/phones/'
        }
    
    def start_monitoring(self):
        for store, url in self.stores.items():
            self.scheduler.add_job(
                self._check_prices,
                'interval',
                hours=12,
                args=[store, url]
            )
        self.scheduler.start()
    
    def _check_prices(self, store, base_url):
        scraper = PriceScraper(base_url, store)
        data = scraper.scrape()
        self.tracker.add_price(
            store=store,
            product_name=data['product_name'],
            product_key=data['product_key'],
            price=data['price'],
            url=data['url']
        )

if __name__ == "__main__":
    monitor = PriceMonitor()
    monitor.start_monitoring()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.scheduler.shutdown()
