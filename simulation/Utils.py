import numpy as np
from persiantools.jdatetime import JalaliDate#,JalaliDateTime
import datetime
import copy
import pandas as pd
from matplotlib import pyplot as plt
from termcolor import colored


def generate_random_nums_normal(n_nums,sum_nums):
    if n_nums > 0:
        rnd_array = np.random.randn(n_nums)
        rnd_array = (rnd_array-rnd_array.min())/((rnd_array.max()-rnd_array.min())+1e-20)
        rnd_array = (rnd_array/(rnd_array.sum()+1e-20))*sum_nums
    else:
        rnd_array = np.array([0])
    return np.round(rnd_array)
###
def generate_random_nums_uniform(n_nums,sum_nums):
    if n_nums > 0:
        rnd_array = np.random.rand(n_nums)
        rnd_array = (rnd_array/rnd_array.sum())*sum_nums
    else:
        rnd_array = np.array([0])
    return np.round(rnd_array)
###
def generate_random_nums_multinomial(n_nums,sum_nums):
    if n_nums > 0:
        rnd_array = np.random.multinomial(sum_nums, np.ones(n_nums)/n_nums, size=1)[0]           
    else:
        rnd_array = np.array([0])
    return np.round(rnd_array)
###
def generate_outcome(sum_month,num_days=31,min_trx=1,max_trx=20,mode=2):
    if mode==0:
        generate_random = generate_random_nums_normal
    if mode==1:
        generate_random = generate_random_nums_uniform
    if mode==2:
        generate_random = generate_random_nums_multinomial
        
#     daily_data = generate_random(num_days,sum_month)
    ###########
    daily_data = list(generate_random(num_days,sum_month))
    while len(daily_data)<31:
        daily_data.insert(np.random.choice(len(daily_data)),0)    
    ###########
    in_days_data = []
    for _cnt,_val in enumerate(daily_data):
        num_trx = np.random.randint(min_trx,max_trx)
        tmp_inday = generate_random(num_trx,_val)
        in_days_data.append([[0],tmp_inday])
    return in_days_data

#####################
def generate_income(in_days_data,n_income=1,p_save=0.2,min_trx=1,max_trx=5,mode=2):
    if mode==0:
        generate_random = generate_random_nums_normal
    if mode==1:
        generate_random = generate_random_nums_uniform
    if mode==2:
        generate_random = generate_random_nums_multinomial
        
    # in_days_data_income = []
    all_vals = np.array([_val[1].sum() for _val in in_days_data])
    all_vals = all_vals + (all_vals*p_save)
#     tmp_income = list(np.zeros_like(all_vals))
    tmp_income = [np.array([0]) for _v in all_vals]

#     if n_income == 0:
#         print('Error => n_income sholud be >= 1')
    assert n_income > 0,'n_income sholud be >= 1'

    if n_income == 1:
        num_trx = np.random.randint(min_trx,max_trx)
        tmp_income[0] = generate_random(num_trx,all_vals.sum())
        # print('*******',all_vals.sum(), tmp_income[0])
        
    if n_income == 2:        
        rnd_choice = np.random.choice(range(1,len(all_vals)-1))
        sum_inco = all_vals[:rnd_choice]
        num_trx = np.random.randint(min_trx,max_trx)
        tmp_income[0] = generate_random(num_trx,sum_inco.sum())
        sum_inco = all_vals[rnd_choice:]
        num_trx = np.random.randint(min_trx,max_trx)        
        tmp_income[rnd_choice] = generate_random(num_trx,sum_inco.sum())        
    if n_income > 2: 
        _rep = False#(n_income>=(len(all_vals)-2))
        rnd_choice = sorted(np.random.choice(range(1,len(all_vals)-1),size=n_income-1,replace=_rep))
        for _idx in range(len(rnd_choice)):
            if _idx==0:
                sum_inco = all_vals[:rnd_choice[_idx]]
                num_trx = np.random.randint(min_trx,max_trx)
                tmp_income[0] = generate_random(num_trx,sum_inco.sum())
    #             print('000_idx',_idx,rnd_choice[_idx])
            elif _idx==(len(rnd_choice)-1):
                min_idx = rnd_choice[_idx-1]
                max_idx = rnd_choice[_idx]
                sum_inco = all_vals[min_idx:max_idx]
                num_trx = np.random.randint(min_trx,max_trx)                
                tmp_income[min_idx] = generate_random(num_trx,sum_inco.sum())
    #             print('between',_idx,min_idx,max_idx)

                sum_inco = all_vals[rnd_choice[_idx]:]
                num_trx = np.random.randint(min_trx,max_trx)
                tmp_income[rnd_choice[_idx]] = generate_random(num_trx,sum_inco.sum())
    #             print('len_idx',_idx,rnd_choice[_idx])            
            else:
                min_idx = rnd_choice[_idx-1]
                max_idx = rnd_choice[_idx]
                sum_inco = all_vals[min_idx:max_idx]
                num_trx = np.random.randint(min_trx,max_trx)                
                tmp_income[min_idx] = generate_random(num_trx,sum_inco.sum())
    #             print('between_idx_min',_idx,min_idx,max_idx)                        
        
    return tmp_income
