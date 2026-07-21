import re

# ==========================================================
# ENTITY KEYWORDS
# ==========================================================

ENTITY_KEYWORDS = {

    "shipment": [
        "shipment", "shipments", "booking", "cargo",
        "parcel", "consignment", "freight", "load"
    ],

    "customer": [
        "customer", "customers", "client",
        "clients", "buyer", "buyers"
    ],

    "carrier": [
        "carrier", "carriers", "transport",
        "shipping company", "logistics company",
        "courier"
    ],

    "warehouse": [
        "warehouse", "warehouses",
        "storage", "depot", "hub"
    ],

    "vehicle": [
        "vehicle", "vehicles",
        "truck", "lorry",
        "rail", "train",
        "ship", "vessel",
        "aircraft", "plane"
    ],

    "route": [
        "route", "routes",
        "path", "lane"
    ],

    "weather": [
        "weather", "forecast",
        "rain", "storm",
        "temperature", "humidity"
    ],

    "product": [
        "product", "products",
        "item", "items",
        "goods"
    ],

    "delivery": [
        "delivery",
        "deliveries",
        "status",
        "tracking"
    ],

    "customs": [
        "custom",
        "customs",
        "clearance",
        "inspection"
    ],

    "prediction": [
        "prediction",
        "risk",
        "probability",
        "inference"
    ]
}

# ==========================================================
# SQL INTENTS
# ==========================================================

SQL_INTENTS = [

    # Retrieval
    "show",
    "list",
    "display",
    "give",
    "find",
    "fetch",
    "search",
    "get",
    "view",

    # Aggregation
    "count",
    "how many",
    "total",
    "average",
    "avg",
    "maximum",
    "minimum",
    "highest",
    "lowest",

    # Shipment operations
    "track",
    "tracking",
    "status",
    "shipment status",
    "delivery status",
    "booking",
    "booking id",

    # Filters
    "active",
    "inactive",
    "pending",
    "processing",
    "delivered",
    "transit",
    "returned",
    "cancelled",
    "failed",

    # Shipment properties
    "fragile",
    "insured",
    "insurance",
    "priority",

    # Risk
    "high",
    "medium",
    "low",
    "risk",
    "delay",

    # Dates
    "today",
    "yesterday",
    "tomorrow",
    "date",

    # AI
    "prediction",
    "probability",
    "alert",
    "latency",
    "model"
]

# ==========================================================
# HYBRID INTENTS
# ==========================================================

HYBRID_INTENTS = [

    # Explanation
    "why",
    "reason",
    "because",
    "cause",
    "explain",

    # Analysis
    "analyze",
    "analysis",
    "evaluate",
    "compare",

    # Recommendation
    "recommend",
    "recommendation",
    "suggest",
    "advice",
    "best",

    # Improvement
    "improve",
    "optimize",
    "reduce",
    "prevent",

    # Impact
    "impact",
    "effect",
    "influence",

    # Decision
    "should",
    "can i",
    "is it good",
    "is it safe",

    # AI
    "risk",
    "probability",
    "prediction",

    # Logistics knowledge
    "incoterms",
    "customs process",
    "documentation",
    "procedure",
    "workflow",
    "policy",
    "guideline",
    "standard",

    # Meaning
    "meaning",
    "what does",
    "how does"
]

FOLLOW_UP_KEYWORDS = [

    "it",
    "its",
    "this",
    "that",

    "this shipment",
    "that shipment",

    "this one",
    "that one",

    "more",
    "more details",
    "more information",

    "tell me more",

    "explain",

    "why",

    "how",

    "what about",

    "carrier",
    "customer",
    "warehouse",
    "vehicle",
    "route",

    "risk",
    "delay",

    "destination",
    "origin",

    "insurance",

    "fragile"
]

# ==========================================================
# HELPERS
# ==========================================================

def contains_keywords(query, keywords):

    query = query.lower()

    return any(
        re.search(rf"\b{re.escape(word)}\b", query)
        for word in keywords
    )


def contains_entity(query):

    query = query.lower()

    for words in ENTITY_KEYWORDS.values():

        if contains_keywords(query, words):
            return True

    return False


# ==========================================================
# ROUTER
# ==========================================================

def route_query(query, last_shipment_id=None):

    print("=" * 50)
    print("ROUTER FILE EXECUTED")
    print("QUERY:", query)
    print("=" * 50)
    
    query = query.lower()
    
    # ------------------------------------
    # Follow-up questions
    # ------------------------------------

    if last_shipment_id:

        if contains_keywords(query, FOLLOW_UP_KEYWORDS):

            if not contains_keywords(query, SQL_INTENTS):

                print("RETURN SQL (FOLLOW-UP)")
                return "SQL"

    # ------------------------------------
    # Booking IDs always SQL
    # ------------------------------------

    if re.search(r"ALC-\d{4}-\d+", query, re.I):
        print("RETURN SQL (UUID)")
        return "SQL"

    # ------------------------------------
    # Shipment UUID always SQL
    # ------------------------------------

    if re.search(

        r"[0-9a-f]{8}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{4}-"
        r"[0-9a-f]{12}",

        query,

        re.I

    ):
        print("RETURN SQL (UUID)")
        return "SQL"

    entity = contains_entity(query)

    # ------------------------------------------------
    # HYBRID
    # ------------------------------------------------

    has_entity = contains_entity(query)
    has_sql = contains_keywords(query, SQL_INTENTS)
    has_hybrid = contains_keywords(query, HYBRID_INTENTS)

    if has_entity and has_hybrid:

        print("RETURN HYBRID")
        return "HYBRID"

    # ------------------------------------------------
    # SQL
    # ------------------------------------------------

    if has_entity and not has_hybrid:
        return "SQL"

    if has_sql:

        print("RETURN SQL (INTENT)")
        return "SQL"

    # ------------------------------------------------
    # VECTOR
    # ------------------------------------------------

    print("RETURN VECTOR")
    return "VECTOR"