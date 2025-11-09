import pandas as pd
import os
from pathlib import Path
from django.conf import settings
import requests
import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod

csv_path = Path(settings.BASE_DIR) / 'model' / 'templates' / 'gpu_rank.csv'

class Website(ABC):

    def __init__(self, gpu_name1):
        self.name1 = gpu_name1  # 城市名稱屬性

    @abstractmethod
    def scrape(self):  # 爬取票券抽象方法
        pass


class gpuchallenge(Website):
    def scrape(self):
        result = []  # 回傳結果
        if self.name1:

            df = pd.read_csv(csv_path, encoding='big5')
            qs = self.name1
            # qs2=self.name2
            #df2 = np.array(df)
            namlst = []
            numlst = []
            aa = 1
            alst = []
            sele = True

            if " " in qs:
                qs = qs.split(" ")
                for i in range(len(df['gpu'])):

                    for x in range(len(qs)):
                        if qs[x].upper() in df['gpu'][i].upper():
                            sele = True
                        else:
                            sele = False
                    if sele == True:
                        namlst.append(df['gpu'][i])
                        numlst.append(df['gpu_point'][i])
                        alst.append(aa)
                        aa += 1
                    ans1 = df['gpu_point'][i]
                    #strans1 = str(ans1)

                for i in range(len(namlst)):

                    a = namlst[i]
                    b = numlst[i]
                    c = alst[i]
                    ctxt = "No "+str(c)

                    result.append(
                        dict(gpuone=a, score_one=b, nober=ctxt))

                return result

            else:
                for i in range(len(df['gpu'])):
                    if qs.upper() in df['gpu'][i].upper():
                        namlst.append(df['gpu'][i])
                        numlst.append(df['gpu_point'][i])
                        alst.append(aa)
                        aa += 1
                        ans1 = df['gpu_point'][i]
                #strans1 = str(ans1)

                for i in range(len(namlst)):

                    a = namlst[i]
                    b = numlst[i]
                    c = alst[i]
                    ctxt = "No "+str(c)
                    result.append(
                        dict(gpuone=a, score_one=b, nober=ctxt))

                return result

        else:
            df = pd.read_csv(csv_path, encoding='big5')
            namlst = []
            numlst = []
            aa = 1
            alst = []
            for i in range(len(df['gpu'])):
                namlst.append(df['gpu'][i])
                numlst.append(df['gpu_point'][i])
                alst.append(aa)
                aa += 1
                ans1 = df['gpu_point'][i]

            for i in range(len(namlst)):

                a = namlst[i]
                b = numlst[i]
                c = alst[i]
                ctxt = "No "+str(c)
                result.append(
                    dict(gpuone=a, score_one=b, nober=ctxt))

            return result
