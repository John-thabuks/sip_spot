
import os
import sys
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from colorama import Fore, Style
from models import Customer, Drink, Review, engine

sys.path.append(os.getcwd())

# Data validation dictionary for error messages or codes
error_messages = {
    "invalid_input": "Invalid input. Please enter a valid value.",
    "invalid_integer": "Invalid input. Please enter an integer value.",
    "under_age": "You are underage!! Go home, underage!"
}

def view_customers(session):
    customers = session.query(Customer).all()
    customer_data = [[customer.id, customer.first_name, customer.last_name, customer.age] for customer in customers]
    print(tabulate(customer_data, headers=["ID", "First Name", "Last Name", "Age"], tablefmt="fancy_grid"))

def view_customer_details(session, customer_id):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer:
        print(f"{Fore.BLUE}Name:{Style.RESET_ALL} {customer.first_name} {customer.last_name}")
        print(f"{Fore.BLUE}Age:{Style.RESET_ALL} {customer.age}")
        print(f"{Fore.BLUE}Drinks:{Style.RESET_ALL}")
        for drink in customer.drinks:
            print(f"{Fore.GREEN}- {drink.name}, {drink.price}, Alcohol Content: {drink.alcohol_content}%{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Customer not found.{Style.RESET_ALL}")

def create_customer(session, first_name, last_name, age):
    customer = Customer(first_name=first_name, last_name=last_name, age=age)
    session.add(customer)
    session.commit()
    print(f"{Fore.GREEN}Customer created successfully.{Style.RESET_ALL}")

def delete_customer(session, customer_id):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer:
        session.delete(customer)
        session.commit()
        print(f"{Fore.GREEN}Customer deleted successfully.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Customer not found.{Style.RESET_ALL}")

def create_drink(session, name, price, alcohol_content):
    drink = Drink(name=name, price=price, alcohol_content=alcohol_content)
    session.add(drink)
    session.commit()
    print(f"{Fore.GREEN}Drink created successfully.{Style.RESET_ALL}")

def delete_drink(session, drink_id):
    drink = session.query(Drink).filter(Drink.id == drink_id).first()
    if drink:
        session.delete(drink)
        session.commit()
        print(f"{Fore.GREEN}Drink deleted successfully.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Drink not found.{Style.RESET_ALL}")

def view_reviews(session, customer_id):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer:
        print(f"{Fore.BLUE}Reviews for {customer.first_name} {customer.last_name}:{Style.RESET_ALL}")
        for review in customer.reviews:
            drink = session.query(Drink).filter(Drink.id == review.drink_id).first()
            print(f"{Fore.GREEN}- Drink: {drink.name}, Rating: {review.rating}, Comment: {review.comment}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Customer not found.{Style.RESET_ALL}")

def add_review(session, customer_id, drink_id, rating, comment):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer:
        drink = session.query(Drink).filter(Drink.id == drink_id).first()
        if drink:
            review = Review(customer_id=customer_id, drinks_id=drink_id, rating=rating, comment=comment)
            session.add(review)
            session.commit()
            print(f"{Fore.GREEN}Review added successfully.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Drink not found.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Customer not found.{Style.RESET_ALL}")

def view_drinks(session):
    drinks = session.query(Drink).limit(20).all()
    for drink in drinks:
        print(f"{Fore.BLUE}Drink: {drink.name}, Price: {drink.price}, Alcohol Content: {drink.alcohol_content}%{Style.RESET_ALL}")
        if drink.review:
            print(f"{Fore.GREEN}Reviews:{Style.RESET_ALL}")
            for review in drink.review[:5]:
                customer = session.query(Customer).filter(Customer.id == review.customer_id).first()
                print(f"   - Customer: {customer.first_name} {customer.last_name}, Rating: {review.rating}, Comment: {review.comment}")
        else:
            print(f"{Fore.YELLOW}No reviews available for this drink.{Style.RESET_ALL}")

def get_valid_integer_input(prompt):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print(error_messages["invalid_integer"])

def main():
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("\n" + "-"*50)
        print(f"{Fore.CYAN}Welcome to Drink Review System{Style.RESET_ALL}")
        print("-"*50)
        print("1. View Customers")
        print("2. View Customer Details")
        print("3. Create Customer")
        print("4. Delete Customer")
        print("5. Create Drink")
        print("6. Delete Drink")
        print("7. View Drinks")
        print("8. Add Review")
        print("9. Exit")
        choice = input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")

        if choice == '1':
            view_customers(session)
        elif choice == '2':
            customer_id = get_valid_integer_input(f"{Fore.YELLOW}Enter the customer ID: {Style.RESET_ALL}")
            view_customer_details(session, customer_id)
        elif choice == '3':
            first_name = input(f"{Fore.YELLOW}Enter first name: {Style.RESET_ALL}")
            last_name = input(f"{Fore.YELLOW}Enter last name: {Style.RESET_ALL}")
            age = get_valid_integer_input(f"{Fore.YELLOW}Enter age: {Style.RESET_ALL}")
            create_customer(session, first_name, last_name, age)
        elif choice == '4':
            customer_id = get_valid_integer_input(f"{Fore.YELLOW}Enter customer ID to delete: {Style.RESET_ALL}")
            delete_customer(session, customer_id)
            get_valid_integer_input(f"{Fore.YELLOW}Enter customer ID to delete: {Style.RESET_ALL}")
            delete_customer(session, customer_id)
        elif choice == '5':
            name = input(f"{Fore.YELLOW}Enter drink name: {Style.RESET_ALL}")
            price = input(f"{Fore.YELLOW}Enter drink price: {Style.RESET_ALL}")
            alcohol_content = get_valid_integer_input(f"{Fore.YELLOW}Enter alcohol content: {Style.RESET_ALL}")
            create_drink(session, name, price, alcohol_content)
        elif choice == '6':
            drink_id = get_valid_integer_input(f"{Fore.YELLOW}Enter drink ID to delete: {Style.RESET_ALL}")
            delete_drink(session, drink_id)
        elif choice == '7':
            view_drinks(session)
        elif choice == '8':
            customer_id = get_valid_integer_input(f"{Fore.YELLOW}Enter your customer ID: {Style.RESET_ALL}")
            drink_id = get_valid_integer_input(f"{Fore.YELLOW}Enter the drink ID: {Style.RESET_ALL}")
            rating = get_valid_integer_input(f"{Fore.YELLOW}Enter your rating (1-10): {Style.RESET_ALL}")
            comment = input(f"{Fore.YELLOW}Enter your comment: {Style.RESET_ALL}")
            add_review(session, customer_id, drink_id, rating, comment)
        elif choice == '9':
            print(f"{Fore.CYAN}May your hangover be as short as your memory! Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

        
