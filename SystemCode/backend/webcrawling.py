# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 17:11:35 2020

@author: Lakshmi Subramanian
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import numpy as np
import RAKE

def get(url):
    headers = {}
    resp = requests.get(url, headers=headers)
    if resp.ok:
        return resp.text


# Extract the main content from each web url
def colcontent(url):
    data2 = get(url)
    soup = BeautifulSoup(data2, "html.parser")
    qmaindiv = soup.find("div", {"class": "entry-content"})
    return qmaindiv


def colcontent_mcq(url):
    data2 = get(url)
    soup = BeautifulSoup(data2, "html.parser")
    qmaindiv = soup.find("div", {"class": "row"})
    return qmaindiv


def rakeTextInput(text):
    soup = BeautifulSoup(text, "html.parser")

    textip = soup.get_text(strip=True)
    # Reka setup with stopword directory
    stop_dir = "SmartStoplist.txt"
    rake_object = RAKE.Rake(stop_dir)
    # Extract keywords
    keywords = rake_object.run(textip)
    # print ("keywords: ", keywords)
    ret = [i[0] for i in keywords[:5]]
    return (ret)


def getLinks(query):
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"
    resp = requests.get(URL, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    # print(soup)
    results = []
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                # title = g.find('h3').text
                # item = {
                #     "title": title,
                #     "link": link
                # }
                results.append(link)
        # print(results)
    return (results)


####################################################################################################


# ################# webscrapping from learncbse for descriptive questions ###########################

website = "https://www.learncbse.in/chapter-wise-important-questions-class-10-science/"
data = get(website)

# Access all the relevant urls and store them in a list
soup = BeautifulSoup(data, "html.parser")
alltags = soup.findAll("a")

urls = []
names = []
for a_tag in alltags:
    href = a_tag.get("href")
    if href and href != "" and re.search(r'-chapter-wise-important-questions-class-10-science',
                                         a_tag.get('href')) is not None:
        span_tag = a_tag

        if span_tag:
            clean = span_tag.text.strip(',')
            clean = clean.split(" ", 2)[2]
            print(clean)
            names.append(clean)
            urls.append(href)

tempDF1 = []
for item in urls[0:len(urls)]:
    x = colcontent(item)

    for i in x.findAll('p'):
        if i.strong is not None:
            newQA1 = [str(i), names[urls.index(item)]]
            tempDF1.append(newQA1)

    print(names[urls.index(item)] + " downloaded.")

df1 = pd.DataFrame(tempDF1, columns=["QnA", "topic"])

df1['question_description'] = np.nan
df1['options'] = np.nan
df1['options'] = '-'
df1['solution'] = np.nan
df1['difficulty_level'] = np.nan
df1['marks'] = np.nan
df1['avg_solving_time'] = np.nan
df1['type_of_question'] = np.nan
df1['type_of_question'] = "Descriptive"
df1['keywords'] = np.nan

marksList = [2, 3, 4, 5]
levelList = ['Easy', 'Medium', 'Hard']

df1['QnA1'] = df1.QnA.str.replace("<p>|</p>|<strong>|</strong>|<br/>|<sub>|</sub>", "").copy()
df1['question_description'] = df1['QnA1'].str.split("Answer.", 1).str[0]
df1['solution'] = df1['QnA1'].str.split("Answer.", 1).str[1]

df1 = df1.drop(columns=['QnA1', 'QnA'])

df1['difficulty_level'] = np.random.choice(levelList, size=len(df1))
df1['marks'] = np.random.choice(marksList, size=len(df1))
df1['avg_solving_time'] = df1['marks'].copy()

df1['question_description'].replace('', np.nan, inplace=True)
df1['solution'].replace('', np.nan, inplace=True)
df1['solution'].replace(' ', np.nan, inplace=True)

df1.dropna(subset=['question_description'], inplace=True)
df1.dropna(subset=['solution'], inplace=True)

df1 = df1.drop_duplicates(subset='question_description').copy()

df1 = df1[~df1['question_description'].astype(str).str.startswith('<')].copy()
df1 = df1[~(df1['question_description'] == 'Short ')].copy()
df1 = df1[~df1['solution'].astype(str).str.endswith(':')].copy()

df1["question_description"] = df1["question_description"].str.replace(r"^Question.", r"").str.replace(r"^Question ",
                                                                                                      r"")
df1["question_description"] = df1.question_description.str.lstrip('0123456789- ')
df1["question_description"] = df1.question_description.str.lstrip('.- ')

df1 = df1.reset_index(drop=True)

# ####### question as dict ############################

df1['keywords'] = df1.apply(lambda x: rakeTextInput(x['solution']), axis=1)

# for i in range(len(df1)):
#     df1.question_description[i] = df1.question_description[i].splitlines()

df1 = df1.drop(df1[df1.question_description.str.contains("<img")].index)
df1 = df1.drop(df1[df1.solution.str.contains("<img")].index)

df1 = df1.reset_index(drop=True)

# ########### df1 is dataframe created for descriptive questions


# ################# webscrapping from careerlaunch for mcq questions ###################################

urls = []
names = []
websites = ["https://www.careerlauncher.com/cbse-ncert/class-10/Biology/MCQ.html",
            "https://www.careerlauncher.com/cbse-ncert/class-10/Physics/MCQ.html",
            "https://www.careerlauncher.com/cbse-ncert/class-10/Chemistry/MCQ.html"]
for website in websites:
    data = get(website)

    # Access all the relevant urls and store them in a list
    soup = BeautifulSoup(data, "html.parser")
    alltags = soup.findAll("a")
    for a_tag in alltags:
        href = a_tag.get("href")

        if href and href != "" and re.search(r'MCQ', a_tag.get('href')) is not None:

            span_tag = a_tag
            href = website.rstrip('MCQ.html') + href
            # print(href)
            if span_tag:
                clean = span_tag.text.strip(',').lstrip(' ')
                names.append(clean)
                urls.append(href)

tempDF = []
for item in urls[0:len(urls)]:
    x = colcontent_mcq(item)
    tempDF1 = []
    for i in x.findAll("div", {"class": "row"}):
        tempv = i.get_text()
        if i.strong != None and i.br == None and tempv.find("Answers") == -1:
            newQA1 = [names[urls.index(item)], str(i.get_text(strip=True))]

        elif i.br == None and tempv.find("ANSWERS") == -1:
            newQA1.append(str(i.get_text()))
            tempDF1.append(newQA1)
            # solutions_i = str(i.get_text())

    solutions_i = str(i.get_text())
    solutions_i = ''.join(solutions_i.replace("\n", " ").replace("\xa0", " ").lstrip())
    solutions_i = [i for i in
                   solutions_i.replace(".", "").lstrip("ANSWERS ").lstrip("Answers ").replace(":", "").split(" ") if i][
                  1::2]

    for i in range(len(tempDF1)):
        if len(tempDF1[i]) == 3 and tempDF1[i][1] != 'ANSWERS':
            tempDF1[i][1] = tempDF1[i][1].lstrip('0123456789.-')
            tempDF1[i][2] = tempDF1[i][2].replace("\n", " ").replace("\xa0", " ").lstrip()

            if re.search(".*I.*II.*III.*IV.*", tempDF1[i][2]) is not None:
                ans = []
                temp_ans = tempDF1[i][2].lstrip('I.')
                temp_ans = temp_ans.split(' II.')
                ans.append(temp_ans[0].lstrip(" ").rstrip(" "))
                temp_ans = temp_ans[1].split('III.')
                ans.append(temp_ans[0].lstrip(" ").rstrip(" "))
                temp_ans = temp_ans[1].split('IV.')
                ans.append(temp_ans[0].lstrip(" ").rstrip(" "))
                ans.append(temp_ans[1].lstrip(" ").rstrip(" "))
                tempDF1[i][2] = ans

            elif re.search(".*\(a\).*\(b\).*\(c\).*\(d\).*", tempDF1[i][2]) is not None:
                ans = []
                temp_ans = tempDF1[i][2].lstrip('(a)')
                temp_ans = temp_ans.split('(b)')
                ans.append(temp_ans[0].lstrip(" ").rstrip(" "))
                temp_ans = temp_ans[1].split('(c)')
                ans.append(temp_ans[0].lstrip(" ").rstrip(" "))
                temp_ans = temp_ans[1].split('(d)')
                ans.append(temp_ans[0].lstrip(" ").rstrip(" "))
                ans.append(temp_ans[1].lstrip(" ").rstrip(" "))
                tempDF1[i][2] = ans

            elif re.search(".*a.*b.*c.*d.*", tempDF1[i][2]) is not None:
                ans = []
                temp_ans = tempDF1[i][2].lstrip('a.')
                temp_ans = temp_ans.split('b.')
                ans.append(temp_ans[0].lstrip(" ").rstrip(" "))
                temp_ans = temp_ans[1].split('c.')
                ans.append(temp_ans[0].lstrip(" ").rstrip(" "))
                temp_ans = temp_ans[1].split('d.')
                ans.append(temp_ans[0].lstrip(" ").rstrip(" "))
                ans.append(temp_ans[1].lstrip(" ").rstrip(" "))
                tempDF1[i][2] = ans

    for s in range(len(solutions_i)):
        if solutions_i[s] in ['a', '(a)', 'A', 'I'] and len(tempDF1) > 1:
            tempDF1[s].append('(a) ' + tempDF1[s][2][0])
        elif solutions_i[s] in ['b', '(b)', 'B', 'II'] and len(tempDF1) > 1:
            tempDF1[s].append('(b) ' + tempDF1[s][2][1])
        elif solutions_i[s] in ['c', '(c)', 'C', 'III'] and len(tempDF1) > 1:
            tempDF1[s].append('(c) ' + tempDF1[s][2][2])
        elif solutions_i[s] in ['d', '(d)', 'D', 'IV'] and len(tempDF1) > 1:
            tempDF1[s].append('(d) ' + tempDF1[s][2][3])
    tempDF1 = pd.DataFrame(tempDF1)

    if type(tempDF) == list:
        tempDF = tempDF1
    else:
        tempDF = tempDF.append(tempDF1)

    print(names[urls.index(item)] + " downloaded.")

df2 = tempDF.copy()
df2.columns = ['topic', 'question_description', 'options', 'solution', 'junk']

df2 = df2.reset_index(drop=True)
df2 = df2.drop(columns=['junk'])

df2.dropna(subset=['solution'], inplace=True)
df2.drop(df2[df2['options'].map(type) != list].index, inplace=True)

df2['difficulty_level'] = np.nan
df2['marks'] = np.nan
df2['avg_solving_time'] = np.nan
df2['type_of_question'] = np.nan
df2['type_of_question'] = "mcq"
df2['keywords'] = np.nan

marksList = [1, 2, 3]

df2['difficulty_level'] = np.random.choice(levelList, size=len(df2))
df2['marks'] = np.random.choice(marksList, size=len(df2))
df2['avg_solving_time'] = df2['marks'].copy()

df2 = df2.reset_index(drop=True)

df2['keywords'] = df2.apply(lambda x: rakeTextInput(x['question_description']), axis=1)
# ############# df2 is dataframe for mcq type of questions

# ################################ appending 2 dataframes to load into mongoDB ########################
df = df1.copy()
df = df.append(df2)

df.topic = df.topic.str.rstrip().str.lstrip().str.replace("-", " ").str.replace(",", " ").str.replace("  ", " ")
# #####################################################################################################


# ####################### topic table ##############################

topic_table = df.topic.unique().tolist()

# ############################ links for each topic collected #########################################

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent": USER_AGENT}

topic_list = df.topic.unique()

link_list = []
for i in range(len(topic_list)):
    query = "Class 10 " + topic_list[i] + " notes"
    links = getLinks(query)
    link_list.append([topic_list[i], links])

link_list = pd.DataFrame(link_list, columns=["topic", "links"])
df = pd.merge(df, link_list, how="left", on='topic')

###################################################################################################

# ############################# MongoDB loading ############################

from pymongo import MongoClient

myclient = MongoClient("mongodb+srv://lakshmi:lakshmi@cluster0.kkm2g.mongodb.net/test")
mydb = myclient["adaptive_test"]
mycol = mydb["question_bank"]
topic_collection = mydb["topics"]

# ########################## Truncate and load ############################################
# x = mycol.delete_many({})
# print(x.deleted_count, " documents deleted.")

data_list = df.to_dict("records")  # Convert to dictionary

for data_dict in data_list:
    if data_dict['type_of_question'] != 'mcq':
        data_dict['options'] = []
    topic_object = topic_collection.find_one({'topic_name': data_dict['topic']})
    if not topic_object:
        topic_id = topic_collection.insert({'topic_name': data_dict['topic']})
    mycol.insert_one({'question_description': data_dict['question_description'], 'difficulty_level':
                  data_dict['difficulty_level'], 'type_of_question': data_dict['type_of_question'],
                  'options': data_dict['options'], 'topic_id': topic_object['_id'], 'marks': str(data_dict['marks']),
                  'avg_solving_time': str(data_dict['avg_solving_time']), 'solution': data_dict['solution'],
                  'keywords': data_dict['keywords']})