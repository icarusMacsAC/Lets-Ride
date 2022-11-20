from sklearn.feature_extraction.text import TfidfVectorizer
import json
import re
import numpy as np
import pandas as pd
import pickle

from nltk.corpus import stopwords
import nltk
from gensim.parsing.preprocessing import remove_stopwords
from main import models
nltk.download('stopwords')

df = pd.read_csv("media/archive/news_csv.csv")

with open('media/archive/tf_idf_vecoubulary_index_value.pickle', 'rb') as handle:
    tf_idf_vecoubulary_index_value = pickle.load(handle)

with open('media/archive/tf_idf_vecoubulary_value_index.pickle', 'rb') as handle:
    tf_idf_vecoubulary_value_index = pickle.load(handle)

with open('media/archive/word_file_no_prob.pickle', 'rb') as handle:
    word_file_no_prob = pickle.load(handle)


def filter_article_topic(s1):
    if type(s1) is float:
        s1 = ""
    s1 = re.subn('[^a-z ]', '', s1.lower())[0]
    s1 = remove_stopwords(s1)
    return s1


def find_article(topic, genre="all"):
    req_data = df
    if genre != "all":
        req_data = df[df.category == genre]
    req_file_list = req_data.index
    print(req_file_list)
    topic = filter_article_topic(topic)
    print(topic)
    vectorizer2 = TfidfVectorizer(ngram_range=(1, 2))
    ss = vectorizer2.fit_transform([topic])
    token = vectorizer2.get_feature_names()
    dict1_data = pd.DataFrame(columns=["key", "file_no", "prob"])
    dict2_data = pd.DataFrame(columns=["key", "file_no", "prob"])
    i = 0
    for ele in token:
        a = tf_idf_vecoubulary_value_index.get(ele)
        if a is None:
            continue
        print(ele, a)
        data = word_file_no_prob[a]
        for file in data:
            file_no = file[0]
            if file_no not in req_file_list:
                print("jhjj", file_no)
                continue
            prob = file[1]
            x = pd.DataFrame([[ele, file_no, prob]], columns=[
                             "key", "file_no", "prob"], index=[i])
            i += 1
            dict1_data = dict1_data.append(x)
    i = 0
    n = dict1_data.file_no.unique()
    for j in n:
        v = dict1_data[dict1_data.file_no == j]
        ele = list(v.key)
        prob = sum(v.prob)
        x = pd.DataFrame([[ele, j, prob]], columns=[
                         "key", "file_no", "prob"], index=[i])
        i += 1
        dict2_data = dict2_data.append(x)
    dict2_data.sort_values(by=["prob"], ascending=False)
    return dict2_data


def req_res(text, format):
    dict2_data = find_article(text, genre=format)
    dict2_data.sort_values(by=["prob"], ascending=False)
    files = dict2_data.file_no
    req_df = pd.DataFrame(columns=["category", "headline", "authors", "link",
                          "short_description", "title", "very_short_description", "token"])
    for i, ele in enumerate(files):
        x = df[df.index == ele]
        req_df = req_df.append(x)
    dat = []
    for ele in req_df.values:
        if type(ele[4]) is float:
            continue
        dat.append([ele[0], ele[1], ele[2], ele[3], ele[4]])
    return dat


global asset_transportation_request_df, asset_transportation_request_lst

asset_transportation_request_df = pd.DataFrame(columns=["ACCEPTED PERSON DETAILS", "FROM", "TO", "DATE AND TIME",
                                                        "NO OF PEOPLE", "ACCESS TYPE", "ACCESS SENSITIVITY", "WHOM TO DELIVER", "STATUS"])

asset_transportation_request_lst = []

share_travel_info_df = pd.DataFrame(columns=["FROM", "TO", "DATE AND TIME",
                                             "MEDIUM", "NO OF PEOPLE"])

share_travel_info_lst = []


def create_share_travel_info(username):
    print("hiiiiiiiiii\n\n\n\n")
    global share_travel_info_df, share_travel_info_lst
    share_travel_info_df = pd.DataFrame(columns=["FROM", "TO", "DATE AND TIME",
                                                 "MEDIUM", "NO OF PEOPLE"])
    share_travel_info_lst = []
    data = models.share_travel_information_model.objects.all()

    for i in range(len(data)):
        temp = data[i].__dict__
        x = {
            "FROM": temp["src"],
            "TO": temp["to"],
            "DATE AND TIME": temp["date_time"],
            "MEDIUM": temp["medium"],
            "NO OF PEOPLE": temp["no_of_assets"],
        }
        share_travel_info_df = share_travel_info_df.append(
            pd.DataFrame(x, index=[i]))
    for ele in share_travel_info_df.values:
        share_travel_info_lst.append(
            [ele[0], ele[1], ele[2], ele[3], ele[4]])
    print("create___", share_travel_info_df)
    print("create___", share_travel_info_lst)
    return share_travel_info_lst


