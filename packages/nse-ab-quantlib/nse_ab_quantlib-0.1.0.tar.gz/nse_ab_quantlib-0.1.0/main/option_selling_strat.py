import logging

import nsepython

from alphatools.backtesting_app import BackTestingApp
from datetime import datetime
from alphatools.utils.token_manager import TokenManager

import instruments


class OptionSellingStratApp(BackTestingApp):
    watch_token = 0
    token_mgr = None
    acquired = False

    def on_md(self, data_row):
        # your strat code goes here
        print("New row found: {}".format(data_row))
        token = data_row['token']
        if token != self.watch_token:
            return

        curr_strike = data_row['ltp']
        self._acquire_positions(curr_strike)

    def _acquire_positions(self, curr_underlying_ltp, distance):
        # TODO Define conditions for rollover
        curr_strike = instruments.round_to_base(curr_underlying_ltp, 50)
        need_to_rollover = self.curr_base_strike != curr_strike
        if need_to_rollover:
            self._squareOffCurrentPositions()
            self.acquired = False

        if not self.acquired:
            # TODO Replace instruments with token numbers
            call_to_acquire = self.token_mgr.get_opt(self.symbol, self.expiry, curr_strike + distance, "CE")
            put_to_acquire = self.token_mgr.get_opt(self.symbol, self.expiry, curr_strike - distance, "PE")
            self.trade(call_to_acquire['token'], 10)
            self.trade(put_to_acquire['token'], 10)
            self.acquired = True
            self.curr_base_strike = curr_strike

    def _subscribe_instruments(self, symbol='NIFTY'):
        self.token_mgr = TokenManager()
        curr_weekly_exp = instruments.get_kth_expiry(symbol)
        curr_monthly_exp = instruments.get_kth_expiry(symbol, type=instruments.ExpiryType.MONTHLY)
        future_info = self.token_mgr.get_fut(symbol, curr_monthly_exp)
        # subscribe to future
        self.add_instrument(future_info['token'], future_info['exch_seg'])
        self.watch_token = future_info['token']

        # subscribe to options with strikes
        for strike in range(16700, 18900, 50):
            ce_info = self.token_mgr.get_opt(symbol, curr_weekly_exp, strike, 'CE')
            pe_info = self.token_mgr.get_opt(symbol, curr_weekly_exp, strike, 'PE')
            self.add_instrument(ce_info['token'], ce_info['exch_seg'])
            self.add_instrument(pe_info['token'], pe_info['exch_seg'])

    def _set_universe(self):
        """
        Include all NIFTY Options with strikes in 16000 to 18000 with intervals and

        :return:
        """
        # self.add_instrument(, )
        self.set_start_date(datetime.strptime('2023-02-01 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        self.set_end_date(datetime.strptime('2023-02-08 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        self._subscribe_instruments()
        self.set_interval('ONE_MINUTE')

    def __init__(self, config_file):
        self.logger.setLevel(logging.INFO)
        super().__init__(config_file)
        self._set_universe()
        self.load_data()  # Loads the data into a dataframe

    def simulate(self, start=0):
        super().simulate(start=start)
        pass

    def _squareOffCurrentPositions(self):
        # TODO Add logic for squaring off current positions
        for token in self.pnl_calculator.instrument_pnl_calculators.keys():
            inst_pnl_info = self.pnl_calculator.instrument_pnl_calculators[token]
            net_position = inst_pnl_info.total_sell_qty - inst_pnl_info.total_buy_qty
            self.trade(token, -net_position)

    def post_simulation(self):
        self._squareOffCurrentPositions()
        self.logger.info(self.get_total_pnl())


if __name__ == '__main__':
    app = OptionSellingStratApp('/Users/jaskiratsingh/projects/smart-api-creds.ini')
    app.simulate()