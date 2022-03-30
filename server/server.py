class Server:
    nextAvailableAccountNumber = 1
    db = Database()
    listeners = {}

    def __init__(self, server):
        self.server =  server

    def processOpenAccount(self, reqReceived):
        req = reqReceived.requestObj
        self.nextAvailableAccountNumber += 1
        accountNumber = nextAvailableAccountNumber

        self.db.store(accountNumber,  AccountDetail(req.name, req.password, req.currency, req.balance))
        self.server.sendToClient(ResponseMessage(reqReceived.id, reqReceived.method,Status.OK,  OpenAccountResponse(accountNumber)))
        self.broadcast(String.format("User %s opens  account with number %d", req.name, accountNumber))

    def queryAccount(self, reqReceived):
        req = reqReceived.requestObj
        accountDetail  = self.db.query(req.accountNumber)
        resp = None
        if not accountDetail:
            resp = QueryAccountResponse.failed("this account number doesn't exist")
        elif not (req.password == accountDetail.password):
            resp = QueryAccountResponse.failed("You've entered a Wrong password")
        else:
            resp =  QueryAccountResponse(accountDetail.name, accountDetail.currency, accountDetail.amount, true, "")
         
        self.server.sendToClient( ResponseMessage(reqReceived.id,reqReceived.method,Status.OK, resp))
        self.broadcast(String.format("Someone queries account %d", req.accountNumber))

    
    def processDeposit(self, reqReceived):
        req = reqReceived.requestObj
        resp = None
        
        accountDetail = self.db.query(req.accountNumber)
        if not accountDetail:
            resp = DepositAccountResponse.failed("self account number doesn't exist")
        elif not accountDetail.name == req.name:
            resp = DepositAccountResponse.failed("The account number is not under self name")
        elif not accountDetail.password == req.password: 
            resp = DepositAccountResponse.failed("Wrong password")
        elif accountDetail.currency != req.currency:
            resp = DepositAccountResponse.failed("The currency doesn't match")
        elif (accountDetail.amount + req.amount) < 0:
            resp = DepositAccountResponse.failed("There's not enough balance to withdraw")
        else:
            self.db.store(req.accountNumber, AccountDetail(accountDetail.name, accountDetail.password, accountDetail.currency, accountDetail.amount + req.amount))
            accountDetail = self.db.query(req.accountNumber)
            if (req.amount > 0):
                resp =  DepositAccountResponse(accountDetail.name,req.amount,accountDetail.currency,accountDetail.amount,true,"Deposit","")
                self.broadcast(String.format("User %s deposit %f %s to account %d", req.name, req.amount, req.currency, req.accountNumber))

             else:
                resp =  DepositAccountResponse(accountDetail.name,req.amount,accountDetail.currency,accountDetail.amount,true,"Withdraw","")
                self.broadcast(String.format("User %s withdraw %f %s from account %d", req.name, -req.amount, req.currency, req.accountNumber))
            
            self.server.sendToClient( ResponseMessage(reqReceived.id,reqReceived.method,Status.OK, resp))
        
    
    
    def processPayMaintenanceFee(self, reqReceived):
        req = reqReceived.requestObj
        resp = None
        
        accountDetail = self.db.query(req.accountNumber)
        if (accountDetail == None):
            resp =  MaintenanceFeeAccountResponse.failed("self account number doesn't exist")
        else:
            self.db.store(req.accountNumber,  AccountDetail(accountDetail.name, accountDetail.password, accountDetail.currency, accountDetail.amount * 0.99D))
            accountDetail = self.db.query(req.accountNumber)
            self.broadcast(String.format("User %s pays maintenance fee for account %d", req.name, req.accountNumber))
            resp =  MaintenanceFeeAccountResponse(accountDetail.currency, accountDetail.amount, true, "")
        
        self.server.sendToClient( ResponseMessage(reqReceived.id,reqReceived.method,Status.OK, resp))

    
    
    def processCloseAccount(self, reqReceived):
        req = reqReceived.requestObj
        resp = None
        
        accountDetail = self.db.query(req.accountNumber)
        if not accountDetail:
            resp = CloseAccountResponse.failed("self account number doesn't exist")
        elif accountDetail.name != req.name: 
            resp = CloseAccountResponse.failed("The account number is not under self name")
        elif accountDetail.password != (req.password):
            resp = CloseAccountResponse.failed("Wrong password")
        else:
            self.db.delete(req.accountNumber)
            self.broadcast(String.format("User %s deletes account with number %d", req.name, req.accountNumber))
            resp =  CloseAccountResponse(true, "")
        
        self.server.sendToClient( ResponseMessage(reqReceived.id,reqReceived.method,Status.OK, resp))

    

    
    def processMonitor(self, reqReceived):
        req = reqReceived.requestObj
        interval = req.interval
        self.listeners.put( InetSocketAddress(req.ipAddress, req.port), Instant.now().plusSeconds(interval))
        System.out.printf("User at %s with port %d starts to monitor for %d seconds\n", req.ipAddress,req.port,interval)
        resp =  MonitorAccountStatusResponse(true)
        self.server.sendToClient( ResponseMessage(reqReceived.id,reqReceived.method,Status.OK, resp))
    
    def broadcast(self, info): 
        self.purgeListeners()        
        self.listeners.forEach((socketAddress, x) -> 
            try 
                self.server.broadcastToRegisteredClients( ResponseMessage(UUID.randomUUID(),"MonitorAccount",Status.OK,  MonitorAccountResponse(info)), socketAddress)
             catch (IllegalAccessException e) 
                e.printStackTrace()
        )
    

    def purgeListeners(self):
        self.listeners.entrySet().removeIf((x) -> 
            return ((Instant)x.getValue()).isBefore(Instant.now())
        )
    
    
    

