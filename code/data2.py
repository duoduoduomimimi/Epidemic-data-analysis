import requests
import pandas
import json
import re

AK = "g3BKaOdwqnCI1Knhe0AXSFW0gESg6HE7"  # 把复制的AK直接粘贴过来就可以了
# ret_coordtype = 'gcj02ll' 采用火星坐标系

def transform(address):
    url = 'http://api.map.baidu.com/geocoding/v3/?address={}&ret_coordtype=gcj02ll&output=json&ak={}'.format(address, AK)
    res = requests.get(url)
    if res.status_code == 200:
        val = res.json()
        if val["status"] == 0:
            retval = {'地址': address, '经度': val['result']['location']['lng'], '纬度': val['result']['location']['lat'],
                      '地区标签': val['result']['level'], '是否精确查找': val['result']['precise']}
        else:
            retval = None
        return retval
    else:
        print('无法获取%s经纬度' % address)


def BatchConvert():
    number = int(input('请输入要转换的地址总数；'))
    while(number):
        address = input('请输入要转换的地址位置：')
        print(transform(address))
        number = number - 1


if __name__ == '__main__':
    BatchConvert()
