# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 09:38:16 2021

@author: Shahamat
"""
from sklearn.cluster import KMeans
import time
import pandas as pd
import numpy as np
import pickle
from pyod.utils.utility import standardizer
from sklearn.linear_model import LinearRegression


        
###################Threshold finder######################################

class Dynamic_Threshold_Finder:
    def __init__(self, min_required_samples=2, max_ratio=100, random_seed=2020,cards_list=[]):
        self.random_seed = random_seed
        self.max_ratio = max_ratio
        self.min_required_samples = min_required_samples
        self.final_dict = {}
        self.cards_list = cards_list
        
        
    def find_max_and_ratio_thr_count(self,df,final_dict={},
                                     _type='OUTPUT',_duration='DAILY'):
        _col_name = 'COUNT'
        cols_list = ['CARDIDHASH',_col_name]
        df = pd.DataFrame(df,columns=cols_list)
        
        if len(self.cards_list)>0:
            df = df.loc[df['CARDIDHASH'].isin(self.cards_list),:]
        start_time = time.time()    
        grps = df.groupby(['CARDIDHASH'])
        for _crd in df['CARDIDHASH'].unique():
            _grp = grps.get_group(_crd)
            
            _vals = _grp[_col_name].values
            _vals = (_vals[_vals!=0]).astype(float)
            if len(_vals)<self.min_required_samples:
                final_dict = self.check_dict(final_dict,_crd)
                final_dict[_crd]['RATIO_'+_duration+'_'+_type+'_FREQ'] = np.float16(-1)
            else:
                final_dict = self.check_dict(final_dict,_crd)
                final_dict[_crd]['RATIO_'+_duration+'_'+_type+'_FREQ'] = np.float16(min(self.max_ratio,np.max(_vals[1:]/_vals[:-1])))
                # if _duration=='WEEKLY' and ('RATIO_DAILY_'+_type+'_FREQ' in final_dict[_crd]):
                #     final_dict[_crd]['RATIO_'+_duration+'_'+_type+'_FREQ']=min(final_dict[_crd]['RATIO_'+_duration+'_'+_type+'_FREQ'],7*final_dict[_crd]['RATIO_DAILY_'+_type+'_FREQ'])
                # if _duration=='MONTHLY' and ('RATIO_DAILY_'+_type+'_FREQ' in final_dict[_crd]):
                #     final_dict[_crd]['RATIO_'+_duration+'_'+_type+'_FREQ']=min(final_dict[_crd]['RATIO_'+_duration+'_'+_type+'_FREQ'],30*final_dict[_crd]['RATIO_DAILY_'+_type+'_FREQ'])
                
        print('computation time of finding RATIO threshold:',time.time()-start_time) 
        
        #########find max count##########
        start_time = time.time()    
        df['cnt_max_main'] = grps[_col_name].transform('max')
        
        ###########clustering##########
        stim = time.time()    
#         brc = Birch(n_clusters=None)
        brc = KMeans()
        df['cluster'] = brc.fit_predict(standardizer(df[['cnt_max_main']].values))
        print('computation time of birch clustering:',time.time()-stim)                


        #########find max cluster#######
        grps_2 = df.groupby('cluster')
        df['cnt_max_cluster']= grps_2['cnt_max_main'].transform('max')
        ##########add to dict###############
        for _crd in df['CARDIDHASH'].unique():
            _grp = grps.get_group(_crd)
            _vals = _grp['cnt_max_cluster'].values
            final_dict = self.check_dict(final_dict,_crd)
            final_dict[_crd]['MAX_'+_duration+'_'+_type+'_FREQ'] = np.int16(np.max(_vals))
            
            if _duration=='WEEKLY' and ('MAX_DAILY_'+_type+'_FREQ' in final_dict[_crd]):
                final_dict[_crd]['MAX_'+_duration+'_'+_type+'_FREQ']=min(final_dict[_crd]['MAX_'+_duration+'_'+_type+'_FREQ'],7*final_dict[_crd]['MAX_DAILY_'+_type+'_FREQ'])

            if _duration=='MONTHLY' and ('MAX_DAILY_'+_type+'_FREQ' in final_dict[_crd]):
                final_dict[_crd]['MAX_'+_duration+'_'+_type+'_FREQ']=min(final_dict[_crd]['MAX_'+_duration+'_'+_type+'_FREQ'],30*final_dict[_crd]['MAX_DAILY_'+_type+'_FREQ'])

        
        print('computation time of finding MAX threshold:',time.time()-start_time)                
        return final_dict

    def find_max_and_ratio_thr_amount(self,df,final_dict={},_type='OUTPUT',_duration='DAILY'):
        _col_name = 'SUM'
        cols_list = ['CARDIDHASH',_col_name]
        df = pd.DataFrame(df,columns=cols_list)
        
        if len(self.cards_list)>0:
            df = df.loc[df['CARDIDHASH'].isin(self.cards_list),:]
            
            
        grps = df.groupby(['CARDIDHASH'])

        for _crd in df['CARDIDHASH'].unique():
            _grp = grps.get_group(_crd)                
                
            _vals = _grp[_col_name].values
            _vals = (_vals[_vals!=0]).astype(float)
            if len(_vals)<self.min_required_samples:
                final_dict = self.check_dict(final_dict,_crd)
                final_dict[_crd]['RATIO_'+_duration+'_'+_type+'_AMOUNT'] = np.float16(-1)
            else:
                final_dict = self.check_dict(final_dict,_crd)
                final_dict[_crd]['RATIO_'+_duration+'_'+_type+'_AMOUNT'] =np.float16(min(self.max_ratio,np.max(_vals[1:]/_vals[:-1])))
        


        #########find max amount##########
        df['amnt_max_main'] = grps[_col_name].transform('max')
        ###########clustering###########
#         brc = Birch(n_clusters=None)
        brc = KMeans()
        df['cluster'] = brc.fit_predict(standardizer(df[['amnt_max_main']].values))
        #########find max cluster#######
        grps_2 = df.groupby('cluster')    
        df['amnt_max_cluster'] = grps_2['amnt_max_main'].transform('max')
        
        for _crd in df['CARDIDHASH'].unique():
            _grp = grps.get_group(_crd)
            _vals = _grp['amnt_max_cluster'].values
            final_dict = self.check_dict(final_dict,_crd)
            final_dict[_crd]['MAX_'+_duration+'_'+_type+'_AMOUNT'] = np.float32(np.max(_vals))
                        
        return final_dict
  

    def find_max_and_ratio_thr_turnover(self,df,final_dict={},_duration='DAILY'):
        _type = 'AMOUNT'
        
        _col_name = 'TURNOVER'
        cols_list = ['CARDIDHASH',_col_name]
        df = pd.DataFrame(df,columns=cols_list)
        
        if len(self.cards_list)>0:
            df = df.loc[df['CARDIDHASH'].isin(self.cards_list),:]
            
        grps = df.groupby(['CARDIDHASH'])

        for _crd in df['CARDIDHASH'].unique():
            _grp = grps.get_group(_crd)
        
            _vals = _grp[_col_name].values
            _vals = (_vals[_vals!=0]).astype(float)
                        
            if len(_vals)<self.min_required_samples:
                final_dict = self.check_dict(final_dict,_crd)
                final_dict[_crd]['RATIO_'+_duration+'_TURNOVER_'+_type] = np.float16(-1)
            else:
                final_dict = self.check_dict(final_dict,_crd)
                final_dict[_crd]['RATIO_'+_duration+'_TURNOVER_'+_type] = np.float16(np.max(_vals[1:]/_vals[:-1]))

                
        ###########find max turnover###########
        df['amnt_max_main'] = grps[_col_name].transform('max')  
        ###########clustering###########
#         brc = Birch(n_clusters=None)
        brc = KMeans()
        df['cluster'] = brc.fit_predict(standardizer(df[['amnt_max_main']].values))
    
        ##########find max cluster##########      
        grps_2 = df.groupby('cluster')
        df['cnt_max_cluster']= grps_2['amnt_max_main'].transform('max')
        #############################
        for _crd in df['CARDIDHASH'].unique():
            _grp = grps.get_group(_crd)
            _vals = _grp['cnt_max_cluster'].values
            final_dict = self.check_dict(final_dict,_crd)
            final_dict[_crd]['MAX_'+_duration+'_TURNOVER_'+_type] = np.float32(np.max(_vals))
        
                        
        return final_dict


    def find_anomaly_score_thr(self,df,final_dict={},_duration='DAILY',model_name=''):
        _col_name = 'col'
        cols_list = ['CARDIDHASH',_col_name]
        df = pd.DataFrame(df,columns=cols_list)
        
        if len(self.cards_list)>0:
            df = df.loc[df['CARDIDHASH'].isin(self.cards_list),:]
            
        start_time = time.time()    
        all_cards = []
        all_vals = []
        grps = df.groupby('CARDIDHASH')
        for _crd in df['CARDIDHASH'].unique():
            _grp = grps.get_group(_crd)        
            _vals = _grp[_col_name].values
            all_cards.append(_crd)
            all_vals.append(_vals)
        
        all_cards = np.array(all_cards)
        all_vals = np.array(all_vals)
        del df
        tmp_df = pd.DataFrame(all_cards,columns=['CARDIDHASH'])
        del all_cards
        print('computation time of data preparation (AS):',time.time()-start_time)                
        
        ###########clustering###########  
        start_time = time.time()            
        brc = KMeans()#Birch(n_clusters=None)
        tmp_df['cluster'] = brc.fit_predict(standardizer(all_vals))
        print('computation time of clustering (AS):',time.time()-start_time)                
        
        ######find anomaly score#######  
        start_time = time.time()    
        tmp_df['A_Score'] = 0      
        _preds = []
        for _row in all_vals:
            _tas = self.find_anomaly_score(_row)
            _preds.append(_tas)
        tmp_df['A_Score'] = _preds
        ################################
        tmp_df['A_Score_max_cluster'] = 0
        tmp_df['A_Score_max_cluster'] = tmp_df.groupby('cluster')['A_Score'].transform('max')

        grps = tmp_df.groupby('CARDIDHASH')
        for _crd in tmp_df['CARDIDHASH'].unique():            
            _grp = grps.get_group(_crd)        
            _preds = _grp['A_Score_max_cluster'].values           
            
            if len(_preds)<1:#self.min_required_samples:
                A_score = -1
            else:
                A_score = np.max(_preds)
                
            final_dict = self.check_dict(final_dict,_crd)
            final_dict[_crd]['MAX_'+_duration+'_ANOMALY_SCORE_'+model_name] = np.float32(A_score)
        print('computation time of finding AScore threshold (AS):',time.time()-start_time)                

        return final_dict
    
    def find_anomaly_score(self,_data):  
        _data = _data.reshape(-1,1)
        X,Y=_data[:-2,:],_data[1:-1,0] 
        model = LinearRegression()
        model.fit(X, Y)
        y_pred = model.predict(_data)
        ascore = np.abs(_data[-1]-y_pred[-1])
        # ascore = 
        return ascore

    def save_dict(self,final_dict,fname='thresholds_dict.pickle'):
        with open(fname, 'wb') as fp:
            pickle.dump(final_dict, fp)

    def load_dict(self,fname='thresholds_dict.pickle'):
        with open(fname, 'rb') as fp:
            result_dict = pickle.load(fp)
        return result_dict

    def check_dict(self,final_dict,_card):        
        tmp_dict = { }        
        if not(_card in final_dict):
            final_dict[_card] = tmp_dict.copy()
            
        return final_dict
        
    
        
