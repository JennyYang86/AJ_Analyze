DEBUG = True
db_connect = {
    "db_file_path": "D:\\JennyYang\\testfiles\\caipan_202302.db",
    "bronze_table_1": "bronze data stage_1",
    "silver_table 1": "silver_fact_caipan",
    "fact_caipan": "gold_fact_caipan",
    "dim_program": "gold_dim_category",
    "fact_profit": "gold_fact_profit",
    "fact_crime": "gold_fact_crime",
    "dim_crime": "gold_dim_crime",
    "silver_dim_crime": "silver_AJ_crime"
}

datasource_setting={
    "file_to_bronze":"D:\\JennyYang\\testfiles\\full.xlsx"
}

data_rules = {
    "panjue_section": {
        "rule1": "判决如下",
        "rule2": "本院认为",
    },
    "profit_section": {
        "front": {
            "rule1":"赃款",
            "rule2":"行贿",
            "rule3":"违法",
            "rule4":"受贿",
            "rule5":"涉案",
            "rule6":"犯罪",
            "rule7":"非法",
            "rule8":"贿赂",
            "rule10":"贪污",
            "rule11":"收受",
            "rule12":"退缴",
            "rule13":"在案",
            "rule14":"公款",
            "rule15":"挪用",
            "rule16":"谋取",
            "rule17": "追缴",
            "rule18": "没收",
            "rule19": "上缴",
            "rule20": "收缴",
            "rule21": "扣押",
            "rule22": "涉案",
            "rule23": "给予",
            "rule24": "国家工作人员",
            "rule25": "退"
        },
        "back": {

        }
    }
}

table_definition = {
    "bronze_data_stage_1": {
        "AJ_ID": "TEXT",
        "Category": "TEXT",
        "Unit_1": "TEXT",
        "Unit_2": "TEXT",
        "Open_Date": "TEXT",
        "Log_Date": "TEXT",
        "AJ_Desc": "TEXT",
        "AJ_Title": "TEXT",
        "AJ_ZM": "TEXT",
        "RDGC":"TEXT",
        "FZSD": "TEXT",
        "MQLY": "TEXT"
    },
    "silver_fact_caipan": {
        "AJ_ID": "TEXT",  # 文书ID
        "Category": "TEXT",  # 审批程序:一审。
        "Unit_1": "TEXT",  # 法院名称
        "Unit_2": "TEXT",  # 公诉机关
        "Open_Date": "TEXT",  # 起诉时间
        "Log_Date": "TEXT",  # 发布时间
        "AJ_ZH_Desc": "TEXT",  # 处理后的案件描述
        "AJ_Title": "TEXT",
        "AJ_ZM": "TEXT",
        "RDGC":"TEXT",
        "FZSD": "TEXT",
        "MQLY": "TEXT"
    },
    "silver_profit_sentences":{
        "AJ ID":"TEXT",
        "Profit_Desc":"TEXT",#利益金额在案件中的描述
        "Profit_Sentence":"TEXT",
        "Profit_Sentence_1":"TEXT",
        "Profit_Sentence_2":"TEXT"

    },
    "gold_fact_caipan": {
        "AJ_ID": "TEXT",
        "Category_ID": "INTEGER",  # 审批程年ID
        "AJ_ZH_Desc": "TEXT",  # 处理后的案件
        "AJ_PJ_PJRX": "TEXT",  # 判决模块截取
        "AJ_PJ_BYRW": "TEXT",  # 判决模块截取工
        "AJ_Title": "TEXT",
        "AJ_ZM": "TEXT",
        "RDGC":"TEXT",
        "FZSD": "TEXT",
        "MQLY": "TEXT"
    },
    "gold_dim_category": {
        "Category_ID": "INTEGER",
        "Category_Desc": "TEXT"
    },
    "gold_fact_profit": {
        "AJ_ID": "TEXT",
        "Profit_Desc": "TEXT",  # 利益金额在案件中的描述
        "Profit_Num": "TEXT",  # 数字显示
        "Source_ID": "INTEGER"
    },
    "gold_fact_crime":  {
        "AJ_ID": "TEXT",
        "Crime_ID": "INTEGER",  # 审批程年ID
    },
    "gold_dim_crime": {
        "Crime_ID": "INTEGER",
        "Crime_Category": "TEXT",
        "Crime_Desc": "TEXT"
    },
    "silver_AJ_crime": {
        "AJ_ID": "TEXT",
        "Crime_Desc": "TEXT"
    }
}

