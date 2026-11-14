from backend.database import SessionLocal, Customer, Order, Lead
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

def get_customer(customer_id: int = None,name: str = None,email: str = None):
  db = SessionLocal()
  get = None
  try:
   conditions = []

   if customer_id is not None:
      conditions.append(Customer.customer_id == customer_id)

   if name:
      conditions.append(Customer.name == name)

   if email:
      conditions.append(Customer.email == email)

   if not conditions:
      return None
   customers = db.query(Customer).filter(or_(*conditions)).first()
   if customers:
      get = {"customer_id": customers.customer_id, "name":customers.name, "email":customers.email}
  finally:
    db.close()
  print("Database customers:", db.query(Customer).count())
  print("Searching for:", repr(name))
  print("Direct match:", db.query(Customer).filter(Customer.name == "Priya").first())
  return get
customer = get_customer(1)
#print(get_customer(1))
#print(get_customer(999))
print(get_customer(name="priya"))
print(get_customer(email="priya@gmail.com")) 
print(get_customer(name="Rahul"))
print("customer:",get_customer(name="Priya"))

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
#print(get_order(1))

def get_lead(lead_id: int = None, name: str = None, email: str = None, source: str = None):
   db = SessionLocal()
   get = None
   try:
        conditions = []

        if lead_id is not None:
            conditions.append(Lead.lead_id == lead_id)
        if name:
            conditions.append(Lead.name == name)

        if email:
            conditions.append(Lead.email == email)
        if source:
          conditions.append(Lead.source == source)
        if not conditions:
            return None

        leads = db.query(Lead).filter(or_(*conditions)).first()
        if leads:
         get = {"lead_id": leads.lead_id, "name": leads.name,"email": leads.email, "source": leads.source}
   finally:
      db.close()
   return get
#print(get_lead(1))

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
#print(calculator(1,2,"add"))

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

#print(create_lead("Amit","amit@gmail.com","LinkedIn"))
#print(create_lead("Amit","amit@gmail.com","LinkedIn"))

  
db = SessionLocal()

customers = db.query(Customer).all()

for c in customers:
    print(c.customer_id, c.name, c.email)

db.close()

def count_records(entity: str):
    db = SessionLocal()

    models = {
        "customers": Customer,
        "leads": Lead,
        "orders": Order
    }

    try:
        if entity not in models:
            return {"error": "Invalid entity"}

        total = db.query(models[entity]).count()

        return {
            "entity": entity,
            "total": total
        }

    finally:
        db.close()
