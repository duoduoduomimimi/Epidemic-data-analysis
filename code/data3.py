import os
import re
import time
import openpyxl
import requests

AK = "1vc6xuWUmdBzEYdnyEeucNqP31k41Ocw"  # 百度AK


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


def BatchConvert(addresses):
    number = len(addresses)
    longitude = []  # 提取经度
    latitude = []  # 提取纬度
    while number:
        for address in addresses:
            for item in address:
                if item != 'null':
                    result = transform(address)  # 进行地址转换
                    time.sleep(3)
            # print(result)
            longitude.append(result['经度'])
            latitude.append(result['纬度'])
            number = number - 1
    print(longitude)
    print(latitude)


def getDataFromExcel(path):
    ex = os.path.join(os.getcwd(), '{}'.format(path))
    wb = openpyxl.load_workbook(path)  # 打开excel文件
    ws = wb['Sheet1']
    # res = ws.cell(row=1, column=1).value  # 获取单元格的内容
    all_value = []
    # print(res)
    for row in ws.values:
        all_value.append(row)
    print(all_value)
    del (all_value[0])
    print(all_value)
    all_row = []
    for i in all_value:
        row = []
        for j in i:
            row.append(j)
        all_row.append(row)  # 将元组列表转换成嵌套列表
    print(all_row)
    all_data = []
    count = 0
    for i in all_row:
        del (i[0])
    for i in all_row:
        del (i[0])
        count += 1
        print(count)
        print(i)
        tmp = []
        for j in i:
            m = re.split('\W+', j)
            tmp.append(m)
        all_data.append(tmp)
    return all_data


if __name__ == '__main__':
    path = 'D:\\projects\\Epidemic data visualization\\data_new.xlsx'
    getDataFromExcel(path)
    # print(len(all_data[0]))
    # print(len(all_data[0][1]))
    # BatchConvert(all_value)
