"""
write a function that uses a generator to fetch rows one by one 
from the user_data table. You must use the Yield python generator
Prototype: def stream_users()
Your function should have no more than 1 loop
""" 

from . import seed

def stream_users():
    # connect to the database
    connection = seed.connect_prodev()
    
