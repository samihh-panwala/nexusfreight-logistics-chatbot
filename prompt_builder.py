def build_messages(
    system_prompt,
    summary,
    history,
    rag_context,
    current_query
):

    MAX_SUMMARY = 1000
    MAX_HISTORY = 600
    MAX_CONTEXT = 4000

    messages = [

        {
            "role": "system",
            "content": system_prompt
        }

    ]

    # -----------------------------------
    # Conversation Summary
    # -----------------------------------

    if summary:

        messages.append({

            "role": "system",

            "content":
                "Conversation Summary:\n\n"
                + summary[:MAX_SUMMARY]

        })

    # -----------------------------------
    # Recent Conversation
    # -----------------------------------

    for msg in history[-6:]:

        messages.append({

            "role": msg["role"],

            "content":
                msg["content"][:MAX_HISTORY]

        })

    # -----------------------------------
    # Database / Document Context
    # -----------------------------------

    if rag_context:

        messages.append({

            "role": "system",

            "content":

f"""
Verified Context

The following information has already been retrieved
from the NexusFreight system.

It may include:

• Shipment records

• Customer information

• Product information

• Warehouse information

• Carrier information

• Logistics documentation

• SOPs

• Customs documentation

• AI shipment analysis

Always use this information as the primary source of truth.

Do not invent information.

Context

{rag_context[:MAX_CONTEXT]}
"""

        })

    # -----------------------------------
    # User Question
    # -----------------------------------

    messages.append({

        "role": "user",

        "content": current_query

    })

    return messages