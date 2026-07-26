import re

from database_query import (
    query_table,
    query_where,
    query_like,
    query_count,
    get_complete_shipment,
    get_all_shipments_with_delivery,

    # Analytics
    query_top_carriers,
    query_top_customers,
    query_top_warehouses,
    query_average_weight
)

# ==========================================================
# MASTER DATA
# ==========================================================

CITY_NAMES = [
    "surat",
    "mumbai",
    "delhi",
    "kolkata",
    "chennai",
    "bangalore",
    "hyderabad",
    "guangzhou",
    "tokyo",
    "singapore",
    "felixstowe",
    "london",
    "dubai",
    "new york"
]

COUNTRIES = [
    "india",
    "china",
    "japan",
    "usa",
    "uk",
    "germany",
    "singapore",
    "netherlands",
    "united kingdom"
]

PRODUCT_CATEGORIES = [
    "electronics",
    "furniture",
    "textile",
    "food",
    "machinery",
    "chemical"
]

VEHICLE_TYPES = [
    "truck",
    "rail",
    "ship",
    "aircraft"
]

# ==========================================================
# LOOKUP DICTIONARIES
# ==========================================================

CARRIER_TYPES = {
    "air": "Air",
    "road": "Road",
    "rail": "Rail",
    "sea": "Sea"
}

DELIVERY_STATUS = {
    "pending": "Pending",
    "delivered": "Delivered",
    "in transit": "In Transit",
    "transit": "In Transit",
    "failed": "Failed",
    "returned": "Returned",
    "cancelled": "Cancelled"
}

CUSTOMER_STATUS = {
    "active": "Active",
    "inactive": "Inactive"
}

CUSTOMER_TYPE = {
    "business": "Business",
    "individual": "Individual"
}

SHIPMENT_PRIORITY = {
    "high priority": "High",
    "normal": "Normal",
    "low priority": "Low"
}

SHIPMENT_TYPE = {
    "import": "Import",
    "export": "Export",
    "domestic": "Domestic"
}

RISK_LEVELS = {
    "high": "HIGH",
    "medium": "MEDIUM",
    "low": "LOW"
}

# ==========================================================
# ENTITY SYNONYMS
# ==========================================================

ENTITY_SYNONYMS = {
    "shipment": [
        "shipment",
        "shipments",
        "cargo",
        "parcel",
        "consignment",
        "booking",
        "order",
        "freight",
        "load"
    ],

    "customer": [
        "customer",
        "customers",
        "client",
        "clients",
        "buyer",
        "buyers",
        "consignee",
        "shipper"
    ],

    "carrier": [
        "carrier",
        "carriers",
        "shipping company",
        "shipping line",
        "transport",
        "transporter",
        "courier",
        "logistics company",
        "logistics partner"
    ],

    "warehouse": [
        "warehouse",
        "warehouses",
        "storage",
        "storage center",
        "distribution center",
        "distribution",
        "hub",
        "depot"
    ],

    "vehicle": [
        "vehicle",
        "vehicles",
        "truck",
        "lorry",
        "trailer",
        "rail",
        "train",
        "ship",
        "vessel",
        "aircraft",
        "plane"
    ],

    "route": [
        "route",
        "routes",
        "path",
        "lane",
        "corridor",
        "journey"
    ],

    "weather": [
        "weather",
        "forecast",
        "rain",
        "storm",
        "wind",
        "temperature",
        "humidity",
        "climate"
    ],

    "customs": [
        "custom",
        "customs",
        "clearance",
        "inspection",
        "documentation",
        "documents",
        "import duty",
        "export duty"
    ],

    "product": [
        "product",
        "products",
        "item",
        "items",
        "goods",
        "commodity"
    ],

    "delivery": [
        "delivery",
        "deliveries",
        "tracking",
        "tracking history",
        "history",
        "status"
    ],

    "feature": [
        "feature",
        "feature store",
        "feature vector"
    ],

    "prediction": [
        "prediction",
        "predictions",
        "inference",
        "risk prediction",
        "delay prediction"
    ],

    "model": [
        "model",
        "models",
        "registry",
        "ai model",
        "ml model"
    ],

    "alert": [
        "alert",
        "alerts",
        "warning",
        "warnings",
        "monitor",
        "monitoring"
    ]
}

