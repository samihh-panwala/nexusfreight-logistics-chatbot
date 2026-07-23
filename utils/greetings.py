GREETINGS = {
    "hi",
    "hello",
    "hey",
    "hii",
    "hiii",
    "good morning",
    "good afternoon",
    "good evening",
    "how are you",
    "thanks",
    "thank you",
    "bye",
    "goodbye"
}

GENERAL_QUERIES = {
    "who are you",
    "what can you do",
    "help",
    "what is this",
    "what are you"
}


def is_greeting(query):
    query = query.lower().strip()
    return query in GREETINGS


def is_general_query(query):
    query = query.lower().strip()
    return query in GENERAL_QUERIES


def greeting_response():
    return """
Hello! 👋 Welcome to NexusFreight AI.

I'm your intelligent enterprise logistics assistant.

I can help you with:

• Shipment information
• Customer details
• Warehouse information
• Delivery history
• Vehicles & carriers
• Customs & Incoterms
• Shipment risk analysis
• Logistics knowledge

How may I assist you today?
"""


def assistant_response():
    return """
I am NexusFreight AI, an enterprise logistics assistant developed to help employees retrieve logistics information.

I can answer questions related to:

• Shipments
• Warehouses
• Customers
• Delivery history
• Routes
• Vehicles
• Customs
• Incoterms
• Shipment risk analysis
• Company logistics knowledge

Please ask your logistics-related question.
"""