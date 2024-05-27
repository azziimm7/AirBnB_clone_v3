#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.city import City
from models.state import State
from models.user import User
from models.place import Place

print("All objects: {}".format(storage.all(User)))

print("All objects: {}".format(storage.all(City)))
print("All objects: {}".format(storage.all(Place)))


dic = {'city_id':'196a003e-e748-4597-a992-f56456545382', 'user_id':'66b01ff0-f48c-422d-beb8-77776bba399d', 'name':'HYPER',
       'number_rooms':10,  "number_bathrooms":2, 'price_by_night':1000}
obj = Place(**dic)
obj.save()
print("All objects: {}".format(storage.all(Place)))

# storage.new(obj)
# print("All objects: {}".format(storage.all(City)))
# print("State objects: {}".format(storage.count(State)))

# first_state_id = list(storage.all(User).values())[0].id
# print("First state: {}".format(storage.get(User, first_state_id)))
