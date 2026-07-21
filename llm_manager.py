import time

from providers.groq_provider import generate_response as groq_generate
from providers.gemini_provider import generate_response as gemini_generate
from providers.openrouter_provider import generate_response as openrouter_generate


PROVIDERS = [

    ("Groq", groq_generate),

    ("Gemini", gemini_generate),

    ("OpenRouter", openrouter_generate)

]


def generate_response(messages):

    errors = []

    for provider_name, provider_function in PROVIDERS:

        print("\n" + "=" * 50)
        print(f"Trying Provider : {provider_name}")
        print("=" * 50)

        start = time.time()

        try:

            response = provider_function(messages)

            elapsed = round(time.time() - start, 2)

            if response is None:
                raise Exception("Provider returned None.")

            if not isinstance(response, str):
                raise Exception("Provider returned invalid response type.")

            response = response.strip()

            if len(response) == 0:
                raise Exception("Empty response returned.")

            print(f"{provider_name} Success")
            print(f"Response Time : {elapsed} sec")

            return response

        except Exception as e:

            elapsed = round(time.time() - start, 2)

            print(f"{provider_name} Failed")
            print(f"Time : {elapsed} sec")
            print(f"Reason : {e}")

            errors.append(
                f"{provider_name}: {str(e)}"
            )

    print("\nAll providers failed.\n")

    raise Exception(

        "\n".join(errors)

    )