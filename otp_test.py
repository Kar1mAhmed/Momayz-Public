import requests

# Define the base URL
base_url = "https://smsmisr.com/api/OTP/"

# Define the query parameters
params = {
    "environment": "2",
    "username": "56a55ca4-0e7a-4101-bb5d-948d1a3a18bb",
    "password": "f13f2ba17ccdab76de5ce2f3e6672ea6a6c8bc875dd277f37b8f1c06fb1aa9ff",
    "sender": "b611afb996655a94c8e942a823f1421de42bf8335d24ba1f84c437b2ab11ca27",
    "mobile": "201551022078",
    "template": "58a6fba490f281f6c73f6d7db9a221a98c30dc81af70d15951ecc85a54012af5",
    "otp": "KoskManga"
}

# Send the GET request
response = requests.post(base_url, params=params)

# Check the response status code and handle different cases
if response.status_code == 200:
    response_data = response.json()
    if "code" in response_data:
        code = response_data["code"]
        if code == "4901":
            print("Message submitted successfully")
            print("SMSID:", response_data.get("SMSID"))
            print("Cost:", response_data.get("Cost"))
        elif code == "4906":
            print("Insufficient credit.")
        elif code == "4907":
            print("Server under updating.")
        # Add more cases for other error codes as needed
        else:
            print(f"Received response with code {code}.")
    else:
        print("Unexpected response data:", response_data)
else:
    print("Request failed with status code:", response.status_code)
    print("Error message:", response.text)
