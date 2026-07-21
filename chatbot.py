from system_prompt import SYSTEM_PROMPT
from llm_manager import generate_response

from hybrid_router import route_query
from sql_engine import execute_sql
from rag.search import search_documents

from memory import ConversationMemory
from prompt_builder import build_messages

import json
import re

memory = ConversationMemory()
import hybrid_router

print("=" * 60)
print("HYBRID ROUTER FILE:")
print(hybrid_router.__file__)
print("=" * 60)
print(route_query("show shipment 5fd50c5c-973f-43bc-a629-06e4b5cd541b"))


def format_sql_context(result):

    if not result:
        return "No matching database records found."

    context = ""

    # ======================================================
    # SINGLE RECORD
    # ======================================================

    if isinstance(result, dict):

        # ======================================================
        # SHIPMENT
        # ======================================================

        if "shipment_id" in result:

            return f"""
==================================================
SHIPMENT INFORMATION
==================================================

Shipment ID          : {result.get("shipment_id")}
Booking ID           : {result.get("booking_id")}

---------------- BASIC DETAILS ----------------

Shipping Mode        : {result.get("shipping_mode")}
Shipment Type        : {result.get("shipment_type")}
Priority             : {result.get("priority")}

Booking Date         : {result.get("booking_date")}
Ship Date            : {result.get("ship_date")}

---------------- CARGO ----------------

Product             : {result.get("product_name")}
Category            : {result.get("category")}
Supplier            : {result.get("supplier_name")}

Weight              : {result.get("weight_kg")} kg
Volume              : {result.get("volume_cbm")} cbm
Declared Value      : {result.get("declared_value")}

Insurance           : {result.get("insurance")}
Fragile             : {result.get("fragile")}
Hazardous           : {result.get("hazardous")}
Perishable          : {result.get("perishable")}

---------------- CUSTOMER ----------------

Customer            : {result.get("customer_name")}
Customer Type       : {result.get("customer_type")}
Industry            : {result.get("industry")}

---------------- CARRIER ----------------

Carrier             : {result.get("carrier_name")}
Carrier Type        : {result.get("carrier_type")}
Average Rating      : {result.get("average_rating")}
Fleet Size          : {result.get("fleet_size")}

---------------- ROUTE ----------------

Origin              : {result.get("origin_city")}, {result.get("origin_country")}
Destination         : {result.get("destination_city")}, {result.get("destination_country")}

Distance            : {result.get("distance_km")} km
Transit Time        : {result.get("average_transit_days")} days
Route Risk          : {result.get("route_risk")}

---------------- VEHICLE ----------------

Vehicle Number      : {result.get("vehicle_number")}
Vehicle Type        : {result.get("vehicle_type")}
Fuel Type           : {result.get("fuel_type")}

---------------- WAREHOUSE ----------------

Warehouse           : {result.get("warehouse_name")}
Warehouse Type      : {result.get("warehouse_type")}

---------------- WEATHER ----------------

Weather             : {result.get("weather_condition")}
Temperature         : {result.get("temperature")} °C
Humidity            : {result.get("humidity")} %
Wind Speed          : {result.get("wind_speed")} km/h

---------------- DELIVERY ----------------

Delivery Status     : {result.get("delivery_status")}
Expected Delivery   : {result.get("expected_delivery_date")}
Actual Delivery     : {result.get("actual_delivery_date")}
Delay Days          : {result.get("delay_days")}
Delivery Attempts   : {result.get("delivery_attempts")}

---------------- AI PREDICTION ----------------

Risk Level          : {result.get("risk_level")}
Risk Category       : {result.get("risk_category")}
Delay Probability   : {result.get("delay_probability")}

Reason              : {result.get("classification_reason")}
Description         : {result.get("risk_description")}
Recommended Action  : {result.get("recommended_action")}

Alert Status        : {result.get("alert_status")}
Alert Severity      : {result.get("severity")}
"""

        # ======================================================
        # CUSTOMER
        # ======================================================

        if "customer_name" in result:

            return f"""
==================================================
CUSTOMER INFORMATION
==================================================

Customer Name       : {result.get("customer_name")}
Customer Type       : {result.get("customer_type")}
Industry            : {result.get("industry")}

City                : {result.get("city")}
State               : {result.get("state")}
Country             : {result.get("country")}

Registration Date   : {result.get("registration_date")}
Status              : {result.get("customer_status")}
"""

        # ======================================================
        # PRODUCT
        # ======================================================

        if "product_name" in result:

            return f"""
==================================================
PRODUCT INFORMATION
==================================================

Product Name        : {result.get("product_name")}
Category            : {result.get("category")}
HS Code             : {result.get("hs_code")}

Supplier            : {result.get("supplier_name")}

Weight              : {result.get("weight_per_unit")}
Temperature Control : {result.get("temperature_controlled")}

Hazardous           : {result.get("hazardous")}
Fragile             : {result.get("fragile")}
Perishable          : {result.get("perishable")}
"""

        # ======================================================
        # CARRIER
        # ======================================================

        if "carrier_name" in result:

            return f"""
==================================================
CARRIER INFORMATION
==================================================

Carrier Name        : {result.get("carrier_name")}
Carrier Type        : {result.get("carrier_type")}

Fleet Size          : {result.get("fleet_size")}
Average Rating      : {result.get("average_rating")}

Years of Service    : {result.get("years_of_service")}
Headquarters        : {result.get("headquarters")}
"""

        # ======================================================
        # WAREHOUSE
        # ======================================================

        if "warehouse_name" in result:

            return f"""
==================================================
WAREHOUSE INFORMATION
==================================================

Warehouse Name      : {result.get("warehouse_name")}
Warehouse Type      : {result.get("warehouse_type")}

City                : {result.get("city")}
Country             : {result.get("country")}

Capacity            : {result.get("warehouse_capacity")}
Current Utilization : {result.get("current_utilization")} %
"""

        # ======================================================
        # VEHICLE
        # ======================================================

        if "vehicle_number" in result:

            return f"""
==================================================
VEHICLE INFORMATION
==================================================

Vehicle Number      : {result.get("vehicle_number")}
Vehicle Type        : {result.get("vehicle_type")}

Capacity            : {result.get("capacity_kg")} kg
Fuel Type           : {result.get("fuel_type")}

Maintenance Status  : {result.get("maintenance_status")}
Vehicle Age         : {result.get("vehicle_age")} years
"""

        # ======================================================
        # ROUTE
        # ======================================================

        if "origin_city" in result:

            return f"""
==================================================
ROUTE INFORMATION
==================================================

Origin              : {result.get("origin_city")}, {result.get("origin_country")}
Destination         : {result.get("destination_city")}, {result.get("destination_country")}

Origin Port         : {result.get("origin_port")}
Destination Port    : {result.get("destination_port")}

Distance            : {result.get("distance_km")} km
Transit Time        : {result.get("average_transit_days")} days

Traffic Index       : {result.get("traffic_index")}
Risk Level          : {result.get("route_risk")}
"""

        # ======================================================
        # WEATHER
        # ======================================================

        if "weather_condition" in result:

            return f"""
==================================================
WEATHER INFORMATION
==================================================

Forecast Date       : {result.get("forecast_date")}

Condition           : {result.get("weather_condition")}

Temperature         : {result.get("temperature")} °C
Humidity            : {result.get("humidity")} %
Rainfall            : {result.get("rainfall")} mm
Wind Speed          : {result.get("wind_speed")} km/h
Visibility          : {result.get("visibility")} km
"""

        # ======================================================
        # CUSTOMS
        # ======================================================

        if "customs_required" in result:

            return f"""
==================================================
CUSTOMS INFORMATION
==================================================

Destination Country : {result.get("destination_country")}
Cargo Type          : {result.get("cargo_type")}

Customs Required    : {result.get("customs_required")}
Documentation       : {result.get("documentation_complete")}
Inspection Required : {result.get("inspection_required")}
"""

        # ======================================================
        # DELIVERY HISTORY
        # ======================================================

        if (
            "delivery_status" in result
            and "shipment_id" not in result
        ):

            return f"""
==================================================
DELIVERY HISTORY
==================================================

Delivery Status     : {result.get("delivery_status")}

Expected Delivery   : {result.get("expected_delivery_date")}
Actual Delivery     : {result.get("actual_delivery_date")}

Delivery Attempts   : {result.get("delivery_attempts")}

Remarks             : {result.get("remarks")}
"""

        # ======================================================
        # AI FEATURE STORE
        # ======================================================

        if "feature_vector_version" in result:

            return f"""
==================================================
AI FEATURE STORE
==================================================

Shipment ID         : {result.get("shipment_id")}

Feature Version     : {result.get("feature_vector_version")}
Created At          : {result.get("created_at")}
"""

        # ======================================================
        # AI INFERENCE LOG
        # ======================================================

        if "delay_probability" in result:

            return f"""
==================================================
AI INFERENCE RESULT
==================================================

Shipment ID          : {result.get("shipment_id")}

Risk Category        : {result.get("risk_category")}
Delay Probability    : {result.get("delay_probability")}

Prediction Time      : {result.get("prediction_timestamp")}
Latency              : {result.get("latency_ms")} ms
"""

        # ======================================================
        # AI MODEL REGISTRY
        # ======================================================

        if "model_name" in result:

            return f"""
==================================================
AI MODEL INFORMATION
==================================================

Model Name          : {result.get("model_name")}
Version             : {result.get("model_version")}

Deployment Status   : {result.get("deployment_status")}

Accuracy            : {result.get("accuracy")}
F1 Score            : {result.get("f1_score")}
"""

        # ======================================================
        # AI MONITORING ALERTS
        # ======================================================

        if "alert_status" in result:

            return f"""
==================================================
AI ALERT INFORMATION
==================================================

Shipment ID         : {result.get("shipment_id")}

Alert Type          : {result.get("alert_type")}
Severity            : {result.get("severity")}
Status              : {result.get("alert_status")}

Recommended Action  : {result.get("recommended_action")}
Generated At        : {result.get("generated_at")}
"""

    # ======================================================
    # GENERIC DICTIONARY
    # ======================================================

    if isinstance(result, dict):

        context = ""

        for key, value in result.items():

            pretty_key = key.replace("_", " ").title()

            context += f"{pretty_key:<30}: {value}\n"

        return context

    # ======================================================
    # LIST OF RECORDS
    # ======================================================

    if isinstance(result, list):

        if len(result) == 0:
            return "No matching records found."

        output = ""

        for index, row in enumerate(result, start=1):

            output += f"\n========== Record {index} ==========\n"

            if isinstance(row, dict):

                for key, value in row.items():

                    pretty_key = key.replace("_", " ").title()

                    output += f"{pretty_key:<30}: {value}\n"

            else:

                output += str(row) + "\n"

        return output

    # ======================================================
    # STRING
    # ======================================================

    if isinstance(result, str):
        return result

    # ======================================================
    # NUMBER
    # ======================================================

    if isinstance(result, (int, float)):
        return str(result)

    # ======================================================
    # FINAL FALLBACK
    # ======================================================

    try:
        return json.dumps(
            result,
            indent=2,
            default=str
        )

    except Exception:
        return str(result)
   

