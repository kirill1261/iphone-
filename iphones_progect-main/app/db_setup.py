from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class ProductPrice(Base):
    __tablename__ = 'product_prices'
    
    id = Column(Integer, primary_key=True)
    store = Column(String(50))
    product_name = Column(String(255))
    product_key = Column(String(255), unique=True)
    price = Column(Float)
    date = Column(DateTime, default=datetime.now)
    url = Column(String(500))

class PriceTracker:
    def __init__(self, db_path="sqlite:///settings/stores.db"):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def add_price(self, store, product_name, product_key, price, url):
        session = self.Session()
        try:
            new_price = ProductPrice(
                store=store,
                product_name=product_name,
                product_key=product_key,
                price=price,
                url=url
            )
            session.add(new_price)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_lowest_price(self, product_key):
        session = self.Session()
        try:
            result = session.query(ProductPrice)\
                .filter_by(product_key=product_key)\
                .order_by(ProductPrice.price)\
                .first()
            return result
        finally:
            session.close()
