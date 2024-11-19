import ambr
import asyncio
import json
import os

async def main() -> None:
    async with ambr.AmbrAPI() as client:
        return await client.fetch_characters()

char = asyncio.run(main())


async def main() -> None:
    async with ambr.AmbrAPI() as client:
        return await client.fetch_namecards()

nc = asyncio.run(main())

char_list = {}
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

with open("encard/src/assets/data/namecard.json", "w")as out_file:
    json.dump(out, out_file, indent=4)
