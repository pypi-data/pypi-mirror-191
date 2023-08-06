from chenosis.client import ChenosisClient

phone_number = "27832002715"
chenosis_client = ChenosisClient(
    host="https://sandbox.api.chenosis.io",
    client_id="1WJKhc4fNAZUJ5qh7wFbJmjINQIzmgv8",
    client_secret="Jfb1zUJV3TnJ3Ohg"
)

r = chenosis_client.get_network_information(phone_number=phone_number)
print(r)
