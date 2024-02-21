import requests

AK = ""  # 百度AK

def transform(address):
    url = ''
    res = requests.get(url)
    if res.status_code == 200:
        val = res.json()
        if val["status"] == 0:
            retval = {'地址': address, '经度': val['result']['location']['lng'], '纬度': val['result']['location']['lat'], '地区标签': val['result']['level'],'是否精确查找': val['result']['precise']}
        else:
            retval = None
        return retval
    else:
        print('无法获取%s经纬度'%address)


if __name__ == '__main__':
    print(transform('故宫博物馆'))