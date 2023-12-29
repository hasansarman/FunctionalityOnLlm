from chatlab import Chat,system
import openai
import os
import asyncio
openai.api_key = "functionary" # We just need to set this something other than None
os.environ['OPENAI_API_KEY'] = "functionary" # chatlab requires us to set this too
openai.api_base = "http://localhost:18000/v1"

# now provide the function with description
def get_car_price(car_name: str):
    """this function is used to get the price of the car given the name
    :param car_name: name of the car to get the price
    """
    car_price = {
        "tang": {"price": "$20000"},
        "song": {"price": "$25000"} 
    }
    for key in car_price:
        if key in car_name.lower():
            return {"price": car_price[key]}
    return {"price": "unknown"}



chat = Chat(model="meetkai/functionary-7b-v2",base_url=openai.api_base,api_key=openai.api_key)
chat.register(get_car_price)  # register this function
async def aboo():
    await chat.submit("what is the price of the car named Tang?") # submit user prompt
    # print the flow
    for message in chat.messages:
        role = message["role"].upper()
        if "function_call" in message:
            func_name = message["function_call"]["name"]
            func_param = message["function_call"]["arguments"]
            print(f"{role}: call function: {func_name}, arguments:{func_param}")
        else:
            content = message["content"]
            print(f"{role}: {content}")
async def main():
    await aboo()
asyncio.run(main())
