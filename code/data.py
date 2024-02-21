import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])  # 日期标号
y = np.array([1, 7, 12, 16, 7, 11, 6, 5, 4, 4, 0, 2])  # 每日确诊病例数
v = ['20221013', '20221014', '20221015', '20221016', '20221017', '20221018',
     '20221019', '20221020', '20221021', '20221022', '20221023', '20221024']
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置为字体SimHei
plt.title('北仑区新冠疫情每日确诊病例数')
plt.plot(x, y)
plt.xlabel('日期')
plt.xticks(x, v, rotation=45)  # v为与x对应的字符刻度，ritation为旋转角度
plt.ylabel('确诊人数（例）')
plt.show()
