import re

# ==========================================================
# ENTITY KEYWORDS
# ==========================================================

ENTITY_KEYWORDS = {
    "shipment": [
        "shipment", "shipments", "cargo", "parcel",
        "booking", "consignment", "freight"
    ],

    "customer": [
        "customer", "customers", "client", "clients"
    ],

    "carrier": [
        "carrier", "carriers", "shipping company",
        "logistics company", "courier"
    ],

    "warehouse": [
        "warehouse", "warehouses", "storage", "depot"
    ],

    "vehicle": [
        "vehicle", "vehicles", "truck",
        "train", "ship", "plane"
    ],

    "route": [
        "route", "routes"
    ],

    "product": [
        "product", "products", "goods", "item"
    ],

    "weather": [
        "weather", "forecast"
    ]
}

# ==========================================================
# INTENTS
# ==========================================================

INTENTS = {

    "list": [
        "show",
        "list",
        "display",
        "find",
        "get",
        "fetch",
        "view"
    ],

    "count": [
        "count",
        "how many",
        "total",
        "number of"
    ],

    "average": [
        "average",
        "avg"
    ],

    "highest": [
        "highest",
        "maximum",
        "top",
        "best"
    ],

    "lowest": [
        "lowest",
        "minimum",
        "least"
    ]
}

# ==========================================================
# FILTERS
# ==========================================================

FILTERS = {

    "priority": {
        "high priority": "High",
        "normal": "Normal",
        "low priority": "Low"
    },

    "customer_status": {
        "active": "Active",
        "inactive": "Inactive"
    },

    "delivery_status": {
        "delivered": "Delivered",
        "pending": "Pending",
        "transit": "In Transit",
        "returned": "Returned",
        "cancelled": "Cancelled"
    },

    "fragile": {
        "fragile": True
    },

    "hazardous": {
        "hazardous": True
    },

    "perishable": {
        "perishable": True
    },
    "shipment_type": {
        "import": "Import",
        "export": "Export",
        "domestic": "Domestic"
    },
    "customer_type": {
        "business": "Business",
        "individual": "Individual"
    },
    
    "shipping_mode": {
        "air": "Air",
        "road": "Road",
        "rail": "Rail",
        "sea": "Sea"
    },
    
    "insurance": {
        "insured": True,
        "insurance": True
    }
}

# ==========================================================
# HELPERS
# ==========================================================

def detect_entity(query):

    query = query.lower()

    for entity, words in ENTITY_KEYWORDS.items():

        for word in words:

            if re.search(rf"\b{re.escape(word)}\b", query):
                return entity

    return None


def detect_intent(query):

    query = query.lower()

    for intent, words in INTENTS.items():

        for word in words:

            if word in query:
                return intent

    return "single"


def detect_filters(query):

    query = query.lower()

    filters = {}

    for field, values in FILTERS.items():

        for keyword, value in values.items():

            if keyword in query:

                filters[field] = value

    return filters


def detect_shipment_id(query):

    match = re.search(
        r"[0-9a-f]{8}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{12}",
        query,
        re.I
    )

    if match:
        return match.group()

    return None


def detect_booking_id(query):

    match = re.search(
        r"ALC-\d{4}-\d+",
        query,
        re.I
    )

    if match:
        return match.group()

    return None


# ==========================================================
# MAIN PARSER
# ==========================================================

def parse_query(query):

    parsed = {

        "entity": detect_entity(query),

        "intent": detect_intent(query),

        "filters": detect_filters(query),

        "shipment_id": detect_shipment_id(query),

        "booking_id": detect_booking_id(query)

    }

    return parsed