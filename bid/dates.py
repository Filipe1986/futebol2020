from datetime import datetime, timedelta

x = datetime.now()
print(x)
print(x.strftime("%d/%m/%Y"))
y = x - timedelta(days=1)
print('past ', y)

print( datetime.now().month)

date = datetime(2020, 3, 13)

print(date.strftime("%d/%m/%Y"))

date = datetime(2019, 12, 31)
print(date.year)