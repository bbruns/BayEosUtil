import xmlrpclib, base64, datetime

class BayEosClient(object):
    """simple client for BayEOS XML-RPC API, you proxy member of calling API-functions"""
    measureValState = 0

    def __init__(self, serverUri = "", userName = "", secret = ""):
        self.isConnected = False
        self.serverUri = serverUri
        self.userName = userName
        self.secret = secret
        self.proxy = xmlrpclib.ServerProxy(uri=serverUri, use_datetime=True, verbose=False)


    def connect(self):
        loginVec = self.proxy.LoginHandler.createSession(self.userName, self.secret)
        authHeaderBase64 = base64.b64encode(str(loginVec[0]) + ":" + str(loginVec[1]))

        class SpecialTransport(xmlrpclib.Transport):
            accept_gzip_encoding = False
            def send_host(self, connection, headers):
                connection.putheader("Authentication", authHeaderBase64)
            
        self.proxy = xmlrpclib.ServerProxy(uri=self.serverUri, use_datetime=True, verbose=False, transport=SpecialTransport())
        self.isConnected = True

    def addSingleValue(self, id, measureTime, measureVal):
        importOk = False
        if self.isConnected:
            importOk = self.proxy.MassenTableHandler.addRow(id, measureTime, measureVal, BayEosClient.measureValState)

        return importOk

    def disconnect(self):
         loggedOut = self.proxy.LogOffHandler.terminateSession()
         if loggedOut:
             self.isConnected = False
