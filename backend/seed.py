
from backend.database import SessionLocal, Customer, Order, Lead


def seed_data():
    db = SessionLocal()

    try:
        # 1. Create customers if they don't exist
        customers = [
            ("Rahul", "rahul@gmail.com"),
            ("Priya", "priya@gmail.com")
        ]

        customer_records = {}

        for name, email in customers:
            customer = db.query(Customer).filter_by(email=email).first()

            if not customer:
                customer = Customer(name=name, email=email)
                db.add(customer)
                db.flush()

            customer_records[email] = customer

        # 2. Create orders if they don't exist
        orders = [
            ("rahul@gmail.com", "Shipped", 1499.0),
            ("priya@gmail.com", "Processing", 2499.0)
        ]

        for email, status, amount in orders:
            customer = customer_records[email]

            existing_order = db.query(Order).filter_by(
                customer_id=customer.customer_id,
                status=status,
                amount=amount
            ).first()

            if not existing_order:
                db.add(Order(
                    customer_id=customer.customer_id,
                    status=status,
                    amount=amount
                ))

        # 3. Create leads if they don't exist
        leads = [
            ("Arjun", "arjun@gmail.com", "Website"),
            ("Sneha", "sneha@gmail.com", "LinkedIn")
        ]

        for name, email, source in leads:
            existing_lead = db.query(Lead).filter_by(email=email).first()

            if not existing_lead:
                db.add(Lead(
                    name=name,
                    email=email,
                    source=source
                ))

        db.commit()
        print("COLC AI synthetic data seeded successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
