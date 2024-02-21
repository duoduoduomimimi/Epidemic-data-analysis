import pandas as pd
import requests
import numpy as np

AK = "g3BKaOdwqnCI1Knhe0AXSFW0gESg6HE7" #百度AK



def transform(address):
    url = 'http://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak={}'.format(address, AK)
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


def BatchConvert(path):
    addresses = pd.read_csv('{}'.format(path), header=None)  # 读入保存地理位置的txt文件
    number = len(addresses)
    positions = np.array(addresses)
    addresses = positions.tolist()  # 将DataFrame数据类型转换为List数据类型
    longitude = []   # 提取经度
    latitude = []  # 提取纬度
    while number:
        for address in addresses:
            result = transform(address)  # 进行地址转换
            # print(result)
            longitude.append(result['经度'])
            latitude.append(result['纬度'])
            number = number - 1
    print(longitude)
    print(latitude)
    data = {'longitude': longitude, 'latitude': latitude}
    df = pd.DataFrame(data)  # 将Narray数组转换为DataFrame数据类型
    print(df)
    df.to_csv('Longitude and latitude value.csv') # 将转换后的经纬度值保存在csv文件中


if __name__ == '__main__':
    BatchConvert('D:\\projects\\Epidemic data visualization\\geographical position.txt')

