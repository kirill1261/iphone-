from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests

class ScraperStrategy(ABC):
    @abstractmethod
    def extract_data(self, soup):
        pass

class RozetkaScraper(ScraperStrategy):
    def extract_data(self, soup):
        name = soup.find("meta", property="og:title")["content"]
        price_tag = soup.find("p", class_="product-price__big")
        price = float(price_tag.text.strip().replace(" ", "").replace("₴", ""))
        return {"name": name, "price": price}

class ComfyScraper(ScraperStrategy):
    def extract_data(self, soup):
        script = soup.find("script", type="application/ld+json")
        data = json.loads(script.string)
        return {
            "name": data["name"],
            "price": float(data["offers"]["price"])
        }

class PriceScraper:
    def __init__(self, url, store):
        self.url = url
        self.store = store
        self.strategies = {
            "rozetka": RozetkaScraper(),
            "comfy": ComfyScraper()
        }
    
    def scrape(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        if self.store not in self.strategies:
            raise ValueError(f"No strategy for store: {self.store}")
            
        data = self.strategies[self.store].extract_data(soup)
        normalizer = ProductNormalizer(data["name"])
        return {
            "product_name": normalizer.normalized_name,
            "product_key": normalizer.product_key,
            "price": data["price"],
            "url": self.url
        }
