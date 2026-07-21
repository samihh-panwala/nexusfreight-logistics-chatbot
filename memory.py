MAX_HISTORY = 12


class ConversationMemory:

    def __init__(self):

        self.messages = []

        self.summary = ""

        # Current references
        self.last_shipment_id = None
        self.last_booking_id = None
        self.last_customer = None
        self.last_carrier = None
        self.last_route = None

        # Recent references
        self.shipment_history = []
        self.customer_history = []
        self.carrier_history = []

    # ---------------------------------

    def add_user(self, message):

        self.messages.append({

            "role": "user",
            "content": message

        })

    # ---------------------------------

    def add_assistant(self, message):

        self.messages.append({

            "role": "assistant",
            "content": message

        })

    # ---------------------------------

    def remember_shipment(self, shipment_id):

        if not shipment_id:
            return

        self.last_shipment_id = shipment_id

        if shipment_id not in self.shipment_history:

            self.shipment_history.append(shipment_id)

        self.shipment_history = self.shipment_history[-10:]

    # ---------------------------------

    def remember_customer(self, customer):

        if not customer:
            return

        self.last_customer = customer

        if customer not in self.customer_history:

            self.customer_history.append(customer)

        self.customer_history = self.customer_history[-10:]

    # ---------------------------------

    def remember_carrier(self, carrier):

        if not carrier:
            return

        self.last_carrier = carrier

        if carrier not in self.carrier_history:

            self.carrier_history.append(carrier)

        self.carrier_history = self.carrier_history[-10:]

    # ---------------------------------

    def get_recent_messages(self, limit=6):

        return self.messages[-limit:]

    # ---------------------------------

    def clear(self):

        self.messages = []

        self.summary = ""

        self.last_shipment_id = None
        self.last_booking_id = None
        self.last_customer = None
        self.last_carrier = None
        self.last_route = None

        self.shipment_history = []
        self.customer_history = []
        self.carrier_history = []

    # ---------------------------------

    def need_summary(self):

        return len(self.messages) > MAX_HISTORY

    # ---------------------------------

    def summarize(self):

        old_messages = self.messages[:-6]

        summary = ""

        if self.last_shipment_id:

            summary += f"Current Shipment: {self.last_shipment_id}\n"

        if self.last_booking_id:

            summary += f"Booking ID: {self.last_booking_id}\n"

        if self.last_customer:

            summary += f"Customer: {self.last_customer}\n"

        if self.last_carrier:

            summary += f"Carrier: {self.last_carrier}\n"

        if self.last_route:

            summary += f"Route: {self.last_route}\n"

        if self.shipment_history:

            summary += (
                "\nRecent Shipments: "
                + ", ".join(self.shipment_history)
                + "\n"
            )

        summary += "\nConversation Summary:\n"

        for msg in old_messages:

            if msg["role"] == "user":

                summary += f"User: {msg['content']}\n"

            else:

                summary += f"Assistant: {msg['content'][:250]}\n"

        if self.summary:

            self.summary += "\n\n" + summary

        else:

            self.summary = summary

        self.messages = self.messages[-6:]