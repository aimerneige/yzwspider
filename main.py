# -*- coding: utf8 -*-
import re
import json
import requests

root_url = "https://yz.chsi.com.cn/"

sc_data = []

mldm_工学 = "08"
yjxkdm_计算机科学与技术 = "0812"

xxfs_全日制 = "1"
xxfs_非全日制 = "2"


def query_ss_data():
    ss_url = root_url + "zsml/pages/getSs.jsp"
    ss_resp = requests.post(ss_url)
    return json.loads(ss_resp.text)


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


def query_school_detail(ssdm, dwmc, mldm, yjxkdm, zymc, xxfs):
    query_url = root_url + "zsml/querySchAction.do"
    query_data = {
        "ssdm": ssdm,  # 省市代码
        "dwmc": dwmc,  # 单位名称
        "mldm": mldm,  # 门类代码
        "mlmc": "",  # 门类名称 (留空即可)
        "yjxkdm": yjxkdm,  # 学科类别代码
        "zymc": zymc,  # 专业名称
        "xxfs": xxfs,  # 学习方式
    }
    response = requests.get(query_url, params=query_data)
    return response.text


def parse_school_detail(html_data):
    table_data = re.findall(
        r'<table class="ch-table more-content">.*?</table>', html_data, re.S
    )[0]
    tr_list = re.findall(r"<tr>.*?</tr>", table_data, re.S)
    head_data = tr_list[0]
    head_item_list = re.findall(r"<th.*?>(.*?)</th>", head_data, re.S)
    school_detail_data_list = tr_list[1:]
    parsed_school_detail_list = []
    for school_detail_data in school_detail_data_list:
        school_detail_item_list = re.findall(
            r"<td.*?>(.*?)</td>", school_detail_data, re.S
        )
        sd_考试方式_data = school_detail_item_list[0]
        sd_院系所_data = school_detail_item_list[1]
        sd_专业_data = school_detail_item_list[2]
        sd_研究方向_data = school_detail_item_list[3]
        sd_学习方式_data = school_detail_item_list[4]
        sd_指导教师_data = school_detail_item_list[5]
        sd_拟招生人数_data = school_detail_item_list[6]
        sd_考试范围_data = school_detail_item_list[7]
        sd_备注_data = school_detail_item_list[8]
        sd_考试方式 = sd_考试方式_data
        sd_院系所 = sd_院系所_data
        sd_专业 = sd_专业_data
        sd_研究方向 = sd_研究方向_data
        sd_学习方式 = sd_学习方式_data
        sd_指导教师 = re.findall(r"<span.*?>(.*?)</span>", sd_指导教师_data, re.S)[0]
        sd_拟招生人数 = re.findall(
            r"document.write\(cutString\('(.*?)',6\)\);", sd_拟招生人数_data, re.S
        )[0]
        sd_考试范围 = re.findall(
            r'<a href="(.*?)" target="_blank">查看</a>', sd_考试范围_data, re.S
        )[0][1:]
        sd_备注 = re.findall(
            r"document.write\(cutString\('(.*?)',6\)\);", sd_备注_data, re.S
        )[0]
        _school_detail = {
            head_item_list[0]: sd_考试方式,
            head_item_list[1]: sd_院系所,
            head_item_list[2]: sd_专业,
            head_item_list[3]: sd_研究方向,
            head_item_list[4]: sd_学习方式,
            head_item_list[5]: sd_指导教师,
            head_item_list[6]: sd_拟招生人数,
            head_item_list[7]: sd_考试范围,
            head_item_list[8]: sd_备注,
        }
        parsed_school_detail_list.append(_school_detail)
    return parsed_school_detail_list


def query_test_data(test_url):
    query_url = root_url + test_url
    response = requests.get(query_url)
    return response.text


def parse_test_data(html_data):
    test_table_div_data = re.findall(r'<div class="zsml-result">.*?</div>', html_data, re.S)[0]
    table_data = re.findall(r'<table.*?>.*?</table>', test_table_div_data, re.S)[0]
    tr_list = re.findall(r"<tr>.*?</tr>", table_data, re.S)
    head_data = tr_list[0]
    head_item_list = re.findall(r"<th.*?>(.*?)</th>", head_data, re.S)
    test_data_list = tr_list[1:]
    parsed_data_list = []
    for test_data in test_data_list:
        test_item_list = re.findall(r"<td.*?>(.*?)</td>", test_data, re.S)
        test_政治_data = test_item_list[0]
        test_外语_data = test_item_list[1]
        test_业务课一_data = test_item_list[2]
        test_业务课二_data = test_item_list[3]
        test_政治 = "".join(test_政治_data.split('<')[0].split())
        test_政治_备注 = re.findall(r'<span class="sub-msg">(.*?)</span>', test_政治_data, re.S)[0]
        test_外语 = "".join(test_外语_data.split('<')[0].split())
        test_外语_备注 = re.findall(r'<span class="sub-msg">(.*?)</span>', test_外语_data, re.S)[0]
        test_业务课一 = "".join(test_业务课一_data.split('<')[0].split())
        test_业务课一_备注 = re.findall(r'<span class="sub-msg">(.*?)</span>', test_业务课一_data, re.S)[0]
        test_业务课二 = "".join(test_业务课二_data.split('<')[0].split())
        test_业务课二_备注 = re.findall(r'<span class="sub-msg">(.*?)</span>', test_业务课二_data, re.S)[0]
        _test = {
            head_item_list[0]: {
                "考试科目": test_政治,
                "备注": test_政治_备注,
            },
            head_item_list[1]: {
                "考试科目": test_外语,
                "备注": test_外语_备注,
            },
            head_item_list[2]: {
                "考试科目": test_业务课一,
                "备注": test_业务课一_备注,
            },
            head_item_list[3]: {
                "考试科目": test_业务课二,
                "备注": test_业务课二_备注,
            },
        }
        parsed_data_list.append(_test)
    return parsed_data_list


def write_to_file(text_data, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(text_data)


def get_cs_school_data():
    cs_school_data = {}
    ss_data = query_ss_data()
    for ss in ss_data:
        _省市名称 = ss["mc"]
        _省市代码 = ss["dm"]
        school_data = query_school_data(
            _省市代码, "", mldm_工学, yjxkdm_计算机科学与技术, "", xxfs_全日制
        )
        parsed_school_data = parse_school_data(school_data)
        for i in range(0, len(parsed_school_data)):
            school = parsed_school_data[i]
            school_name = school["招生单位"].split(")")[1]
            school_detail_data = query_school_detail(
                _省市代码, school_name, mldm_工学, yjxkdm_计算机科学与技术, "", xxfs_全日制
            )
            parsed_school_detail = parse_school_detail(school_detail_data)
            print(f'{school_name} parsed')
            parsed_school_data[i]["专业目录"] = parsed_school_detail
        cs_school_data[_省市名称] = parsed_school_data
        print(f"{_省市名称} parsed")
    write_to_file(
        json.dumps(cs_school_data, ensure_ascii=False), "./cs_school_data.json"
    )


if __name__ == "__main__":
    # html_data = query_school_detail("14", "山西大学", "08", "0812", "", "1")
    # parsed_result = parse_school_detail(html_data)
    # write_to_file(json.dumps(parsed_result, ensure_ascii=False), "./school_detail.json")
    # write_to_file(html_data, "./example.html")
    # html_data = query_test_data("zsml/kskm.jsp?id=1010821022081200011")
    # write_to_file(html_data, "./test_example.html")
    get_cs_school_data()
