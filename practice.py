from datetime import date, timedelta
today = date.today()
tomorrow = today + timedelta(days=1)  # today + 1 day is tomorrow
products = [
    {'sku': '1', 'expiration_date': today, 'price': 100.0},
    {'sku': '2', 'expiration_date': tomorrow, 'price': 50},
    {'sku': '3', 'expiration_date': today, 'price': 20},
]
for product in products:
    if product['expiration_date'] != today:
        continue # skip that loop to the next 
    product['price'] *= 0.8  # equivalent to applying 20% discount
    print(
        'Price for sku', product['sku'],
        'is now', product['price'])


####################################### STRING MANIPULATION FUNCTIONS###################################################
name = "Dylan dzvene"
print(name[:5])  # Get the first 5 letters
print(name[5:])  # start getting letters from index 5


class triangle():
    def __init__(self, base, hieght) -> None:
        self.base = base
        self.hieght = hieght

    def area(self):
        return (0.5*self.base*self.hieght)


tria = triangle(5, 10)
print("the are area is ", tria.area())

print(f"my name is {name[:5]} {name[5:]}")

list1 = [1, 5, 6.9, 89, 4]
list1.append(55)
list1.insert(0, 66)  # to specify the position of insertation
print(list1)
list1.reverse()
min(list1)  # to print the minimum value
print("the minimum value of the list is ", min(list1))
print(type(name))  # outputs <class 'str'>
for i in list1:
    print(i)

for i in range(1, 5):
    print(list1[i])

print(list1)
###################################################################################################
lstnames = ["dylan", "tashinga", "precious", "Dzvene"]
lstage = [23, 25, 23, 50]

for name, age in zip(lstnames, lstage):
    print(name, age)

###################################################################################################