def create_asset_transportation_request(username):
    print("hiiiiiiiiii\n\n\n\n")
    global asset_transportation_request_df, asset_transportation_request_lst
    asset_transportation_request_df = pd.DataFrame(columns=["ACCEPTED PERSON DETAILS", "FROM", "TO", "DATE AND TIME",
                                                            "NO OF PEOPLE", "ACCESS TYPE", "ACCESS SENSITIVITY", "WHOM TO DELIVER", "STATUS"])

    asset_transportation_request_lst = []
    if username != "last":
        data = models.asset_transport_request_model.objects.filter(
            username=username)
    else:
        create_share_travel_info(username)
        data = models.asset_transport_request_model.objects.all()
    for i in range(len(data)):
        temp = data[i].__dict__
        x = {
            "ACCEPTED PERSON DETAILS": temp["whom_to_deliver"],
            "FROM": temp["src"],
            "TO": temp["to"],
            "DATE AND TIME": temp["date_time"],
            "NO OF PEOPLE": temp["no_of_assets"],
            "ACCESS TYPE": temp["asset_type"],
            "ACCESS SENSITIVITY": temp["asset_sensitivity"],
            "WHOM TO DELIVER": temp["whom_to_deliver"],
            "STATUS": int(temp["status"])
        }
        asset_transportation_request_df = asset_transportation_request_df.append(
            pd.DataFrame(x, index=[i]))
    for ele in asset_transportation_request_df.values:
        asset_transportation_request_lst.append(
            [ele[0], ele[1], ele[2], ele[3], ele[4], ele[5], ele[6], ele[7], ele[8]])
    print("create___", asset_transportation_request_df)
    print("create___", asset_transportation_request_lst)
    return asset_transportation_request_lst


def append_asset_transportation_request(last_data):
    global asset_transportation_request_df, asset_transportation_request_lst
    x = {
        "ACCEPTED PERSON DETAILS": last_data["whom_to_deliver"],
        "FROM": last_data["src"],
        "TO": last_data["to"],
        "DATE AND TIME": last_data["date_time"],
        "NO OF PEOPLE": last_data["no_of_assets"],
        "ACCESS TYPE": last_data["asset_type"],
        "ACCESS SENSITIVITY": last_data["asset_sensitivity"],
        "WHOM TO DELIVER": last_data["whom_to_deliver"],
        "STATUS": int(last_data["status"])
    }
    asset_transportation_request_df = asset_transportation_request_df.append(
        pd.DataFrame(x, index=[asset_transportation_request_df.shape[0]]))
    asset_transportation_request_lst.append(
        list(asset_transportation_request_df[-1:].values[0]))
    print("append___", asset_transportation_request_df)
    print("append___", asset_transportation_request_lst)


def append_share_travel_info(last_data):
    global share_travel_info_df, share_travel_info_lst
    x = {
        "FROM": last_data["src"],
        "TO": last_data["to"],
        "DATE AND TIME": last_data["date_time"],
        "MEDIUM": last_data["medium"],
        "NO OF PEOPLE": last_data["no_of_assets"],
    }
    share_travel_info_df = share_travel_info_df.append(
        pd.DataFrame(x, index=[share_travel_info_df.shape[0]]))
    share_travel_info_lst.append(
        list(share_travel_info_df[-1:].values[0]))
    print("append___", share_travel_info_df)
    print("append___", share_travel_info_lst)


def update_asset_transportation_request(data):
    data = data.split("?")
    print("kkkkkk", data)
    global asset_transportation_request_df, asset_transportation_request_lst
    a = asset_transportation_request_df[asset_transportation_request_df["ACCEPTED PERSON DETAILS"] == data[0]]
    a = a[a["FROM"] == data[1]]
    a = a[a["TO"] == data[2]]
    a = a[a["NO OF PEOPLE"] == data[4]]
    a = a[a["ACCESS TYPE"] == data[5]]
    a = a[a["ACCESS SENSITIVITY"] == data[6]]
    ind = list(a.index)[0]
    val = asset_transportation_request_df.loc[ind, :].STATUS
    print("kkkkkkkkkkkkkkkkkkkkkkkkkkk", a,
          "llllllllllllllllllllllllllll", ind, val)
    if val == 0:
        print("hi")
        asset_transportation_request_df.loc[ind, "STATUS"] = 1
        asset_transportation_request_lst[ind][-1] = 1
        models.asset_transport_request_model.objects.filter(
            id=ind+1).update(status=1)
    else:
        print("Bye")
        asset_transportation_request_df.loc[ind, "STATUS"] = 0
        asset_transportation_request_lst[ind][-1] = 0
        models.asset_transport_request_model.objects.filter(
            id=ind+1).update(status=0)
    print("kkkkkkkkkkkkkkkkkkkkkkkkkkk",
          asset_transportation_request_df.loc[ind, :])
    print("update___", asset_transportation_request_df)
    print("\nupdate___", asset_transportation_request_lst)


