import json
import re

with open("data.json", "r", encoding='utf-8') as file:
    jsFile = json.load(file)

# Timings for tea infuzion are in the 'mod de preparare' section we webscraped
# - we used regex to extract them and put them in their respective DB fields
newList = []

for elem in jsFile:
    minInfuzion = 0
    maxInfuzion = 0
    currElem = elem['mod_preparare']

    num = ""
    num = re.search(r'infuzat (.*?) min', currElem).group(1)

    if (len(num) == 1):
        maxInfuzion = int(num)
    else:
        minInfuzion = int(num[0])
        maxInfuzion = int(num[2:])
    elem['min_infuzion'] = minInfuzion
    elem['max_infuzion'] = maxInfuzion
    newList.append(elem)


with open("data_final.json", "w", encoding='utf-8') as file:
    jsFile = json.dump(newList, file, ensure_ascii=False)
