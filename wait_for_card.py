from multiprocessing.forkserver import connect_to_new_process
from smartcard.CardRequest import CardRequest
from smartcard.CardConnection import CardConnection
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.CardType import AnyCardType
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard import util

def transmit(connection, apdu, purpose=None):
    if purpose == None:  
        purpose = "Data" 

    data, sw1, sw2 = connection.transmit(apdu)
    status = util.toHexString([sw1, sw2])
    data = util.toHexString(data)
    print("{}: {}\tStatus: {}".format(str(purpose), data, status))
    return data, sw1, sw2


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
data , sw1, sw2 = transmit(conn,[0xFF, 0xC2, 0x00, 0x01, 0x03, 0xFA, 0xFB, 0xFC],"Data")


