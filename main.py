# -*- coding: utf8 -*-
import re
import json
import requests

root_url = "https://yz.chsi.com.cn/"

sc_data = []

xxfs_全日制 = "1"
xxfs_非全日制 = "2"


def query_sc_data():
    sc_url = root_url + "zsml/pages/getSs.jsp"
    sc_resp = requests.post(sc_url)
    return json.loads(sc_resp.text)


def query_ml_data():
    ml_url = root_url + "zsml/pages/getMl.jsp"
    ml_resp = requests.post(ml_url)
    return json.loads(ml_resp.text)


def query_xk_data(mldm):
    xk_url = root_url + "zsml/pages/getZy.jsp"
    xk_resp = requests.post(xk_url, data={"mldm": mldm})
    return json.loads(xk_resp.text)


def query_zy_data(xkdm):
    zy_url = root_url + "zsml/code/zy.do"
    zy_resp = requests.post(zy_url, data={"q": xkdm})
    return json.loads(zy_resp.text)


def query_school_data(ssdm, dwmc, mldm, yjxkdm, zymc, xxfs):
    school_url = root_url + "zsml/queryAction.do"
    form_data = {
        "ssdm": ssdm,  # 省市代码
        "dwmc": dwmc,  # 单位名称
        "mldm": mldm,  # 门类代码
        "mlmc": "",  # 门类名称 (留空即可)
        "yjxkdm": yjxkdm,  # 学科类别代码
        "zymc": zymc,  # 专业名称
        "xxfs": xxfs,  # 学习方式
    }
    response = requests.post(school_url, data=form_data)
    return response.text


def parse_school_data(html_data):
    table_data = re.findall(r'<table class="ch-table">.*?</table>', html_data, re.S)[0]
    tr_list = re.findall(r"<tr>.*?</tr>", table_data, re.S)
    head_data = tr_list[0]
    head_item_list = re.findall(r"<th.*?>(.*?)</th>", head_data, re.S)
    school_data_list = tr_list[1:]
    parsed_data_list = []
    for schoo_data in school_data_list:
        school_item_list = re.findall(r"<td.*?>(.*?)</td>", schoo_data, re.S)
        school_招生单位_data = school_item_list[0]
        school_所在地_data = school_item_list[1]
        school_研究生院_data = school_item_list[2]
        school_自划线院校_data = school_item_list[3]
        school_博士点_data = school_item_list[4]
        school_招生单位 = re.findall(r"<a.*?>(.*?)</a>", school_招生单位_data, re.S)[0]
        school_所在地 = school_所在地_data
        school_研究生院 = False if school_研究生院_data == "&ensp;" else True
        school_自划线院校 = False if school_自划线院校_data == "&ensp;" else True
        school_博士点 = False if school_博士点_data == "&ensp;" else True
        _school = {
            head_item_list[0]: school_招生单位,
            head_item_list[1]: school_所在地,
            head_item_list[2]: school_研究生院,
            head_item_list[3]: school_自划线院校,
            head_item_list[4]: school_博士点,
        }
        parsed_data_list.append(_school)
    return parsed_data_list


def write_to_file(text_data, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(text_data)


if __name__ == "__main__":
    html_data = query_school_data("14", "", "08", "0812", "", "1")
    print(parse_school_data(html_data))
