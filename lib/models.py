from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Table, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from faker import Faker



BASE = declarative_base()
engine = create_engine("sqlite:///db/member_club.db")

#We define variable name as: customer_drinks
customer_drinks = Table(
    #name of table: customer_drinks
        "customer_drinks",
        #Links table with metadata object BASE
        BASE.metadata,
        #column names: "customer_id" , "drink_id"
        #All should have primary_key
        #rows filled with ForeignKeys
        Column("customer_id", ForeignKey("customers.id"), primary_key=True),
        Column("drink_id", ForeignKey("drinks.id"), primary_key=True), 
        extend_existing=True
    )

class Customer(BASE):
    #table named: customers
    __tablename__ = "customers"

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    age = Column(Integer())

    #many to many relationship: (class to relate to, join table, virtual table to relate to drinks)
    drinks = relationship("Drink", secondary=customer_drinks, back_populates="customers") 
    #One to many relationship; (class to relate to, virtual column, delete chirld when parent deleted)
    reviews = relationship("Review", backref="virtual_customer", cascade=("all, delete"))


class Drink(BASE):
    
    __tablename__ = "drinks"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(String())
    alcohol_content = Column(Integer())

    customers = relationship("Customer", secondary=customer_drinks, back_populates="drinks")
    review = relationship("Review", backref="virtual_drinks", cascade=("all, delete"))


class Review(BASE):
    
    __tablename__ = "reviews"

    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer(), ForeignKey("customers.id"))
    drinks_id = Column(Integer(), ForeignKey("drinks.id"))
    comment = Column(String())
    rating = Column(Integer(), nullable=False)










