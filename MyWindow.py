from tkinter import *
from DbOpt import *
from GlobalLoger import ta_log
import config
import pandas as pd
from DataHandle import *
import tkinter.ttk as ttk


class MyWindow(Frame ):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        # widget can take all window
        self.pack(fill=BOTH, expand=1)

        # create button, link it to clickExitButton()
        exitButton = Button(self, text="Exit", command=self.clickExitButton)
        createButton = Button(self, text="Create table", command=self.clickCreateButton)
        loadButton = Button(self, text="load excel", command=self.load_bronze_data)
        cleanButton = Button(self, text="clean to silver", command=self.load_silver_data)
        stage1Button = Button(self, text="stage 1", command=self.clickStage1Button)
        otherButton = Button(self, text="other", command=self.clickotherButton)
        extractProfitButoon = Button(self, text="extra Profit", command=self.clickextractProfitButton)
        extractCrimeButoon = Button(self, text="extra Crime", command=self.clickextractCrimeButton)
        extractCrimeDimensionButoon = Button(self, text="extra Crime_dimension", command=self.clickextractCrimeDimensionButton)

        # place button at (e,0)
        exitButton.place(x=0, y=0)
        createButton.place(x=0, y=30)
        loadButton.place(x=0, y=60)
        cleanButton.place(x=0, y=90)
        stage1Button.place(x=0, y=120)
        otherButton.place(x=0, y=150)
        extractProfitButoon.place(x=100, y=0)
        extractCrimeButoon.place(x=100, y=30)
        extractCrimeDimensionButoon.place(x=100, y=60)

        # tab_main = ttk.Notebook()
        # tab_main.place(relx=0.02, rely=0.02, relwidth=0.887, relheight=0.876)
        #
        # tab1 = Frame(tab_main)
        # tab1.place(x=0, y=30)
        # tab_main.add(tab1, text="first")
        #
        # tab2 = Frame(tab_main)
        # tab2.place(x=100, y=30)
        # tab_main.add(tab2, text="second")

    def clickExitButton(self):
        exit()

    def clickCreateButton(self):
        db = DbOpt()
        table_name = "gold_dim_crime"
        db.create_table(table_name)
        ta_log.info(table_name + "is created.")
        table_data = config.dim_data.get(table_name)
        db.insert_table_data(table_name, table_data)
        ta_log.info(table_name + ": data is inserted.")

        table_name ="gold_dim_category"
        db.create_table(table_name)
        ta_log.info(table_name + " is reated." )
        table_data = config.dim_data.get(table_name)
        db.insert_table_data(table_name, table_data)
        ta_log.info(table_name + ": data is inserted.")

        table_name="bronze_data_stage_1"
        db.create_table(table_name)
        ta_log.info(table_name + " is created.")

        table_name = "silver_fact_caipan"
        db.create_table(table_name)
        ta_log.info(table_name + "is created.")
        table_name = "gold_fact_profit"
        db.create_table(table_name)
        ta_log.info(table_name + " is created.")
        table_name = "gold_fact_crime"
        db.create_table(table_name)
        ta_log.info(table_name + "is created.")
        table_name = "gold_fact_caipan"
        db.create_table(table_name )
        ta_log.info(table_name + "is created.")

    def load_bronze_data(self):
        db = DbOpt()
        filename = config.datasource_setting["file_to_bronze"]
        data = pd.read_excel(filename, sheet_name=0, header=None, skiprows=1, engine="openpyxl")
        df = data[ [5,8,9,10, 24,25,42,6,7,30,31,32]]
        df.columns = ["AJ_ID","Category","Unit_1","Unit_2","Open_Date","Log_Date","AJ_Desc","AJ_Title","AJ_ZM","RDGC","FZSD","MQLY"]
        df = df.apply(lambda x: tuple(x), axis=1).values.tolist()
        table_name = "bronze_data_stage_1"
        db.insert_table_data(table_name, df)
        ta_log.info(table_name + ": data is inserted.")

    def load_silver_data(self) :
        db = DbOpt()
        sql = "select "
        title =[]
        for key in config.table_definition.get("bronze_data_stage_1").keys():
            sql += key + ","
            title. append(str(key))
        sql = sql[:-1] + " from bronze_data_stage_1"
        # print (sq1)
        # print(title)
        df = pd.DataFrame(db.select_table_data(sql), columns=title)
        print(df.head(5))
        handle = DataHandle()
        df = handle.clean_bronze_data(df)

        db = DbOpt()
        table_name = "silver_fact_caipan"
        db.insert_table_data(table_name, df.values.tolist())
        ta_log.info(table_name +":data is inserted in load_silver_data.")
        #print(df.head(3))

    def clickStage1Button(self):
        db = DbOpt()
        sql = "Select AJ_ID, Category_ID, AJ_ZH_Desc,\"\",\"\", AJ_Title,AJ_ZM,RDGC,FZSD,MQLY from silver_fact_caipan inner join gold_dim_category on silver_fact_caipan.Category = gold_dim_category.Category_Desc where gold_dim_category.Category_ID=1"
        df = pd.DataFrame(db.select_table_data(sql), columns=["AJ_ID","Category_ID","AJ_ZH_Desc","AJ_PJ_PJRX","AJ_PJ_BYRW","AJ_Title","AJ_ZM","RDGC","FZSD","MQLY"])
        # df["AJ_PJ_PJRX"] = ""
        # df["AJ_PJ_BYRW"] = ""
        handle = DataHandle()
        df = handle.clean_silver_data(df)

        table_name = "gold_fact_caipan"
        db.insert_table_data(table_name, df.values.tolist())
        ta_log.info(table_name + ":data is inserted in clickStage1Button.")

    def clickotherButton(self):
        db= DbOpt()
        table_name = "silver_profit_sentences"
        # db.insert_table_data(table_name, [["test1","test2","test3"],["test4","test2","test3"]])
        db.create_table(table_name)

        sql = "select AJ_ID, AJ_PJ_PJRX from gold_fact_caipan"
        df = pd.DataFrame(db.select_table_data(sql), columns=["AJ_ID", "AJ_PJ_PJRX"])
        handle = DataHandle()
        df = handle.extract_profit_data_for_word(df)
        db.insert_table_data(table_name, df.values.tolist())
        ta_log.info(table_name + ":data is inserted in clickOtherButton.")
        #ta_log.info(table_name + "is created in clickotherButton.")

    def clickextractProfitButton(self) :
        db = DbOpt()
        sql = "select AJ_ID, AJ_PJ_PJRX, AJ_PJ_BYRW from gold_fact_caipan"
        df = pd.DataFrame(db.select_table_data(sql), columns=["AJ_ID", "AJ_PJ_PJRX", "AJ_PJ_BYRW"])
        handle = DataHandle()
        df = handle.extract_profit_data(df)
        # print(df.head(5))

        table_name = "gold_fact_profit"
        db.create_table(table_name)
        db.insert_table_data(table_name, df.values.tolist())
        ta_log.info(table_name +":data is inserted in clickextractProfitButton.")

    def clickextractCrimeButton(self):
        db = DbOpt()
        sql = "select AJ_ID, AJ_PJ_PJRX from gold_fact_caipan"
        df = pd.DataFrame(db.select_table_data(sql), columns=["AJ_ID","AJ_PJ_PJRX"])
        print(df.head(5))
        sql = "select Crime_ID, Crime_Desc from gold_dim_crime"
        strList = db.select_table_data(sql)
        crimeDict={}
        for str in strList:
            crimeDict[str[1]] = str[0]
        handle = DataHandle()
        df = handle.extract_crime_data(df, crimeDict)

        print(df.head(5))
        table_name ="gold_fact_crime"
        db.insert_table_data(table_name, df.values.tolist())
        ta_log.info(table_name + ": data is inserted in clickextractCrimeButton.")

    def clickextractCrimeDimensionButton(self):
        db = DbOpt()

        table_name = "silver_AJ_crime"
        # db.create_table(table_name)
        # ta_log.info(table_name + " is created in clickotherButton.")
        sql = "select AJ_ID, AJ_PJ_PJRX from gold_fact_caipan where not exists " \
              "(select 1 from gold_fact_crime where gold_fact_crime.AJ_ID = gold_fact_caipan.AJ_ID)"
        df = pd.DataFrame(db.select_table_data(sql), columns=["AJ_ID", "AJ_PJ_PJRX"])
        print("step1")
        handle = DataHandle()
        df = handle.extract_crime_dimension(df)
        db.insert_table_data(table_name, df.values.tolist())
        ta_log.info(table_name + ": data is inserted in clickextractCrimeDimensionButton.")
