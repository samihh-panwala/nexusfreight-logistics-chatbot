import re


def route_query(query):

    query = query.lower()

    # ==========================================
    # SQL KEYWORDS
    # ==========================================

    sql_keywords = [

        "count",
        "how many",
        "total",
        "average",
        "avg",
        "maximum",
        "minimum",
        "highest",
        "lowest",
        "top",
        "list",
        "show",
        "display",
        "find",
        "search",
        "shipment",
        "shipments",
        "customer",
        "customers",
        "carrier",
        "carriers",
        "route",
        "routes",
        "warehouse",
        "warehouses",
        "vehicle",
        "vehicles",
        "product",
        "products",
        "weather",
        "customs",
        "delivery history",
        "tracking",
        "booking id"
    ]

    # ==========================================
    # VECTOR KEYWORDS
    # ==========================================

    vector_keywords = [

        "what is",
        "what are",
        "define",
        "definition",
        "explain",
        "procedure",
        "process",
        "workflow",
        "policy",
        "policies",
        "guideline",
        "guidelines",
        "incoterms",
        "letter of credit",
        "customs clearance",
        "warehouse handling",
        "documentation",
        "international trade",
        "logistics",
        "transportation",
        "freight"
    ]

    # ==========================================
    # HYBRID KEYWORDS
    # ==========================================

    hybrid_keywords = [

        "why",
        "reason",
        "impact",
        "analysis",
        "compare",
        "performance",
        "delay",
        "delayed",
        "rain",
        "rainy",
        "storm",
        "weather delay",
        "route risk",
        "carrier performance",
        "shipment delay",
        "sea shipment",
        "air shipment"
    ]

    # ==========================================
    # UUID
    # ==========================================

    if re.search(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        query,
        re.I
    ):
        return "SQL"

    # ==========================================
    # Booking ID
    # ==========================================

    if re.search(r"ALC-\d{4}-\d+", query, re.I):
        return "SQL"

    # ==========================================
    # HYBRID
    # ==========================================

    if any(word in query for word in hybrid_keywords):
        return "HYBRID"

    # ==========================================
    # VECTOR
    # ==========================================

    if any(word in query for word in vector_keywords):
        return "VECTOR"


    # ==========================================
    # SQL
    # ==========================================

    if any(word in query for word in sql_keywords):
        return "SQL"


    # ==========================================
    # DEFAULT
    # ==========================================

    return "VECTOR"