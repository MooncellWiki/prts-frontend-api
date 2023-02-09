import json

from src.config import GAMEDATA_BASE_DIR


def trans_prof(profession):
    return {
        "PIONEER": "先锋",
        "WARRIOR": "近卫",
        "SNIPER": "狙击",
        "SUPPORT": "辅助",
        "CASTER": "术师",
        "SPECIAL": "特种",
        "MEDIC": "医疗",
        "TANK": "重装",
    }[profession]

def fetch_data(path):
    with open(f"{GAMEDATA_BASE_DIR}/{path}", encoding="utf-8") as f:
        return json.load(f)
