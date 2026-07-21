from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# -----------------------------
# Connect to Supabase
# -----------------------------
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# =====================================================
# SHIPMENTS
# =====================================================

def get_shipment(shipment_id):
    try:
        response = (
            supabase.table("shipments")
            .select("*")
            .eq("Shipment_ID", shipment_id)
            .execute()
        )
        return response.data if response.data else None
    except Exception:
        return None


def get_all_shipments():
    try:
        response = (
            supabase.table("shipments")
            .select("*")
            .limit(20)
            .execute()
        )
        return response.data
    except Exception:
        return None


def get_latest_shipments(limit=5):
    try:
        response = (
            supabase.table("shipments")
            .select("*")
            .order("Dispatch_Date", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data
    except Exception:
        return None


def get_shipments_by_status(status):
    try:
        response = (
            supabase.table("shipments")
            .select("*")
            .eq("Shipment_Status", status)
            .execute()
        )
        return response.data
    except Exception:
        return None


def get_shipments_by_carrier(carrier):
    try:
        response = (
            supabase.table("shipments")
            .select("*")
            .ilike("Carrier", f"%{carrier}%")
            .execute()
        )
        return response.data
    except Exception:
        return None


def get_shipments_by_date(dispatch_date):
    try:
        response = (
            supabase.table("shipments")
            .select("*")
            .eq("Dispatch_Date", dispatch_date)
            .execute()
        )
        return response.data
    except Exception:
        return None


def count_shipments():
    try:
        response = supabase.table("shipments").select("*").execute()
        return len(response.data)
    except Exception:
        return 0


def get_shipments_by_status(status):
    try:
        response = (
            supabase.table("shipments")
            .select("*")
            .eq("Shipment_Status", status)
            .limit(10)          # <-- Add this
            .execute()
        )
        return response.data
    except Exception:
        return None


# =====================================================
# ORDERS
# =====================================================

def get_order(order_id):
    try:
        response = (
            supabase.table("orders")
            .select("*")
            .eq("Order_ID", order_id)
            .execute()
        )
        return response.data if response.data else None
    except Exception:
        return None


def get_all_orders():
    try:
        response = supabase.table("orders").select("*").limit(20).execute()
        return response.data
    except Exception:
        return None


def get_orders_by_status(status):
    try:
        response = (
            supabase.table("orders")
            .select("*")
            .eq("Order_Status", status)
            .execute()
        )
        return response.data
    except Exception:
        return None


def get_orders_by_city(city):
    try:
        response = (
            supabase.table("orders")
            .select("*")
            .ilike("Destination_City", f"%{city}%")
            .execute()
        )
        return response.data
    except Exception:
        return None


def get_orders_by_customer(customer):
    try:
        response = (
            supabase.table("orders")
            .select("*")
            .ilike("Customer_Name", f"%{customer}%")
            .execute()
        )
        return response.data
    except Exception:
        return None


def count_orders():
    try:
        response = supabase.table("orders").select("*").execute()
        return len(response.data)
    except Exception:
        return 0


# =====================================================
# WAREHOUSES
# =====================================================

def get_warehouse(warehouse_id):
    try:
        response = (
            supabase.table("warehouses")
            .select("*")
            .eq("Warehouse_ID", warehouse_id)
            .execute()
        )
        return response.data if response.data else None
    except Exception:
        return None


def get_all_warehouses():
    try:
        response = supabase.table("warehouses").select("*").execute()
        return response.data
    except Exception:
        return None


# =====================================================
# TRACKING
# =====================================================

def get_tracking(shipment_id):
    try:
        response = (
            supabase.table("tracking_events")
            .select("*")
            .eq("Shipment_ID", shipment_id)
            .order("Event_Date")
            .execute()
        )
        return response.data
    except Exception:
        return None


# =====================================================
# DELIVERY AGENTS
# =====================================================

def get_all_agents():
    try:
        response = supabase.table("delivery_agents").select("*").execute()
        return response.data
    except Exception:
        return None


# =====================================================
# FAQs
# =====================================================

def get_faq():
    try:
        response = supabase.table("faqs").select("*").limit(20).execute()
        return response.data
    except Exception:
        return None


def search_faq(keyword):
    try:
        response = (
            supabase.table("faqs")
            .select("*")
            .or_(f"Question.ilike.%{keyword}%,Answer.ilike.%{keyword}%")
            .execute()
        )
        return response.data
    except Exception:
        return None


def count_shipments_by_status(status):

    try:

        response = (
            supabase.table("shipments")
            .select("*")
            .eq("Shipment_Status", status)
            .execute()
        )

        return len(response.data)

    except Exception:

        return 0