#####################

def generate_data(sum_month,num_days=20,
                  min_trx_outc=1,max_trx_outc=20,
                  n_income=1,p_save=0.2,
                  min_trx_inc=1,max_trx_inc=5,
                  mode=2):
    outc_data = generate_outcome(sum_month,num_days,min_trx_outc,max_trx_outc,mode)
    inc_data = generate_income(outc_data,n_income,p_save,min_trx_inc,max_trx_inc,mode)
    for _idx in range(len(outc_data)):
        outc_data[_idx][0]=inc_data[_idx]
    return outc_data
#####################
#####################
#####################
	
	
def generate_income_much(sum_month,num_days=30,min_trx=1,max_trx=20,mode=2):
    if mode==0:
        generate_random = generate_random_nums_normal
    if mode==1:
        generate_random = generate_random_nums_uniform
    if mode==2:
        generate_random = generate_random_nums_multinomial
        
    daily_data = list(generate_random(num_days,sum_month))
    while len(daily_data)<31:
        daily_data.insert(np.random.choice(len(daily_data)),0)
    in_days_data = []
    for _cnt,_val in enumerate(daily_data):
        if _val!=0:
            num_trx = np.random.randint(min_trx,max_trx)            
            tmp_inday = generate_random(num_trx,_val)
        else:
            tmp_inday = generate_random(0,_val)
        in_days_data.append([tmp_inday,[0]])
    return in_days_data

#####################
def generate_outcome_much(in_days_data,n_outcome=1,p_save=0.2,min_trx=1,max_trx=5,mode=2):
    if mode==0:
        generate_random = generate_random_nums_normal
    if mode==1:
        generate_random = generate_random_nums_uniform
    if mode==2:
        generate_random = generate_random_nums_multinomial
        
    all_vals = np.array([_val[0].sum() for _val in in_days_data])
    all_vals = all_vals - (all_vals*p_save)
#     tmp_income = list(np.zeros_like(all_vals))
    tmp_outcome = [np.array([0]) for _v in all_vals]

#     if n_income == 0:
#         print('Error => n_income sholud be >= 1')
    assert n_outcome > 0,'n_outcome sholud be >= 1'

    if n_outcome == 1:
        num_trx = np.random.randint(min_trx,max_trx)
        tmp_outcome[-1] = generate_random(num_trx,all_vals.sum())
        
    if n_outcome == 2:        
        rnd_choice = np.random.choice(range(1,len(all_vals)-1))
        sum_inco = all_vals[:rnd_choice]
        num_trx = np.random.randint(min_trx,max_trx)
        tmp_outcome[rnd_choice] = generate_random(num_trx,sum_inco.sum())
        sum_inco = all_vals[rnd_choice:]
        num_trx = np.random.randint(min_trx,max_trx)        
        tmp_outcome[-1] = generate_random(num_trx,sum_inco.sum())        
    if n_outcome > 2: 
        _rep = False#(n_income>=(len(all_vals)-2))
        rnd_choice = sorted(np.random.choice(range(1,len(all_vals)-1),size=n_outcome-1,replace=_rep))
        for _idx in range(len(rnd_choice)):
            if _idx==0:
                sum_inco = all_vals[:rnd_choice[_idx]]
                num_trx = np.random.randint(min_trx,max_trx)
                tmp_outcome[rnd_choice[_idx]] = generate_random(num_trx,sum_inco.sum())
            elif _idx==(len(rnd_choice)-1):
                min_idx = rnd_choice[_idx-1]
                max_idx = rnd_choice[_idx]
                sum_inco = all_vals[min_idx:max_idx]
                num_trx = np.random.randint(min_trx,max_trx)                
                tmp_outcome[max_idx] = generate_random(num_trx,sum_inco.sum())
                sum_inco = all_vals[rnd_choice[_idx]:]
                num_trx = np.random.randint(min_trx,max_trx)
                tmp_outcome[-1] = generate_random(num_trx,sum_inco.sum())
            else:
                min_idx = rnd_choice[_idx-1]
                max_idx = rnd_choice[_idx]
                sum_inco = all_vals[min_idx:max_idx]
                num_trx = np.random.randint(min_trx,max_trx)                
                tmp_outcome[max_idx] = generate_random(num_trx,sum_inco.sum())
        
    return tmp_outcome