# ==========================================================
# INTENTS
# ==========================================================

INTENTS = {
    "count": [
        "count",
        "how many",
        "total",
        "number of"
    ],

    "show": [
        "show",
        "display",
        "list",
        "find",
        "fetch",
        "view",
        "give"
    ],

    "status": [
        "status",
        "current status",
        "delivery status"
    ],

    "location": [
        "location",
        "where",
        "where is",
        "current location"
    ],

    "carrier": [
        "carrier",
        "handled by",
        "transported by",
        "shipping company"
    ],

    "delivery": [
        "delivery",
        "eta",
        "expected delivery",
        "arrival",
        "arrive"
    ],

    "delay": [
        "delay",
        "delayed",
        "late"
    ],

    "risk": [
        "risk",
        "high risk",
        "medium risk",
        "low risk"
    ]
}

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def has_entity(query, entity):
    query = query.lower()

    for word in ENTITY_SYNONYMS.get(entity, []):
        if re.search(rf"\b{re.escape(word)}\b", query):
            return True

    return False


def detect_intent(query):
    query = query.lower()

    for intent, words in INTENTS.items():
        for word in words:
            if word in query:
                return intent

    return None


def keyword_filter(query, mapping):
    query = query.lower()

    for keyword, value in mapping.items():
        if keyword in query:
            return value

    return None


def extract_city(query):
    query = query.lower()

    for city in CITY_NAMES:
        if city in query:
            return city.title()

    return None


def extract_country(query):
    query = query.lower()

    for country in COUNTRIES:
        if country in query:
            return country.title()

    return None


def extract_booking_id(query):
    match = re.search(r"ALC-\d{4}-\d+", query, re.I)
    return match.group() if match else None


def extract_shipment_uuid(query):
    match = re.search(
        r"[0-9a-f]{8}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{12}",
        query,
        re.I
    )

    return match.group() if match else None

# ==========================================================
# MAIN SQL ENGINE
# ==========================================================

