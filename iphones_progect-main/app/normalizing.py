import re
from typing import Tuple, Optional

class ProductNormalizer:
    BRAND_SYNONYMS = {
        'apple': 'Apple',
        'samsung': 'Samsung',
        'xiaomi': 'Xiaomi'
    }
    
    COLOR_SYNONYMS = {
        'гб': 'gb',
        'синій': 'blue',
        'чорний': 'black',
        # ... другие синонимы
    }
    
    @classmethod
    def normalize_name(cls, raw_name: str) -> Tuple[str, Optional[dict]]:
        """Нормализует название продукта и извлекает атрибуты"""
        name = raw_name.lower()
        
        # Удаление лишних слов
        for word in ['смартфон', 'мобильный телефон', 'купить']:
            name = name.replace(word, '')
            
        # Извлечение бренда
        brand = None
        for brand_synonym, normalized_brand in cls.BRAND_SYNONYMS.items():
            if brand_synonym in name:
                brand = normalized_brand
                name = name.replace(brand_synonym, '')
                break
                
        # Дальнейшая обработка...
        return normalized_name, {
            'brand': brand,
            'model': extracted_model,
            'storage': storage,
            'color': color
        }