#####################

def generate_data_much_inc(sum_month,num_days=25,
                  min_trx_outc=1,max_trx_outc=2,
                  n_outcome=1,p_save=0.2,
                  min_trx_inc=40,max_trx_inc=80,                  
                  mode=2):
    inc_data = generate_income_much(sum_month,num_days,min_trx_inc,max_trx_inc,mode)
    outc_data = generate_outcome_much(inc_data,n_outcome,p_save,min_trx_outc,max_trx_outc,mode)
#     print(outc_data)
    for _idx in range(len(inc_data)):
        inc_data[_idx][1]=outc_data[_idx]
    return inc_data
	
	
#####################
def generate_population(n_pop = 100,min_sum_month=2e3,max_sum_month=5e3,
                        min_n_income=3,max_n_income=5,
                        min_p_save=0.3,max_p_save=0.4,
                        min_trx_outc=16,max_trx_outc=20,
                        min_trx_inc=1,max_trx_inc=3):
    pop_data = []
    for _pop in range(n_pop):
        person = []
        rnd_sum_month = np.random.randint(min_sum_month,max_sum_month)#*1000.0
        rnd_n_income = np.random.randint(min_n_income,max_n_income)
        rnd_p_save = min((np.random.rand()+min_p_save),max_p_save)

        for _month in range(10):
            tmp = generate_data(sum_month=rnd_sum_month,num_days=20,
                                min_trx_outc=min_trx_outc,max_trx_outc=max_trx_outc,
                                n_income=rnd_n_income,p_save=rnd_p_save,
                                min_trx_inc=min_trx_inc,max_trx_inc=max_trx_inc)
            person.append(tmp)
            # print('tmp:',tmp)
            
        pop_data.append(person)
    return pop_data
################################
def generate_population_much_inc(n_pop = 100,
                                 min_sum_month=80e7,max_sum_month=99e7,
                                 min_n_outcome=3,max_n_outcome=5,
                                 min_p_save=0.05,max_p_save=0.10,
                                 min_trx_outc=1,max_trx_outc=2,
                                 min_trx_inc=40,max_trx_inc=80):
    pop_data = []
    for _pop in range(n_pop):
        person = []
        rnd_sum_month = np.random.randint(min_sum_month,max_sum_month)#*1000.0
        rnd_n_outcome = np.random.randint(min_n_outcome,max_n_outcome)
        rnd_p_save = min((np.random.rand()+min_p_save),max_p_save)

        for _month in range(10):
            tmp = generate_data_much_inc(sum_month=rnd_sum_month,num_days=25,
                                min_trx_outc=min_trx_outc,max_trx_outc=max_trx_outc,
                                n_outcome=rnd_n_outcome,p_save=rnd_p_save,
                                min_trx_inc=min_trx_inc,max_trx_inc=max_trx_inc)
            person.append(tmp)
        pop_data.append(person)
    return pop_data	
############################

def add_date_to_pops(pops_list,_today = JalaliDate(year=1400,month=3,day=11)):
    # if _today==[]:
    #     _today = JalaliDate.today()
    
    tdel = datetime.timedelta(days=1)
    pops=copy.deepcopy(pops_list)#([pop_1,pop_2,pop_3,pop_4])

    for _pop in range(len(pops)):
        for _person in range(len(pops[_pop])):
            end_day = _today - tdel
            for _month in range(len(pops[_pop][_person]),0,-1):
                pops[_pop][_person][_month-1] = pops[_pop][_person][_month-1][:end_day.day]                
                for _day in range(len(pops[_pop][_person][_month-1]),0,-1):
                    (pops[_pop][_person][_month-1][_day-1]).append(end_day)#append(date_2_str(end_day))                
                    end_day = end_day - tdel
    return pops

##################################################
def date_2_str(_date):
    y=str(_date.year)
    m=str(_date.month)
    d=str(_date.month)
    if len(m)<2:
        m='0'+m    
    if len(d)<2:
        d='0'+d
    return y+m+d

