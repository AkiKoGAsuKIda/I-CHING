import time
import json
import hashlib


def generate_seed(text):
    seed1 = int(hashlib.sha256(text.encode()).hexdigest(), 16) % (2**32)
    
    timestamp = str(time.time())
    seed2 = int(hashlib.sha256(timestamp.encode()).hexdigest(), 16) % (2**32)
    
    combined_seed = (seed1 + seed2) % (2**32)
    return combined_seed


def 计算卦序(卦, up=True):
    卦序 = 1
    
    if up: 卦 = 卦[::-1];
    for i in range(6):
        卦序 += 2**i * 卦[i]

    return 卦序


def 读取JSON文件(path):
    with open(path, 'r', encoding='utf-8') as g:
        obj = json.load(g)
        
    return obj


def 爻辞信息(卦信息, 卦, up=True):
    阴阳可视化 = {1: '——  ——', 0: '——————'}
    爻 = {1: '六', 0: '九'}
    
    if up: 卦 = 卦[::-1];
    
    x1_name = f"上{爻[卦[0]]}"
    x1 = f"{阴阳可视化[卦[0]]}\t{x1_name}: {卦信息['爻辞'][x1_name]}"
    
    x2_name = f"{爻[卦[1]]}五"
    x2 = f"{阴阳可视化[卦[1]]}\t{x2_name}: {卦信息['爻辞'][x2_name]}"
    
    x3_name = f"{爻[卦[2]]}四"
    x3 = f"{阴阳可视化[卦[2]]}\t{x3_name}: {卦信息['爻辞'][x3_name]}"
    
    x4_name = f"{爻[卦[3]]}三"
    x4 = f"{阴阳可视化[卦[3]]}\t{x4_name}: {卦信息['爻辞'][x4_name]}"
    
    x5_name = f"{爻[卦[4]]}二"
    x5 = f"{阴阳可视化[卦[4]]}\t{x5_name}: {卦信息['爻辞'][x5_name]}"
    
    x6_name = f"初{爻[卦[5]]}"
    x6 = f"{阴阳可视化[卦[5]]}\t{x6_name}: {卦信息['爻辞'][x6_name]}"
    
    return (x1, x2, x3, x4, x5, x6)


def 寻找变爻(本卦, 之卦, up=True):
    爻 = {1: '六', 0: '九'}
    template = {1: '上{}', 2: '{}五', 3: '{}四', 4: '{}三', 5: '{}二', 6: '初{}'}
    
    if up: 本卦, 之卦 = 本卦[::-1], 之卦[::-1];
    
    tmp = -1
    for i in range(6):
        if 本卦[i] != 之卦[i]: 
            tmp = i + 1
            break
    
    if tmp == -1:
        return '没有变爻，请看卦辞'
    
    本卦变爻, 之卦变爻 = template[tmp].format(爻[本卦[tmp-1]]), template[tmp].format(爻[之卦[tmp-1]])
    return 本卦变爻, 之卦变爻