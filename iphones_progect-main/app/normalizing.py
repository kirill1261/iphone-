import re
from dataclasses import dataclass

@dataclass
class ProductInfo:
    brand: str
    model: str
    storage: str
    color: str

class ProductNormalizer:
    def __init__(self, raw_name):
        self.raw_name = raw_name
        self._normalize()
    
    def _normalize(self):
        name = self.raw_name.lower()
        name = re.sub(r'\(.*?\)', '', name)  # Удаляем скобки
        
        # Извлекаем компоненты
        self.product_info = ProductInfo(
            brand=self._extract_brand(name),
            model=self._extract_model(name),
            storage=self._extract_storage(name),
            color=self._extract_color(name)
        )
        
        self.normalized_name = f"{self.product_info.brand} {self.product_info.model}"
        self.product_key = f"{self.product_info.brand}_{self.product_info.model}"
    
    def _extract_brand(self, name):
        if 'apple' in name or 'iphone' in name:
            return 'Apple'
        return 'Unknown'
    
    # Другие методы извлечения...
