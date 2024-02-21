import folium
from folium import DivIcon

m = folium.Map(
        location=[29.875832, 121.560474],
        zoom_start=15,
        tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}', # 高德街道图
        # tiles='http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', # 高德卫星图
        # tiles='https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', # google 卫星图
        # tiles='https://mt.google.com/vt/lyrs=h&x={x}&y={y}&z={z}', # google 地图
        attr='default'
    )
num = 7
folium.Marker(location=[29.878105319486554, 121.92272110636715], popup='test', icon=folium.Icon(prefix='fa', icon="tag")).add_to(m)
folium.Marker(location=[29.874836657731702, 121.92229441125005],popup='test',icon=DivIcon(
        icon_size=(150,36),
        icon_anchor=(7,20),
        html=f'<div style="font-size: 18pt; color : black">{num}</div>',
        )).add_to(m)
m.save('two.html')