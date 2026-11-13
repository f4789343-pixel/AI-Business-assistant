from database import SessionLocal, Customer, Order, Lead

def seed_customers():
 try:
  db = SessionLocal()
  customer1 = Customer(name="Rahul", email="rahul@gmail.com")
  customer2 = Customer(name='Priya', email="priya@gmail.com")
  db.add_all([customer1, customer2])
  db.commit()
 finally:
  db.close()
 

#customers = db.query(Customer).all()
#for customer in customers:
 #print(customer.customer_id, customer.name, customer.email)
def seed_orders():
 try:
  db = SessionLocal()
  order1 = Order(customer_id=1, status="Shipped", amount=1499.0)
  order2 = Order(customer_id=2, status="Processing", amount=2499.0)
  db.add_all([order1,order2])
  db.commit()
  orders = db.query(Order).all()
  for order in orders:
   print(order.order_id, order.customer_id, order.status, order.amount)
 finally:
  db.close()
 return 

print(seed_orders())

def seed_lead():
 try:
  db = SessionLocal()
  lead1 = Lead(name="Arjun", email="arjun@gmail.com", source="Website")
  lead2 = Lead(name="Sneha", email="sneha@gmail.com", source="LinkedIn")
  db.add_all([lead1, lead2])
  db.commit()
  leads = db.query(Lead).all()
  for lead in leads:
    print(lead.lead_id, lead.name, lead.email, lead.source)
 finally:
  db.close()
 return 

print(seed_lead())