import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from collections import defaultdict
import os

# ==================== 解決中文字體問題（跨平台兼容） ====================
plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']  # 先使用默認無襯線字體
# 嘗試加載中文字體（兼容Windows/Mac/Linux）
try:
    # Windows
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
except:
    try:
        # Mac
        plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti TC']
    except:
        # Linux
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'Noto Sans CJK SC']

plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# ==================== 設置暗黑模式樣式 ====================
plt.style.use('dark_background')  # 開啟暗黑模式
# 自定義顏色配置
TEXT_COLOR = 'white'          # 文字顏色
GRID_COLOR = '#444444'        # 網格線顏色
AXIS_LINE_COLOR = '#666666'   # 軸線顏色
TICK_COLOR = '#888888'        # 刻度顏色

# ---------------------- 原始數據 ----------------------
data = {
    'T0': [
        ('Shake', 300, 6), ('Patty', 300, 6), ('Sober', 300, 6), ('Chub', 300, 6), ('Moth', 300, 6),
        ('台虎', 500, 6), ('Baba', 500, 6), ('Boga', 500, 6), ('JKSt', 300, 6), ('LeBo', 500, 6),
        ('Nach', 300, 6), ('WEDO', 300, 6), ('Savo', 300, 6)
    ],
    'T1': [
        ('Five', 400, 5), ('Texa', 500, 5), ('Ever', 300, 5), ('Burg', 300, 5), ('旅人', 500, 5),
        ('RouJ', 1000, 5), ('HIMa', 300, 5), ('SWBu', 800, 5), ('JBs', 500, 5), ('Omni', 500, 5),
        ('Lawr', 300, 5), ('Comf', 300, 5), ('LayB', 300, 5), ('Ninj', 500, 5), ('Liqu', 300, 5),
        ('Burg', 500, 5), ('Poun', 300, 5), ('Ping', 300, 5), ('Cafe', 800, 5), ('藍家', 100, 5),
        ('Sinc', 300, 5), ('Hale', 500, 5), ('Nola', 500, 5), ('Boom', 300, 5), ('Spro', 500, 5),
        ('BAGE', 300, 5), ('Deli', 300, 5), ('Memo', 500, 5), ('Wild', 800, 5)
    ],
    'T2': [
        ('Subw', 200, 4), ('Wool', 500, 4), ('Full', 300, 4), ('Roma', 300, 4), ('Temp', 300, 4),
        ('Craf', 500, 4), ('Park', 500, 4), ('分號', 500, 4), ('BeaB', 300, 4), ('福嗑', 300, 4),
        ('角窩', 300, 4), ('Gofl', 500, 4), ('ABea', 300, 4), ('Intr', 500, 4), ('Burg', 300, 4),
        ('Self', 300, 4), ('Three', 300, 4), ('Cluc', 300, 4), ('Toas', 300, 4), ('Liva', 300, 4),
        ('Tort', 100, 4), ('Blue', 500, 4), ('What', 500, 4), ('SALT', 800, 4), ('45Pu', 500, 4),
        ('Twen', 300, 4), ('午葉', 500, 4), ('Ilpa', 300, 4), ('Pani', 300, 4), ('Dayn', 500, 4),
        ('FaBu', 300, 4)
    ],
    'T3': [
        ('貳樓', 500, 3), ('Take', 300, 3), ('Powe', 500, 3), ('ANBu', 300, 3), ('Take', 300, 3),
        ('Lill', 500, 3), ('Past', 500, 3), ('Racl', 300, 3), ('Skra', 300, 3), ('13Bu', 300, 3),
        ('Roas', 300, 3), ('Trib', 300, 3), ('SBre', 500, 3), ('Awes', 300, 3), ('吉米', 300, 3),
        ('Loui', 300, 3), ('Burg', 300, 3), ('LeBl', 800, 3), ('Coff', 300, 3), ('饃饃', 100, 3),
        ('Savo', 100, 3), ('Retr', 300, 3), ('第二', 300, 3), ('Shed', 300, 3)
    ],
    'T4': [
        ('漢堡王', 300, 2), ('TGI', 500, 2), ('TheC', 500, 2), ('傑克', 500, 2), ('Pond', 800, 2),
        ('Hoda', 500, 2), ('MrMo', 300, 2), ('Burg', 300, 2), ('ZACZ', 100, 2), ('草根', 300, 2),
        ('Moot', 300, 2), ('青春', 500, 2), ('林斯', 300, 2), ('厭世', 500, 2), ('Munc', 300, 2),
        ('波麗', 800, 2), ('YumY', 300, 2), ('台虎', 300, 2), ('Sunr', 300, 2), ('BURNT', 300, 2),
        ('MOne', 500, 2), ('Camp', 300, 2), ('青沐', 500, 2), ('WTNC', 300, 2), ('Art', 100, 2),
        ('Babb', 100, 2), ('Corn', 500, 2), ('入口', 100, 2), ('復刻', 50, 2), ('Este', 300, 2),
        ('Joyf', 300, 2), ('覓\'s', 100, 2), ('Berg', 300, 2), ('Huge', 300, 2), ('畊PL', 300, 2),
        ('Isla', 300, 2), ('Butc', 500, 2), ('Bark', 300, 2), ('Oldi', 500, 2), ('YouS', 300, 2)
    ],
    'T5': [
        ('麥當勞', 200, 1), ('Stan', 500, 1), ('Alph', 300, 1), ('InnC', 300, 1), ('Hoot', 500, 1),
        ('吉比', 500, 1), ('Chil', 500, 1), ('CeLa', 500, 1), ('Lilla', 800, 1), ('Trin', 300, 1),
        ('樂子', 500, 1), ('Rang', 500, 1), ('AK12', 300, 1), ('Brav', 300, 1), ('ABV', 500, 1),
        ('Uncl', 300, 1), ('Stan', 300, 1), ('Wils', 500, 1), ('Barc', 500, 1), ('鱷吐司', 100, 1),
        ('Chil', 100, 1), ('江記', 300, 1), ('Doub', 500, 1), ('念饗', 500, 1), ('Waku', 500, 1),
        ('Kobi', 100, 1), ('Blah', 500, 1), ('Hungr', 100, 1), ('Park', 500, 1), ('螢火', 500, 1),
        ('LitL', 300, 1), ('BOE', 300, 1), ('Marc', 500, 1)
    ],
    'T6': [
        ('MosB', 200, 0), ('硫磺', 300, 0), ('BigA', 300, 0), ('Butt', 800, 0), ('Eds', 500, 0),
        ('Boul', 500, 0), ('Burg', 300, 0), ('Runn', 300, 0), ('0000', 300, 0), ('Roxy', 300, 0),
        ('OnTa', 500, 0), ('Secr', 300, 0), ('Juic', 300, 0), ('Burg', 300, 0), ('Paus', 300, 0),
        ('Yell', 300, 0), ('KGB', 300, 0), ('Boun', 300, 0), ('小黑', 100, 0), ('Open', 300, 0),
        ('Char', 500, 0), ('Shee', 300, 0), ('Patt', 500, 0), ('J.S.F', 500, 0), ('威宇', 300, 0),
        ('民生', 300, 0), ('茉莉', 100, 0), ('Chur', 300, 0), ('MyTy', 100, 0), ('OneM', 100, 0),
        ('Lovs', 300, 0), ('福二', 100, 0), ('嶼木', 100, 0), ('Trou', 100, 0), ('Good', 300, 0),
        ('Woos', 300, 0), ('Orom', 500, 0)
    ]
}

