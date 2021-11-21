# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import alpaca_trade_api as tradeapi 
from rasa_sdk.events import SlotSet

API_KEY = 'PK00UD6CGM9H2Y8NFCZT'
API_SECRET = '6dAIEGalw7mYBqFYSIgAJXMvH88vzmk1DDoceHOc'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(
    base_url = APCA_API_BASE_URL,
    key_id = API_KEY,
    secret_key = API_SECRET
)

class ActionPortfolio(Action):

    def name(self) -> Text:
        return "action_portfolio"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        account = api.get_account()

        if account.trading_blocked:
            message = "Your account is restricted ffrom trading."

        else:
            mess = 'Your Trading account Number is: {}'.format(account.account_number)
            mess1 = 'Your portfolio Value is ${}'.format(account.portfolio_value)

            mess2 = '${} is available cash for trading.'.format(account.cash)
            mess3 = '${} is available as buying power.'.format(account.buying_power)

            total_stock = float(account.portfolio_value) - float(account.cash)
            mess4 = 'Total value of stock available in your porfolio is ${}'.format(total_stock)

            balance_change = float(account.equity) - float(account.last_equity)
            mess5 = f'Today portfolio balance changes: ${balance_change}'

            message = mess + '\n' + mess1 + '\n' + mess2 + '\n' + mess3 + '\n' + mess4 + '\n' + mess5

        dispatcher.utter_message(text=message)

        return []

class ActionTransaction(Action):

    def name(self) -> Text:
        return "action_last_trans"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = ''
        last = api.list_orders(status = 'all', limit = 5, direction = 'desc')
        for order in last:
            if order.order_type == 'limit':
                mess = 'Transacted At '+ str(order.submitted_at)+ ' '+ order.order_type.capitalize()+ ' order to '+ order.side + ' '+ str(order.qty) + ' stock of '
                +order.symbol + ' company'+ ' is '+ order.status + ' with limit price of $' + order.limit_price + '.'
            else:
                mess = 'Transacted At '+ str(order.submitted_at)+ ' '+ order.order_type.capitalize() + ' order to ' + order.side+ ' ' + str(order.qty) + ' stock of '
                + order.symbol + ' company is ' + order.status+'.'

            message = message + '\n' + mess
            
        dispatcher.utter_message(text= message)

        return []

class ActionSlots(Action):

    def name(self) -> Text:
        return "action_slots"

    def run(self, dispatcher,tracker,domain):
        ticker = tracker.get_slot("ticker")
        stock = api.get_barset(ticker, '15Min', limit = 1).df 
        x = stock[ticker]['close']

        return [SlotSet('last_price', float(x))]

class ActionStockBuy(Action):

    def name(self) -> Text:
        return "action_buy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        account = api.get_account()
        if account.trading_blocked:
            print("Account is currently restricted from trading.")

        ticker = tracker.get_slot('ticker')
        quantity = tracker.get_slot('quantity')
        order_type = tracker.get_slot("types")

        if order_type.lower() == 'limit':
            price = tracker.get_slot("price")
            order = api.submit_order(symbol = ticker, qty = quantity, side = 'buy', type = 'limit', limit_price = price, time_in_force = 'day')
            mess = order.order_type.capitalize() + ' order to '+ order.side + ' ' + str(order.qty)+ ' stock of ' + order.symbol + ' company is '+ order.status + ' with limit price of $'+order.limit_price +'.'

        else:
            order = api.submit_order(symbol = ticker, qty = quantity, side = 'buy', type='market', time_in_force = 'day')
            mess = order.order_type.capitalize() + ' order to '+order.side +' '+ str(order.qty) + ' stock of ' + order.symbol + ' company is ' + order.status + '.'

        balance_change = float(account.equity) - float(account.last_equity)
        message = mess + '\n' + "Your Portfolio value is ${}".format(account.portfolio_value) +'\n' + f'Today portfolio balance change: ${balance_change}'

        dispatcher.utter_message(text=message)

        return []
