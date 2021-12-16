from datetime import date, datetime

string = "15/12/21"

string2date = datetime.strptime(string, '%d/%m/%y')

print(type(string2date))

