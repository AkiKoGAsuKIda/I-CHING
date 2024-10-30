import json

with open('i_ching.json', 'r', encoding='utf-8') as g:
    x = json.load(g)

result = {}
for key, value in x.items():
    try:
        tmp = {}
        items = [x.strip() for x in value['爻辞'].split("\r\n") if x.strip()]
        for z in items:
            z1, z2 = z.split("：")[0].strip(), z.split("：")[1].strip()
            tmp[z1] = z2
        value["爻辞"] = tmp
    except Exception as e:
        print(value)
    
    result[key] = value

with open('../i_ching.json', 'w', encoding='utf-8') as g:
    json.dump(result, g, ensure_ascii=False, indent=2)