def matched_asset_transportation_request(data):
    global asset_transportation_request_df, asset_transportation_request_lst
    data1 = {}
    required_field = []
    whole_data = models.asset_transport_request_model.objects.all()
    req_data = models.asset_transport_request_model.objects.all()
    for key, val in data.items():
        if key == "csrfmiddlewaretoken":
            continue
        print("lll", key, val)
        if type(val) is str:
            data1[key] = val.strip()
        else:
            data1[key] = val[0].strip()
        if data1[key] == "" or key == "date_time":
            continue
        else:
            required_field.append(key)
            if key == "src":
                req_data = req_data.filter(src=val)
            elif key == "to":
                req_data = req_data.filter(to=val)
            elif key == "username":
                req_data = req_data.filter(username=val)
                whole_data = whole_data.filter(username=val)
            # elif key == "no_of_assets":
            #     req_data = req_data.filter(no_of_assets=val)
            elif key == "status":
                req_data = req_data.filter(status=val)
            elif key == "asset_type":
                req_data = req_data.filter(asset_type=val)
            elif key == "asset_sensitivity":
                req_data = req_data.filter(asset_sensitivity=val)
        print("kjsbkjsbkbskbskjbjsbjsjbsjkbkjsbjksbkjbsjbjjjs", req_data)
    print("ahahahahahahhahhahhahhahha", req_data)
    if len(req_data) == 0:
        return "no record"
    if data1["date_time"] == "default text" or len(req_data) == 1:
        ans = []
        for n in req_data:
            ans.append(n.__dict__)
        ans2 = []
        for ele in whole_data:
            ans2.append(ele.__dict__)
        print("xccccccccccccccccccccccccccccccccccccc\n\n", ans, "\n\n", ans2)
        c = []
        for ele in ans:
            c.append(ele["id"])

        for ele in ans2:
            id_ = ele["id"]
            if id_ in c:
                ele["flag"] = True
            else:
                ele["flag"] = False
        print("xccccccccccccccccccccccccccccccccccccc\n\n", ans, "\n\n", ans2)
        result = []
        for ele in ans2:
            # person, from, to, date, people, type, sens, whom, status
            result.append([ele["whom_to_deliver"], ele["src"], ele["to"], ele["date_time"], ele["no_of_assets"],
                           ele["asset_type"], ele["asset_sensitivity"], ele["whom_to_deliver"],  ele["status"], ele["flag"]])
        print("hshshshhs", result)
        return result
    print("hhhhhh", data1["date_time"])
    x = data1["date_time"].split("T")[0]
    ans = []
    for ele in req_data:
        print("jajajajajajjajajja", str(
            ele.__dict__["date_time"]).split(" ")[0], x)
        if str(ele.__dict__["date_time"]).split(" ")[0] == x:
            ans.append(ele.__dict__)
    print("smbmsbmbssjbjsbmnsbsmnbsnbs", ans)
    ans2 = []
    for ele in whole_data:
        ans2.append(ele.__dict__)
    print("xccccccccccccccccccccccccccccccccccccc\n\n", ans, "\n\n", ans2)
    c = []
    for ele in ans:
        c.append(ele["id"])

    for ele in ans2:
        id_ = ele["id"]
        if id_ in c:
            ele["flag"] = True
        else:
            ele["flag"] = False
    print("xccccccccccccccccccccccccccccccccccccc\n\n", ans, "\n\n", ans2)

    result = []
    for ele in ans2:
        # person, from, to, date, people, type, sens, whom, status
        result.append([ele["whom_to_deliver"], ele["src"], ele["to"], ele["date_time"], ele["no_of_assets"],
                      ele["asset_type"], ele["asset_sensitivity"], ele["whom_to_deliver"],  ele["status"], ele["flag"]])
    print("hshshshhs", result)
    return result