def execute_sql(query):

    query_lower = query.lower()

    intent = detect_intent(query)

    booking_id = extract_booking_id(query)
    shipment_uuid = extract_shipment_uuid(query)

    city = extract_city(query)
    country = extract_country(query)

    # =====================================================
    # ANALYTICS QUERIES
    # =====================================================

    if (
        "top carrier" in query_lower
        or "most shipments" in query_lower
        or "highest shipments" in query_lower
    ):
        return query_top_carriers()

    if (
        "top customer" in query_lower
        or "highest customer" in query_lower
    ):
        return query_top_customers()

    if (
        "highest utilization" in query_lower
        or "warehouse utilization" in query_lower
    ):
        return query_top_warehouses()

    if (
        "average weight" in query_lower
        or "avg weight" in query_lower
    ):
        return query_average_weight()

    # =====================================================
    # SHIPMENT QUERIES
    # =====================================================

    if has_entity(query, "shipment"):

        # -----------------------------------------------
        # Booking ID
        # -----------------------------------------------

        if booking_id:

            shipment = query_where(
                "shipments",
                "booking_id",
                booking_id
            )

            if shipment:
                return get_complete_shipment(
                    shipment[0]["shipment_id"]
                )

            return {
                "message": "No shipment found for this Booking ID."
            }

        # -----------------------------------------------
        # Shipment UUID
        # -----------------------------------------------

        if shipment_uuid:
            return get_complete_shipment(shipment_uuid)

        # -----------------------------------------------
        # Shipment Count
        # -----------------------------------------------

        if intent == "count":

            return {
                "Total Shipments":
                query_count("shipments")
            }

        # -----------------------------------------------
        # Delayed Shipments
        # -----------------------------------------------

        if intent == "delay":

            delayed = []

            for row in get_all_shipments_with_delivery():

                shipment = get_complete_shipment(
                    row["shipment_id"]
                )

                if shipment["delay_days"] > 0:
                    delayed.append(shipment)

            return delayed

        # -----------------------------------------------
        # Shipment Risk
        # -----------------------------------------------

        if intent == "risk":

            level = keyword_filter(
                query,
                RISK_LEVELS
            )

            if level:

                result = []

                for row in get_all_shipments_with_delivery():

                    shipment = get_complete_shipment(
                        row["shipment_id"]
                    )

                    if shipment["risk_level"] == level:
                        result.append(shipment)

                return result

        # -----------------------------------------------
        # Shipment Status
        # -----------------------------------------------

        status = keyword_filter(
            query,
            DELIVERY_STATUS
        )

        if status:
            return query_where(
                "shipment_delivery_history",
                "delivery_status",
                status
            )

        # -----------------------------------------------
        # Shipment Type
        # -----------------------------------------------

        shipment_type = keyword_filter(
            query,
            SHIPMENT_TYPE
        )

        if shipment_type:
            return query_where(
                "shipments",
                "shipment_type",
                shipment_type
            )

        # -----------------------------------------------
        # Shipment Priority
        # -----------------------------------------------

        priority = keyword_filter(
            query,
            SHIPMENT_PRIORITY
        )

        if priority:
            return query_where(
                "shipments",
                "priority",
                priority
            )

        # -----------------------------------------------
        # Shipping Mode
        # -----------------------------------------------

        shipping_mode = keyword_filter(
            query,
            CARRIER_TYPES
        )

        if shipping_mode:
            return query_where(
                "shipments",
                "shipping_mode",
                shipping_mode
            )

        # -----------------------------------------------
        # Fragile Shipments
        # -----------------------------------------------

        if "fragile" in query_lower:
            return query_where(
                "shipments",
                "fragile",
                True
            )

        # -----------------------------------------------
        # Insured Shipments
        # -----------------------------------------------

        if (
            "insured" in query_lower
            or "insurance" in query_lower
        ):
            return query_where(
                "shipments",
                "insurance",
                True
            )

        # -----------------------------------------------
        # Search by Origin/Destination City
        # -----------------------------------------------

        if city:

            shipments = query_like(
                "shipments",
                "origin_city",
                city
            )

            if shipments:
                return shipments

            return query_like(
                "shipments",
                "destination_city",
                city
            )

        # -----------------------------------------------
        # Search by Origin/Destination Country
        # -----------------------------------------------

        if country:

            shipments = query_like(
                "shipments",
                "origin_country",
                country
            )

            if shipments:
                return shipments

            return query_like(
                "shipments",
                "destination_country",
                country
            )

        # -----------------------------------------------
        # Default
        # -----------------------------------------------

        return get_all_shipments_with_delivery()
    
    # =====================================================
    # CUSTOMER QUERIES
    # =====================================================

    if has_entity(query, "customer"):

        # -----------------------------------------------
        # Total Customers
        # -----------------------------------------------

        if intent == "count":
            return {
                "Total Customers":
                query_count("customers")
            }

        # -----------------------------------------------
        # Customer Status
        # -----------------------------------------------

        status = keyword_filter(
            query,
            CUSTOMER_STATUS
        )

        if status:
            return query_where(
                "customers",
                "customer_status",
                status
            )

        # -----------------------------------------------
        # Customer Type
        # -----------------------------------------------

        customer_type = keyword_filter(
            query,
            CUSTOMER_TYPE
        )

        if customer_type:
            return query_where(
                "customers",
                "customer_type",
                customer_type
            )

        # -----------------------------------------------
        # City
        # -----------------------------------------------

        if city:
            return query_where(
                "customers",
                "city",
                city
            )

        # -----------------------------------------------
        # Country
        # -----------------------------------------------

        if country:
            return query_where(
                "customers",
                "country",
                country
            )

        # -----------------------------------------------
        # Customer Name
        # -----------------------------------------------

        name = query_lower

        remove_words = [
            "show",
            "list",
            "display",
            "find",
            "give",
            "customer",
            "customers",
            "client",
            "clients",
            "buyer",
            "buyers"
        ]

        for word in remove_words:
            name = name.replace(word, "")

        name = name.strip()

        if name:

            data = query_like(
                "customers",
                "customer_name",
                name
            )

            if data:
                return data

        return query_table("customers")

    # =====================================================
    # PRODUCT QUERIES
    # =====================================================

    if has_entity(query, "product"):

        # -----------------------------------------------
        # Total Products
        # -----------------------------------------------

        if intent == "count":
            return {
                "Total Products":
                query_count("products")
            }

        # -----------------------------------------------
        # Product Category
        # -----------------------------------------------

        for category in PRODUCT_CATEGORIES:

            if category in query_lower:
                return query_where(
                    "products",
                    "category",
                    category.title()
                )

        # -----------------------------------------------
        # Fragile Products
        # -----------------------------------------------

        if "fragile" in query_lower:
            return query_where(
                "products",
                "fragile",
                True
            )

        # -----------------------------------------------
        # Hazardous Products
        # -----------------------------------------------

        if (
            "hazardous" in query_lower
            or "dangerous" in query_lower
        ):
            return query_where(
                "products",
                "hazardous",
                True
            )

        # -----------------------------------------------
        # Perishable Products
        # -----------------------------------------------

        if (
            "perishable" in query_lower
            or "fresh" in query_lower
        ):
            return query_where(
                "products",
                "perishable",
                True
            )

        # -----------------------------------------------
        # Temperature Controlled Products
        # -----------------------------------------------

        if (
            "temperature" in query_lower
            or "cold" in query_lower
            or "cold chain" in query_lower
        ):
            return query_where(
                "products",
                "temperature_controlled",
                True
            )

        # -----------------------------------------------
        # Supplier Search
        # -----------------------------------------------

        supplier = query_lower

        remove_words = [
            "supplier",
            "supplied",
            "product",
            "products",
            "show",
            "list",
            "find",
            "give"
        ]

        for word in remove_words:
            supplier = supplier.replace(word, "")

        supplier = supplier.strip()

        if supplier:

            data = query_like(
                "products",
                "supplier_name",
                supplier
            )

            if data:
                return data

        # -----------------------------------------------
        # Product Name
        # -----------------------------------------------

        product_name = query_lower

        remove_words = [
            "show",
            "list",
            "display",
            "find",
            "give",
            "product",
            "products",
            "item",
            "items",
            "goods",
            "commodity"
        ]

        for word in remove_words:
            product_name = product_name.replace(word, "")

        product_name = product_name.strip()

        if product_name:

            data = query_like(
                "products",
                "product_name",
                product_name
            )

            if data:
                return data

        return query_table("products")
    
    # =====================================================
    # CARRIER QUERIES
    # =====================================================

    if has_entity(query, "carrier"):

        if intent == "count":
            return {
                "Total Carriers":
                query_count("carriers")
            }

        # -----------------------------------------------
        # Carrier Type
        # -----------------------------------------------

        carrier_type = keyword_filter(
            query,
            CARRIER_TYPES
        )

        if carrier_type:
            return query_where(
                "carriers",
                "carrier_type",
                carrier_type
            )

        # -----------------------------------------------
        # Headquarters Country
        # -----------------------------------------------

        if country:
            return query_like(
                "carriers",
                "headquarters",
                country
            )

        # -----------------------------------------------
        # Carrier Name
        # -----------------------------------------------

        carrier_name = query_lower

        remove_words = [
            "carrier",
            "carriers",
            "shipping company",
            "shipping line",
            "transport",
            "transporter",
            "courier",
            "show",
            "list",
            "display",
            "find",
            "give"
        ]

        for word in remove_words:
            carrier_name = carrier_name.replace(word, "")

        carrier_name = carrier_name.strip()

        if carrier_name:

            data = query_like(
                "carriers",
                "carrier_name",
                carrier_name
            )

            if data:
                return data

        return query_table("carriers")

    # =====================================================
    # WAREHOUSE QUERIES
    # =====================================================

    if has_entity(query, "warehouse"):

        if intent == "count":
            return {
                "Total Warehouses":
                query_count("warehouses")
            }

        # -----------------------------------------------
        # City
        # -----------------------------------------------

        if city:
            return query_where(
                "warehouses",
                "city",
                city
            )

        # -----------------------------------------------
        # Warehouse Type
        # -----------------------------------------------

        if "regional" in query_lower:
            return query_where(
                "warehouses",
                "warehouse_type",
                "Regional"
            )

        if "central" in query_lower:
            return query_where(
                "warehouses",
                "warehouse_type",
                "Central"
            )

        # -----------------------------------------------
        # Capacity / Utilization
        # -----------------------------------------------

        if (
            "capacity" in query_lower
            or "utilization" in query_lower
        ):
            return query_table("warehouses")

        # -----------------------------------------------
        # Warehouse Name
        # -----------------------------------------------

        warehouse_name = query_lower

        remove_words = [
            "warehouse",
            "warehouses",
            "storage",
            "storage center",
            "distribution",
            "distribution center",
            "hub",
            "depot",
            "show",
            "list",
            "display",
            "find",
            "give"
        ]

        for word in remove_words:
            warehouse_name = warehouse_name.replace(word, "")

        warehouse_name = warehouse_name.strip()

        if warehouse_name:

            data = query_like(
                "warehouses",
                "warehouse_name",
                warehouse_name
            )

            if data:
                return data

        return query_table("warehouses")

    # =====================================================
    # ROUTE QUERIES
    # =====================================================

    if has_entity(query, "route"):

        if intent == "count":
            return {
                "Total Routes":
                query_count("routes")
            }

        risk = keyword_filter(
            query,
            {
                "high": "High",
                "medium": "Medium",
                "low": "Low"
            }
        )

        if risk:
            return query_where(
                "routes",
                "route_risk",
                risk
            )

        if city:

            routes = query_where(
                "routes",
                "origin_city",
                city
            )

            if routes:
                return routes

            return query_where(
                "routes",
                "destination_city",
                city
            )

        if country:

            routes = query_where(
                "routes",
                "origin_country",
                country
            )

            if routes:
                return routes

            return query_where(
                "routes",
                "destination_country",
                country
            )

        return query_table("routes")
    
    # =====================================================
    # VEHICLE QUERIES
    # =====================================================

    if has_entity(query, "vehicle"):

        if intent == "count":
            return {
                "Total Vehicles":
                query_count("vehicles")
            }

        # -----------------------------------------------
        # Fuel Type
        # -----------------------------------------------

        if "diesel" in query_lower:
            return query_where(
                "vehicles",
                "fuel_type",
                "Diesel"
            )

        if "electric" in query_lower:
            return query_where(
                "vehicles",
                "fuel_type",
                "Electric"
            )

        # -----------------------------------------------
        # Vehicle Type
        # -----------------------------------------------

        for vehicle in VEHICLE_TYPES:

            if vehicle in query_lower:
                return query_where(
                    "vehicles",
                    "vehicle_type",
                    vehicle.title()
                )

        # -----------------------------------------------
        # Maintenance Status
        # -----------------------------------------------

        if "good" in query_lower:
            return query_where(
                "vehicles",
                "maintenance_status",
                "Good"
            )

        if "poor" in query_lower:
            return query_where(
                "vehicles",
                "maintenance_status",
                "Poor"
            )

        # -----------------------------------------------
        # Vehicle Number
        # -----------------------------------------------

        vehicle_number = re.search(
            r"[A-Z]{2}-\d{4}-\d+",
            query,
            re.I
        )

        if vehicle_number:
            return query_where(
                "vehicles",
                "vehicle_number",
                vehicle_number.group().upper()
            )

        return query_table("vehicles")

    # =====================================================
    # DELIVERY HISTORY
    # =====================================================

    if has_entity(query, "delivery"):

        if intent == "count":
            return {
                "Total Delivery Records":
                query_count("shipment_delivery_history")
            }

        status = keyword_filter(
            query,
            DELIVERY_STATUS
        )

        if status:
            return query_where(
                "shipment_delivery_history",
                "delivery_status",
                status
            )

        if shipment_uuid:
            return query_where(
                "shipment_delivery_history",
                "shipment_id",
                shipment_uuid
            )

        return query_table(
            "shipment_delivery_history"
        )

    # =====================================================
    # WEATHER QUERIES
    # =====================================================

    if has_entity(query, "weather"):

        # -----------------------------------------------
        # City Search
        # -----------------------------------------------

        if city:
            return query_where(
                "weather",
                "city",
                city
            )

        # -----------------------------------------------
        # Weather Condition
        # -----------------------------------------------

        weather_conditions = [
            "rain",
            "clear",
            "fog",
            "storm",
            "snow",
            "cloudy",
            "high wind",
            "wind"
        ]

        for condition in weather_conditions:

            if condition in query_lower:
                return query_like(
                    "weather",
                    "weather_condition",
                    condition.title()
                )

        return query_table("weather")
    
    # =====================================================
    # CUSTOMS QUERIES
    # =====================================================

    if has_entity(query, "customs"):

        if country:
            return query_where(
                "customs",
                "destination_country",
                country
            )

        if (
            "inspection" in query_lower
            or "inspect" in query_lower
        ):
            return query_where(
                "customs",
                "inspection_required",
                True
            )

        if (
            "documentation" in query_lower
            or "document" in query_lower
            or "papers" in query_lower
        ):
            return query_where(
                "customs",
                "documentation_complete",
                True
            )

        if (
            "required" in query_lower
            or "mandatory" in query_lower
        ):
            return query_where(
                "customs",
                "customs_required",
                True
            )

        cargo_types = [
            "electronics",
            "machinery",
            "chemical",
            "food",
            "textile",
            "furniture"
        ]

        for cargo in cargo_types:

            if cargo in query_lower:
                return query_where(
                    "customs",
                    "cargo_type",
                    cargo.title()
                )

        return query_table("customs")

    # =====================================================
    # AI FEATURE STORE
    # =====================================================

    if has_entity(query, "feature"):

        if shipment_uuid:
            return query_where(
                "ai_feature_store",
                "shipment_id",
                shipment_uuid
            )

        return query_table("ai_feature_store")

    # =====================================================
    # AI INFERENCE LOG
    # =====================================================

    if has_entity(query, "prediction"):

        if shipment_uuid:
            return query_where(
                "ai_inference_log",
                "shipment_id",
                shipment_uuid
            )

        risk = keyword_filter(
            query,
            {
                "high": "High",
                "medium": "Medium",
                "low": "Low"
            }
        )

        if risk:
            return query_where(
                "ai_inference_log",
                "risk_category",
                risk
            )

        return query_table("ai_inference_log")

    # =====================================================
    # AI MODEL REGISTRY
    # =====================================================

    if has_entity(query, "model"):

        deployment = keyword_filter(
            query,
            {
                "production": "Production",
                "testing": "Testing",
                "staging": "Staging"
            }
        )

        if deployment:
            return query_where(
                "ai_model_registry",
                "deployment_status",
                deployment
            )

        return query_table("ai_model_registry")

    # =====================================================
    # AI MONITORING ALERTS
    # =====================================================

    if has_entity(query, "alert"):

        if shipment_uuid:
            return query_where(
                "ai_monitoring_alerts",
                "shipment_id",
                shipment_uuid
            )

        status = keyword_filter(
            query,
            {
                "resolved": "Resolved",
                "open": "Open"
            }
        )

        if status:
            return query_where(
                "ai_monitoring_alerts",
                "alert_status",
                status
            )

        return query_table("ai_monitoring_alerts")

    # =====================================================
    # SMART FALLBACK SEARCH
    # =====================================================

    FALLBACK_TABLES = {
        "shipment": "shipments",
        "customer": "customers",
        "carrier": "carriers",
        "warehouse": "warehouses",
        "vehicle": "vehicles",
        "route": "routes",
        "product": "products",
        "weather": "weather",
        "customs": "customs",
        "delivery": "shipment_delivery_history",
        "feature": "ai_feature_store",
        "prediction": "ai_inference_log",
        "model": "ai_model_registry",
        "alert": "ai_monitoring_alerts"
    }

    # Search using entity synonyms

    for entity, table in FALLBACK_TABLES.items():

        if has_entity(query, entity):
            return query_table(table)

    # Natural language fallback

    if any(
        word in query_lower
        for word in [
            "show",
            "list",
            "display",
            "find",
            "search",
            "give",
            "fetch",
            "view"
        ]
    ):

        for entity, table in FALLBACK_TABLES.items():

            if entity in query_lower:
                return query_table(table)

    # =====================================================
    # NOTHING FOUND
    # =====================================================

    return None