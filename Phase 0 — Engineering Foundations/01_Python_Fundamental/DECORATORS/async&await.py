# What is async and await in python?
#-> Async and await are keywords in python
#-> They are used to define asynchronous functions and to wait for the completion of asynchronous operations , respectively.
#-> Asynchronous programming help to run multiple task concurrently without blocking the main thread of executions.

# Start with import asyncio module

import asyncio

# Define function using async keyword

async def fetch_data():
    print("Starting to fetch data...")
    await asyncio.sleep(2)
    print("Data fetch successfully..")

async def other():
    asyncio.create_task(fetch_data())
    print("Doing other work while fetching data...")
    await asyncio.sleep(1)
    print("Other work done..")

async def main():
    await asyncio.gather(
        fetch_data() ,
        other()
        )
    
asyncio.run(main())


# Fetch user and orders

async def get_user(user_id):
    print(f"Fetching user with id {user_id}...")
    await asyncio.sleep(1)
    return {"id" : user_id , "name" : "Yash" }

async def get_orders(user_id):
    print(f"Fetching orders for user if {user_id}...")
    await asyncio.sleep(2)
    return [{"order_id" : 1 , "item" : "Asus Laptop"} , {"order_id" : 2 , "item" : "iphone 16"}]

async def main():
    user , order = await asyncio.gather(
        get_user(1) ,
        get_orders(1)
    ) 

    print(f"User: {user}")
    print(f"Orders: {order}")

asyncio.run(main())