price_intervals = {
    50:    (0, 100),
    100:   (0, 200),
    200:   (0, 200),
    300:   (200, 400),
    400:   (400, 600),
    500:   (400, 600),
    800:   (600, 1000),
    1000:  (800, 1200)
}

# 匹配你提供圖例的顏色（調整透明度讓暗黑模式更協調）
level_colors = {
    'T0': '#E04040',  # 敲級好吃（紅）
    'T1': '#F29339',  # 滿好吃的（橙）
    'T2': '#F7D054',  # 普通好吃（淺黃）
    'T3': '#F0EE47',  # 雞肋勘吃（亮黃）
    'T4': '#72B992',  # 將就果腹（青綠）
    'T5': '#829AB1',  # 難以吞噬（灰藍）
    'T6': '#5A9FD4'   # 犬不爭食（淺藍）
}

# ---------------------- 自訂 X 軸轉換：1-200砍半，600-1200砍半 ----------------------
def x_transform(x):
    if x <= 200:
        return x / 2  # 1-200 間距砍半
    elif x <= 600:
        return 100 + (x - 200)  # 200-600 維持原間距
    else:
        return 500 + (x - 600) / 2  # 600-1200 間距砍半

# ---------------------- 橫軸：價格區間均勻散開 ----------------------
interval_point_count = defaultdict(int)
for level, shops in data.items():
    for name, x, y in shops:
        interval = price_intervals.get(x, (x-100, x+100))
        interval_point_count[(y, interval)] += 1

