import asyncio
import json

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import *

def trans_rarity(rarity):
    return {0: "一星", 1: "二星", 2: "三星", 3: "四星", 4: "五星", 5: "六星"}[rarity]


async def fetch_char_data():
    with open(f"{GAMEDATA_BASE_DIR}/excel/character_table.json") as f:
        return json.load(f)


async def fetch_item_data():
    with open(f"{GAMEDATA_BASE_DIR}/excel/item_table.json") as f:
        return json.load(f)


async def ensure_item_exists(item_demand, item_name, char_id, char_detail):
    if not item_demand.get(item_name):
        item_demand[item_name] = {}
    if not item_demand[item_name].get(char_id):
        item_demand[item_name][char_id] = {
            "rarity": char_detail["rarity"],
            "name": char_detail["name"],
            "profession": char_detail["profession"],
            "elite": 0,
            "skill": 0,
            "mastery": [0, 0, 0],
        }


async def get_item_demand():
    character_table = await fetch_char_data()
    item_table = await fetch_item_data()

    item_demand = {}
    for char_id, char_detail in character_table.items():

        if char_detail["profession"] == "TRAP" or char_detail["profession"] == "TOKEN":
            continue

        for phase in char_detail["phases"]:
            if phase["evolveCost"]:
                for evolve_cost_item in phase["evolveCost"]:
                    item_name = item_table["items"][evolve_cost_item["id"]]["name"]
                    await ensure_item_exists(
                        item_demand, item_name, char_id, char_detail
                    )
                    item_demand[item_name][char_id]["elite"] += evolve_cost_item[
                        "count"
                    ]

            if char_detail["skills"]:
                for skill_level_up in char_detail["allSkillLvlup"]:
                    if skill_level_up["lvlUpCost"]:
                        for demand in skill_level_up["lvlUpCost"]:
                            item_name = item_table["items"][demand["id"]]["name"]
                            await ensure_item_exists(
                                item_demand, item_name, char_id, char_detail
                            )
                            item_demand[item_name][char_id]["skill"] += demand["count"]

                for skill in char_detail["skills"]:
                    if skill["levelUpCostCond"]:
                        for cost_cond in skill["levelUpCostCond"]:
                            if cost_cond["levelUpCost"]:
                                i = 0
                                for demand in cost_cond["levelUpCost"]:
                                    item_name = item_table["items"][demand["id"]][
                                        "name"
                                    ]
                                    await ensure_item_exists(
                                        item_demand, item_name, char_id, char_detail
                                    )
                                    item_demand[item_name][char_id]["mastery"][
                                        i
                                    ] += demand["count"]
                                    i += 1

    for item_name, demand in item_demand.items():
        print(item_name, item_demand)


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    job = scheduler.add_job(get_item_demand, "interval", seconds=5)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass