# coding:utf-8
import os
import re
import random
import openpyxl
import requests
import folium
from folium import FeatureGroup, Marker, LayerControl, DivIcon

#  Font Awesome markers
markers = ['address-book', 'address-book-o', 'address-card', 'address-card-o',
           'id-badge', 'id-card', 'id-card-o', 'adjust',
           'anchor', 'archive', 'asterisk', 'at',
           'balance-scale', 'ban', 'barcode', 'bars',
           'battery-empty', 'battery-full', 'battery-half', 'battery-quarter',
           'battery-three-quarters', 'bed', 'beer', 'bell',
           'bell-o', 'bell-slash', 'bell-slash-o', 'binoculars',
           'birthday-cake', 'bluetooth', 'bluetooth-b', 'bomb',
           'book', 'bookmark', 'bookmark-o', 'briefcase',
           'bug', 'building', 'building-o', 'bullhorn',
           'bullseye', 'calculator', 'calendar', 'calendar-check-o',
           'camera', 'camera-retro', 'certificate', 'check',
           'check-circle', 'check-circle-o', 'child', 'circle-thin',
           'clock-o', 'clone', 'cloud', 'cloud-download',
           'cloud-upload', 'code', 'code-fork', 'coffee',
           'cogs', 'comment', 'comment-o', 'commenting',
           'commenting-o', 'comments', 'comments-o', 'compass',
           'copyright', 'crop', 'crosshairs', 'cube',
           'cubes', 'cutlery', 'dashboard', 'database',
           'desktop', 'diamond', 'download', 'edit',
           'ellipsis-h', 'ellipsis-v', 'envelope', 'envelope-o',
           'envelope-square', 'envelope-open', 'envelope-open-o', 'eraser',
           'exclamation', 'exclamation-circle', 'external-link', 'fa-external-link-square',
           'eye', 'eye-slash', 'low-vision', 'fax',
           'female', 'film', 'filter', 'fire',
           'fire-extinguisher', 'flag', 'flag-o', 'flash',
           'flask', 'folder', 'folder-o', 'folder-open',
           'folder-open-o', 'frown-o', 'futbol-o', 'gamepad',
           'gavel', 'gift', 'glass', 'globe',
           'graduation-cap', 'hashtag', 'hdd-o', 'headphones',
           'heart', 'heart-o', 'history', 'heartbeat',
           'home', 'hourglass', 'hourglass-end', 'hourglass-half',
           'hourglass-o', 'hourglass-start', 'i-cursor', 'image',
           'inbox', 'info', 'info-circle', 'key',
           'keyboard-o', 'language', 'laptop', 'leaf',
           'lemon-o', 'level-down', 'level-up', 'life-ring',
           'lightbulb-o', 'location-arrow', 'lock', 'magic',
           'male', 'map', 'map-marker',  'map-o',
           'map-signs', 'meh-o', 'microphone', 'microphone-slash',
           'minus', 'minus-circle', 'mobile', 'moon-o',
           'mouse-pointer', 'music', 'music', 'newspaper-o',
           'object-ungroup', 'paint-brush', 'paper-plane', 'paper-plane-o',
           'paw', 'pencil', 'pencil-square', 'percen',
           'phone', 'phone-square', 'volume-control-phone', 'plug',
           'plus', 'plus-circle', 'power-off', 'print',
           'puzzle-piece', 'qrcode', 'question', 'question-circle',
           'question-circle-o', 'random', 'recycle', 'registered',
           'reply', 'reply-all', 'retweet', 'road',
           'rss', 'rss-square', 'search', 'search-minus',
           'search-plus', 'server', 'share', 'share-alt',
           'share-alt-square', 'share-square', 'share-square-o', 'shield']

# folium中所支持的颜色种类
colors = ['red', 'lightgreen', 'blue', 'darkblue',
          'darkgreen', 'white', 'lightblue', 'beige',
          'lightred', 'cadetblue', 'lightgray', 'orange',
          'gray', 'green', 'black', 'purple',
          'darkpurple', 'darkred', 'pink']

# AK = "1vc6xuWUmdBzEYdnyEeucNqP31k41Ocw" #百度AK
# AK = "g3BKaOdwqnCI1Knhe0AXSFW0gESg6HE7"
# AK = "SUsO1PsNTB3Fpo7oVuiFvR0T1WEHpyKU"
# AK = "cvtGl9H0Dr2O4o56H4oKioOgY1xbNqlv"
AK = "BebX5c5SgX38LvgZTSjZeTtujB9N0YGa"
# ret_coordtype = gcj02ll 采用火星坐标系

# 从excel表中读取疫情数据
def getDataFromExcel(path):
    ex = os.path.join(os.getcwd(), '{}'.format(path))
    wb = openpyxl.load_workbook(path)  # 打开excel文件
    ws = wb['Sheet1']
    all_value = []
    for row in ws.values:
        all_value.append(row)
    del (all_value[0])  # 删除excel表中的title数据
    all_row = []
    for i in all_value:
        row = []
        for j in i:
            row.append(j)
        all_row.append(row)  # 将元组列表转换成嵌套列表
    # print(all_row)
    all_data = []
    count = 0
    for i in all_row:
        del (i[0])   # 删除id
    for i in all_row:
        del (i[0])  # 删除日期
        count += 1
        # print(count)
        # print(i)
        tmp = []
        for j in i:
            m = re.split('\W+', j)  # 使用正则表达式进行切分
            tmp.append(m)
        all_data.append(tmp)
    return all_data


def transform(address):
    url = 'http://api.map.baidu.com/geocoding/v3/?address={}&ret_coordtype=gcj02ll&output=json&ak={}'.format(address, AK)
    res = requests.get(url)  # 向百度地图API请求服务
    if res.status_code == 200:  # HTTP的返回码，返回200为请求成功
        val = res.json()  # 返回结果的Json对象
        if val["status"] == 0:  # 结果状态返回码，返回0为成功
            retval = {'地址': address, '经度': val['result']['location']['lng'], '纬度': val['result']['location']['lat'],
                      '地区标签': val['result']['level'], '是否精确查找': val['result']['precise']}
        else:
            retval = None
        return retval
    else:
        print('无法获取%s经纬度' % address)


def BatchConvert(addresses):
    """

    :param addresses:
    :return:
    all_adds: 三层嵌套列表 [[[经纬度值],[], ……],[[],[]],……]
    all_locs: 三层嵌套列表 [[[地点位置],[], ……],[[],[]],……]
    """

    number = len(addresses)
    print(number)   # 病例数
    all_adds = []  # 所有病例的行程轨迹的经纬度
    all_locs = []  # 所有病例的行程轨迹的位置地点
    for address in addresses:  # 遍历每一个病例的行程轨迹
        adds = []  # 保存经纬度
        locs = []  # 保存地理位置
        print(address)
        for tmp in address: # 遍历病例每一天的行程轨迹
            # print(tmp)
            num = len(tmp)
            if num > 1:
                for pos in tmp:  # 遍历病例每一天行程轨迹中到过的地点
                    print(pos)
                    add = []
                    loc = []
                    if pos != 'null':
                        result = transform(pos)  # 进行地址转换
                        print(result)
                        loc.append(pos)
                        locs.append(loc)
                        add.append(result['纬度'])
                        add.append(result['经度'])
                        adds.append(add)
            else:
                for pos in tmp:  # 要把列表中的数据读取出来
                    add = []
                    loc = []
                    if pos != 'null':   # 不为null，且该病例当日行程只有一个地点
                        print(pos)
                        result = transform(pos)  # 进行地址转换
                        print(result)
                        loc.append(pos)
                        locs.append(loc)
                        add.append(result['纬度'])
                        add.append(result['经度'])
                        adds.append(add)
        print(adds)
        print(locs)
        all_adds.append(adds)
        all_locs.append(locs)

    return all_adds, all_locs




if __name__ == '__main__':
    path = 'D:\\projects\\Epidemic data visualization\\data_new.xlsx'
    addresses = getDataFromExcel(path)
    values, locations = BatchConvert(addresses)

    map = folium.Map(location=[29.866068124069646, 121.63084278185603, ],
                     tiles='https://rt0.map.gtimg.com/tile?z={z}&x={x}&y={-y}', # 高德街道图',
                     attr='default',
                     zoom_start=12)

    num = 0
    for adds, locs in zip(values, locations):
        # color = random.choice(colors)  # 从中随机选取一种颜色
        marker = markers[num]
        num += 1
        feature_group = FeatureGroup(name=f"病例{num}轨迹")
        for add, loc in zip(adds, locs):
            Marker(location=add, popup=loc[0], icon=DivIcon(
                icon_size=(150, 36),
                icon_anchor=(7, 20),
                html=f'<div style="font-size: 18pt; color : green">{num}</div>',
            )).add_to(feature_group)
            #  Marker(location=add, popup=loc[0], icon=folium.Icon(prefix='fa', icon=marker)).add_to(
            #     feature_group)

        feature_group.add_to(map)
    LayerControl().add_to(map)

map.save('final_v9.html')

