## portfolio
* greet
  - utter_greet
* portfolio
  - action_portfolio
  - utter_end_greet

## transaction details
* greet
  - utter_greet
* last_trans
  - action_last_trans
  - utter_end_greet
  
## buy market
* greet
  - utter_greet
* trade
  - utter_trade
* buy
  - utter_buy_details
* buy_details
  - utter_order_type
* order_type_market
  - utter_details
  - action_buy
  - utter_end_greet

## buy limit
* greet
  - utter_greet
* trade
  - utter_trade
* buy
  - utter_buy_details
* buy_details
  - utter_order_type
* order_type_limit
  - action_slots
  - utter_limit_price
* limit_price
  - utter_details
  - action_buy
  - utter_end_greet

## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
