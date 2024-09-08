import os
import threading
from dhanhq import dhanhq
import json


class fandoProject:
    def __init__(self,namesoftheaccountholder,connector, whattodo , qty):
        self.namesoftheaccountholder = namesoftheaccountholder
        self.dhan = connector
        self.whattodo = whattodo
        self.qty = qty
    
    def connected(self):
        if self.dhan:
            print(f" Connected to Account : {self.namesoftheaccountholder}")
            return True
        return False
    
    def CreateOrder(self):
        dhan = self.dhan
        # type of order
        if self.whattodo == "buy":
            if self.connected():
                try:
                    
                    
                    
                    
                    
                    result = dhan.place_order(
                        tag='Option Buy Order (Hedge)',
                        transaction_type=dhan.BUY,
                        exchange_segment=dhan.NSE_FNO,
                        product_type=dhan.CO,
                        order_type=dhan.MARKET,
                        validity='DAY',
                        security_id='23462',
                        quantity=self.qty,
                        disclosed_quantity=0,
                        price=0,
                        trigger_price=0,
                        after_market_order=False,
                        amo_time='OPEN',
                        bo_profit_value=0,
                        bo_stop_loss_Value=0,
                        drv_expiry_date=None,
                        drv_options_type=None,
                        drv_strike_price=None
                    )
                    # print(json.load(result))
                    
                    if result['status'] == 'failure':
                        # error_code = result['remarks'].get('error_code')
                        error_message = result['remarks'].get('message')
                        
                        # print(f"Error Code: {error_code}")
                        # print(f"Error Message: {error_message}")
                        print(f"Failed to create order for {self.namesoftheaccountholder} : {error_message}")
                    else:
                        print(f"Order Created for {self.namesoftheaccountholder}")
                        # print(result)
                    
                except Exception as Ex :
                    print(Ex)
                    # print("Something Gone Wrong with the code while creating the Order")
                
            else :
                print("Connection Failed : ", self.namesoftheaccountholder)
        elif self.whattodo == "sell":
            exit()
        
        else:
            print("Invalid Input (Buy or sell) : ", self.whattodo)

def Config_Data():
    """
        Open the config file and load all the data and send the config data
    """
    try:
        config_path = os.path.join(os.getcwd(), 'config.json')  # Using relative path
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            return config
    except Exception as e:
        print(f"Error loading config file: {e}")
        return None

def accountname():
    config = Config_Data()
    if config:
        noofaccountspecified = config["noofaccounts"]
        countingthenomberofaccount = len(config["accounts"])
        
        if noofaccountspecified == countingthenomberofaccount:
            print("Matched! No of accounts are:", noofaccountspecified)
        else:
            print("No of accounts Not Matched")
        
        for names in config["accounts"]:
            print(names["account_name"])
    else:
        print("Config data is missing")

# Function to run order in a separate thread
def run_order(account):
    account.CreateOrder()
    
if __name__=="__main__":
    
    print("                           Welcome to the Mahendar's Algo - Trader")
    
    print("Checking account Status : ")
    accountname()
    
    
    #Buy or sell from User
    print("Do you want to buy or sell",end="\t")
    typeoftransation = str(input()).lower()
    
    if typeoftransation not in ["buy", "sell"]:
        print("Invalid input. Please enter 'buy' or 'sell'.")
        exit()
    
    if typeoftransation == "buy":
        # Hedge Buy
        print("Put or Call : >>>",end="\t")
        typeofoptions = str(input()).lower()
        if typeoftransation not in ["put", "call"]:
            print("Invalid input. Please enter 'put' or 'call'.")
            exit()
        
        
        
        #Strike Price
        print("Enter The Strike Price of banknifty : >>>",end="\t")
        strike_price = int(input())
        
        
        print(f"Enter the qty Size in : >>>",end="\t")
        qty = int(input())
        if qty % 15 != 0:
            print(f" Qty Size is Wrong ")
        
    
        config = Config_Data()
        if config:
            threads = []
            for account_config in config['accounts']:
                dhan_account = dhanhq(account_config['account_id'], account_config['api_token'])
                project = fandoProject(
                    account_config["account_name"],
                    dhan_account,
                    typeoftransation,
                    1000
                )
                
                # Create thread for each account
                thread = threading.Thread(target=run_order, args=(project,))
                threads.append(thread)
                thread.start()
                
            # Join all threads to ensure they complete
            for thread in threads:
                thread.join()

            print("All Orders Processed In All Account")
        else:
            print("Wrong with config File")