import pandas as pd
import os
from pathlib import Path
from django.conf import settings
import requests
import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod

csv_path = Path(settings.BASE_DIR) / 'model' / 'templates' / 'cpu_rank.csv'

class Website(ABC):

    def __init__(self, cpu_name1):
        self.name1 = cpu_name1  # 程式名稱屬性

    @abstractmethod
    def scrape(self):  # 爬取票券抽象方法
        pass


class cpuchallenge(Website):
    def scrape(self):
        result = []  # 回傳結果

        if self.name1:
            df = pd.read_csv(csv_path, encoding='big5')
            qs = self.name1
            # qs2=self.name2s
            #df2 = np.array(df)
            namlst = []
            numlst = []
            aa = 1
            dis = []
            alst = []
            sele=True


            if " " in qs:
                qs = qs.split(" ")
                for i in range(len(df['cpu'])):

                    for x in range(len(qs)):
                        if qs[x].upper() in df['cpu'][i].upper():
                            sele=True
                        else:
                            sele=False
                    if sele == True:
                        namlst.append(df['cpu'][i])
                        numlst.append(df['cpu_point'][i])
                        alst.append(aa)
                        aa += 1
                        ans1 = df['cpu_point'][i]
                #strans1 = str(ans1)

                for i in range(len(namlst)):

                    a = namlst[i]
                    b = numlst[i]
                    c = alst[i]
                    ctxt = "No "+str(c)
                    result.append(
                        dict(cpuone=a, score_one=b, nober=ctxt))

            else:

                for i in range(len(df['cpu'])):
                    if qs.upper() in df['cpu'][i].upper():
                        namlst.append(df['cpu'][i])
                        numlst.append(df['cpu_point'][i])
                        alst.append(aa)
                        aa += 1
                        ans1 = df['cpu_point'][i]
                #strans1 = str(ans1)

                for i in range(len(namlst)):

                    a = namlst[i]
                    b = numlst[i]
                    c = alst[i]
                    ctxt = "No "+str(c)
                    result.append(
                        dict(cpuone=a, score_one=b, nober=ctxt))

            return result

        else:
            df = pd.read_csv(csv_path, encoding='big5')
            namlst = []
            numlst = []
            alst = []
            aa = 1
            for i in range(len(df['cpu'])):
                namlst.append(df['cpu'][i])
                numlst.append(df['cpu_point'][i])
                alst.append(aa)
                aa += 1
                ans1 = df['cpu_point'][i]

            for i in range(len(namlst)):

                a = namlst[i]
                b = numlst[i]
                c = alst[i]
                ctxt = "No "+str(c)
                result.append(
                    dict(cpuone=a, score_one=b, nober=ctxt))

            return result
