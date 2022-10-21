from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.ATR import ATR
from smartcard.util import toHexString, toBytes

if __name__ == "__main__":
    cardtype = AnyCardType()
    cardrequest = CardRequest( cardType=cardtype )
    cardservice = cardrequest.waitforcard()
    cardservice.connection.connect()
    atr = ATR(toBytes(toHexString(cardservice.connection.getATR())))
    print(atr)
    print("Historical Bytes: " , toHexString(atr.getHistoricalBytes()))
    print(cardservice.connection.getReader())