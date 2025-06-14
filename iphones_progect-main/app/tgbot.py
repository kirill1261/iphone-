from telebot import TeleBot
from db_setup import PriceTracker

class PriceBot:
    def __init__(self, token):
        self.bot = TeleBot(token)
        self.tracker = PriceTracker()
        self._register_handlers()
    
    def _register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.reply_to(message, "Введите модель телефона для поиска лучшей цены")
        
        @self.bot.message_handler(content_types=['text'])
        def handle_search(message):
            results = self.tracker.search_products(message.text)
            if results:
                response = self._format_response(results)
            else:
                response = "Ничего не найдено"
            self.bot.reply_to(message, response)
    
    def _format_response(self, products):
        # Форматирование ответа
        pass
    
    def run(self):
        self.bot.polling()

if __name__ == "__main__":
    bot = PriceBot('YOUR_TOKEN')
    bot.run()
