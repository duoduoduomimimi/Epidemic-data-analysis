import random
import folium
from folium import FeatureGroup, Marker, LayerControl, DivIcon

all_adds = [[[29.878105319486554, 121.92272110636715], [29.874836657731702, 121.92229441125005]],
            [[29.883115282835508, 121.92029666962706], [29.80106423949353, 122.00142183173142]]]
all_locs = [[['宁波市柴桥街道薪桥北路162号附近农村自建房'], ['宁波市柴桥惠百佳快餐店']],
            [['宁波市北仑区第二人民医院'], ['宁波市北仑区人民医院']]]
colors = ['red', 'lightgreen', 'blue', 'darkblue', 'darkgreen', 'white', 'lightblue', 'beige', 'lightred', 'cadetblue', 'lightgray', 'orange', 'gray', 'green', 'black', 'purple', 'darkpurple', 'darkred', 'pink']
markers = ['ambulance', 'taxi', 'bell', 'bicycle','plug','volume-control-phone','phone-square']

map = folium.Map(location=[29.866068124069646, 121.63084278185603, ],
                 tiles='https://rt0.map.gtimg.com/tile?z={z}&x={x}&y={-y}', # 高德街道图
                 attr='default',
                 zoom_start=12)

# 批量在map中，标记地点

num = 0
for adds, locs in zip(all_adds, all_locs):
    # color = random.choice(colors)  # 从中随机选取一种颜色
    marker = markers[num]
    num += 1
    print(marker)
    if num > 0:
        group = FeatureGroup(name=f"病例{num}轨迹")
    for add, loc in zip(adds, locs):
        Marker(location=add, popup=loc[0], icon=DivIcon(
            icon_size=(150, 36),
            icon_anchor=(7, 20),
            html=f'<div style="font-size: 18pt; color : black">{num}</div>',
        )).add_to(map)
        # Marker(location=add, popup=loc[0], icon=folium.Icon(prefix='fa', icon=marker)).add_to(group)
        # print(add)
        # print(type(add))
        # print(add[0])
        # print(type(add[0]))
        # print(loc)
        # print(type(loc))
        # print(loc[0])
        # print(type(loc[0]))

    group.add_to(map)

LayerControl().add_to(map)



map.save('four.html')

