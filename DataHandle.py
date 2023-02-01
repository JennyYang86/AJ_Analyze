import pandas as pd
import datetime
import re
import jionlp as jio
import config
import json

class DataHandle:

    def clean_bronze_data(self, df_query):
        for i in range(len(df_query)):
            #处理0pen Date
            str_time = str(df_query.loc[i, 'Open_Date'])
            if len(str_time)< 6:
                df_query.loc[i, 'Open_Date'] = ''
            else:
                obj = re.match(r'\\d{4}年\\{1,2}月\{1,2}日', str_time)
                if obj:
                    if self.validate_2(obj.group()):
                        datetime_p = datetime . datetime.strptime (obj.group(), '%Y年%m月%d日') .strftime('%Y-%m-%d')
                        df_query.loc[i, 'Open_Date'] = datetime_p
                    else:
                        df_query.loc[i, 'Open_Date'] = ''
                else:
                        df_query.loc[i, 'Open_Date'] =''

            #处理Open Date
            str_time = str(df_query .loc[i, 'Log_Date'])
            if len(str_time) < 6:
                df_query.loc[i, 'Log_Date'] = ''
            else:
                obj = re.match(r'\\{4}-\{1,2}-\{1,2}', str_time)
                if obj:
                    if self.validate_2(obj.group()):
                        datetime_p = datetime.datetime.strptime(obj.group(), '%Y-%m-%d')
                        df_query.loc[i, 'Log_Date'] = datetime_p
                    else:
                        df_query.loc[i, 'Log_Date'] = ''
                else:
                    df_query.loc[i, 'Log_Date'] = ''
            #处理正文
            text = str(df_query.loc[i, 'AJ_Desc'])
            if (len(text)) > 6:
                df_query.loc[i, 'AJ_Desc'] = jio.clean_text(text)
            else:
                df_query.loc[i,'AJ_Desc']='数据清洗错误'
        # print(df_query.head(5))
        df_query = df_query.drop_duplicates(['AJ_ID'])
        return df_query

    def clean_silver_data(self, df_query):

        strPattern= r'判决如下'
        strPattern2 =r'本院认为(.*?)'
        for i in range(len(df_query)):
            text = str(df_query.loc[i, 'AJ_ZH_Desc'])
            mydict = {}
            f = re.finditer(strPattern2, text)
            b = []
            if f:
                for j in f:
                    inta = j.span()
                    b.append(inta[0])
            else:
                mydict["case0"] = '找不到本院认为的描述'
                df_query.loc[i, 'AJ_PJ_BYRW'] = str(json.dumps(mydict, ensure_ascii=False))

            ret = re.search(strPattern, text)
            if ret:
                a = ret.span()
                df_query.loc[i, 'AJ_PJ_PJRX'] = text[a[0]:]
                if len(b) > 0:
                    for k in range(len(b)):
                        key = "case" + str(k)
                        if k + 1< len(b):
                            mydict[key] = text[b[k]:b[k + 1]]
                        else:
                            mydict[key] = text[b[k]:a[0]]
                    df_query.loc[i, 'AJ_PJ_BYRW'] = str(json.dumps(mydict, ensure_ascii=False))
            else:
                df_query.loc[i, 'AJ_PJ_PJRX'] = '找不到判决如下的描述'
                if len(b) > 0:
                    for k in range(len(b)) :
                        key = "case" + str(k)
                        if k+ 1< len(b):
                            mydict[key] = text[b[k]:b[k + 1]]
                        else:
                            mydict[key] = text[b[k]:]
                    df_query.loc[i, 'AJ_PJ_BYRW'] = str(json.dumps (mydict, ensure_ascii=False))
        return df_query

    def extract_profit_data(self, df_query):
        AJ_ID = []
        Profit_Desc = []
        Profit_Num = []
        strDataRule = []
        for key, value in config.data_rules["profit_section"]["front"].items():
            strDataRule.append(value)
        strDataRule = '|'.join(strDataRule)

        strDataRule2 = []
        for key, value in config.data_rules["profit_section"]["back"].items():
            strDataRule2.append(value)
        strDataRule2 = '|'.join(strDataRule2)
        for i in range(len(df_query)):
            strProfit = str(df_query.loc[i, 'AJ_PJ_PJRX'])
            results = jio.ner.extract_money(strProfit, with_parsing=True)
            intAJLen = len(AJ_ID)
            for item in results:
                intstrPos = item['offset'][0]
                intPos3 = 8
                intPos1 = strProfit.rfind('，', 0, intstrPos)
                intPos2 = strProfit.rfind('。', 0, intstrPos)
                if (intPos1>intPos2):
                    intPos3 = intPos1
                else:
                    intPos3 = intPos2
                strSentence = strProfit[intPos3:item['offset'][1]]
                # strPattern=r'(.*?)(赃款丨行贿丨违法所得)%s(.*?)'%(item[ 'text'])
                strPattern = rf"%s[\u4E00-\u9FA5]*%s" %(strDataRule, str(item['text']))
                # matchObj = re.finditer(strPattern,strSentence)
                for matchobj in re.finditer(strPattern, strSentence):
                    if (matchobj):
                        AJ_ID.append(df_query.loc[i, 'AJ_ID'])
                        Profit_Desc.append(str(item['text']))
                        strNum = item['detail']['num']
                        if (is_number(str(strNum))):
                            Profit_Num.append(strNum)
                        else:
                            # print(df query. loc[i,‘A)_ID'])
                            # print(strNum)
                            # print(strlNum[0])
                            Profit_Num.append(strNum[0])
                    # else:
                    #     intstrPos2 = item['offset'][1]
                    #     intPos32 = 0
                    #     intPos12 = strProfit.find('，', intstrPos)
                    #     intPos22 = strProfit.find('。', intstrPos)
                    #     if (intPos12 < intPos22):
                    #         intPos32 = intPos12
                    #     else:
                    #         intPos32 = intPos22
                    #     strSentence2 = strProfit[item['offset'][1]:intPos32]
                    #     # strPattern=r'(.*?)(赃款丨行贿丨违法所得)%s(.*?)'%(item[ 'text'])
                    #     strPattern2 = rf"%s[\u4E00-\u9FA5]*%s" % (str(item['text']),strDataRule2)
                    #     # matchObj = re.finditer(strPattern,strSentence)
                    #     for matchobj2 in re.finditer(strPattern2, strSentence2):
                    #         if (matchobj2):
                    #             AJ_ID.append(df_query.loc[i, 'AJ_ID'])
                    #             Profit_Desc.append(str(item['text']))
                    #             strNum = item['detail']['num']
                    #             if (is_number(str(strNum))):
                    #                 Profit_Num.append(strNum)
                    #             else:
                    #                 Profit_Num.append(strNum[0])
            # if(intAJLen == len(AJ_ID)):
            #     strProfit = str(df_query.loc[i, 'AJ_PJ_BYRW'])
            #     results = jio.ner.extract_money(strProfit, with_parsing=True)
            #     for item in results:
            #         intstrPos = item['offset'][0]
            #         intPos3 = 8
            #         intPos1 = strProfit.rfind('，', 0, intstrPos)
            #         intPos2 = strProfit.rfind('。', 0, intstrPos)
            #         if (intPos1 > intPos2):
            #             intPos3 = intPos1
            #         else:
            #             intPos3 = intPos2
            #         strSentence = strProfit[intPos3:item['offset'][1]]
            #         # strPattern=r'(.*?)(赃款丨行贿丨违法所得)%s(.*?)'%(item[ 'text'])
            #         strPattern = rf"%s[\u4E00-\u9FA5]*%s" % (strDataRule, str(item['text']))
            #         matchObj = re.finditer(strPattern, strSentence)
            #         if (matchObj):
            #             AJ_ID.append(df_query.loc[i, 'AJ_ID'])
            #             Profit_Desc.append(str(item['text']))
            #             strNum = item['detail']['num']
            #             if (is_number(str(strNum))):
            #                 Profit_Num.append(strNum)
            #             else:
            #                 # print(df query. loc[i,‘A)_ID'])
            #                 # print(strNum)
            #                 # print(strlNum[0])
            #                 Profit_Num.append(strNum[0])
        list = {"AJ_ID": AJ_ID, "Profit_Desc": Profit_Desc,"Profit_Num":Profit_Num}
        df_result = pd.DataFrame(list)

        return df_result

    def extract_crime_data(self, df_query, dict_crime):
        AJ_ID = []
        Category_ID = []
        strList = []
        for key, value in dict_crime.items():
            strList.append(key)
        strPattern = rf"({'|'.join(strList)})"
        for i in range(len(df_query)):
            text = str(df_query.loc[i, 'AJ_PJ_PJRX'])
            f = re.finditer(strPattern, text)
            if f:
                for j in f:
                    AJ_ID.append(df_query.loc[i, 'AJ_ID'])
                    Category_ID.append(dict_crime[j.group()])
        list = {"AJ_ID": AJ_ID, "Category _ID": Category_ID}
        df_result = pd.DataFrame(list)
        df_result = df_result.drop_duplicates()
        return df_result

    def extract_crime_dimension(self, df_query):
        AJ_ID = []
        Crime_Desc = []
        strPatern = r"犯[\u4E00-\u9FA5]+罪"
        for i in range(len(df_query)):
            text = str(df_query.loc[i, 'AJ_PJ_PJRX'])
            f = re.finditer(strPatern, text)
            if f:
                for j in f:
                    AJ_ID.append(df_query.loc[i, 'AJ_ID'])
                    Crime_Desc.append(j.group())
            else:
                AJ_ID.append(df_query.loc[i, 'AJ_ID'])
                Crime_Desc.append("找不到罪名描述")
        list = {"AJ _ID": AJ_ID, "Crime_Desc": Crime_Desc}
        df_result = pd.DataFrame(list)
        return df_result

    def extract_profit_data_for_word(self, df_query):
        AJ_ID = []
        Profit_Desc = []
        Profit_Semtemce = []
        Profit_Semtemce_1 = []
        Profit_Semtemce_2 = []

        for i in range(len(df_query)):
            strProfit = str(df_query.loc[i, 'AJ_PJ_PJRX'])
            results = jio.ner.extract_money(strProfit, with_parsing=True)
            for item in results:
                intstrPos = item['offset'][0]
                intPos3 = 8
                intPos1 = strProfit.rfind('，', 0, intstrPos)
                intPos2 = strProfit.rfind('。', 0, intstrPos)
                if (intPos1 > intPos2):
                    intPos3 = intPos1
                else:
                    intPos3 = intPos2
                # strSentence = strProfit[intPos3:item['offset'][1]]

                intstrPos2 = item['offset'][1]
                intPos32 = 0
                intPos12 = strProfit.find('，', intstrPos)
                intPos22 = strProfit.find('。', intstrPos)
                if (intPos12 < intPos22):
                    intPos32 = intPos12
                else:
                    intPos32 = intPos22
                strSentence = strProfit[intPos2+1:intPos22+1]

                AJ_ID.append(df_query.loc[i, 'AJ_ID'])
                Profit_Desc.append(str(item['text']))
                Profit_Semtemce.append(strSentence)
                strSentence = strProfit[intPos3 + 1:item['offset'][1]]
                Profit_Semtemce_1.append(strSentence)
                strSentence = strProfit[item['offset'][0]:intPos32 + 1]
                Profit_Semtemce_2.append(strSentence)
        list = {"AJ_ID": AJ_ID, "Profit_Desc": Profit_Desc, "Profit_Sentence": Profit_Semtemce,"Profit_Sentence_1": Profit_Semtemce_1,"Profit_Sentence_2": Profit_Semtemce_2}
        df_result = pd.DataFrame(list)

        return df_result

    def validate_2(date_text):
        try:
            if date_text != datetime.datetime.strptime(date_text,"%Y年%m月%d日").strftime('%Y年%m月%d日') \
                    .replace('月0','月').replace('年0','年'):
                raise ValueError
            return True
        except ValueError:
                # raise ValueError('
            return False

    def validate_3(date_text):
        try:
            if date_text != datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            return True

        except ValueError:
            # raise ValueError('
             return False


def is_number(str_Number):
    try:
        float(str_Number)
        return True
    except ValueError:
        pass
    return False