# ---------------------- 縱軸：每個T都在「自己T線 ~ 下一個T線」之間平均分配 ----------------------
final_data = defaultdict(list)

t_y_range = {
    'T0': (6, 5),
    'T1': (5, 4),
    'T2': (4, 3),
    'T3': (3, 2),
    'T4': (2, 1),
    'T5': (1, 0),
    'T6': (0, -1.0)
}

for level, shops in data.items():
    y_upper, y_lower = t_y_range[level]
    n = len(shops)
    current_x_pos = defaultdict(int)

    for i, (name, x, _) in enumerate(shops):
        interval_min, interval_max = price_intervals.get(x, (x-100, x+100))
        key = (y_upper, (interval_min, interval_max))
        total = interval_point_count[key]
        margin = 10
        w = interval_max - interval_min - 2*margin
        step = w/(total-1) if total>1 else 1
        raw_x = interval_min + margin + current_x_pos[key]*step
        current_x_pos[key] += 1

        new_x = x_transform(raw_x)

        if n == 1:
            new_y = y_upper
        else:
            new_y = y_upper - i * ((y_upper - y_lower) / (n - 1))

        final_data[level].append((name, new_x, new_y))

# ---------------------- 繪圖 ----------------------
# 調整圖表尺寸（稍微加大高度，確保文字不被裁切）
fig, ax = plt.subplots(figsize=(18, 14))  # 高度從12改為14
fig.patch.set_facecolor('black')  # 設置圖表整體背景為黑色

# 背景色塊（經過 x 轉換）
def rect_x(x):
    return x_transform(x)

# 1. 繪製T級區間背景色（T0-T1用T0色，T1-T2用T1色，依此類推）
# T0-T1 區間 (y=5 ~ y=6) → T0顏色
ax.add_patch(patches.Rectangle((rect_x(0), 5), rect_x(1200)-rect_x(0), 1.0, 
                               fc=level_colors['T0'], alpha=0.2, zorder=0))
# T1-T2 區間 (y=4 ~ y=5) → T1顏色
ax.add_patch(patches.Rectangle((rect_x(0), 4), rect_x(1200)-rect_x(0), 1.0, 
                               fc=level_colors['T1'], alpha=0.2, zorder=0))
# T2-T3 區間 (y=3 ~ y=4) → T2顏色
ax.add_patch(patches.Rectangle((rect_x(0), 3), rect_x(1200)-rect_x(0), 1.0, 
                               fc=level_colors['T2'], alpha=0.2, zorder=0))
# T3-T4 區間 (y=2 ~ y=3) → T3顏色
ax.add_patch(patches.Rectangle((rect_x(0), 2), rect_x(1200)-rect_x(0), 1.0, 
                               fc=level_colors['T3'], alpha=0.2, zorder=0))
# T4-T5 區間 (y=1 ~ y=2) → T4顏色
ax.add_patch(patches.Rectangle((rect_x(0), 1), rect_x(1200)-rect_x(0), 1.0, 
                               fc=level_colors['T4'], alpha=0.2, zorder=0))
