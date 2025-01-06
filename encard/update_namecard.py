import aiohttp 
import asyncio
import json
import os

async def fetch_data(url): 
    async with aiohttp.ClientSession() as session: 
        async with session.get(url) as response: 
            if response.status == 200: 
                data = await response.json() 
                return data 
            else: 
                print(f"Error: {response.status}") 
                return None

dir = os.path.dirname(__file__)
file = f"{dir}/src/assets/data/namecard.json"
 
link_image = "https://gi.yatta.moe/assets/UI/namecard/{image}.png" 
link_icon = "https://gi.yatta.moe/assets/UI/namecard/{icon}.png" 
default_icon = "https://gi.yatta.moe/assets/UI/namecard/UI_NameCardIcon_0.png" 
default_image = "https://gi.yatta.moe/assets/UI/namecard/UI_NameCardPic_0_P.png" 
 
json_new = {} 
 
async def update(): 
    charter_list = await fetch_data("https://gi.yatta.moe/api/v2/en/avatar?vh=5303") 
    for key in charter_list["data"]["items"]: 
        data_charter = await fetch_data(f"https://gi.yatta.moe/api/v2/en/avatar/{key}?vh=5303") 
        if data_charter["data"]["other"] is None: 
            json_new[key] = {"id": 210001, "icon": default_icon, "image": default_image}        
            continue 
        output_string = data_charter["data"]["other"]["nameCard"]["icon"].replace("Icon_", "Pic_") 
        output_string += "_P" 
        json_new[key] = {"id": data_charter["data"]["other"]["nameCard"]["id"], "icon": link_icon.format(icon = data_charter["data"]["other"]["nameCard"]["icon"]), "image": link_image.format(image = output_string)}        


    with open(file, "w")as out_file:
        json.dump(json_new, out_file, indent=4)
