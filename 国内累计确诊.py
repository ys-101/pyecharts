import requests
import re
import json
from pyecharts.charts import Map
from pyecharts import options as opts


# 爬虫程序
class DingXiangSpider:
    def __init__(self):
        self.__url = 'http://ncov.dxy.cn/ncovh5/view/pneumonia?from=singlemessage&isappinstalled=0'
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}

    def get_data(self):
        """从响应内容中提取包含所抓数据的json"""
        html = requests.get(url=self.__url, headers=self.__headers).content.decode('utf-8', 'ignore')
        regex = "window.getAreaStat = (.*?)catch\(e\)"
        pattern = re.compile(regex, re.S)
        str_data_list = pattern.findall(html)
        str_data = str_data_list[0][:-1] if str_data_list else None
        if str_data:
            return self.__get_json_data(str_data)

    def __get_json_data(self, str_data):
        """转为json数据，并提取所需数据"""
        json_data = json.loads(str_data)
        province_list = []
        for one_province_dict in json_data:
            province_name = self.__format_province(one_province_dict['provinceName'])
            one_province_info = [province_name, (one_province_dict['confirmedCount'])]
            province_list.append(one_province_info)
        return province_list


    def __format_province(self, name: str):
        if name.endswith("省") or name.endswith("市"):
            return name[:-1]
        elif name == "内蒙古自治区":
            return "内蒙古"
        elif name.endswith("自治区"):
            return name[:2]
        elif name.endswith("行政区"):
            return name[:2]
        return name

spider = DingXiangSpider()
data = spider.get_data()

print(data)
# data_pie = [list ((k,v)) for (k,v) in province_distribution.items()]

map = Map()
map.set_global_opts(
    title_opts=opts.TitleOpts(title="20211102中国疫情地图"),
    visualmap_opts=opts.VisualMapOpts(max_=3600, is_piecewise=True,
                                      pieces=[
                                          {"max": 99999, "min": 10001, "label": ">10000", "color": "#330033"},
                                          {"max": 10000, "min": 1000, "label": "1000-10000", "color": "#8A0808"},
                                          {"max": 999, "min": 500, "label": "500-999", "color": "#B40404"},
                                          {"max": 499, "min": 100, "label": "100-499", "color": "#DF0101"},
                                          {"max": 99, "min": 10, "label": "10-99", "color": "#F78181"},
                                          {"max": 9, "min": 1, "label": "1-9", "color": "#F5A9A9"},
                                          {"max": 0, "min": 0, "label": "0", "color": "#FFFFFF"},
                                      ],) #最大数据范围，分段
)
map.add("2021-11-2中国疫情地图", data_pair=data, maptype="china", is_roam=True)
map.render('2021-11-2中国疫情地图.html')