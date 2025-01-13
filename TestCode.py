import time

from simulation.Data_Generation import Data_Generation


class DateGenerationBase:
    def __init__(self):
        self.simulated_data = Data_Generation()
        self.current_week_data = []
        self.data_daily_data = []
        self.data_weekly_data = []
        self.data_monthly_data = []
        self.data_monthly_current = []
        self.current_month_data = []
        self.dbg_s_u = {}

        # for pop_number, state_user in zip([1, 2, 3, 4], ['فروشگاه اینترنتی', 'خرده فروش', 'کارمند', 'سازمان']):
        for pop_number, state_user in zip([1, 2, 3, 4], ['کارمند', 'خرده فروش', 'سازمان', 'فروشگاه اینترنتی']):
            self._data = self.simulated_data.get_random_sample(pop_number)  # pop_number=4

            # final_dict = _data[1]
            # data_daily = _data[2]
            # data_daily_last = _data[4]
            # data_weekly = _data[7]
            # data_weekly_current = _data[8]

            self.final_dict_data = self._data[1]

            for i in self._data[2]:
                data_daily = {'sum_amt_bes': i[1], 'sum_cnt_bes': i[2], 'sum_amt_bed': i[3], 'sum_cnt_bed': i[4]}
                self.data_daily_data.append(data_daily)
                print(i)

            for i in self._data[4]:
                data_weekly = {'sum_amt_bes': i[1], 'sum_cnt_bes': i[2], 'sum_amt_bed': i[3], 'sum_cnt_bed': i[4]}
                self.data_weekly_data.append(data_weekly)
                print(i)

            for i in self._data[7]:
                data_monthly = {'sum_amt_bes': i[1], 'sum_cnt_bes': i[2], 'sum_amt_bed': i[3], 'sum_cnt_bed': i[4]}
                self.data_monthly_data.append(data_monthly)
                print(i)

            self.current_day = {'sum_amt_bes': 0, 'sum_cnt_bes': 0, 'sum_amt_bed': 0, 'sum_cnt_bed': 0}
            self.current_week = {'sum_amt_bes': self._data[5][1], 'sum_cnt_bes': self._data[5][2],
                                 'sum_amt_bed': self._data[5][3], 'sum_cnt_bed': self._data[5][4]}
            self.current_month = {'sum_amt_bes': self._data[8][1], 'sum_cnt_bes': self._data[8][2],
                                  'sum_amt_bed': self._data[8][3], 'sum_cnt_bed': self._data[8][4]}
            self.list_daily = self._data[2]
            self.list_weekly = self._data[4]
            self.list_monthly = self._data[7]
            print("pop_number:", pop_number, " ", "Done")

            self.dbg_s_u[state_user] = self.data_daily_data, self.data_weekly_data, self.data_monthly_data, \
                                       self.current_week, self.current_month, self.final_dict_data, self.current_day, \
                                       self.list_daily, self.list_weekly, self.list_monthly
        print("Done")

    def generate(self):
        self.current_week_data = []
        self.data_daily_data = []
        self.data_weekly_data = []
        self.data_monthly_data = []
        self.data_monthly_current = []
        self.current_month_data = []
        self.dbg_s_u = {}

        # for pop_number, state_user in zip([1, 2, 3, 4], ['فروشگاه اینترنتی', 'خرده فروش', 'کارمند', 'سازمان']):
        for pop_number, state_user in zip([1, 2, 3, 4], ['کارمند', 'خرده فروش', 'سازمان', 'فروشگاه اینترنتی']):
            self._data = self.simulated_data.get_random_sample(pop_number)  # pop_number=4

            # final_dict = _data[1]
            # data_daily = _data[2]
            # data_daily_last = _data[4]
            # data_weekly = _data[7]
            # data_weekly_current = _data[8]

            self.final_dict_data = self._data[1]

            for i in self._data[2]:
                data_daily = {'sum_amt_bes': i[1], 'sum_cnt_bes': i[2], 'sum_amt_bed': i[3], 'sum_cnt_bed': i[4]}
                self.data_daily_data.append(data_daily)
                print(i)

            for i in self._data[4]:
                data_weekly = {'sum_amt_bes': i[1], 'sum_cnt_bes': i[2], 'sum_amt_bed': i[3], 'sum_cnt_bed': i[4]}
                self.data_weekly_data.append(data_weekly)
                print(i)

            for i in self._data[7]:
                data_monthly = {'sum_amt_bes': i[1], 'sum_cnt_bes': i[2], 'sum_amt_bed': i[3], 'sum_cnt_bed': i[4]}
                self.data_monthly_data.append(data_monthly)
                print(i)

            self.current_day = {'sum_amt_bes': 0, 'sum_cnt_bes': 0, 'sum_amt_bed': 0, 'sum_cnt_bed': 0}
            self.current_week = {'sum_amt_bes': self._data[5][1], 'sum_cnt_bes': self._data[5][2],
                                 'sum_amt_bed': self._data[5][3], 'sum_cnt_bed': self._data[5][4]}
            self.current_month = {'sum_amt_bes': self._data[8][1], 'sum_cnt_bes': self._data[8][2],
                                  'sum_amt_bed': self._data[8][3], 'sum_cnt_bed': self._data[8][4]}
            self.list_daily = self._data[2]
            self.list_weekly = self._data[4]
            self.list_monthly = self._data[7]
            print("pop_number:", pop_number, " ", "Done")

            self.dbg_s_u[state_user] = self.data_daily_data, self.data_weekly_data, self.data_monthly_data, \
                                       self.current_week, self.current_month, self.final_dict_data, self.current_day, \
                                       self.list_daily, self.list_weekly, self.list_monthly
        print("Done")

    # def date_generation_pop_number(self, pop_number):
    #     self._data = self.simulated_data.get_random_sample(pop_number)  # pop_number=4
    #
    #     # final_dict = _data[1]
    #     # data_daily = _data[2]
    #     # data_daily_last = _data[4]
    #     # data_weekly = _data[7]
    #     # data_weekly_current = _data[8]
    #
    #     self.final_dict_data = self._data[1]
    #
    #     for i in self._data[2]:
    #         data_daily = {'sum_amt_bes': i[1], 'sum_cnt_bes': i[2], 'sum_amt_bed': i[3], 'sum_cnt_bed': i[4]}
    #         self.data_daily_data.append(data_daily)
    #         print(i)
    #
    #     for i in self._data[4]:
    #         data_weekly = {'sum_amt_bes': i[1], 'sum_cnt_bes': i[2], 'sum_amt_bed': i[3], 'sum_cnt_bed': i[4]}
    #         self.data_weekly_data.append(data_weekly)
    #         print(i)
    #
    #     for i in self._data[7]:
    #         data_monthly = {'sum_amt_bes': i[1], 'sum_cnt_bes': i[2], 'sum_amt_bed': i[3], 'sum_cnt_bed': i[4]}
    #         self.data_monthly_data.append(data_monthly)
    #         print(i)
    #
    #     self.current_week = {'sum_amt_bes': self._data[5][1], 'sum_cnt_bes': self._data[5][2],
    #                     'sum_amt_bed': self._data[5][3], 'sum_cnt_bed': self._data[5][4]}
    #     self.current_month = {'sum_amt_bes': self._data[8][1], 'sum_cnt_bes': self._data[8][2],
    #                      'sum_amt_bed': self._data[8][3], 'sum_cnt_bed': self._data[8][4]}
    #     print("pop_number:", pop_number, " ", "Done")
    #     return self.data_daily_data, self.data_weekly_data, self.data_monthly_data, self.current_week, \
    #            self.current_month, self.final_dict_data

    ###########
    # state_user = session.get('state_user', None)
    # dbg_s_u = session.get('dbg_s_u_save', None)
    # state_user_pop_number = {'فروشگاه اینترنتی': int(1), 'خرده فروش': int(2), 'کارمند': int(3), 'بیزینس من': int(4)}
    # if dbg_s_u is None:
    #     pop_number = state_user_pop_number[state_user]
    #     dbg_s_u[] = DGB.date_generation_pop_number(pop_number)  # with list
    #     # dbg_s_u[state_user] = DGB.date_generation_pop_number(pop_number) # with list?
    #     # data_daily_data, data_weekly_data, data_monthly_data, current_week, current_month, final_dict_data = dbg_s_u
    #     # states = {'data_daily_data': None, 'data_weekly_data': None, 'data_monthly_data': None, 'current_week': None,
    #     #           'current_month': None, 'final_dict_data': None}
    # if pay == "برداشت":
    #     dbg_s_u[3].update(
    #         {'sum_amt_bed': float(dbg_s_u[3]['sum_amt_bed'] + rand_price),
    #          'sum_cnt_bed': int(dbg_s_u[3]['sum_cnt_bed'] + quantity)})
    #     dbg_s_u[4].update(
    #         {'sum_amt_bed': float(dbg_s_u[4]['sum_amt_bed'] + rand_price),
    #          'sum_cnt_bed': int(dbg_s_u[4]['sum_cnt_bed'] + quantity)})
    # #          'sum_cnt_bed': int(dbg_s_u[state_user][4]['sum_cnt_bed'] + quantity)})
    # elif pay == "واریز":
    #     dbg_s_u[3].update(
    #         {'sum_amt_bes': float(dbg_s_u[3]['sum_amt_bes'] + rand_price),
    #          'sum_cnt_bes': int(dbg_s_u[3]['sum_cnt_bes'] + quantity)})
    #     dbg_s_u[4].update(
    #         {'sum_amt_bes': float(dbg_s_u[4]['sum_amt_bes'] + rand_price),
    #          'sum_cnt_bes': int(dbg_s_u[4]['sum_cnt_bes'] + quantity)})
    # session['dbg_s_u_save'] = dbg_s_u
    ############

    # the results:
    # _data = (   card_id, => 0
    #             final_dict[card_id], => 1 # final_dict
    #             data_daily[card_id], => 2 # a list of dictionary with values
    # sum_amt_bes  bes=variz
    # sum_cnt_bes  cnt=tedad
    # sum_amt_bed  bed=bardasht amt=meghdar
    # sum_cnt_bedbbbbbbbbb
    #             data_daily_last[card_id], => 3
    #             data_weekly[card_id], => 4 #
    #             data_weekly_current[card_id], => 5 # current week
    # update values for all values
    #             data_weekly_last[card_id], => 6
    #             data_monthly[card_id], => 7 # a list of dictionary monthly

    #             data_monthly_current[card_id], => 8 #
    # update values for all values
    #             data_monthly_last[card_id],   => 9
    #             )

    # build a new dict with 4 key default 0   float32
    # UI
    # combobox 2 item variz va bardasht be hesab
    # tedad 1 faghat az