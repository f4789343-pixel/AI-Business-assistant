from tools import get_customer, get_order, get_lead, calculator, create_lead
import os
from sqlalchemy.exc import SQLAlchemyError
from openai import OpenAI
from dotenv import load_dotenv
import time
import json

load_dotenv()

model = "liquid/lfm-3-1.7b:free"
start = time.perf_counter()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url=os.getenv("OPENROUTER_BASE_URL"))

customer_schema = {"type":"function", "function":{"name": "get_customer", "description": "Retrieve customer details using customer ID", 
         "parameters":{"type":"object","properties":{"customer_id":{"type":"integer","description":"Retrieve customer details using customer ID"}},
                       "required":["customer_id"]}}}

order_schema = {"type":"function", "function":{"name":"get_order", "description":"Retrieve order details by using order ID",
         "parameters":{"type":"object","properties":{"order_id":{"type":"integer","description":"Retrieve order details using order ID"}},"required":["order_id"]}}}

lead_schema = {"type":"function", "function":{"name": "get_lead", "description": "Retrieve lead details using lead ID", 
               "parameters":{"type":"object", "properties":{"lead_id":{"type":"integer", "description":"Retrieve lead details using lead ID"}}, "required":["lead_id"]}}}

calculator_schema = {"type":"function", "function":{"name": "calculator", "description": "Perform basic arithmetic operations on two numbers.", 
                   "parameters":{"type":"object","properties":{"a":{"type":"number"}, "b":{"type":"number"}, 
                    "operation":{"type":"string", "enum": ["add", "subtract", "multiply", "divide"]}}, "required":["a","b","operation"]}}}

create_lead_schema = {"type":"function", "function":{"name": "create_lead", "description":"Create a new business lead with name, email, and source.", 
                     "parameters":{"type":"object", "properties":{"name":{"type":"string"}, "email":{"type":"string"},
                      "source":{"type":"string"}},"required":["name", "email","source"]}}}

start = time.perf_counter()

messages = [{"role": "user", "content": "Find order number 2 and tell me the name and email address of the customer who placed it"}]
response = client.chat.completions.create(model=model, messages=messages,
        tools = [customer_schema,order_schema,lead_schema,calculator_schema,create_lead_schema])
tool_calls = response.choices[0].message.tool_calls


mapping = {"get_customer": get_customer, "get_order": get_order, "get_lead": get_lead, 
           "calculator": calculator, "create_lead": create_lead}
while tool_calls:
 messages.append(response.choices[0].message)
 for tool_call in tool_calls:
   try:
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    print(function_name, arguments)
    if function_name not in mapping:
     tool_results = {"error": "Invalid function name"}
    else:
     function_to_call = mapping[function_name]
     try:
       tool_results = function_to_call(**arguments)
     except SQLAlchemyError:
          tool_results = {"error": "Database operation failed"}
     except Exception:
        tool_results = {"error": "Unexpected tool execution error"}
   except json.JSONDecodeError:
    tool_results = {"error": "Invalid JSON arguments"}
   tools = {"role": "tool", "tool_call_id": tool_call.id, "content":json.dumps(tool_results)}
   messages.append(tools)
 response = client.chat.completions.create(model=model, messages=messages, 
                  tools = [customer_schema,order_schema,lead_schema,calculator_schema,create_lead_schema])
 tool_calls = response.choices[0].message.tool_calls
end = time.perf_counter()
print(response.choices[0].message.content)
print(f"execution time: {end - start:.2f}s")