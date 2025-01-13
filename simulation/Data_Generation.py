import numpy as np
from simulation.Utils import *# generate_data, print_data, generate_population,pops_to_historical_data
import time
from persiantools.jdatetime import JalaliDate

from simulation.Dynamic_Threshold_Finder import Dynamic_Threshold_Finder

class Data_Generation:
    def __init__(self):
        DTF = Dynamic_Threshold_Finder()
        pop_1 = generate_population(n_pop = 100,min_sum_month=2e6,max_sum_month=5e6,
                                    min_n_income=1,max_n_income=2,
                                    min_p_save=0.3,max_p_save=0.4,
                                    min_trx_outc=1,max_trx_outc=10,
                                    min_trx_inc=1,max_trx_inc=2)
        
        pop_2 = generate_population(n_pop = 100,min_sum_month=2e6,max_sum_month=5e6,
                                    min_n_income=25,max_n_income=28,
                                    min_p_save=0.3,max_p_save=0.4,
                                    min_trx_outc=1,max_trx_outc=10,
                                    min_trx_inc=5,max_trx_inc=100)
        
        pop_3 = generate_population_much_inc(n_pop = 100,
                                             min_sum_month=20e7,max_sum_month=99e7,
                                             min_n_outcome=3,max_n_outcome=5,
                                             min_p_save=0.05,max_p_save=0.10,
                                             min_trx_outc=1,max_trx_outc=2,
                                             min_trx_inc=40,max_trx_inc=80)
        
        pop_4 = generate_population_much_inc(n_pop = 100,
                                             min_sum_month=10e7,max_sum_month=20e7,
                                             min_n_outcome=10,max_n_outcome=20,
                                             min_p_save=0.15,max_p_save=0.20,
                                             min_trx_outc=1,max_trx_outc=5,
                                             min_trx_inc=20,max_trx_inc=50)
        
        data_frame,data_dict = pops_to_historical_data([pop_1,pop_2,pop_3,pop_4],JalaliDate(year=1400,month=3,day=11))
        data_daily,data_daily_last = get_daily_data(data_dict)
        data_weekly,data_weekly_current,data_weekly_last = get_weekly_data(data_dict)
        data_monthly,data_monthly_current,data_monthly_last = get_monthly_data(data_dict)
    
        #####   DAYLY  #######
        final_dict = {}
        
        object_file=[(_d[0],_d[1]) for _d in data_daily]
        final_dict = DTF.find_max_and_ratio_thr_amount(object_file,final_dict,_type='INPUT',_duration='DAILY')
        object_file=[(_d[0],_d[2]) for _d in data_daily]
        final_dict = DTF.find_max_and_ratio_thr_count(object_file,final_dict,_type='INPUT',_duration='DAILY')
        object_file=[(_d[0],_d[3]) for _d in data_daily]
        final_dict = DTF.find_max_and_ratio_thr_amount(object_file,final_dict,_type='OUTPUT',_duration='DAILY')
        object_file=[(_d[0],_d[4]) for _d in data_daily]
        final_dict = DTF.find_max_and_ratio_thr_count(object_file,final_dict,_type='OUTPUT',_duration='DAILY')
        # final_dict = DTF.find_anomaly_score_thr(object_file,final_dict,_duration='DAILY',model_name='OUTPUT_FREQ')
        
        #####   WEEKLY  #######
        object_file=[(_d[0],_d[1]) for _d in data_weekly]
        final_dict = DTF.find_max_and_ratio_thr_amount(object_file,final_dict,_type='INPUT',_duration='WEEKLY')
        object_file=[(_d[0],_d[2]) for _d in data_weekly]
        final_dict = DTF.find_max_and_ratio_thr_count(object_file,final_dict,_type='INPUT',_duration='WEEKLY')
        object_file=[(_d[0],_d[3]) for _d in data_weekly]
        final_dict = DTF.find_max_and_ratio_thr_amount(object_file,final_dict,_type='OUTPUT',_duration='WEEKLY')
        object_file=[(_d[0],_d[4]) for _d in data_weekly]
        final_dict = DTF.find_max_and_ratio_thr_count(object_file,final_dict,_type='OUTPUT',_duration='WEEKLY')
        # final_dict = DTF.find_anomaly_score_thr(object_file,final_dict,_duration='WEEKLY',model_name='OUTPUT_FREQ')
        
        #####   MONTHLY  #######
        object_file=[(_d[0],_d[1]) for _d in data_monthly]
        final_dict = DTF.find_max_and_ratio_thr_amount(object_file,final_dict,_type='INPUT',_duration='MONTHLY')
        object_file=[(_d[0],_d[2]) for _d in data_monthly]
        final_dict = DTF.find_max_and_ratio_thr_count(object_file,final_dict,_type='INPUT',_duration='MONTHLY')
        object_file=[(_d[0],_d[3]) for _d in data_monthly]
        final_dict = DTF.find_max_and_ratio_thr_amount(object_file,final_dict,_type='OUTPUT',_duration='MONTHLY')
        object_file=[(_d[0],_d[4]) for _d in data_monthly]
        final_dict = DTF.find_max_and_ratio_thr_count(object_file,final_dict,_type='OUTPUT',_duration='MONTHLY')
        # final_dict = DTF.find_anomaly_score_thr(object_file,final_dict,_duration='MONTHLY',model_name='OUTPUT_FREQ')
        self.final_dict = final_dict
        self.data_daily = self.list_to_dict(data_daily)
        self.data_daily_last = data_daily_last
        self.data_weekly = self.list_to_dict(data_weekly)
        self.data_weekly_current = data_weekly_current
        self.data_weekly_last = data_weekly_last
        self.data_monthly = self.list_to_dict(data_monthly)
        self.data_monthly_current = data_monthly_current
        self.data_monthly_last = data_monthly_last
        
    def list_to_dict(self,data):
        ddict = {}
        for _d in data:
            if _d[0] in ddict:
                ddict[_d[0]].append(_d)
            else:
                ddict[_d[0]] = [_d]        
        return ddict
    
    def get_random_sample(self,pop_number=4):  
        if pop_number==1:
            card_id = np.random.randint(0,100) 
        if pop_number==2:
            card_id = np.random.randint(100,200) 
        if pop_number==3:
            card_id = np.random.randint(200,300) 
        if pop_number==4:
            card_id = np.random.randint(300,400) 
         
        _data = (   card_id,
                    self.final_dict[card_id],
                    self.data_daily[card_id],
                    self.data_daily_last[card_id],
                    self.data_weekly[card_id],
                    self.data_weekly_current[card_id],
                    self.data_weekly_last[card_id],
                    self.data_monthly[card_id],
                    self.data_monthly_current[card_id],
                    self.data_monthly_last[card_id],    
                    )
        return _data