from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Float, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    author = Column(String(40), nullable=False)
    price = Column(Float, nullable=False)

    def __str__(self):
        return f'Book title:{self.title}; Author: {self.author}; Price: {self.price}'
    
engine = create_engine('sqlite:///books.db', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()





book1 = Books(title='Python', author='Guido van Rossum', price=100.0)
session.add(book1)
session.commit()

book2 = Books(title='Calculus', author='Newton', price=200.0)
session.add(book2)
session.commit()

result = session.query(Books).all()
for row in result:
    print(row)