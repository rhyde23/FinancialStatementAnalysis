#Reggie Hyde

from sec_api import QueryApi

import requests, re

from bs4 import BeautifulSoup


with open("C:\\Users\\u9704\\Downloads\\sec_api_key.txt", 'r') as file :
    
    api_key = file.readline().strip()

query_api = QueryApi(api_key=api_key)


def get_report_url(ticker, form_type) :
    #Query
    query = {
        "query": {
            "query_string": {
                "query": "ticker:" + ticker + " AND formType:\"" + form_type + "\""
            }
        },
        "from": "0",
        "size": "1",
        "sort": [{"filedAt": {"order": "desc"}}]
    }

    filings = query_api.get_filings(query)

    if filings and filings["filings"] :
        
        latest_filing = filings["filings"][0]

        return latest_filing["linkToFilingDetails"]

    else :
        
        print("No filings found.")

def convert_to_millions(string) :

    return int("".join(re.findall("[0-9]+", string)))*1000000


def get_data_from_edgar(ticker, form_type, desired_data_points) :

    headers = {
        "User-Agent": "Personal Tool - contact: reginaldjhyde@gmail.com",
        "Accept-Encoding": "gzip, deflate"
    }

    report_url = get_report_url(ticker, form_type)
    
    request = requests.get(report_url, headers=headers)
    
    soup = BeautifulSoup(request.content, "html.parser")
    
    collected_data_points = {}
    
    for data_point in desired_data_points :
        
        tag = soup.find(lambda tag: tag.name == "td" and tag.text == data_point)

        parent_tr = tag.find_parent("tr")
        
        collected_data_points[data_point] = convert_to_millions([td.text for td in parent_tr.find_all("td") if not td.text in ["", "$"]][1:][0])
        
    return collected_data_points

print(get_data_from_edgar("AAPL", "10-K", ["Net income", "Marketable securities"]))
