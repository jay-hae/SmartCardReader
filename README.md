# SmartCardReader

# Problem
## Installation von Pyscard

* libpcscilte war nicht installiert
* wheel musste noch installiert werden

## Probleme bei Nutzung von Pyscard
* erst versuch scheitert mit:
    " raise EstablishContextException(hresult)
smartcard.pcsc.PCSCExceptions.EstablishContextException: Failed to establish context: Service not available. (0x8010001D) "
* aber Device wird mit lsusb erkannt
* Lösungs versuche:
* Installieren von PC/SC Drivers von https://www.acs.com.hk/en/products/403/acr1255u-j1-acs-secure-bluetooth%C2%AE-nfc-reader/
* dafür noch libusb mit "sudo apt-get install libusb-1.0-0-dev"
* -> hat auch nicht Funktioniert