# T5-T6 區間 (y=0 ~ y=1) → T5顏色
ax.add_patch(patches.Rectangle((rect_x(0), 0), rect_x(1200)-rect_x(0), 1.0, 
                               fc=level_colors['T5'], alpha=0.2, zorder=0))
# T6 區間 (y=-1 ~ y=0) → T6顏色
ax.add_patch(patches.Rectangle((rect_x(0), -1.0), rect_x(1200)-rect_x(0), 1.0, 
                               fc=level_colors['T6'], alpha=0.2, zorder=0))

# 2. 繪製價格區間的淺色背景（疊加在T級背景上，調整顏色適配暗黑模式）
price_ranges_dark = [
    (0,200,'#331111'), (200,400,'#332211'),
    (400,600,'#112211'), (600,1000,'#111122'), (800,1200,'#221122')
]
for x1, x2, c in price_ranges_dark:
    ax.add_patch(patches.Rectangle((rect_x(x1), -1.0), rect_x(x2)-rect_x(x1), 7.0, 
                                   fc=c, alpha=0.1, zorder=1))

# T 等級線（調整顏色適配暗黑模式）
for t in [0,1,2,3,4,5,6]:
    ax.axhline(t, c='#555555', lw=2, zorder=2)

# 畫點 - 改為白色（暗黑模式下更醒目）
point_size = 80
for level, shops in final_data.items():
    for name, x, y in shops:
        ax.scatter(x, y, c='white', s=point_size, alpha=1.0, lw=0, zorder=3)
        ax.text(x+5, y-0.06, name, fontsize=6.5, ha='center', va='top', zorder=4, color='white')

# 軸設定 - 只保留 0,200,400,600,800,1000,1200 標註
ax.set_xlim(rect_x(0), rect_x(1200))
raw_ticks = [0,200,400,600,800,1000,1200]
transformed_ticks = [rect_x(t) for t in raw_ticks]
tick_labels = [str(t) for t in raw_ticks]

ax.set_xticks(transformed_ticks)
ax.set_xticklabels(tick_labels, color=TICK_COLOR)

# 設置軸標籤（白色文字）
ax.set_xlabel('價格（新台幣）', fontsize=14, fontweight='bold', color=TEXT_COLOR)
ax.set_ylim(-1.5, 6.5)  # 擴大Y軸範圍，避免邊緣文字被切
ax.set_yticks([0,1,2,3,4,5,6])
ax.set_yticklabels(['T6','T5','T4','T3','T2','T1','T0'], color=TICK_COLOR)
ax.set_ylabel('好吃程度', fontsize=14, fontweight='bold', color=TEXT_COLOR)

# 設置標題（白色文字）
ax.set_title('台北漢堡指南：價格 × 好吃程度分布圖', fontsize=18, fontweight='bold', pad=20, color=TEXT_COLOR)

# 設置網格和軸線樣式
ax.grid(alpha=0.3, zorder=2, color=GRID_COLOR)
ax.spines['top'].set_color(AXIS_LINE_COLOR)
ax.spines['bottom'].set_color(AXIS_LINE_COLOR)
ax.spines['left'].set_color(AXIS_LINE_COLOR)
ax.spines['right'].set_color(AXIS_LINE_COLOR)

# --- 最終邊距調整 ---
plt.subplots_adjust(top=0.92, bottom=0.07, left=0.05, right=0.98, hspace=0.2, wspace=0.2)

# 保存圖片（確保路徑可寫入，暗黑模式下保存為黑色背景）
try:
    plt.savefig('taipei_burger_final_dark.png', dpi=300, bbox_inches='tight', facecolor='black')
    print("✅ 暗黑模式圖片已成功保存為 taipei_burger_final_dark.png")
except Exception as e:
    print(f"⚠️ 保存圖片失敗：{e}")
    print("💡 建議：請檢查當前目錄的寫入權限，或更換保存路徑")

# 顯示圖表
plt.show()