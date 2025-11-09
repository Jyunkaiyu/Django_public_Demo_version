from distutils import core
from this import d
from unittest import result
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod
import os
from pathlib import Path
from django.conf import settings

csv_path = Path(settings.BASE_DIR) / 'model' / 'templates' / 'universal_gpu.csv'

class Website(ABC):
 
    def __init__(self, gpu_name1,gpu_name2):
        self.name1 = gpu_name1  # 城市名稱屬性
        self.name2 = gpu_name2
    @abstractmethod
    def scrape(self):  # 爬取票券抽象方法
        pass

class unigpurank(Website):
    def scrape(self):
        result = []  # 回傳結果
        if self.name1:

            df = pd.read_csv(csv_path, encoding='big5')
            qs=self.name1
            qs2=str(self.name2)
            #df2 = np.array(df)
            namlst = []
            namlst2 = []
            numlst = []
            numlst2 = []
            gdvalue = []
            gdvalue2 = []
            memory = []
            memory2 = []
            clock_rate = []
            clock_rate2 = []


            for i in range(len(df['gpu'])):
                if qs == df['gpu'][i]:
                    namlst.append(df['gpu'][i])
                    numlst.append(df['gpu_point'][i])
                    gdvalue.append(df['cost_performance'][i])
                    clock_rate.append(df['clock_rate'][i])
                    memory.append(df['memory'][i])

                if qs2 == df['gpu'][i]:
                    namlst2.append(df['gpu'][i])
                    numlst2.append(df['gpu_point'][i])
                    gdvalue2.append(df['cost_performance'][i])
                    clock_rate2.append(df['clock_rate'][i])
                    memory2.append(df['memory'][i])

            i = 0

            nam=namlst[i]
            nam2=namlst2[i]
            num=numlst[i]
            num2=numlst2[i]
            pgdvalue = gdvalue[i]
            pgdvalue2 = gdvalue2[i]
            pclock_rate = clock_rate[i]
            pclock_rate2 = clock_rate2[i]
            pmemory = memory[i]
            pmemory2 = memory2[i]
            a=0
            b=0
            c=0

            numans =str((round((num/num2)-1 , 2))*100)+"%"
            pgdvalueans =str((round((pgdvalue/pgdvalue2)-1 , 2))*100)+"%"
            pclock_rateans = str((round((pclock_rate/pclock_rate2)-1 , 2))*100)+"%"
            pmemoryans = str((round((pmemory/pmemory2)-1 , 2))*100)+"%"


            if num > num2:
                #numanssss = str(num)+"  win  &  "+str(num2)+"  lose"
                numans ="+"+str((round((num/num2)-1 , 2))*100)+"%"
                a+=1
            if num < num2:
                #numans = str(num)+"  lose  &  "+str(num2)+"  win"
                b+=1
            if num == num2:
                numans = "0%"
                c+=1


            if pgdvalue > pgdvalue2:
                #pgdvalueansss = str(pgdvalue)+"  win & "+str(pgdvalue2)+"lose"
                pgdvalueans = "+"+str((round((pgdvalue/pgdvalue2)-1 , 2))*100)+"%"
                a+=1
            if pgdvalue < pgdvalue2:
                #pgdvalueansss = str(pgdvalue)+"  lose & "+str(pgdvalue2)+"win"
                b+=1
            if pgdvalue == pgdvalue2:
                pgdvalueans = "0%"
                c+=1

            if pmemory > pmemory2:
                #pcoreansss = str(pcore)+"  win  &  "+str(pcore2)+"  lose"
                pmemoryans = "+"+str((round((pmemory/pmemory2)-1 , 2))*100)+"%"
                a+=1
            if pmemory < pmemory2:
                #pcoreansss = str(pcore)+"  lose  &  "+str(pcore2)+"  win"
                b+=1
            if pmemory == pmemory2:
                pmemoryans = "0%"
                c+=1

            if pclock_rate > pclock_rate2:
                #pclock_rateansss = str(pclock_rate)+"  win  &  "+str(pclock_rate2)+"  lose"
                pclock_rateans = "+"+str((round((pclock_rate/pclock_rate2)-1 , 2))*100)+"%"
                a+=1
            if pclock_rate < pclock_rate2:
                #pclock_rateans = str(pclock_rate)+"  lose  &  "+str(pclock_rate2)+"win"
                b+=1
            if pclock_rate == pclock_rate2:
                pclock_rateans = "0%"
                c+=1

            if a>b:
                ans = nam
            if a<b:
                ans = nam2
            if a==b:
                ans = nam +"  gpu get tie with  "+nam2

            result.append(
                dict(gpuone=nam  , score_one=num , gputwo=nam2 , score_two=num2 , gpugv = pgdvalue , gpugv_two = pgdvalue2 , gpumemory = pmemory , gpumemory_two = pmemory2 , clrat = clock_rate , clrat_two = clock_rate2 , nuans = numans , gpugvans = pgdvalueans , gpumemoryans = pmemoryans , clratans = pclock_rateans , ansr = ans , sum_upa = a , sum_upb = b))

        return result