def chat(user_query):


    if not user_query.strip():
        return {
            "answer": "Please enter a question.",
            "query_type": "NONE",
            "source": "NONE"
        }

    try:
        query_type = route_query(
            user_query,
            memory.last_shipment_id
        )
    except Exception as e:
        print("ROUTER ERROR:", e)
        raise
 
    shipment = re.search(
        r"[0-9a-f]{8}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{12}",
        user_query,
        re.I
    )


    if shipment:
        memory.last_shipment_id = shipment.group()

    follow_up_words = [

        "it",
        "its",
        "this shipment",
        "that shipment",
        "this one",
        "that one",

        "tell me more",
        "more details",
        "more information",

        "why is it",
        "why",
        "how about it",

        "what about it",
        "what about this",

        "explain this",
        "explain it",

        "its carrier",
        "its customer",
        "its warehouse",
        "its vehicle",
        "its route"

    ]

    new_query_words = [

        "show all",
        "list",
        "find",
        "display",
        "count",
        "total",
        "highest",
        "lowest",
        "average",
        "customers",
        "shipments",
        "carriers",
        "routes",
        "warehouses",
        "vehicles",
        "weather",
        "products"

    ]

    if any(word in user_query.lower() for word in new_query_words):

        memory.last_shipment_id = None

    query_lower = user_query.lower()

    is_follow_up = False

    for phrase in follow_up_words:

        if re.search(rf"\b{re.escape(phrase)}\b", query_lower):
            is_follow_up = True
            break

    if is_follow_up and memory.last_shipment_id:

        user_query += (
            f" (referring to shipment {memory.last_shipment_id})"
        )
    context = ""
    source = ""

    # -----------------------------
    # VECTOR
    # -----------------------------

    if query_type == "VECTOR":

        source = "ChromaDB"

        docs = search_documents(user_query)

        MAX_CONTEXT = 1000

        for doc in docs:

            if len(context) >= MAX_CONTEXT:
                break

            context += f"""

==============================
DOCUMENT
==============================

Source:
{doc.get("source", doc["metadata"].get("document_name", "Unknown"))}

Content:
{doc["document"]}

"""
    # -----------------------------
    # SQL
    # -----------------------------

    elif query_type == "SQL":

        source = "PostgreSQL"

        try:
            result = execute_sql(user_query)
            context = f"""
            VERIFIED DATABASE RECORDS

            The following information was retrieved directly from the NexusFreight system.

            This information is authoritative.

            Do NOT modify it.

            Do NOT infer missing values.

            Do NOT replace values.

            Use these records exactly.

            -------------------------

            {format_sql_context(result)}

            -------------------------

            End of verified records.
            """
        except Exception as e:
            print(e)
            context = f"Database query failed: {e}"

    # -----------------------------
    # HYBRID
    # -----------------------------

    elif query_type == "HYBRID":

        source = "Hybrid"

        sql_result = execute_sql(user_query)

        docs = search_documents(user_query)

        context = ""

        if sql_result:

            context += format_sql_context(sql_result)

        MAX_CONTEXT = 1000

        for doc in docs:

            if len(context) >= MAX_CONTEXT:
                break

            context += f"""

    ==============================
    DOCUMENT
    ==============================

    Source:
    {doc.get("source", doc["metadata"].get("document_name", "Unknown"))}

    Content:
    {doc["document"]}

    """


    memory.add_user(user_query)

    history = memory.get_recent_messages()

    messages = build_messages(
        system_prompt=SYSTEM_PROMPT,
        summary=memory.summary,
        history=history,
        rag_context=context,
        current_query=user_query
    )

    print("\n========== PROMPT DEBUG ==========")

    total = 0

    for m in messages:
        size = len(m["content"])
        total += size
        print(m["role"], ":", size)

    print("TOTAL CHARACTERS:", total)
    print("=================================\n")

    print("\n==============================")
    print("FINAL SQL CONTEXT SENT TO LLM")
    print("==============================")
    print(context)
    print("==============================")

    answer = generate_response(messages)
    print("\n========== LLM ANSWER ==========")
    print(answer)
    print("================================")

    memory.add_assistant(answer)

    if memory.need_summary():
        memory.summarize()

    return {

        "answer": answer,

        "query_type": query_type,

        "source": source

    }

if __name__ == "__main__":

    print("=" * 60)
    print(" NexusFreight Logistics AI Assistant ")
    print("=" * 60)

    while True:

        query = input("\nYou : ")

        if query.lower() == "exit":
            break

        result = chat(query)

        print()

        print("Bot :", result["answer"])
        print("Source :", result["source"])
        print("Query Type :", result["query_type"])