 # =====================================================
# SHIPMENT QUERIES
# =====================================================

if entity == "shipment":

    # -------------------------------------------------
    # Search using Booking ID
    # -------------------------------------------------

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
            "message":
            "No shipment found for this Booking ID."
        }

    # -------------------------------------------------
    # Search using Shipment UUID
    # -------------------------------------------------

    if shipment_uuid:

        print("Searching shipment:", shipment_uuid)

        result = get_complete_shipment(shipment_uuid)

        print(result)

        return result

    # -------------------------------------------------
    # Total Shipment Count
    # -------------------------------------------------

    if intent == "count":

        return {
            "Total Shipments":
            query_count("shipments")
        }

    # -------------------------------------------------
    # Delayed Shipments
    # -------------------------------------------------

    if intent == "delay":

        delayed = []

        for row in get_all_shipments_with_delivery():

            shipment = get_complete_shipment(
                row["shipment_id"]
            )

            if shipment["delay_days"] > 0:

                delayed.append(shipment)

        return delayed

    # -------------------------------------------------
    # Shipment Risk
    # -------------------------------------------------

    if intent == "risk":

        level = keyword_filter(
            query,
            RISK_LEVELS
        )

        if level:

            data = []

            for row in get_all_shipments_with_delivery():

                shipment = get_complete_shipment(
                    row["shipment_id"]
                )

                if shipment["risk_level"] == level:

                    data.append(shipment)

            return data

    # -------------------------------------------------
    # Shipment Status
    # -------------------------------------------------

    status = filters.get("delivery_status")

    if status:

        return query_where(
            "shipment_delivery_history",
            "delivery_status",
            status
        )

    # -------------------------------------------------
    # Shipment Type
    # -------------------------------------------------

    shipment_type = filters.get("shipment_type")

    if shipment_type:

        return query_where(
            "shipments",
            "shipment_type",
            shipment_type
        )

    # -------------------------------------------------
    # Shipment Priority
    # -------------------------------------------------

    priority = filters.get("priority")

    if priority:

        return query_where(
            "shipments",
            "priority",
            priority
        )

    # -------------------------------------------------
    # Shipping Mode
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Fragile Shipments
    # -------------------------------------------------

    if "fragile" in query_lower:

        return query_where(
            "shipments",
            "fragile",
            True
        )

    # -------------------------------------------------
    # Insured Shipments
    # -------------------------------------------------

    if (
        "insured" in query_lower
        or "insurance" in query_lower
    ):

        return query_where(
            "shipments",
            "insurance",
            True
        )

    # -------------------------------------------------
    # Shipment by City
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Shipment by Country
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Default
    # -------------------------------------------------

    return get_all_shipments_with_delivery()

    # -------------------------------------------------
    # Shipment Status
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Shipment Type
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Shipment Priority
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Shipping Mode
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Fragile Shipments
    # -------------------------------------------------

    if "fragile" in query_lower:

        return query_where(
            "shipments",
            "fragile",
            True
        )

    # -------------------------------------------------
    # Insured Shipments
    # -------------------------------------------------

    if (
        "insured" in query_lower
        or "insurance" in query_lower
    ):

        return query_where(
            "shipments",
            "insurance",
            True
        )

    # -------------------------------------------------
    # Shipment by City
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Shipment by Country
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Default
    # -------------------------------------------------

    return get_all_shipments_with_delivery()