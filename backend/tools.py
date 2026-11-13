from database import SessionLocal, Customer, Order, Lead
from sqlalchemy.exc import SQLAlchemyError

def get_customer(customer_id):
  db = SessionLocal()
  get = None
  try:
   customers = db.query(Customer).filter(Customer.customer_id == customer_id).first()
   if customers:
      get = {"customer_id": customers.customer_id, "name":customers.name, "email":customers.email}
  finally:
    db.close()
  return get
customer = get_customer(1)
print(get_customer(1))
#print(get_customer(999))

def get_order(order_id):
   db = SessionLocal()
   get = None
   try:
      orders = db.query(Order).filter(Order.order_id == order_id).first()
      if orders:
       get = {"order_id": orders.order_id, "customer_id": orders.customer_id, "status": orders.status, "amount": orders.amount}
   finally:
      db.close()
   return get
print(get_order(1))

def get_lead(lead_id):
   db = SessionLocal()
   get = None
   try:
      leads = db.query(Lead).filter(Lead.lead_id == lead_id).first()
      if leads:
       get = {"lead_id": leads.lead_id, "name": leads.name,"email": leads.email, "source": leads.source}
   finally:
      db.close()
   return get
print(get_lead(1))

def calculator(a,b,operation):
  try: 
   if operation == "add":
    return a + b
   elif operation == "subtract":
    return a - b
   elif operation == "multiply":
    return a * b
   elif operation == "divide":
    return a / b
   else:
     return "Invalid operation"
  except ZeroDivisionError:
    return 'Cannot divisible by zero'
print(calculator(1,2,"add"))

def create_lead(name, email, source):
 get = None
 db = SessionLocal()
 try:
  leads = Lead(name=name, email=email, source=source)
  db.add(leads)
  db.commit()
  get = {"lead_id": leads.lead_id, "name": leads.name,"email": leads.email, "source": leads.source}
 except SQLAlchemyError:
   {"error": "Email already exists"}
   db.rollback()
 finally:
   db.close()
 return get

print(create_lead("Amit","amit@gmail.com","LinkedIn"))
print(create_lead("Amit","amit@gmail.com","LinkedIn"))

  

  
  
