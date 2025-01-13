import random
import webbrowser
import zipfile
import jdatetime
from datetime import date, datetime
import elasticsearch.helpers
import configparser
import requests
import os
import json
import numpy as np

from flask import Flask, request, redirect, url_for, render_template, jsonify, session
from TestCode_v8 import DateGenerationBase
from fuzzy_inference_simulator.fuzzy_inference import SimulatedFFI

config = configparser.ConfigParser()
config.read('cfg/config.cfg')

proxy = 'http://172.16.107.134:3128'
static_folder = './static'
# cache = Cache(config={'CACHE_TYPE':'redis'})
app = Flask(__name__)
app.config['CACHE_TYPE'] = "null"
# cache.init_app(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # add 18
app.secret_key = config.get('settings', 'secret_key')
app.config['MAX_CONTENT_LENGTH'] = int(config.get('settings', 'MAX_CONTENT_LENGTH'))
app.secret_key = config.get('settings', 'secret_key')
token = config.get('path', 'PODSPACE_TOKEN')
podspace_download_url = config.get('path', 'PODSPACE_DOWNLOAD_URL')
podspace_upload_url = config.get('path', 'PODSPACE_UPLOAD_URL')
upload_folder = config.get('path', 'UPLOAD_FOLDER')
upload_images = config.get('path', 'upload_images')
payload_filename = config.get('path', 'payload_filename')

DGB = DateGenerationBase()
ffi = SimulatedFFI()


# global dbg_s_u


@app.route('/')
def upload_form():
    # session['dbg_s_u_save'] = None
    session['dicts_info'] = []
    session['quantity_sum'] = 0
    return render_template('master_fraud_detection_V8.html', flag=False)


@app.route('/state_report', methods=['POST'])
def state_user_report():
    flag_user = True
    # session['dicts_info'] = []
    state_user = session.get('state_user', None)
    ############
    # state_user_pop_number = {'فروشگاه اینترنتی': 1, 'خرده فروش': 2, 'کارمند': 3, 'بیزینس من': 4}
    # data_daily_data, data_weekly_data, data_monthly_data, current_week, current_month, final_dict_data = DGB.date_generation_pop_number(
    #     pop_number=state_user_pop_number[state_user])
    data_daily_data, data_weekly_data, data_monthly_data, current_week, current_month, final_dict_data, current_day, list_daily, list_weekly, list_monthly = DGB.dbg_s_u[state_user]
    ############
    return render_template('print_result_V8.html', flag_user=flag_user, flag=False, state_user=state_user,
                           current_week=current_week, current_month=current_month, final_dict_data=final_dict_data,
                           current_day=current_day)


@app.route('/threshold_report', methods=['POST'])
def state_threshold_report():
    id_threshold = request.form['id']
    flag_user = True
    list_result = []
    state_user = session.get('state_user', None)
    ############
    data_daily_data, data_weekly_data, data_monthly_data, current_week, current_month, final_dict_data, current_day, list_daily, list_weekly, list_monthly = DGB.dbg_s_u[state_user]
    id_threshold_value = final_dict_data[id_threshold]
    id_threshold_split = id_threshold.split('_')
    if id_threshold_split[1] == 'DAILY':
        if id_threshold_split[2] == 'INPUT' and id_threshold_split[3] == 'FREQ':
            for i in list_daily:
                list_result.append(i[2])
        elif id_threshold_split[2] == 'INPUT' and id_threshold_split[3] == 'AMOUNT':
            for i in list_daily:
                list_result.append(i[1])
        elif id_threshold_split[2] == 'OUTPUT' and id_threshold_split[3] == 'FREQ':
            for i in list_daily:
                list_result.append(i[4])
        else:
            for i in list_daily:
                list_result.append(i[3])
    elif id_threshold_split[1] == 'WEEKLY':
        if id_threshold_split[2] == 'INPUT' and id_threshold_split[3] == 'FREQ':
            for i in list_weekly:
                list_result.append(i[2])
        elif id_threshold_split[2] == 'INPUT' and id_threshold_split[3] == 'AMOUNT':
            for i in list_weekly:
                list_result.append(i[1])
        elif id_threshold_split[2] == 'OUTPUT' and id_threshold_split[3] == 'FREQ':
            for i in list_weekly:
                list_result.append(i[4])
        else:
            for i in list_weekly:
                list_result.append(i[3])
    else:
        if id_threshold_split[2] == 'INPUT' and id_threshold_split[3] == 'FREQ':
            for i in list_monthly:
                list_result.append(i[2])
        elif id_threshold_split[2] == 'INPUT' and id_threshold_split[3] == 'AMOUNT':
            for i in list_monthly:
                list_result.append(i[1])
        elif id_threshold_split[2] == 'OUTPUT' and id_threshold_split[3] == 'FREQ':
            for i in list_monthly:
                list_result.append(i[4])
        else:
            for i in list_monthly:
                list_result.append(i[3])
    ############
    return render_template('print_threshold.html', flag_user=flag_user, flag=False, state_user=state_user,
                           final_dict_data=final_dict_data, id_threshold=id_threshold,
                           id_threshold_value=id_threshold_value, list_result=list_result,
                           state_dailty=id_threshold_split[1])


