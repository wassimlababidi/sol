# Warning: Do NOT edit this file directly. Your changes may be overwritten. 
# This file is automatically generated by GenIpMgrSubscribe.py

import threading

from   SmartMeshSDK import ApiException

class IpMgrSubscribe(object):
    '''
    \brief Notification listener for IpMgrConnectorMux object
    '''
    
    class SubscribeError(Exception) :
        def __init__(self, msg) :
            self.msg = msg
        def __str__(self):
            return self.msg
    
    ERROR                = "error"
    FINISH               = "finish"
    NOTIFEVENT           = "notifEvent"
    NOTIFLOG             = "notifLog"
    NOTIFDATA            = "notifData"
    NOTIFIPDATA          = "notifIpData"
    NOTIFHEALTHREPORT    = "notifHealthReport"
    ALLNOTIF             = [NOTIFEVENT, NOTIFLOG, NOTIFDATA, NOTIFIPDATA, NOTIFHEALTHREPORT]
    EVENTMOTERESET       = "eventMoteReset"
    EVENTNETWORKRESET    = "eventNetworkReset"
    EVENTCOMMANDFINISHED = "eventCommandFinished"
    EVENTMOTEJOIN        = "eventMoteJoin"
    EVENTMOTEOPERATIONAL = "eventMoteOperational"
    EVENTMOTELOST        = "eventMoteLost"
    EVENTNETWORKTIME     = "eventNetworkTime"
    EVENTPINGRESPONSE    = "eventPingResponse"
    EVENTPATHCREATE      = "eventPathCreate"
    EVENTPATHDELETE      = "eventPathDelete"
    EVENTPACKETSENT      = "eventPacketSent"
    EVENTMOTECREATE      = "eventMoteCreate"
    EVENTMOTEDELETE      = "eventMoteDelete"

    _trNotifNameTable = {
    "eventMoteReset" : "notifEvent",
    "eventNetworkReset" : "notifEvent",
    "eventCommandFinished" : "notifEvent",
    "eventMoteJoin" : "notifEvent",
    "eventMoteOperational" : "notifEvent",
    "eventMoteLost" : "notifEvent",
    "eventNetworkTime" : "notifEvent",
    "eventPingResponse" : "notifEvent",
    "eventPathCreate" : "notifEvent",
    "eventPathDelete" : "notifEvent",
    "eventPacketSent" : "notifEvent",
    "eventMoteCreate" : "notifEvent",
    "eventMoteDelete" : "notifEvent",

    }
    
    #======================== public ==========================================
    
    def __init__(self, ipMgrConnector) :
        # Structure of self._callback :
        #     Notification Name : 
        #         [0] - subscription mask mask, 
        #         [1] - cb-function. Notification is subscribed if [1]!=None, 
        #         [2] - transport for notification: True - reliable, false - unreliable
        self._callback = {
            self.ERROR             : [0x00, None, True],
            self.FINISH            : [0x00, None, True],
            self.NOTIFEVENT        : [0x02, None, True],
            self.NOTIFLOG          : [0x04, None, True],
            self.NOTIFDATA         : [0x10, None, True],
            self.NOTIFIPDATA       : [0x20, None, True],
            self.NOTIFHEALTHREPORT : [0x40, None, True],
        
        }
        self._con    = ipMgrConnector
        self._thread = None
        self._mask = self._unrlblMask = 0
        self._isStarted = False
        self._lock = threading.Lock()
        
    def start(self):
        '''
        \brief Start the subscriber _thread.
        '''
        
        if self._thread :   # Wait finish disconnect process
            try :
                self._thread.join(1.0)
                if  self._thread.isAlive() :
                    raise ApiException.ConnectionError("Already connected")
            except RuntimeError :
                pass    # Ignore join error
            self._thread = None 
        
        # Clear _callback table
        for i in self._callback :
            self._callback[i][1] = None
            self._callback[i][2] = True
        self._mask = self._unrlblMask = 0
        self._thread = threading.Thread(target = self._process) 
        self._thread.name = "IpMgrSubscribe"
        self._thread.start()
        self._isStarted = True
        
    def subscribe(self, notifTypes, fun, isRlbl):
        '''
        \brief Subscribe to notification(s).
        
        Calling this function multiple times will not cancel the effects of
        the previous calls.
        
        \pre Call start() before calling this function.
        
        \param notifTypes Type(s) of notification(s) to subscribe to. This can
            be a single string (when subscribing to a single notification), or
            a list of strings (when subscribing to multiple notifications).
            The list of possible types is:
            ERROR, FINISH, NOTIFEVENT, NOTIFLOG, NOTIFDATA, NOTIFIPDATA, NOTIFHEALTHREPORT, ALLNOTIF

        \param fun The function to call when any of the notification types
            specified in the notifTypes parameter occurs. If you wish to assign
            a different _callback function to different notification types,
            call this function multiple times. The signature of the function
            needs to be fun(<notification name>, <notification parameter>),
            as described below.
        \param isRlbl define type of transport using for delivery 
             notification: reliable (True) or best effort (False)
        The _callback function is called with a notification name and a
        notification parameter. Depending on the type of notification, the
        parameter will be of a different format, according to the table below.
        
        <table>
            <tr><th>Notification Name   </th><th>Parameter</th>
            <tr><td>ERROR               </td><td>Exception</td>
            <tr><td>FINISH              </td><td>''</td>
            <tr><td>NOTIFLOG            </td><td>Tuple_notifLog</td>
            <tr><td>NOTIFDATA           </td><td>Tuple_notifData</td>
            <tr><td>NOTIFIPDATA         </td><td>Tuple_notifIpData</td>
            <tr><td>NOTIFHEALTHREPORT   </td><td>Tuple_notifHealthReport</td>
            <tr><td>EVENTMOTERESET      </td><td>Tuple_eventMoteReset</td>
            <tr><td>EVENTNETWORKRESET   </td><td>Tuple_eventNetworkReset</td>
            <tr><td>EVENTCOMMANDFINISHED</td><td>Tuple_eventCommandFinished</td>
            <tr><td>EVENTMOTEJOIN       </td><td>Tuple_eventMoteJoin</td>
            <tr><td>EVENTMOTEOPERATIONAL</td><td>Tuple_eventMoteOperational</td>
            <tr><td>EVENTMOTELOST       </td><td>Tuple_eventMoteLost</td>
            <tr><td>EVENTNETWORKTIME    </td><td>Tuple_eventNetworkTime</td>
            <tr><td>EVENTPINGRESPONSE   </td><td>Tuple_eventPingResponse</td>
            <tr><td>EVENTPATHCREATE     </td><td>Tuple_eventPathCreate</td>
            <tr><td>EVENTPATHDELETE     </td><td>Tuple_eventPathDelete</td>
            <tr><td>EVENTPACKETSENT     </td><td>Tuple_eventPacketSent</td>
            <tr><td>EVENTMOTECREATE     </td><td>Tuple_eventMoteCreate</td>
            <tr><td>EVENTMOTEDELETE     </td><td>Tuple_eventMoteDelete</td>
        </table>
        
        \exception IpMgrSubscribe.SubscribeError The subscriber hasn't been
            started, or the notification type(s) specified is (are) not valid.
        '''
        
        if not self._isStarted :
            raise self.SubscribeError("Error: subscriber is not started")
        if isinstance(notifTypes, str) :
            notifTypes = [notifTypes]
        for nType in notifTypes :  # subscribe type validation
            if nType not in self._callback :
                raise self.SubscribeError("Error subscribe type: {0}".format(nType))
        
        self._lock.acquire()
        for nType in notifTypes :
            self._callback[nType][1] = fun
            self._callback[nType][2] = isRlbl
        self._lock.release()
        
        mask = unrlblMask = 0
        # Structure of self._callback.values() :
        #     [0] - subscription mask mask, 
        #     [1] - cb-function. Notification is subscribed if [1]!=None, 
        #     [2] - transport for notification: True - reliable, false - unreliable
        for cb in self._callback.values() :
            if cb[1] :
                mask = mask | cb[0]
            if cb[2] == False :
                unrlblMask = unrlblMask | cb[0] 
        if mask != self._mask or unrlblMask != self._unrlblMask :
            self._mask = mask
            self._unrlblMask = unrlblMask
            self._con.dn_subscribe([0,self._mask], [0,self._unrlblMask])

    #======================== private =========================================
    
    def _process(self):
        while True :
            try :
                notif = self._con.getNotification()
                name = notif[0]
                if name in self._trNotifNameTable :
                    name = self._trNotifNameTable[name]
                self._processOneNotif(name, notif[0], notif[1])
            except ApiException.QueueError:
                self._processOneNotif(self.FINISH, self.FINISH, '')
                self._isStarted = False
                break
            except Exception as ex :
                self._processOneNotif(self.ERROR, self.ERROR, ex)
    
    def _processOneNotif(self, notifType, notifName, payload):
        cb = self._getCallback(notifType)
        if cb : 
            cb(notifName, payload)
    
    def _getCallback(self, name) :
        res = None

        self._lock.acquire()
        if name in self._callback :
            res = self._callback[name][1]
        self._lock.release()
        
        return res
