
from bs4 import BeautifulSoup
import requests
import time
import json


def prodPage(driver, allTeas):
    teaDict = {}

    url = driver.current_url

    req = requests.get(url)
    doc = BeautifulSoup(req.text, "html.parser")

    script_tag = doc.find("script", type="application/ld+json")
    json_data = json.loads(script_tag.string)

    name = json_data["name"]
    name = name.split(" ", 1)
    id = name[0]
    name = name[1]

    try:
        img = json_data["image"]
    except Exception as e:
        img = ""

    prodDetails = doc.find_all('div', {"class": "productAttr"})

    tip = ""
    continut = ""
    mod_preparare = ""

    for curr in prodDetails:
        if "Categorii:" in curr.text:
            tip = (curr.text.replace("Categorii: ", ""))

        if "Continut:" in curr.text:
            continut = (curr.text.replace("Continut: ", ""))

        if "Mod Preparare:" in curr.text:
            mod_preparare = (curr.text.replace("Mod Preparare: ", ""))

    print(id + " - " + name + " - " + tip)
    teaDict["id"] = id
    teaDict["name"] = name
    teaDict["image"] = img
    teaDict["continut"] = continut
    teaDict["type"] = tip
    teaDict["mod_preparare"] = mod_preparare
    allTeas.append(teaDict)