@app.route('/users2', methods=['POST'])
def user2():
    session['dbg_s_u_save'] = None
    flag_user = True
    state_user = 'فروشگاه اینترنتی'
    session['state_user'] = state_user
    session['dicts_info'] = []
    DGB.generate()
    return render_template('master_fraud_detection_V8.html', flag_user=flag_user, flag=False, state_user=state_user)


@app.route('/users3', methods=['POST'])
def user3():
    session['dbg_s_u_save'] = None
    flag_user = True
    state_user = 'خرده فروش'
    session['state_user'] = state_user
    session['dicts_info'] = []
    DGB.generate()
    return render_template('master_fraud_detection_V8.html', flag_user=flag_user, flag=False, state_user=state_user)


@app.route('/users4', methods=['POST'])
def user4():
    # session['dbg_s_u_save'] = None
    flag_user = True
    state_user = 'کارمند'
    session['state_user'] = state_user
    session['dicts_info'] = []
    DGB.generate()
    return render_template('master_fraud_detection_V8.html', flag_user=flag_user, flag=False, state_user=state_user)


@app.route('/users5', methods=['POST'])
def user5():
    session['dbg_s_u_save'] = None
    flag_user = True
    state_user = 'سازمان'
    session['state_user'] = state_user
    session['dicts_info'] = []
    DGB.generate()
    return render_template('master_fraud_detection_V8.html', flag_user=flag_user, flag=False, state_user=state_user)


