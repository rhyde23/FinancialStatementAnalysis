#Fill Excel Sheet

from get_sec_data import get_data_from_edgar

companies = [
    "AAPL",
    "GOOGL",
    "MSFT"
]

forms = [
    "10-K",
    "10-Q"
]

desired_data_points = [
    "Net income",
    "Marketable securities"
]


def fill_excel_sheet() :
    for company in companies :
        for form in forms :
            print(get_data_from_edgar(company, form, desired_data_points))
    
fill_excel_sheet()
