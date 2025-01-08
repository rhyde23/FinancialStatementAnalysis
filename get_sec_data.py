#Reggie Hyde

from sec_api import QueryApi

import requests

from bs4 import BeautifulSoup


with open("C:\\Users\\u9704\\Downloads\\sec_api_key.txt", 'r') as file :
    
    api_key = file.readline().strip()

query_api = QueryApi(api_key=api_key)

#Query
query = {
    "query": {
        "query_string": {
            "query": "ticker:AAPL AND formType:\"10-K\""
        }
    },
    "from": "0",
    "size": "1",
    "sort": [{"filedAt": {"order": "desc"}}]
}

filings = query_api.get_filings(query)

if filings and filings["filings"] :
    
    latest_filing = filings["filings"][0]

    report_url = latest_filing["linkToFilingDetails"]

else :
    
    print("No filings found.")


headers = {
    "User-Agent": "Personal Tool - contact: reginaldjhyde@gmail.com",
    "Accept-Encoding": "gzip, deflate"
}

edgar_resp = requests.get(report_url, headers=headers)

soup = BeautifulSoup(edgar_resp.content, "html.parser")
for f in soup.find_all("td") :
    print(f.text)
