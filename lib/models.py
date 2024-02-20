from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Table, create_engine, ForeignKey
from sqlalchemy.orm import relationship,sessionmaker
from faker import Faker



BASE = declarative_base()
engine = create_engine("sqlite:///db/member_club.db")
Session = sessionmaker(bind=engine)
session = Session()


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

    #Find customer favourite beer
    def favaorite_drink(self):
        customer_reviews = self.reviews
        sorted_reviews = sorted(customer_reviews, key= lambda review: review.rating)
        print(sorted_reviews)
        print(sorted_reviews[-1])
        return sorted_reviews[-1]


    #customer should add a review
    def customer_new_review(self, drink, rating, comment):
         
        customer_identity = session.query(Customer).filter_by(first_name=self.first_name).first()
        if customer_identity is None:
            print("Customer not found.")
            return False

        # Create and add the review
        customer_review = Review(
            drinks_id=drink.id,
            customer_id=customer_identity.id,
            rating=rating,
            comment=comment
        )
        session.add(customer_review)
        session.commit()
        return True




    #find favourite drink


    #customer should delete a review


class Drink(BASE):
    
    __tablename__ = "drinks"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(String())
    alcohol_content = Column(Integer())

    customers = relationship("Customer", secondary=customer_drinks, back_populates="drinks")
    review = relationship("Review", backref="virtual_drinks", cascade=("all, delete"))

    #find best rated drink

    #find all reviews

class Review(BASE):
    
    __tablename__ = "reviews"

    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer(), ForeignKey("customers.id"))
    drinks_id = Column(Integer(), ForeignKey("drinks.id"))
    comment = Column(String())
    rating = Column(Integer(), nullable=False)


   # give a full review








