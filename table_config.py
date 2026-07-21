TABLES = {

    "shipments": {

        "keywords": [
            "shipment",
            "shipments",
            "booking",
            "tracking"
        ],

        "id_columns": [
            "shipment_id",
            "booking_id"
        ],

        "search_columns": [
            "shipping_mode",
            "shipment_type",
            "priority"
        ]
    },

    "customers": {

        "keywords": [
            "customer",
            "customers",
            "client"
        ],

        "id_columns": [
            "customer_id"
        ],

        "search_columns": [
            "customer_name",
            "country",
            "city",
            "customer_status",
            "industry"
        ]
    },

    "products": {

        "keywords": [
            "product",
            "products",
            "item"
        ],

        "id_columns": [
            "product_id"
        ],

        "search_columns": [
            "product_name",
            "category",
            "supplier_name"
        ]
    },

    "carriers": {

        "keywords": [
            "carrier",
            "carriers"
        ],

        "id_columns": [
            "carrier_id"
        ],

        "search_columns": [
            "carrier_name",
            "carrier_type",
            "headquarters"
        ]
    },

    "routes": {

        "keywords": [
            "route",
            "routes"
        ],

        "id_columns": [
            "route_id"
        ],

        "search_columns": [
            "origin_city",
            "destination_city",
            "origin_country",
            "destination_country",
            "route_risk"
        ]
    },

    "warehouses": {

        "keywords": [
            "warehouse",
            "warehouses"
        ],

        "id_columns": [
            "warehouse_id"
        ],

        "search_columns": [
            "warehouse_name",
            "city",
            "state",
            "warehouse_type"
        ]
    },

    "vehicles": {

        "keywords": [
            "vehicle",
            "vehicles",
            "truck"
        ],

        "id_columns": [
            "vehicle_id"
        ],

        "search_columns": [
            "vehicle_number",
            "vehicle_type",
            "fuel_type",
            "maintenance_status"
        ]
    },

    "weather": {

        "keywords": [
            "weather"
        ],

        "id_columns": [
            "weather_id"
        ],

        "search_columns": [
            "city",
            "weather_condition"
        ]
    },

    "customs": {

        "keywords": [
            "custom",
            "customs"
        ],

        "id_columns": [
            "customs_id"
        ],

        "search_columns": [
            "cargo_type",
            "destination_country"
        ]
    },

    "shipment_delivery_history": {

        "keywords": [
            "history",
            "delivery history"
        ],

        "id_columns": [
            "history_id"
        ],

        "search_columns": [
            "delivery_status"
        ]
    },

    "ai_model_registry": {

        "keywords": [
            "model"
        ],

        "id_columns": [
            "model_id"
        ],

        "search_columns": [
            "model_name",
            "deployment_status"
        ]
    },

    "ai_feature_store": {

        "keywords": [
            "feature"
        ],

        "id_columns": [
            "feature_record_id"
        ],

        "search_columns": [
            "shipment_id"
        ]
    },

    "ai_inference_log": {

        "keywords": [
            "prediction",
            "inference"
        ],

        "id_columns": [
            "inference_id"
        ],

        "search_columns": [
            "risk_category"
        ]
    },

    "ai_monitoring_alerts": {

        "keywords": [
            "alert"
        ],

        "id_columns": [
            "alert_id"
        ],

        "search_columns": [
            "alert_status",
            "severity"
        ]
    }

}