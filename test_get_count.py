#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.city import City
from models.amenity import Amenity

print("All objects: {}".format(storage.all(Amenity)))
# obj = City()
# obj.save()
# # storage.new(obj)
# print("All objects: {}".format(storage.all(City)))
# print("State objects: {}".format(storage.count(State)))

# first_state_id = list(storage.all(User).values())[0].id
# print("First state: {}".format(storage.get(User, first_state_id)))
