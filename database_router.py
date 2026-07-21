import re

from database_query import (
    query_table,
    query_where,
    query_like,
    query_count,
    query_count_where,
    query_multiple_where
)


def route_database_query(query):

    query_lower = query.lower()

    # =====================================================
    # SHIPMENT BY BOOKING ID
    # =====================================================

    booking = re.search(r"ALC-\d{4}-\d+", query, re.I)

    if booking:
        return query_where(
            "shipments",
            "booking_id",
            booking.group()
        )

    # =====================================================
    # SHIPMENT BY UUID
    # =====================================================

    shipment_uuid = re.search(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        query,
        re.I
    )

    if shipment_uuid:
        return query_where(
            "shipments",
            "shipment_id",
            shipment_uuid.group()
        )

    # =====================================================
    # CUSTOMER
    # =====================================================

    if "customer" in query_lower:

        if "how many" in query_lower:
            return query_count("customers")

        name = (
            query_lower
            .replace("show", "")
            .replace("customer", "")
            .replace("customers", "")
            .strip()
        )

        if name:
            return query_like(
                "customers",
                "customer_name",
                name
            )

        return query_table("customers")

    # =====================================================
    # PRODUCT
    # =====================================================

    if "product" in query_lower:

        name = (
            query_lower
            .replace("show", "")
            .replace("product", "")
            .replace("products", "")
            .strip()
        )

        if name:
            return query_like(
                "products",
                "product_name",
                name
            )

        return query_table("products")

    # =====================================================
    # CARRIER
    # =====================================================

    if has_entity(query, "carrier"):

        name = (
            query_lower
            .replace("show", "")
            .replace("carrier", "")
            .replace("carriers", "")
            .strip()
        )

        if name:
            return query_like(
                "carriers",
                "carrier_name",
                name
            )

        return query_table("carriers")

    # =====================================================
    # ROUTE
    # =====================================================

    route = re.search(r"R\d+", query, re.I)

    if route:
        return query_where(
            "routes",
            "route_id",
            route.group()
        )

    if "route" in query_lower:
        return query_table("routes")

    # =====================================================
    # WAREHOUSE
    # =====================================================

    warehouse = re.search(r"WH\d+", query, re.I)

    if warehouse:
        return query_where(
            "warehouses",
            "warehouse_id",
            warehouse.group()
        )

    if has_entity(query, "warehouse"):
        return query_table("warehouses")

    # =====================================================
    # VEHICLE
    # =====================================================

    if has_entity(query, "vehicle"):
        return query_table("vehicles")

    # =====================================================
    # WEATHER
    # =====================================================

    if "weather" in query_lower:

        city = (
            query_lower
            .replace("show", "")
            .replace("weather", "")
            .replace("for", "")
            .strip()
        )

        if city:
            return query_like(
                "weather",
                "city",
                city
            )

        return query_table("weather")

    # =====================================================
    # CUSTOMS
    # =====================================================

    if "custom" in query_lower:

        return query_table("customs")

    # =====================================================
    # SHIPMENTS
    # =====================================================

    if "shipment" in query_lower:

        if "how many" in query_lower:
            return query_count("shipments")

        if "delayed" in query_lower:
            return query_count_where(
                "shipments",
                "status",
                "Delayed"
            )

        if "pending" in query_lower:
            return query_count_where(
                "shipments",
                "status",
                "Pending"
            )

        if "delivered" in query_lower:
            return query_count_where(
                "shipments",
                "status",
                "Delivered"
            )

        return query_table("shipments")

    # =====================================================
    # DELIVERY HISTORY
    # =====================================================

    if (
        "history" in query_lower or
        "tracking history" in query_lower
    ):
        return query_table("shipment_delivery_history")

    # =====================================================
    # AI MODEL REGISTRY
    # =====================================================

    if (
        "model registry" in query_lower or
        "ai model" in query_lower
    ):
        return query_table("ai_model_registry")

    # =====================================================
    # AI FEATURE STORE
    # =====================================================

    if (
        "feature store" in query_lower or
        "feature" in query_lower
    ):
        return query_table("ai_feature_store")

    # =====================================================
    # AI INFERENCE LOG
    # =====================================================

    if (
        "inference" in query_lower or
        "prediction" in query_lower
    ):
        return query_table("ai_inference_log")

    # =====================================================
    # AI MONITORING ALERTS
    # =====================================================

    if (
        "alert" in query_lower or
        "monitoring" in query_lower
    ):
        return query_table("ai_monitoring_alerts")

    # =====================================================
    # README
    # =====================================================

    if "readme" in query_lower:
        return query_table("readme")

    return None