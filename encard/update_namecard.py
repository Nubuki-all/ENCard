import ambr
import asyncio
import json
import os

async def update():
    async with ambr.AmbrAPI(cache_ttl=30) as client:
        char = await client.fetch_characters()
        nc = await client.fetch_namecards()
    
    char_list = {}
    dir = os.path.dirname(__file__)
    file = f"{dir}/src/assets/data/namecard.json"
    for x in char:
        char_list.update({x.id: x.name}) if not x.id in char_list else None
    
    out = {}
    for id in list(char_list.keys()):
        for x in nc:
            if ((str(id)).startswith("10000005-") or (str(id)).startswith("10000007-")):
                if x.id == 210001:
                    pre_image, _e = os.path.splitext(x.icon)
                    image = pre_image.replace("UI_NameCardIcon", "UI_NameCardPic")
                    image += "_P.png"
                    out.update({id: {"id": x.id, "icon": x.icon, "image": image}})
                    break
            elif x.type == 'bond' and x.name.startswith(char_list.get(id)):
                pre_image, _e = os.path.splitext(x.icon)
                image = pre_image.replace("UI_NameCardIcon", "UI_NameCardPic")
                image += "_P.png"
                out.update({id: {"id": x.id, "icon": x.icon, "image": image}})
                break
    for x in nc:
        if x.id == 210192:
            out.update({10000005: {"id": x.id, "icon": x.icon, "image": x.icon}})
            out.update({10000007: {"id": x.id, "icon": x.icon, "image": x.icon}})
    
    with open(file, "w")as out_file:
        json.dump(out, out_file, indent=4)

    print("Successfully updated namecards.")
