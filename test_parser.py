from sql_parser import parse_query

queries = [

    "Show all active customers",

    "Count shipments",

    "Show high priority shipments",

    "Shipment 5fd50c5c-973f-43bc-a629-06e4b5cd541b",

    "Show booking ALC-2026-101"

]

for q in queries:

    print("=" * 50)
    print(q)
    print(parse_query(q))
    
print("=" * 50)
print("Show import shipments")
print(parse_query("Show import shipments"))

print("=" * 50)
print("Show business customers")
print(parse_query("Show business customers"))

print("=" * 50)
print("Show insured shipments")
print(parse_query("Show insured shipments"))

print("=" * 50)
print("Show air shipments")
print(parse_query("Show air shipments"))