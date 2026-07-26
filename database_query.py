import os
from dotenv import load_dotenv
load_dotenv()

print("URL =", os.getenv("SUPABASE_URL"))
print("KEY =", os.getenv("SUPABASE_KEY"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
from supabase import create_client
from database.risk_engine import shipment_risk
from datetime import datetime


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =====================================================
# Get all rows
# =====================================================

def query_table(table, limit=20):

    response = (
        supabase
        .table(table)
        .select("*")
        .limit(limit)
        .execute()
    )

    return response.data


# =====================================================
# Exact Match
# =====================================================

def query_where(table, column, value):

    response = (
        supabase
        .table(table)
        .select("*")
        .eq(column, value)
        .execute()
    )

    return response.data


# =====================================================
# LIKE Search
# =====================================================

def query_like(table, column, value):

    response = (
        supabase
        .table(table)
        .select("*")
        .ilike(column, f"%{value}%")
        .limit(20)
        .execute()
    )

    return response.data


# =====================================================
# Count
# =====================================================

def query_count(table):

    response = (
        supabase
        .table(table)
        .select("*", count="exact")
        .execute()
    )

    return response.count


# =====================================================
# Count with Condition
# =====================================================

def query_count_where(table, column, value):

    response = (
        supabase
        .table(table)
        .select("*", count="exact")
        .eq(column, value)
        .execute()
    )

    return response.count


# =====================================================
# Multiple Conditions
# =====================================================

def query_multiple_where(table, filters):

    query = supabase.table(table).select("*")

    for column, value in filters.items():
        query = query.eq(column, value)

    response = query.execute()

    return response.data




def query_filter(table, column, value):

    return (
        supabase.table(table)
        .select("*")
        .eq(column, value)
        .limit(20)
        .execute()
        .data
    )



def query_shipment_history(shipment_id):

    return (
        supabase.table("shipment_delivery_history")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
        .data
    )



def get_complete_shipment(shipment_id):

    # --------------------------
    # Shipment
    # --------------------------

    shipment = (
        supabase.table("shipments")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
        .data
    )

    if not shipment:
        return None

    shipment = shipment[0]
    carrier = (
        supabase.table("carriers")
        .select("*")
        .eq("carrier_id", shipment["carrier_id"])
        .execute()
        .data
    )

    if carrier:
        shipment.update(carrier[0])

    
    customer = (
        supabase.table("customers")
        .select("*")
        .eq("customer_id", shipment["customer_id"])
        .execute()
        .data
    )

    if customer:
        shipment.update(customer[0])

    product = (
        supabase.table("products")
        .select("*")
        .eq("product_id", shipment["product_id"])
        .execute()
        .data
    )

    if product:
        shipment.update(product[0])


    warehouse = (
        supabase.table("warehouses")
        .select("*")
        .eq("warehouse_id", shipment["warehouse_id"])
        .execute()
        .data
    )

    if warehouse:
        shipment.update(warehouse[0])

    route = (
        supabase.table("routes")
        .select("*")
        .eq("route_id", shipment["route_id"])
        .execute()
        .data
    )

    if route:
        shipment.update(route[0])

    vehicle = (
        supabase.table("vehicles")
        .select("*")
        .eq("vehicle_id", shipment["vehicle_id"])
        .execute()
        .data
    )

    if vehicle:
        shipment.update(vehicle[0])

    customs = (
        supabase.table("customs")
        .select("*")
        .eq("customs_id", shipment["customs_id"])
        .execute()
        .data
    )

    if customs:
        shipment.update(customs[0])

    weather = (
        supabase.table("weather")
        .select("*")
        .eq("weather_id", shipment["weather_id"])
        .execute()
        .data
    )

    if weather:
        shipment.update(weather[0])

    # --------------------------
    # Delivery History
    # --------------------------

    history = (
        supabase.table("shipment_delivery_history")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
        .data
    )

    if history:

        shipment["actual_delivery_date"] = history[0]["actual_delivery_date"]

        shipment["delivery_status"] = history[0]["delivery_status"]

        shipment["delivery_attempts"] = history[0]["delivery_attempts"]

    else:

        shipment["actual_delivery_date"] = None

        shipment["delivery_status"] = "Unknown"

        shipment["delivery_attempts"] = 0


    feature = (
        supabase.table("ai_feature_store")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
        .data
    )

    if feature:
        shipment.update(feature[0])

    inference = (
        supabase.table("ai_inference_log")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
        .data
    )

    if inference:
        shipment.update(inference[0])

    alert = (
        supabase.table("ai_monitoring_alerts")
        .select("*")
        .eq("shipment_id", shipment_id)
        .execute()
        .data
    )

    if alert:
        shipment.update(alert[0])




    # --------------------------
    # Calculate Risk
    # --------------------------

    shipment = shipment_risk(shipment)

    return shipment


def get_all_shipments():

    result = (
        supabase.table("shipments")
        .select("*")
        .execute()
    )

    return result.data


def get_all_shipments_with_delivery():

    # Fetch all shipments
    shipments = (
        supabase.table("shipments")
        .select("*")
        .execute()
        .data
    )

    # Fetch all delivery history in ONE query
    history = (
        supabase.table("shipment_delivery_history")
        .select("*")
        .execute()
        .data
    )

    # Create lookup dictionary
    history_map = {
        row["shipment_id"]: row
        for row in history
    }

    final_data = []

    for shipment in shipments:

        delivery = history_map.get(shipment["shipment_id"])

        if delivery:
            shipment.update(delivery)

        else:
            shipment["actual_delivery_date"] = None
            shipment["delivery_status"] = "Unknown"
            shipment["delivery_attempts"] = 0

        final_data.append(shipment)

    return final_data


def get_unique_values(table, column):

    response = (
        supabase
        .table(table)
        .select(column)
        .execute()
    )

    values = set()

    for row in response.data:

        value = row.get(column)

        if value:
            values.add(str(value))

    return list(values)

def query_top_carriers():

    shipments = (
        supabase.table("shipments")
        .select("carrier_id")
        .execute()
        .data
    )

    carriers = (
        supabase.table("carriers")
        .select("*")
        .execute()
        .data
    )

    carrier_map = {
        c["carrier_id"]: c["carrier_name"]
        for c in carriers
    }

    counts = {}

    for row in shipments:

        cid = row["carrier_id"]
        counts[cid] = counts.get(cid, 0) + 1

    result = []

    for cid, total in counts.items():

        result.append({
            "carrier_name": carrier_map.get(cid, cid),
            "total_shipments": total
        })

    result.sort(
        key=lambda x: x["total_shipments"],
        reverse=True
    )

    return result

def query_top_customers():

    shipments = (
        supabase.table("shipments")
        .select("customer_id")
        .execute()
        .data
    )

    customers = (
        supabase.table("customers")
        .select("*")
        .execute()
        .data
    )

    customer_map = {
        c["customer_id"]: c["customer_name"]
        for c in customers
    }

    counts = {}

    for row in shipments:

        cid = row["customer_id"]
        counts[cid] = counts.get(cid, 0) + 1

    result = []

    for cid, total in counts.items():

        result.append({
            "customer_name": customer_map.get(cid, cid),
            "total_shipments": total
        })

    result.sort(
        key=lambda x: x["total_shipments"],
        reverse=True
    )

    return result

def query_top_warehouses():

    warehouses = (
        supabase.table("warehouses")
        .select("*")
        .execute()
        .data
    )

    warehouses.sort(
        key=lambda x: x.get("utilization_percentage", 0),
        reverse=True
    )

    return warehouses

def query_average_weight():

    shipments = (
        supabase.table("shipments")
        .select("weight")
        .execute()
        .data
    )

    if not shipments:
        return {"average_weight": 0}

    total = 0

    for row in shipments:
        total += row["weight"]

    avg = total / len(shipments)

    return {
        "average_weight": round(avg, 2)
    }
    
print("DATABASE_QUERY IMPORTED FINISHED")