dim_data = {
    "gold_dim_crime": (
        (1, "贪污贿赂罪", "贪污罪"),
        (2, "贪污贿赂罪", "挪用公款罪"),
        (3, "贪污贿赂罪", "受贿罪"),
        (4, "贪污贿赂罪", "单位受贿罪"),
        (5, "贪污贿赂罪", "行贿罪"),
        (6, "贪污贿赂罪", "对单位行贿罪"),
        (7, "贪污贿赂罪", "介绍贿赂罪"),
        (8, "贪污贿赂罪", "单位行贿罪"),
        (9, "贪污贿赂罪", "巨额财产来源不明罪"),
        (10, "贪污贿赂罪", "隐瞒境外存款罪"),
        (11, "贪污贿赂罪", "私分国有资产罪"),
        (12, "贪污贿赂罪", "私分罚没财物罪"),
        (13, "贪污贿赂罪", "利用影响力受贿罪"),
        (14, "渎职罪", "滥用职权罪"),
        (15, "渎职罪", "故意泄露国家秘密罪"),
        (16, "渎职罪", "私放在押人员罪"),
        (17, "渎职罪", "违法发放林木采伐许可证罪"),
        (18, "渎职罪", "办理偷越国（边）境人员出入境证件罪"),
        (19, "渎职罪", "放行偷越国（边）境人员罪"),
        (20, "渎职罪", "阻碍解救被拐卖、绑架妇女、儿童罪"),
        (21, "渎职罪", "帮助犯罪分子逃避处罚罪"),
        (22, "渎职罪", "玩忽职守罪"),
        (23, "渎职罪", "过失泄露国家秘密罪"),
        (24, "渎职罪", "失职致使在押人员脱逃罪"),
        (25, "渎职罪", "国家机关工作人员签订、履行合同失职被骗罪"),
        (26, "渎职罪", "环境监管失职罪"),
        (27, "渎职罪", "传染病防治失职罪"),
        (28, "渎职罪", "商检失职罪"),
        (29, "渎职罪", "动植物检疫失职罪"),
        (30, "渎职罪", "不解救被拐卖、绑架妇女、儿童罪"),
        (31, "渎职罪", "失职造成珍贵文物损毁、流失罪"),
        (32, "渎职罪", "徇私枉法罪"),
        (33, "渎职罪", "民事、行政枉法裁判罪"),
        (34, "渎职罪", "执行裁判玩忽职守、滥用职权罪"),
        (35, "渎职罪", "徇私舞弊减刑、假释、暂予监外执行罪"),
        (36, "渎职罪", "徇私舞弊不移交刑事案件罪"),
        (37, "渎职罪", "滥用管理公司、证券职权罪"),
        (38, "渎职罪", "徇私舞弊不征、少征税款罪"),
        (39, "渎职罪", "徇私舞弊发售发票、抵扣税款、出口退税罪"),
        (40, "渎职罪", "违法提供出口退税凭证罪"),
        (41, "渎职罪", "非法批准征用、占用土地罪"),
        (42, "渎职罪", "非法低价出让国有土地使用权罪"),
        (43, "渎职罪", "放纵走私罪"),
        (44, "渎职罪", "商检徇私舞弊罪"),
        (45, "渎职罪", "动植物检疫徇私舞弊罪"),
        (46, "渎职罪", "放纵制售伪劣商品犯罪行为罪"),
        (47, "渎职罪", "招收公务员、学生徇私舞弊罪"),
        (48, "渎职罪", "帮助逃犯逃避处罚罪"),
        (49, "渎职罪", "枉法裁判罪"),
        (50, "渎职罪", "执行判决、裁定滥用职权罪"),
        (51, "渎职罪", "食品监管渎职罪"),
        (52, "渎职罪", "枉法仲裁罪"),
        (53, "国家机关工作人员利用职权实施的侵犯公民人身权利、民主权利犯罪", "国家机关工作人员利用职权实施的非法拘禁罪"),
        (54, "国家机关工作人员利用职权实施的侵犯公民人身权利、民主权利犯罪", "国家机关工作人员利用职权实施的非法搜查罪"),
        (55, "国家机关工作人员利用职权实施的侵犯公民人身权利、民主权利犯罪", "刑讯逼供罪"),
        (56, "国家机关工作人员利用职权实施的侵犯公民人身权利、民主权利犯罪", "暴力取证罪"),
        (57, "国家机关工作人员利用职权实施的侵犯公民人身权利、民主权利犯罪", "虐待被监管人罪"),
        (58, "国家机关工作人员利用职权实施的侵犯公民人身权利、民主权利犯罪", "报复陷害罪"),
        (59, "国家机关工作人员利用职权实施的侵犯公民人身权利、民主权利犯罪", "国家机关工作人员利用职权实施的破坏选举罪")
    ),
    "gold_dim_category": (
        (1, "一审"),
        (2, "二审"),
        (3, "再审"),
    )
}
