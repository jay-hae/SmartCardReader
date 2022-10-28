from multiprocessing.forkserver import connect_to_new_process
from smartcard.CardRequest import CardRequest
from smartcard.CardConnection import CardConnection
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.CardType import AnyCardType
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard import util

def printHexList(a):
    print(util.toHexString(a))

def printRespo(respo, purpose = None, note = ""):
    if purpose == None:  
        purpose = "Data" 
    if note != "":
        note = "Note: " + note 
    status = util.toHexString([respo[1],respo[2]])
    data = util.toHexString(respo[0])
    print("{}: {}\tStatus: {}\t{}".format(str(purpose), data, status, note))

def transmit(connection, apdu):
    return connection.transmit(apdu)


TIMEOUT = 10
SELECT = [0xFF, 0XCA, 00, 00 ] # get UID 
GET_RESPONSE = [0x00, 0xA4, 0x00, 0x00, 0x00]





# respond to the insertion of any type of smart card
card_type = AnyCardType()

# create the request. Wait for up to x (None) seconds for a card to be attached
request = CardRequest(timeout=TIMEOUT, cardType=card_type)
# listen for the card
service = None

try:
    service = request.waitforcard()
except CardRequestTimeoutException:
    print("ERROR: No card detected")
    exit(-1)

conn = service.connection 

#observer=ConsoleCardConnectionObserver()
#conn.addObserver( observer )
# when a card is attached, open a connection
conn.connect() 
#get_uid = util.toBytes("FF CA 00 00 00")
atr = util.toHexString(conn.getATR())
print("ATR: " + atr)
#data , sw1, sw2 = transmit(conn,[0xFF, 0xCA, 0x00, 0x00, 0x00],"UID")
#data , sw1, sw2 = transmit(conn,[0xFF, 0xCA, 0x00, 0x02, 0x00],"PICC Data", "Page 52") # not supported

#data , sw1, sw2 = transmit(conn,[0xFF, 0xC2, 0x00, 0x01, 0x02, 0x0A, 0x0B, 0x0C],"Data","Page 59") # warum geht es nur für eine Daten länge von 1 Byte? 
# Data: C0 03 01 63 00 ... 01 means error in 1. dataobject 63 00 means no information



# Manage Transparent Session
#data , sw1, sw2 = transmit(conn,[0xFF, 0xC2, 0x00, 0x00, 0x01, 0x80],note="Page 55") 

#Start Transparent Session
#data , sw1, sw2 = transmit(conn,[0xFF, 0xC2, 0x00, 0x00, 0x00, 0x81],note="Page 55") 
#data , sw1, sw2 = transmit(conn,[0xFF, 0xC2, 0x00, 0x00, 0x00, 0x82],note="Page 55") # end session


"""
conn is the connection
req_para is Hexstring in range from 01 to 0A 
Example: "01"
See Page 57 for more infroamtion
"""

def get_session_para(conn, req_para):
    cmd = [0xFF, 0xC2, 0x00, 0x00, 0x05, 0xFF, 0x6D, 0x02, 0x00, 0x00]
    cmd[8] = util.toBytes(req_para)[0]
    data , sw1, sw2 = transmit(conn,cmd) 
    return data , sw1, sw2
"""
Page 57
Request:
FF, C2, 00, 00, 05, FF, 6D, 02, 01, 00
                                    ^ len of TLV Value (here FSDI)
                                ^ Requested Parameter Tag from TLV
                            ^ len of TLV afterwards
                    ^ get Parameter Object (P 55)
                ^ len of Data afterwards
            ^ P2 
        ^ P1
    ^INS
^CLA (Class of Stream)

data , sw1, sw2 = transmit(conn,[0xFF, 0xC2, 0x00, 0x00, 0x05, 0xFF, 0x6D, 0x02, 0x01, 0x00]) 

Response: (P 53)
C0, 03, 00, 90, 00, FF, 6D, 03, 01, 01, 08
                                        ^ Information/Value
                                    ^ len of Value 
                                ^ Requested Parameter Tag from TLV
                            ^ len of Requested Response Object
                    ^ Requestet Parameter Object (P 55)
        ^ error Status description (P 53)
    ^ len of C0 data element Format
^ C0 data element Format
"""

#start transparent session
printRespo(  transmit(conn,[0xFF, 0xC2, 0x00, 0x00, 0x00, 0x81]))

printRespo( transmit(conn,[0xFF, 0xC2, 0x00, 0x01, 0x04, 0x90, 0x02, 0xB0, 0x00])) # Transmission and Reception Flag

# Transmit
data , sw1, sw2 = transmit(conn,[0xFF, 0xC2, 0x00, 0x01, 0x05, 0x93, 0x03, 0x01, 0x02, 0x03]) 

#Recive
data , sw1, sw2 = transmit(conn,[0xFF, 0xC2, 0x00, 0x01, 0x02, 0x94, 0x00]) 

# end transparent session
data , sw1, sw2 = transmit(conn,[0xFF, 0xC2, 0x00, 0x00, 0x00, 0x82]) # end session