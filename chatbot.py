from groq import Groq
import re

from config import GROQ_API_KEY
from system_prompt import SYSTEM_PROMPT

from rag.retriever import *

# ----------------------------
# Initialize Groq
# ----------------------------

client = Groq(api_key=GROQ_API_KEY)


# ----------------------------
# Chat Function
# ----------------------------

def chat(user_query):

    # Empty Input
    if not user_query.strip():
        return "Please enter a question."

    query = user_query.lower()

    context = ""

    # ====================================================
    # Shipment ID
    # ====================================================

    shipment_match = re.search(r"SHP\d+", user_query.upper())

    if shipment_match:

        shipment_id = shipment_match.group()

        shipment = get_shipment(shipment_id)

        if shipment is None:
            return f"Shipment ID {shipment_id} was not found."

        tracking = get_tracking(shipment_id)

        context += f"""

Shipment Details

{shipment}

Tracking Details

{tracking}

"""

    # ====================================================
    # Latest Shipments
    # ====================================================

    elif "latest" in query and "shipment" in query:

        number = re.search(r"\d+", query)

        limit = 5

        if number:
            limit = int(number.group())

        shipments = get_latest_shipments(limit)

        context += f"""

Latest {limit} Shipments

{shipments}

"""

    # ====================================================
    # Show All Shipments
    # ====================================================

    elif "all shipments" in query:

        shipments = get_all_shipments()

        context += f"""

All Shipments

{shipments}

"""

    # ====================================================
    # Delivered Shipments
    # ====================================================

    elif "delivered shipment" in query:

        shipments = get_shipments_by_status("Delivered")

        context += f"""

Delivered Shipments

{shipments}

"""

    # ====================================================
    # Pending Shipments
    # ====================================================

    elif "pending shipment" in query:

        shipments = get_shipments_by_status("Pending")

        context += f"""

Pending Shipments

{shipments}

"""

    # ====================================================
    # In Transit Shipments
    # ====================================================

    elif "transit" in query:

        shipments = get_shipments_by_status("In Transit")

        context += f"""

In Transit Shipments

{shipments}

"""

    # ====================================================
    # Delayed Shipments
    # ====================================================

    elif "delayed" in query:

        shipments = get_shipments_by_status("Delayed")

        context += f"""

Delayed Shipments

{shipments}

"""

    # ====================================================
    # Shipment Count
    # ====================================================

    elif "how many shipments" in query or "count shipment" in query:

        total = count_shipments()

        context += f"""

Total Shipments : {total}

"""

    # ====================================================
    # Delivered Count
    # ====================================================

    elif "how many delivered" in query:

        total = count_shipments_by_status("Delivered")

        context += f"""

Delivered Shipments : {total}

"""

    # ====================================================
    # Pending Count
    # ====================================================

    elif "how many pending" in query:

        total = count_shipments_by_status("Pending")

        context += f"""

Pending Shipments : {total}

"""

    # ====================================================
    # Carrier Search
    # ====================================================

    elif "blue dart" in query:

        shipments = get_shipments_by_carrier("Blue Dart")

        context += f"""

Blue Dart Shipments

{shipments}

"""

    elif "delhivery" in query:

        shipments = get_shipments_by_carrier("Delhivery")

        context += f"""

Delhivery Shipments

{shipments}

"""

    elif "dtdc" in query:

        shipments = get_shipments_by_carrier("DTDC")

        context += f"""

DTDC Shipments

{shipments}

"""

    elif "xpressbees" in query:

        shipments = get_shipments_by_carrier("XpressBees")

        context += f"""

XpressBees Shipments

{shipments}

"""

    # ====================================================
    # Order ID
    # ====================================================

    elif re.search(r"ORD\d+", user_query.upper()):

        order_id = re.search(r"ORD\d+", user_query.upper()).group()

        order = get_order(order_id)

        if order is None:
            return f"Order ID {order_id} was not found."

        context += f"""

Order Details

{order}

"""

    # ====================================================
    # All Orders
    # ====================================================

    elif "all orders" in query:

        orders = get_all_orders()

        context += f"""

All Orders

{orders}

"""

    # ====================================================
    # Pending Orders
    # ====================================================

    elif "pending orders" in query:

        orders = get_orders_by_status("Pending")

        context += f"""

Pending Orders

{orders}

"""

    # ====================================================
    # Delivered Orders
    # ====================================================

    elif "delivered orders" in query:

        orders = get_orders_by_status("Delivered")

        context += f"""

Delivered Orders

{orders}

"""

    # ====================================================
    # Completed Orders
    # ====================================================

    elif "completed orders" in query:

        orders = get_orders_by_status("Completed")

        context += f"""

Completed Orders

{orders}

"""

    # ====================================================
    # Orders by City
    # ====================================================

    elif "orders for" in query:

        city = user_query.lower().split("orders for")[-1].strip()

        orders = get_orders_by_city(city)

        context += f"""

Orders for {city}

{orders}

"""

    # ====================================================
    # Total Orders
    # ====================================================

    elif "how many orders" in query:

        total = count_orders()

        context += f"""

Total Orders : {total}

"""

    # ====================================================
    # Warehouse
    # ====================================================

    elif re.search(r"WH\d+", user_query.upper()):

        warehouse_id = re.search(r"WH\d+", user_query.upper()).group()

        warehouse = get_warehouse(warehouse_id)

        if warehouse is None:
            return f"Warehouse {warehouse_id} was not found."

        context += f"""

Warehouse Details

{warehouse}

"""

    # ====================================================
    # All Warehouses
    # ====================================================

    elif "all warehouses" in query:

        warehouses = get_all_warehouses()

        context += f"""

Warehouses

{warehouses}

"""

    # ====================================================
    # Tracking
    # ====================================================

    elif "tracking" in query:

        shipment = re.search(r"SHP\d+", user_query.upper())

        if shipment:

            tracking = get_tracking(shipment.group())

            context += f"""

Tracking Details

{tracking}

"""

    # ====================================================
    # FAQs
    # ====================================================

    elif "faq" in query:

        faq = get_faq()

        context += f"""

Frequently Asked Questions

{faq}

"""

    # ====================================================
    # FAQ Search
    # ====================================================

    elif "policy" in query or "customs" in query or "delivery" in query:

        faq = search_faq(user_query)

        context += f"""

FAQ Search Results

{faq}

"""

    # ====================================================
    # Default
    # ====================================================

    else:

        context = """
No structured data was found for this query.

Answer only if the information is available in the knowledge base.
Otherwise politely say the information is unavailable.
"""

    # ====================================================
    # Final Prompt
    # ====================================================

    prompt = f"""
{SYSTEM_PROMPT}

Knowledge Base Context

{context}

User Question

{user_query}
"""

    # ====================================================
    # Call Groq LLM
    # ====================================================

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2

        )

        return response.choices[0].message.content

    # ====================================================
    # Error Handling
    # ====================================================

    except Exception as e:

        error = str(e)

        if "401" in error or "api_key" in error.lower():
            return "Invalid Groq API Key."

        elif "timeout" in error.lower():
            return "Request timed out. Please try again."

        elif "connection" in error.lower():
            return "Unable to connect to the database."

        else:
            return f"Unexpected Error : {error}"


# ====================================================
# Terminal Chat
# ====================================================

if __name__ == "__main__":

    print("=" * 55)
    print("      NexusFreight Logistics AI Assistant")
    print("=" * 55)
    print("Ask logistics-related questions.")
    print("Type 'exit' to quit.")
    print("=" * 55)

    while True:

        query = input("\nYou : ")

        if query.strip() == "":
            print("\nBot : Please enter a question.")
            continue

        if query.lower() == "exit":
            print("\nBot : Goodbye! Have a great day.")
            break

        answer = chat(query)

        print("\nBot :", answer)