def gen_random_time():
    h=str(np.random.randint(0,24))
    m=str(np.random.randint(0,60))
    s=str(np.random.randint(0,60))
    if len(m)<2:
        m='0'+m    
    if len(s)<2:
        s='0'+s
    _time = str(int(h+m+s))
    return _time

def data_2_mat(data,_id,_gender,_age):
    list_trx_type_name = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    list_term_type = [chr(i) for i in range(ord('K'), ord('Z') + 1)]

    _list = []
    list_data_1 = list(data[1])
    
    for _i in range(np.random.randint(0,5)):
        list_data_1.insert(np.random.choice(len(list_data_1)),0)
        
    tmp_list = list(data[0]) + list_data_1
    for _cnt,_el in enumerate(tmp_list):
        if _cnt<len(data[0]):
            _transfer_type = 0
            _trx_type = 10
        else:
            _transfer_type = 1
            if _el==0:
                _trx_type = 0
            else:                    
                _trx_type = np.random.randint(1,9)
                                
        _date = date_2_str(data[2])
        _time = gen_random_time()
        _trx_type_name = list_trx_type_name[_trx_type]    
        _term_id = np.random.randint(100,900)         
        _term_type = np.random.randint(0,10)
        _term_type_name = list_term_type[_term_type]
        _card_type = np.random.randint(0,6)
        _list.append((_id,_el,_date,_time,_trx_type,
                      _trx_type_name,_transfer_type,
                      _gender,_age,_term_id,_term_type,
                      _term_type_name,_card_type))   
    return _list

def pops_to_df(pops):
    _idxs = 0
    df_list = []
    for _pop in range(len(pops)):
        for _person in range(len(pops[_pop])):
            _id = _person + _idxs
            _gender = np.random.randint(0,2)
            _age = np.random.randint(18,80)
            for _month in range(len(pops[_pop][_person])):
                for _day in range(len(pops[_pop][_person][_month])):
                    tmp_data = pops[_pop][_person][_month][_day]
                    df_list.extend(data_2_mat(tmp_data,_id,_gender,_age))                
        _idxs += (_pop*100)

        
    cols_list = ['CARDIDHASH','TRANSACTIONAMOUNT',
                 'TRANSACTIONDATE','TRANSACTIONTIME',
                 'TRANSACTIONTYPE','TRANSACTIONTYPENAME',
                 'TRANSFER_TYPE','USERGENDER','USERAGE',
                 'TERMINALID','TERMINALTYPE','TERMINALTYPENAME',
                 'CARDTYPE',
                ]
    df = pd.DataFrame(df_list,columns=cols_list) 
    return df
#################################
def pops_to_historical_data(pops_list,_today = JalaliDate(year=1400,month=3,day=11)):
    pops = add_date_to_pops(pops_list,_today = _today)
    data = []
    _idxs = 0
    for _pop in pops:
        for _id,_person in enumerate(_pop):
            for _,_month in enumerate(_person):
                for _,_day in enumerate(_month):
                    sum_bes = _day[0].sum()
                    cnt_bes = 0 if sum_bes==0 else len(_day[0])
                    sum_bed = _day[1].sum()
                    cnt_bed = 0 if sum_bed==0 else len(_day[1])
                    _date = _day[2]
                    data.append(((_idxs+_id), sum_bes, cnt_bes, sum_bed, cnt_bed,_date))
        _idxs += len(_pop)
        
        
    ddict = {}
    for _d in data:
        if _d[0] in ddict:
            ddict[_d[0]].append(_d)
        else:
            ddict[_d[0]] = [_d]        
     
    data_frame = pops_to_df(pops)
    return data_frame,ddict
#####################################################	
def get_daily_data(ddict):
    data_daily = []
    data_daily_last = {}
    for _key,_val in ddict.items():
        data_daily.extend(_val[-90:])
        data_daily_last[_key]=_val[-1]
        
    return data_daily,data_daily_last

