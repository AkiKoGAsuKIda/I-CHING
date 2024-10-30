import os
import json
import random
from utils import *
from datetime import datetime

ICHING=读取JSON文件('i_ching.json')


def 一次运算(蓍草, 四季=4):
    运算信息 = {}
    
    天 = random.randint(1, 蓍草)
    地 = 蓍草 - 天

    运算信息['天'], 运算信息['地'] = 天, 地

    人 = 1
    天 -= 人
    四季个数 = 0

    if 天 % 四季 != 0: 四季个数, 天剩余 = 四季个数 + 天 // 四季, 天 % 四季;
    else: 四季个数, 天剩余 = 四季个数 + 天 // 四季 - 1, 四季;

    if 地 % 四季 != 0: 四季个数, 地剩余 = 四季个数 + 地 // 四季, 地 % 四季;
    else: 四季个数, 地剩余 = 四季个数 + 地 // 四季 - 1, 四季;

    当前蓍草 = 蓍草 - (人 + 天剩余 + 地剩余)
    
    运算信息['蓍草'], 运算信息['四季'] = 当前蓍草, 四季个数
    return 运算信息


def 蓍草起卦(question):
    所有蓍草 = 50

    太极 = 1
    可变蓍草 = 所有蓍草 - 太极
    
    六爻, 运算过程 = [], {}
    for i in range(6):
        运算过程[i+1] = {}
        
        运算信息 = 一次运算(可变蓍草)
        运算过程[i+1][1] = 运算信息
        
        运算信息 = 一次运算(运算信息['蓍草'])
        运算过程[i+1][2] = 运算信息
        
        运算信息 = 一次运算(运算信息['蓍草'])
        运算过程[i+1][3] = 运算信息

        六爻.append(运算信息['四季'])

    本卦, 之卦 = [], []
    for i, 爻 in enumerate(六爻):
        if 爻 in (7, 9):
            本卦.append(0)
            if 爻 == 7: 之卦.append(0);
            else: 之卦.append(1);
        if 爻 in (6, 8):
            本卦.append(1)
            if 爻 == 8: 之卦.append(1);
            else: 之卦.append(0);
    
    now = datetime.now()
    folder_name = now.strftime("%Y-%m-%d-%H-%M-%S")
    os.makedirs(folder_name, exist_ok=True)
    
    with open(folder_name+'/运算过程.json', 'w', encoding='utf-8') as g:
        json.dump(运算过程, g, ensure_ascii=False, indent=2)
    
    with open(folder_name+'/运算结果.txt', 'w', encoding='utf-8') as g:
        n = 计算卦序(本卦)
        info = ICHING[str(n)]
        g.write(f'本卦\n')
        g.write(f'{info["卦名"]}: {info["卦辞"]}'+'\n')
        res = 爻辞信息(info, 本卦)
        for i in res: g.write(i+'\n');
        g.write(f'彖曰 {info["彖"]}'+'\n')
        g.write(f'象曰 {info["象"]}'+'\n')

        g.write(f'\n\n')
        
        n = 计算卦序(之卦)
        info = ICHING[str(n)]
        g.write(f'之卦\n')
        g.write(f'{info["卦名"]}: {info["卦辞"]}'+'\n')
        res = 爻辞信息(info, 之卦)
        for i in res: g.write(i+'\n');
        g.write(f'彖曰 {info["彖"]}'+'\n')
        g.write(f'象曰 {info["象"]}'+'\n')
        
        g.write(f'\n\n')
        
        g.write(f"你想问：{question}\n")
        
        变爻 = 寻找变爻(本卦, 之卦)
        if isinstance(变爻, str): g.write(f"{变爻}\n");
        else: g.write(f"变爻：{变爻[0]} -> {变爻[1]}，请看爻辞\n");
    
    print(f"结果已保存至{folder_name}")


if __name__ == '__main__':
    question = input("输入问题：")
    seed = generate_seed(question)
    random.seed(seed)

    蓍草起卦(question)