@app.route('/report', methods=['POST'])
def add_report():
    flag_info = True
    err_price = False
    dict_info = []
    dicts_info = []
    pay = None
    quantity_sum = session.get('quantity_sum', None)
    # session['dicts_info'] = None
    try:
        quantity = int(request.form['id1'])
        quantity_sum += quantity
        pay = request.form['id2']

        if pay == '1':
            pay = "برداشت"
        elif pay == '2':
            pay = "واریز"
        # elif pay == '4':
        #     pay = "قسط"
        # elif pay == '5':
        #     pay = "برگشت"
        # elif pay == '6':
        #     pay = "کارت به کارت"

        price_from = int(request.form['id4'])
        price_to = int(request.form['id3'])
        # file_zip = request.files['file1']
    except:
        quantity_sum += 1
        quantity = 1
        if pay == '3':
            pay = "مانده گیری"
        # pay = "مانده گیری"
        price_to = 10000000
        # price_from = 1

    session['quantity_sum'] = quantity_sum
    if price_to < price_from:
        flag_info = True
        err_price = "شروع بازه نباید از انتهای بازه بیشتر باشد"
    try:
        dicts_info = session.get('dicts_info', None)
    except:
        pass
    if err_price != "شروع بازه نباید از انتهای بازه بیشتر باشد":
        rand_price = []
        if quantity == 1:
            rand_price.append(price_from)
        else:
            for i in range(quantity):
                rand_price.append(random.randint(price_from, price_to))
        ###########
        for rand_price_i in rand_price:
            # dbg_s_u = {'فروشگاه اینترنتی': None, 'خرده فروش': None, 'کارمند': None, 'بیزینس من': None}
            state_user = session.get('state_user', None)

            if str(pay) == "برداشت":
                TRANSACTIONTYPENAME = "Purchase"
            else:
                TRANSACTIONTYPENAME = "DepositRq"

            trx = {'USERIDHASH': 1, 'CARDIDHASH': '14768aaa42386ccc40f6fce8447875108bfc55c7',
                   'DEST_CARDIDHASH': '67a74306b06d0c01624fe0d0249a570f4d093747', 'TRANSACTIONDATE': '۱۳۹۹۰۵۲۰',
                   'TRANSACTIONTIME': '210910', 'TRANSACTIONAMOUNT': str(rand_price_i), 'TRANSACTIONTYPE': '۱۰',
                   'MERCHANTCATEGORYCODE': None, 'CARDTYPE': '۰', 'CARDISSUEBANK': '۵۰۲۲۲۹', 'LASTTRXTYPE': None,
                   'LASTSUCCESSFULTRXDATE': '۱۳۹۹۰۹۲۵', 'LASTSUCCESSFULTRXTYPE': None,
                   'FIRSTSUCCESSFULTRXDATE': '۱۳۹۳۱۱۲۶',
                   'FIRSTSUCCESSFULTRXTYPE': None, 'USERAGE': 0, 'USERGENDER': 30, 'TERMINALTYPE': '۱۴',
                   'BANKID': '۵۰۲۲۲۹',
                   'RECBANKID': '۵۸۱۶۷۲۱۲۱', 'TERMINALID': '۱۲۳', 'WORKINGDATE': '۱۳۹۹۰۵۲۰', 'PIN2_STATE': '۱',
                   'PIN2_VALIDATION_TYPE': 'رمز پویا', 'TRANSACTIONID': '۲۳۹۴۲۳۷۳۱۶۱',
                   'TRANSACTIONTYPENAME': TRANSACTIONTYPENAME,
                   'TERMINALTYPENAME': 'پایانه فروش', 'IS_FRAUD': '۰', 'LIST_DETECT': 'WL', 'TRANSFER_TYPE': str(pay),
                   'correlation-id': 'alaki'}
            bhv = {
                'weekly': {'CM_BED_1_2_0': DGB.dbg_s_u[state_user][3]['sum_cnt_bed'],
                           'CM_BES_1_2_0': DGB.dbg_s_u[state_user][3]['sum_cnt_bes'],
                           'SM_BED_1_2_0': DGB.dbg_s_u[state_user][3]['sum_amt_bed'],
                           'SM_BES_1_2_0': DGB.dbg_s_u[state_user][3]['sum_amt_bes']},
                'threshold': {'RDIF': DGB.dbg_s_u[state_user][5]['RATIO_DAILY_INPUT_FREQ'],
                              'RDIA': DGB.dbg_s_u[state_user][5]['RATIO_DAILY_INPUT_AMOUNT'],
                              'MDIF': DGB.dbg_s_u[state_user][5]['MAX_DAILY_INPUT_FREQ'],
                              'MDIA': DGB.dbg_s_u[state_user][5]['MAX_DAILY_INPUT_AMOUNT'],
                              # 'RDTA': DGB.dbg_s_u[state_user][5]['RATIO_DAILY_TURNOVER_AMOUNT'],
                              # 'MDTA': DGB.dbg_s_u[state_user][5]['MAX_DAILY_TURNOVER_AMOUNT'],
                              # 'ATDA': DGB.dbg_s_u[state_user][5]['MAX_DAILY_TURNOVER_AMOUNT'],
                              'RDOF': DGB.dbg_s_u[state_user][5]['RATIO_DAILY_OUTPUT_FREQ'],
                              'RDOA': DGB.dbg_s_u[state_user][5]['RATIO_DAILY_OUTPUT_AMOUNT'],
                              'MDOF': DGB.dbg_s_u[state_user][5]['MAX_DAILY_OUTPUT_FREQ'],
                              'MDOA': DGB.dbg_s_u[state_user][5]['MAX_DAILY_OUTPUT_AMOUNT'],
                              'RWIF': DGB.dbg_s_u[state_user][5]['RATIO_WEEKLY_INPUT_FREQ'],
                              'RWIA': DGB.dbg_s_u[state_user][5]['RATIO_WEEKLY_INPUT_AMOUNT'],
                              'MWIF': DGB.dbg_s_u[state_user][5]['MAX_WEEKLY_INPUT_FREQ'],
                              'MWIA': DGB.dbg_s_u[state_user][5]['MAX_WEEKLY_INPUT_AMOUNT'],
                              # 'RWTA': DGB.dbg_s_u[state_user][5]['RATIO_WEEKLY_TURNOVER_AMOUNT'],
                              # 'MWTA': DGB.dbg_s_u[state_user][5]['MAX_WEEKLY_TURNOVER_AMOUNT'],
                              'RWOF': DGB.dbg_s_u[state_user][5]['RATIO_WEEKLY_OUTPUT_FREQ'],
                              'RWOA': DGB.dbg_s_u[state_user][5]['RATIO_WEEKLY_OUTPUT_AMOUNT'],
                              'MWOF': DGB.dbg_s_u[state_user][5]['MAX_WEEKLY_OUTPUT_FREQ'],
                              'MWOA': DGB.dbg_s_u[state_user][5]['MAX_WEEKLY_OUTPUT_AMOUNT'],
                              # 'RMIF': DGB.dbg_s_u[state_user][5]['MAX_DAILY_TURNOVER_AMOUNT'],
                              'RMIA': DGB.dbg_s_u[state_user][5]['RATIO_MONTHLY_INPUT_AMOUNT'],
                              'MMIF': DGB.dbg_s_u[state_user][5]['MAX_MONTHLY_INPUT_FREQ'],
                              'MMIA': DGB.dbg_s_u[state_user][5]['MAX_MONTHLY_INPUT_AMOUNT'],
                              # 'RMTA': DGB.dbg_s_u[state_user][5]['RATIO_MONTHLY_TURNOVER_AMOUNT'],
                              # 'MMTA': DGB.dbg_s_u[state_user][5]['MAX_MONTHLY_TURNOVER_AMOUNT'],
                              'RMOF': DGB.dbg_s_u[state_user][5]['RATIO_MONTHLY_OUTPUT_FREQ'],
                              'RMOA': DGB.dbg_s_u[state_user][5]['RATIO_MONTHLY_OUTPUT_AMOUNT'],
                              'MMOF': DGB.dbg_s_u[state_user][5]['MAX_MONTHLY_OUTPUT_FREQ'],
                              'MMOA': DGB.dbg_s_u[state_user][5]['MAX_MONTHLY_OUTPUT_AMOUNT']},
                # CM_BED_1_2_0=COUNT_BEDEHKAR_CURRENT_MONTH
                # CM_BES_1_2_0=COUNT_BESTANKAR_CURRENT_MONTH
                # SM_BED_1_2_0=AMOUNT_BEDEHKAR_CURRENT_MONTH
                # SM_BES_1_2_0=AMOUNT_BESTANKAR_CURRENT_MONTH
                'monthly': {'CM_BED_1_2_0': DGB.dbg_s_u[state_user][4]['sum_cnt_bed'],
                            'CM_BES_1_2_0': DGB.dbg_s_u[state_user][4]['sum_cnt_bes'],
                            'SM_BED_1_2_0': DGB.dbg_s_u[state_user][4]['sum_amt_bed'],
                            'SM_BES_1_2_0': DGB.dbg_s_u[state_user][4]['sum_amt_bes']},
                'daily': {'CM_BED_1_2_0': DGB.dbg_s_u[state_user][6]['sum_cnt_bed'],
                          'CM_BES_1_2_0': DGB.dbg_s_u[state_user][6]['sum_cnt_bes'],
                          'SM_BED_1_2_0': DGB.dbg_s_u[state_user][6]['sum_amt_bed'],
                          'SM_BES_1_2_0': DGB.dbg_s_u[state_user][6]['sum_amt_bes']},
                'today': {'PURCHASE_AVG': 242000.0, 'WITHDRAWAL_SUM': 242000, 'WITHDRAWAL_CNT': 1,
                          'PURCHASE_SUM': 242000, 'PURCHASE_CNT': 1, 'WITHDRAWAL_AVG': 242000.0}}
            result = ffi.simulated_fuzzy_inference(trx, bhv)
            ########################################################
            # state_user_pop_number = {'فروشگاه اینترنتی': int(1), 'خرده فروش': int(2), 'کارمند': int(3), 'بیزینس من': int(4)}
            # pop_number = state_user_pop_number[state_user]
            # dbg_s_u[state_user] = DGB.date_generation_pop_number(pop_number)  # with list
            # data_daily_data, data_weekly_data, data_monthly_data, current_week, current_month, final_dict_data = dbg_s_u
            # states = {'data_daily_data': None, 'data_weekly_data': None, 'data_monthly_data': None, 'current_week': None,
            #           'current_month': None, 'final_dict_data': None}
            if pay == "برداشت":  # 3WEEKLY,4MONTHLY,6DAILY
                DGB.dbg_s_u[state_user][3].update(
                    {'sum_amt_bed': float(DGB.dbg_s_u[state_user][3]['sum_amt_bed'] + rand_price_i),
                     'sum_cnt_bed': int(DGB.dbg_s_u[state_user][3]['sum_cnt_bed'] + 1)})
                DGB.dbg_s_u[state_user][4].update(
                    {'sum_amt_bed': float(DGB.dbg_s_u[state_user][4]['sum_amt_bed'] + rand_price_i),
                     'sum_cnt_bed': int(DGB.dbg_s_u[state_user][4]['sum_cnt_bed'] + 1)})
                DGB.dbg_s_u[state_user][6].update(
                    {'sum_amt_bed': float(DGB.dbg_s_u[state_user][6]['sum_amt_bed'] + rand_price_i),
                     'sum_cnt_bed': int(DGB.dbg_s_u[state_user][6]['sum_cnt_bed'] + 1)})
            elif pay == "واریز":
                DGB.dbg_s_u[state_user][3].update(
                    {'sum_amt_bes': float(DGB.dbg_s_u[state_user][3]['sum_amt_bes'] + rand_price_i),
                     'sum_cnt_bes': int(DGB.dbg_s_u[state_user][3]['sum_cnt_bes'] + 1)})
                DGB.dbg_s_u[state_user][4].update(
                    {'sum_amt_bes': float(DGB.dbg_s_u[state_user][4]['sum_amt_bes'] + rand_price_i),
                     'sum_cnt_bes': int(DGB.dbg_s_u[state_user][4]['sum_cnt_bes'] + 1)})
                DGB.dbg_s_u[state_user][6].update(
                    {'sum_amt_bes': float(DGB.dbg_s_u[state_user][6]['sum_amt_bes'] + rand_price_i),
                     'sum_cnt_bes': int(DGB.dbg_s_u[state_user][6]['sum_cnt_bes'] + 1)})
            # session['dbg_s_u_save'] = dbg_s_u
            ############
            dict_info.append({"kind": result, "role": rand_price_i, "exp": pay, "status": result == 'no fired rule'})
            ############
        if dicts_info == None:
            dicts_info = []
        for i in dict_info[:quantity]:
            dicts_info.append(i)
        session['dicts_info'] = dicts_info

    output_message = dicts_info
    return render_template('master_fraud_detection_V8.html', flag_user=True, output_message=output_message,
                           flag_info=flag_info, err_price=err_price, pay=pay, quantity_sum=quantity_sum, flag=False)


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port='5006', threaded=False)