def get_weekly_data(ddict):
    data_weekly = []
    data_weekly_current = {}
    data_weekly_last = {}
    for _key,_val in ddict.items():
        _idx = len(_val)-1
        tmp_data_weekly = []
        for week_cnt in range(13):
            x = _val[_idx][5]
            tmp_vals = []
            end_date = x
            while x.weekday()!=0:
                tmp_vals.append(list(_val[_idx][1:-1]))
                _idx-=1
                x = _val[_idx][5]
            tmp_vals.append(list(_val[_idx][1:-1]))
            start_date = x
            _idx-=1
            tmp_sum = (_key,) + tuple(np.array(tmp_vals).sum(axis=0))+(start_date,end_date,)
            tmp_data_weekly.append(tmp_sum)

        if tmp_data_weekly[0][6].weekday()!=6:
            data_weekly_current[_key] = tmp_data_weekly[0]
            data_weekly_last[_key] = tmp_data_weekly[1]
            del tmp_data_weekly[0]
        else:
            data_weekly_current[_key] = [-1,-1,-1,-1,-1]
            data_weekly_last[_key] = tmp_data_weekly[0]
            del tmp_data_weekly[-1]
            
        data_weekly.extend(tmp_data_weekly[::-1])
        
    return data_weekly,data_weekly_current,data_weekly_last



def get_monthly_data(ddict):
    data_monthly = []
    data_monthly_current = {}
    data_monthly_last = {}
    tdel = datetime.timedelta(days=1)    
    for _key,_val in ddict.items():
        _idx = len(_val)-1
        tmp_data_monthly = []
        for month_cnt in range(7):
            x = _val[_idx][5]
            tmp_vals = []
            end_date = x
            while x.day!=1:
                tmp_vals.append(list(_val[_idx][1:-1]))
                _idx-=1
                x = _val[_idx][5]
            tmp_vals.append(list(_val[_idx][1:-1]))
            start_date = x
            _idx-=1
            tmp_sum = (_key,) + tuple(np.array(tmp_vals).sum(axis=0))+(start_date,end_date,)
            tmp_data_monthly.append(tmp_sum)

        if (tmp_data_monthly[0][6].month)==(tmp_data_monthly[0][6]+tdel).month:
            data_monthly_current[_key] = tmp_data_monthly[0]
            data_monthly_last[_key] = tmp_data_monthly[1]
            del tmp_data_monthly[0]
        else:
            data_monthly_current[_key] = [-1,-1,-1,-1,-1]
            data_monthly_last[_key] = tmp_data_monthly[0]
            del tmp_data_monthly[-1]
        data_monthly.extend(tmp_data_monthly[::-1])
        
    return data_monthly,data_monthly_current,data_monthly_last

#################################
def plot_data(data):
# data=data_daily
    x = np.array([_d[0] for _d in data])
    y = np.array([_d[1] for _d in data])
    plt.plot(x,y,'+')
    plt.pause(0.5)
    y = np.array([_d[2] for _d in data])
    plt.plot(x,y,'+')
    plt.pause(0.5)
    y = np.array([_d[3] for _d in data])
    plt.plot(x,y,'+')
    plt.pause(0.5)
    y = np.array([_d[4] for _d in data])
    plt.plot(x,y,'+')
#################################
def print_data(data_daily_current,data_daily_last,_dict):
    print('data_daily_current=>',data_daily_current)
    for _k,_v in _dict.items():
        _clr = 'blue'
        if 'DAILY' in _k:
            if (_k=='MAX_DAILY_INPUT_AMOUNT') and (data_daily_current[1]>_v):
                _clr = 'red'
            if (_k=='MAX_DAILY_INPUT_FREQ') and (data_daily_current[2]>_v):
                _clr = 'red' 
            if (_k=='MAX_DAILY_OUTPUT_AMOUNT') and (data_daily_current[3]>_v):
                _clr = 'red'                
            if (_k=='MAX_DAILY_OUTPUT_FREQ') and (data_daily_current[4]>_v):
                _clr = 'red'
                
            if (_k=='RATIO_DAILY_INPUT_AMOUNT') and (data_daily_last[1]>0):
                if (data_daily_current[1]/data_daily_last[1])>_v:            
                    _clr = 'red'
            if (_k=='RATIO_DAILY_INPUT_FREQ') and (data_daily_last[2]>0):
                if (data_daily_current[2]/data_daily_last[2])>_v:            
                    _clr = 'red' 
            if (_k=='RATIO_DAILY_OUTPUT_AMOUNT') and (data_daily_last[3]>0):
                if (data_daily_current[3]/data_daily_last[3])>_v:
                    _clr = 'red'                
            if (_k=='RATIO_DAILY_OUTPUT_FREQ') and ((data_daily_last[4]>0)):
                if (data_daily_current[4]/data_daily_last[4])>_v:
                    _clr = 'red'                
            print(colored(_k,_clr),':',colored(_v,_clr))
    # clear_output(wait=True)    