from string import Template
import requests


def call_boss_detail(query : str, company_id : str, user_token) -> str:
    """
    Call boss detail
    """

    # Define the URL
    url = "https://portal.myhr.co.th/chatapi/center/$company_id?api=%2Fplus%2Femployee%2Fboss-detail"

    # Define the headers
    headers = {
        "Authorization": "Bearer " +user_token
    }

    urlTemplate = Template(url)
    templateData = {"company_id": company_id}
    requestUrl = urlTemplate.safe_substitute(templateData)

    # Send the request
    response = requests.get(requestUrl, headers=headers)

    # Print the response
    print(f"Status Code: {response.status_code}")
    print("Response Body:", response.text)

    return response.text


# call_boss_detail(company_id=company_id, user_token=user_token)

