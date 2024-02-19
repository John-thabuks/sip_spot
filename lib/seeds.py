from faker import Faker
from sqlalchemy.orm import sessionmaker
from models import engine, BASE, Customer, Drink, Review, customer_drinks

# Create an instance of Faker
fake = Faker()

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

def create_customers():
    # Generate and insert fake customer data into the customers table
    for _ in range(50):  # Generate 10 customers
        customer = Customer(
            first_name=fake.unique.first_name(),
            last_name=fake.unique.last_name(),
            age=fake.random_int(min=18, max=90)
        )
        session.add(customer)
    session.commit()

def create_drinks():
    # Generate and insert fake drink data into the drinks table
    for _ in range(10):  # Generate 5 drinks
        drink = Drink(
            name=fake.word(),
            price=fake.random_number(digits=3),
            alcohol_content=fake.random_int(min=10, max=45)
        )
        session.add(drink)
    session.commit()

def create_reviews():
    # Generate and insert fake review data into the reviews table
    customers = session.query(Customer).all()
    drinks = session.query(Drink).all()

    for customer in customers:
        for drink in drinks:
            review = Review(
                customer_id=customer.id,
                drinks_id=drink.id,
                comment=fake.sentence(),
                rating=fake.random_int(min=1, max=5)
            )
            session.add(review)
    session.commit()

def associate_customers_and_drinks():
    # Associate customers with drinks in the customer_drinks table
    customers = session.query(Customer).all()
    drinks = session.query(Drink).all()

    # for customer in customers:
    #     # Assign a random number of drinks to each customer
    #     num_drinks = fake.random_int(min=1, max=10)
    #     for _ in range(num_drinks):
    #         drink = fake.random_element(drinks)
    #         customer.drinks.append(drink)
    # session.commit()


    # Retrieve all customers and drinks
    customers = session.query(Customer).all()
    drinks = session.query(Drink).all()

    for customer in customers:
        # Assign a random number of drinks to each customer
        num_drinks = fake.random_int(min=1, max=10)
        # Shuffle the list of drinks
        fake.random.shuffle(drinks)
        for drink in drinks[:num_drinks]:
            customer.drinks.append(drink)
    session.commit()


if __name__ == "__main__":
    BASE.metadata.create_all(engine)  # Create tables if they don't exist
    create_customers()
    create_drinks()
    create_reviews()
    associate_customers_and_drinks()
