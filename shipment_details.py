from database_query import *

booking_id = "ALC-2025-100000"

# Get Shipment
shipment = query_where(
    "shipments",
    "booking_id",
    booking_id
)

if not shipment:
    print("Shipment not found")
    exit()

shipment = shipment[0]

print("=" * 60)
print("SHIPMENT")
print("=" * 60)
print(shipment)

customer = query_where(
    "customers",
    "customer_id",
    shipment["customer_id"]
)

product = query_where(
    "products",
    "product_id",
    shipment["product_id"]
)

carrier = query_where(
    "carriers",
    "carrier_id",
    shipment["carrier_id"]
)

warehouse = query_where(
    "warehouses",
    "warehouse_id",
    shipment["warehouse_id"]
)

route = query_where(
    "routes",
    "route_id",
    shipment["route_id"]
)

vehicle = query_where(
    "vehicles",
    "vehicle_id",
    shipment["vehicle_id"]
)

weather = query_where(
    "weather",
    "weather_id",
    shipment["weather_id"]
)

customs = query_where(
    "customs",
    "customs_id",
    shipment["customs_id"]
)

print("\nCUSTOMER")
print(customer)

print("\nPRODUCT")
print(product)

print("\nCARRIER")
print(carrier)

print("\nWAREHOUSE")
print(warehouse)

print("\nROUTE")
print(route)

print("\nVEHICLE")
print(vehicle)

print("\nWEATHER")
print(weather)

print("\nCUSTOMS")
print(customs)