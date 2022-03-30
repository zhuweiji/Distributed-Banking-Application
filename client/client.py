from dataclasses import dataclass
from pathlib import Path
from enum import Enum

from pkg import config
from pkg.client.communication import SocketCommunicator
from pkg.comm.RPCmessages import *
from pkg.comm.request_types import *
from pkg.comm import marshalling
from pkg.comm.Currency import Currency


class Client:
    def __init__(self):
        self.comm = SocketCommunicator()

    def openBankAccount(self):
        print('Please input the following information to open an account')
        name = ClientUtils.askName()
        password = ClientUtils.askPassword()
        currency = ClientUtils.askCurrency()
        balance = ClientUtils.askAmount()

        request_type = OpenAccountRequest(name, password, currency, balance)
        RPC_request = RPCRequest(request_type)

        response = self.sendRequestToServer(RPC_request)
        if response:
            openAccountResponse = response.obj
            print("\n[Client] Thank you for opening up an account with us");          
            print("************************************************************");
            print("[Client] Your account number is : " + openAccountResponse.accountNumber);
            print("************************************************************");

    def runQueryService(self):
        print("Please input the following information to query from an account");
        accountNumber = ClientUtils.askAccountNumber()
        password = ClientUtils.askPassword()
    
        request_type = QueryAccountRequest(accountNumber, password)
        RPC_request = RPCRequest(request_type)

        resp = self.sendRequest(RPC_request)
        if resp:
            queryAccountResponse = resp.obj;
        
            if queryAccountResponse.success:
                print("\n[Client] Account detail as requested");
                print("************************************************************");
                print("[Client] Account is under     : " + queryResp.name);
                print("[Client] Account currency is  : " + queryResp.currency.toString());
                print("[Client] Account balance is   : " + String.valueOf(queryResp.balance));
                print("************************************************************");

            else:
                print("\n[Client] Error retrieving your account due to the following reason ");
                print("************************************************************");
                print("[Client] : " + queryResp.errorMessage);
                print("************************************************************");
            
    
    def runDepositService(self,transaction):
        print("Please input the following information to perform a " + transaction);
        accountNumber = ClientUtils.askAccountNumber()
        name = ClientUtils.askName()
        password = ClientUtils.askPassword()
        currency = ClientUtils.askCurrency()
        amount = ClientUtils.askAmount()
        
        request_type = DepositAccountRequest(name,accountNumber, password, currency, amount)
        RPC_request = RPCRequest(request_type)

        resp = self.sendRequest(RPC_request)
        if resp:
            DepositAccountResponse = resp.obj;
        
        if DepositAccountResponse.success:
            print("\n[Client] Transaction Successful. Detailed as followed: ");
            print("************************************************************");
            print("[Client] Account is under     : " + DepositResp.name);
            print("[Client] Account currency is  : " + DepositResp.currency.toString());
            print("[Client] Amount to %s is : %s", transaction, String.valueOf(DepositResp.amount));
            print("\n[Client] Account new balance is   : " + String.valueOf(DepositResp.balance));
            print("************************************************************");

        else:
            print("\n[Client] Error retrieving completing your deposit transaction due to the following reason ");
            print("************************************************************");
            print("[Client] : " + DepositResp.errorMessage);
            print("************************************************************");

    def runMonitorService(self):
        interval = ClientUtils.askInterval()        
        
        request_type = MonitorAccountRequest(config.SERVER_IP, config.CLIENT_PORT, interval)
        RPC_request = RPCRequest(request_type)

        resp = self.sendRequest(RPC_request)

        if resp:
            StatusResp = resp.obj;

        if StatusResp.success:
            print("[Client] Successfully requested to monitor, waiting for updates...");
            print("************************************************************");
            self.poll(interval);	
            print("************************************************************");
            print("[Client] Finished monitoring.");
        else:
            print("Failed to request to monitor");
    
    def runMaintenanceService(self):
        print("Please input the following information to pay the maintenance fee")
        accountNumber = ClientUtils.askAccountNumber()
        name = ClientUtils.askName()
        password = ClientUtils.askPassword()
       
        request_type = MaintenanceFeeAccountRequest(accountNumber, name, password)
        RPC_request = RPCRequest(request_type)

        resp = self.sendRequest(RPC_request)
        if resp:
            feeResp = resp.obj;
            if feeResp.success:
                print("************************************************************");
                print("[Client] Successfully pay maintenance fee, new balance = %f %s\n", feeResp.balance, feeResp.currency);
                print("************************************************************");
            else:
                print("************************************************************");
                print("[Client]Failed to pay maintenance fee with reason: %s\n", feeResp.errorMessage);
                print("************************************************************");

    
    def runCloseAccountService(self):
        print("Please input the following information to close an account");
        accountNumber = ClientUtils.askAccountNumber()
        name = ClientUtils.askName()
        password = ClientUtils.askPassword()

        request_type = CloseAccountRequest(name, password, accountNumber)        
        RPC_request = RPCRequest(request_type)

        resp = self.sendRequest(RPC_request)

        if resp:
            closeResp = resp.obj;
            if closeResp.success:
                print("************************************************************")
                print("Successfully closed bank account with number = %d\n", accountNumber);
                print("************************************************************")
            else:
                print("************************************************************")
                print("Failed to close bank account with reason: %s\n", closeResp.errorMessage);
                print("************************************************************")


class ClientUtils:
    def askName():
        return input("Your name = ");

    @classmethod
    def askPassword(cls):
        user_input = input(f"Your password ({config.PASSWORD_LENGTH} characters) = ");
        if (len(user_input) != config.PASSWORD_LENGTH):
            print(f"Password must have exactly {config.PASSWORD_LENGTH} characters!\n");
            return cls.askPassword();
        
        return user_input

    def askAccountNumber():
        return input("Your account number = ")
    
    @classmethod
    def askCurrency(cls):
        user_input = input(f"Your currency choice ({Currency.get_available()}) = ").upper()
        if user_input in Currency:
            return Currency.user_input
        else:
            print("Invalid Currency choice")
            return cls.askCurrency()

    @classmethod
    def askAmount(cls):
        user_input = input("Amount of money = ")
        try:
            user_input = int(user_input)
        except ValueError:
            print("Invalid amount")
            return cls.askAmount()

        if (user_input < 0):
            print("Amount cannot be negative!")
            return cls.askAmount()

        return user_input;

    @classmethod
    def askInterval(cls):
        user_input = input('Monitor Interval (s) = ')
        try:
            user_input = int(user_input)
        except ValueError:
            print("Invalid value")
            return cls.askInterval()




