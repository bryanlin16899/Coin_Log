import requests
from .models import Website_users
from datetime import datetime
from binance import Client
from binance.exceptions import BinanceAPIException
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

COIN_GECKO_URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false'
RQST_FROM_GECKO = requests.get(url=COIN_GECKO_URL).json()
print(len(RQST_FROM_GECKO))


class GetUserInfo:
    def __init__(self):
        self.api_key = None
        self.secret_key = None

    def get_trades_info(self, symbol='BTCUSDT'):
        client = Client(self.api_key, self.secret_key)
        this_coin = {
            'new_trade': {},
            'profit': 0,
            'totle_costs': 0,
            'totle_amount': 0,
            'realized_profit': 0,
            'unrealized_profit': 0,
        }
        ALL_TICKERS = ['ETHBTC', 'LTCBTC', 'BNBBTC', 'NEOBTC', 'QTUMETH', 'EOSETH', 'SNTETH', 'BNTETH', 'BCCBTC',
                       'GASBTC',
                       'BNBETH', 'BTCUSDT', 'ETHUSDT', 'HSRBTC', 'OAXETH', 'DNTETH', 'MCOETH', 'ICNETH', 'MCOBTC',
                       'WTCBTC',
                       'WTCETH', 'LRCBTC', 'LRCETH', 'QTUMBTC', 'YOYOBTC', 'OMGBTC', 'OMGETH', 'ZRXBTC', 'ZRXETH',
                       'STRATBTC', 'STRATETH', 'SNGLSBTC', 'SNGLSETH', 'BQXBTC', 'BQXETH', 'KNCBTC', 'KNCETH', 'FUNBTC',
                       'FUNETH', 'SNMBTC', 'SNMETH', 'NEOETH', 'IOTABTC', 'IOTAETH', 'LINKBTC', 'LINKETH', 'XVGBTC',
                       'XVGETH', 'SALTBTC', 'SALTETH', 'MDABTC', 'MDAETH', 'MTLBTC', 'MTLETH', 'SUBBTC', 'SUBETH',
                       'EOSBTC',
                       'SNTBTC', 'ETCETH', 'ETCBTC', 'MTHBTC', 'MTHETH', 'ENGBTC', 'ENGETH', 'DNTBTC', 'ZECBTC',
                       'ZECETH',
                       'BNTBTC', 'ASTBTC', 'ASTETH', 'DASHBTC', 'DASHETH', 'OAXBTC', 'ICNBTC', 'BTGBTC', 'BTGETH',
                       'EVXBTC',
                       'EVXETH', 'REQBTC', 'REQETH', 'VIBBTC', 'VIBETH', 'HSRETH', 'TRXBTC', 'TRXETH', 'POWRBTC',
                       'POWRETH',
                       'ARKBTC', 'ARKETH', 'YOYOETH', 'XRPBTC', 'XRPETH', 'MODBTC', 'MODETH', 'ENJBTC', 'ENJETH',
                       'STORJBTC', 'STORJETH', 'BNBUSDT', 'VENBNB', 'YOYOBNB', 'POWRBNB', 'VENBTC', 'VENETH', 'KMDBTC',
                       'KMDETH', 'NULSBNB', 'RCNBTC', 'RCNETH', 'RCNBNB', 'NULSBTC', 'NULSETH', 'RDNBTC', 'RDNETH',
                       'RDNBNB', 'XMRBTC', 'XMRETH', 'DLTBNB', 'WTCBNB', 'DLTBTC', 'DLTETH', 'AMBBTC', 'AMBETH',
                       'AMBBNB',
                       'BCCETH', 'BCCUSDT', 'BCCBNB', 'BATBTC', 'BATETH', 'BATBNB', 'BCPTBTC', 'BCPTETH', 'BCPTBNB',
                       'ARNBTC', 'ARNETH', 'GVTBTC', 'GVTETH', 'CDTBTC', 'CDTETH', 'GXSBTC', 'GXSETH', 'NEOUSDT',
                       'NEOBNB',
                       'POEBTC', 'POEETH', 'QSPBTC', 'QSPETH', 'QSPBNB', 'BTSBTC', 'BTSETH', 'BTSBNB', 'XZCBTC',
                       'XZCETH',
                       'XZCBNB', 'LSKBTC', 'LSKETH', 'LSKBNB', 'TNTBTC', 'TNTETH', 'FUELBTC', 'FUELETH', 'MANABTC',
                       'MANAETH', 'BCDBTC', 'BCDETH', 'DGDBTC', 'DGDETH', 'IOTABNB', 'ADXBTC', 'ADXETH', 'ADXBNB',
                       'ADABTC',
                       'ADAETH', 'PPTBTC', 'PPTETH', 'CMTBTC', 'CMTETH', 'CMTBNB', 'XLMBTC', 'XLMETH', 'XLMBNB',
                       'CNDBTC',
                       'CNDETH', 'CNDBNB', 'LENDBTC', 'LENDETH', 'WABIBTC', 'WABIETH', 'WABIBNB', 'LTCETH', 'LTCUSDT',
                       'LTCBNB', 'TNBBTC', 'TNBETH', 'WAVESBTC', 'WAVESETH', 'WAVESBNB', 'GTOBTC', 'GTOETH', 'GTOBNB',
                       'ICXBTC', 'ICXETH', 'ICXBNB', 'OSTBTC', 'OSTETH', 'OSTBNB', 'ELFBTC', 'ELFETH', 'AIONBTC',
                       'AIONETH',
                       'AIONBNB', 'NEBLBTC', 'NEBLETH', 'NEBLBNB', 'BRDBTC', 'BRDETH', 'BRDBNB', 'MCOBNB', 'EDOBTC',
                       'EDOETH', 'WINGSBTC', 'WINGSETH', 'NAVBTC', 'NAVETH', 'NAVBNB', 'LUNBTC', 'LUNETH', 'TRIGBTC',
                       'TRIGETH', 'TRIGBNB', 'APPCBTC', 'APPCETH', 'APPCBNB', 'VIBEBTC', 'VIBEETH', 'RLCBTC', 'RLCETH',
                       'RLCBNB', 'INSBTC', 'INSETH', 'PIVXBTC', 'PIVXETH', 'PIVXBNB', 'IOSTBTC', 'IOSTETH', 'CHATBTC',
                       'CHATETH', 'STEEMBTC', 'STEEMETH', 'STEEMBNB', 'NANOBTC', 'NANOETH', 'NANOBNB', 'VIABTC',
                       'VIAETH',
                       'VIABNB', 'BLZBTC', 'BLZETH', 'BLZBNB', 'AEBTC', 'AEETH', 'AEBNB', 'RPXBTC', 'RPXETH', 'RPXBNB',
                       'NCASHBTC', 'NCASHETH', 'NCASHBNB', 'POABTC', 'POAETH', 'POABNB', 'ZILBTC', 'ZILETH', 'ZILBNB',
                       'ONTBTC', 'ONTETH', 'ONTBNB', 'STORMBTC', 'STORMETH', 'STORMBNB', 'QTUMBNB', 'QTUMUSDT',
                       'XEMBTC',
                       'XEMETH', 'XEMBNB', 'WANBTC', 'WANETH', 'WANBNB', 'WPRBTC', 'WPRETH', 'QLCBTC', 'QLCETH',
                       'SYSBTC',
                       'SYSETH', 'SYSBNB', 'QLCBNB', 'GRSBTC', 'GRSETH', 'ADAUSDT', 'ADABNB', 'CLOAKBTC', 'CLOAKETH',
                       'GNTBTC', 'GNTETH', 'GNTBNB', 'LOOMBTC', 'LOOMETH', 'LOOMBNB', 'XRPUSDT', 'BCNBTC', 'BCNETH',
                       'BCNBNB', 'REPBTC', 'REPETH', 'REPBNB', 'BTCTUSD', 'TUSDBTC', 'ETHTUSD', 'TUSDETH', 'TUSDBNB',
                       'ZENBTC', 'ZENETH', 'ZENBNB', 'SKYBTC', 'SKYETH', 'SKYBNB', 'EOSUSDT', 'EOSBNB', 'CVCBTC',
                       'CVCETH',
                       'CVCBNB', 'THETABTC', 'THETAETH', 'THETABNB', 'XRPBNB', 'TUSDUSDT', 'IOTAUSDT', 'XLMUSDT',
                       'IOTXBTC',
                       'IOTXETH', 'QKCBTC', 'QKCETH', 'AGIBTC', 'AGIETH', 'AGIBNB', 'NXSBTC', 'NXSETH', 'NXSBNB',
                       'ENJBNB',
                       'DATABTC', 'DATAETH', 'ONTUSDT', 'TRXBNB', 'TRXUSDT', 'ETCUSDT', 'ETCBNB', 'ICXUSDT', 'SCBTC',
                       'SCETH', 'SCBNB', 'NPXSBTC', 'NPXSETH', 'VENUSDT', 'KEYBTC', 'KEYETH', 'NASBTC', 'NASETH',
                       'NASBNB',
                       'MFTBTC', 'MFTETH', 'MFTBNB', 'DENTBTC', 'DENTETH', 'ARDRBTC', 'ARDRETH', 'ARDRBNB', 'NULSUSDT',
                       'HOTBTC', 'HOTETH', 'VETBTC', 'VETETH', 'VETUSDT', 'VETBNB', 'DOCKBTC', 'DOCKETH', 'POLYBTC',
                       'POLYBNB', 'PHXBTC', 'PHXETH', 'PHXBNB', 'HCBTC', 'HCETH', 'GOBTC', 'GOBNB', 'PAXBTC', 'PAXBNB',
                       'PAXUSDT', 'PAXETH', 'RVNBTC', 'RVNBNB', 'DCRBTC', 'DCRBNB', 'USDCBNB', 'MITHBTC', 'MITHBNB',
                       'BCHABCBTC', 'BCHSVBTC', 'BCHABCUSDT', 'BCHSVUSDT', 'BNBPAX', 'BTCPAX', 'ETHPAX', 'XRPPAX',
                       'EOSPAX',
                       'XLMPAX', 'RENBTC', 'RENBNB', 'BNBTUSD', 'XRPTUSD', 'EOSTUSD', 'XLMTUSD', 'BNBUSDC', 'BTCUSDC',
                       'ETHUSDC', 'XRPUSDC', 'EOSUSDC', 'XLMUSDC', 'USDCUSDT', 'ADATUSD', 'TRXTUSD', 'NEOTUSD',
                       'TRXXRP',
                       'XZCXRP', 'PAXTUSD', 'USDCTUSD', 'USDCPAX', 'LINKUSDT', 'LINKTUSD', 'LINKPAX', 'LINKUSDC',
                       'WAVESUSDT', 'WAVESTUSD', 'WAVESPAX', 'WAVESUSDC', 'BCHABCTUSD', 'BCHABCPAX', 'BCHABCUSDC',
                       'BCHSVTUSD', 'BCHSVPAX', 'BCHSVUSDC', 'LTCTUSD', 'LTCPAX', 'LTCUSDC', 'TRXPAX', 'TRXUSDC',
                       'BTTBTC',
                       'BTTBNB', 'BTTUSDT', 'BNBUSDS', 'BTCUSDS', 'USDSUSDT', 'USDSPAX', 'USDSTUSD', 'USDSUSDC',
                       'BTTPAX',
                       'BTTTUSD', 'BTTUSDC', 'ONGBNB', 'ONGBTC', 'ONGUSDT', 'HOTBNB', 'HOTUSDT', 'ZILUSDT', 'ZRXBNB',
                       'ZRXUSDT', 'FETBNB', 'FETBTC', 'FETUSDT', 'BATUSDT', 'XMRBNB', 'XMRUSDT', 'ZECBNB', 'ZECUSDT',
                       'ZECPAX', 'ZECTUSD', 'ZECUSDC', 'IOSTBNB', 'IOSTUSDT', 'CELRBNB', 'CELRBTC', 'CELRUSDT',
                       'ADAPAX',
                       'ADAUSDC', 'NEOPAX', 'NEOUSDC', 'DASHBNB', 'DASHUSDT', 'NANOUSDT', 'OMGBNB', 'OMGUSDT',
                       'THETAUSDT',
                       'ENJUSDT', 'MITHUSDT', 'MATICBNB', 'MATICBTC', 'MATICUSDT', 'ATOMBNB', 'ATOMBTC', 'ATOMUSDT',
                       'ATOMUSDC', 'ATOMPAX', 'ATOMTUSD', 'ETCUSDC', 'ETCPAX', 'ETCTUSD', 'BATUSDC', 'BATPAX',
                       'BATTUSD',
                       'PHBBNB', 'PHBBTC', 'PHBUSDC', 'PHBTUSD', 'PHBPAX', 'TFUELBNB', 'TFUELBTC', 'TFUELUSDT',
                       'TFUELUSDC',
                       'TFUELTUSD', 'TFUELPAX', 'ONEBNB', 'ONEBTC', 'ONEUSDT', 'ONETUSD', 'ONEPAX', 'ONEUSDC', 'FTMBNB',
                       'FTMBTC', 'FTMUSDT', 'FTMTUSD', 'FTMPAX', 'FTMUSDC', 'BTCBBTC', 'BCPTTUSD', 'BCPTPAX',
                       'BCPTUSDC',
                       'ALGOBNB', 'ALGOBTC', 'ALGOUSDT', 'ALGOTUSD', 'ALGOPAX', 'ALGOUSDC', 'USDSBUSDT', 'USDSBUSDS',
                       'GTOUSDT', 'GTOPAX', 'GTOTUSD', 'GTOUSDC', 'ERDBNB', 'ERDBTC', 'ERDUSDT', 'ERDPAX', 'ERDUSDC',
                       'DOGEBNB', 'DOGEBTC', 'DOGEUSDT', 'DOGEPAX', 'DOGEUSDC', 'DUSKBNB', 'DUSKBTC', 'DUSKUSDT',
                       'DUSKUSDC', 'DUSKPAX', 'BGBPUSDC', 'ANKRBNB', 'ANKRBTC', 'ANKRUSDT', 'ANKRTUSD', 'ANKRPAX',
                       'ANKRUSDC', 'ONTPAX', 'ONTUSDC', 'WINBNB', 'WINBTC', 'WINUSDT', 'WINUSDC', 'COSBNB', 'COSBTC',
                       'COSUSDT', 'TUSDBTUSD', 'NPXSUSDT', 'NPXSUSDC', 'COCOSBNB', 'COCOSBTC', 'COCOSUSDT', 'MTLUSDT',
                       'TOMOBNB', 'TOMOBTC', 'TOMOUSDT', 'TOMOUSDC', 'PERLBNB', 'PERLBTC', 'PERLUSDC', 'PERLUSDT',
                       'DENTUSDT', 'MFTUSDT', 'KEYUSDT', 'STORMUSDT', 'DOCKUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT',
                       'BTTTRX',
                       'WINTRX', 'CHZBNB', 'CHZBTC', 'CHZUSDT', 'BANDBNB', 'BANDBTC', 'BANDUSDT', 'BNBBUSD', 'BTCBUSD',
                       'BUSDUSDT', 'BEAMBNB', 'BEAMBTC', 'BEAMUSDT', 'XTZBNB', 'XTZBTC', 'XTZUSDT', 'RENUSDT',
                       'RVNUSDT',
                       'HCUSDT', 'HBARBNB', 'HBARBTC', 'HBARUSDT', 'NKNBNB', 'NKNBTC', 'NKNUSDT', 'XRPBUSD', 'ETHBUSD',
                       'BCHABCBUSD', 'LTCBUSD', 'LINKBUSD', 'ETCBUSD', 'STXBNB', 'STXBTC', 'STXUSDT', 'KAVABNB',
                       'KAVABTC',
                       'KAVAUSDT', 'BUSDNGN', 'BNBNGN', 'BTCNGN', 'ARPABNB', 'ARPABTC', 'ARPAUSDT', 'TRXBUSD',
                       'EOSBUSD',
                       'IOTXUSDT', 'RLCUSDT', 'MCOUSDT', 'XLMBUSD', 'ADABUSD', 'CTXCBNB', 'CTXCBTC', 'CTXCUSDT',
                       'BCHBNB',
                       'BCHBTC', 'BCHUSDT', 'BCHUSDC', 'BCHTUSD', 'BCHPAX', 'BCHBUSD', 'BTCRUB', 'ETHRUB', 'XRPRUB',
                       'BNBRUB', 'TROYBNB', 'TROYBTC', 'TROYUSDT', 'BUSDRUB', 'QTUMBUSD', 'VETBUSD', 'VITEBNB',
                       'VITEBTC',
                       'VITEUSDT', 'FTTBNB', 'FTTBTC', 'FTTUSDT', 'BTCTRY', 'BNBTRY', 'BUSDTRY', 'ETHTRY', 'XRPTRY',
                       'USDTTRY', 'USDTRUB', 'BTCEUR', 'ETHEUR', 'BNBEUR', 'XRPEUR', 'EURBUSD', 'EURUSDT', 'OGNBNB',
                       'OGNBTC', 'OGNUSDT', 'DREPBNB', 'DREPBTC', 'DREPUSDT', 'BULLUSDT', 'BULLBUSD', 'BEARUSDT',
                       'BEARBUSD', 'ETHBULLUSDT', 'ETHBULLBUSD', 'ETHBEARUSDT', 'ETHBEARBUSD', 'TCTBNB', 'TCTBTC',
                       'TCTUSDT', 'WRXBNB', 'WRXBTC', 'WRXUSDT', 'ICXBUSD', 'BTSUSDT', 'BTSBUSD', 'LSKUSDT', 'BNTUSDT',
                       'BNTBUSD', 'LTOBNB', 'LTOBTC', 'LTOUSDT', 'ATOMBUSD', 'DASHBUSD', 'NEOBUSD', 'WAVESBUSD',
                       'XTZBUSD',
                       'EOSBULLUSDT', 'EOSBULLBUSD', 'EOSBEARUSDT', 'EOSBEARBUSD', 'XRPBULLUSDT', 'XRPBULLBUSD',
                       'XRPBEARUSDT', 'XRPBEARBUSD', 'BATBUSD', 'ENJBUSD', 'NANOBUSD', 'ONTBUSD', 'RVNBUSD',
                       'STRATBUSD',
                       'STRATBNB', 'STRATUSDT', 'AIONBUSD', 'AIONUSDT', 'MBLBNB', 'MBLBTC', 'MBLUSDT', 'COTIBNB',
                       'COTIBTC',
                       'COTIUSDT', 'ALGOBUSD', 'BTTBUSD', 'TOMOBUSD', 'XMRBUSD', 'ZECBUSD', 'BNBBULLUSDT',
                       'BNBBULLBUSD',
                       'BNBBEARUSDT', 'BNBBEARBUSD', 'STPTBNB', 'STPTBTC', 'STPTUSDT', 'BTCZAR', 'ETHZAR', 'BNBZAR',
                       'USDTZAR', 'BUSDZAR', 'BTCBKRW', 'ETHBKRW', 'BNBBKRW', 'WTCUSDT', 'DATABUSD', 'DATAUSDT',
                       'XZCUSDT',
                       'SOLBNB', 'SOLBTC', 'SOLUSDT', 'SOLBUSD', 'BTCIDRT', 'BNBIDRT', 'USDTIDRT', 'BUSDIDRT',
                       'CTSIBTC',
                       'CTSIUSDT', 'CTSIBNB', 'CTSIBUSD', 'HIVEBNB', 'HIVEBTC', 'HIVEUSDT', 'CHRBNB', 'CHRBTC',
                       'CHRUSDT',
                       'BTCUPUSDT', 'BTCDOWNUSDT', 'GXSUSDT', 'ARDRUSDT', 'ERDBUSD', 'LENDUSDT', 'HBARBUSD',
                       'MATICBUSD',
                       'WRXBUSD', 'ZILBUSD', 'MDTBNB', 'MDTBTC', 'MDTUSDT', 'STMXBNB', 'STMXBTC', 'STMXETH', 'STMXUSDT',
                       'KNCBUSD', 'KNCUSDT', 'REPBUSD', 'REPUSDT', 'LRCBUSD', 'LRCUSDT', 'IQBNB', 'IQBUSD', 'PNTBTC',
                       'PNTUSDT', 'BTCGBP', 'ETHGBP', 'XRPGBP', 'BNBGBP', 'GBPBUSD', 'DGBBNB', 'DGBBTC', 'DGBBUSD',
                       'BTCUAH', 'USDTUAH', 'COMPBTC', 'COMPBNB', 'COMPBUSD', 'COMPUSDT', 'BTCBIDR', 'ETHBIDR',
                       'BNBBIDR',
                       'BUSDBIDR', 'USDTBIDR', 'BKRWUSDT', 'BKRWBUSD', 'SCUSDT', 'ZENUSDT', 'SXPBTC', 'SXPBNB',
                       'SXPBUSD',
                       'SNXBTC', 'SNXBNB', 'SNXBUSD', 'SNXUSDT', 'ETHUPUSDT', 'ETHDOWNUSDT', 'ADAUPUSDT', 'ADADOWNUSDT',
                       'LINKUPUSDT', 'LINKDOWNUSDT', 'VTHOBNB', 'VTHOBUSD', 'VTHOUSDT', 'DCRBUSD', 'DGBUSDT', 'GBPUSDT',
                       'STORJBUSD', 'SXPUSDT', 'IRISBNB', 'IRISBTC', 'IRISBUSD', 'MKRBNB', 'MKRBTC', 'MKRUSDT',
                       'MKRBUSD',
                       'DAIBNB', 'DAIBTC', 'DAIUSDT', 'DAIBUSD', 'RUNEBNB', 'RUNEBTC', 'RUNEBUSD', 'MANABUSD',
                       'DOGEBUSD',
                       'LENDBUSD', 'ZRXBUSD', 'DCRUSDT', 'STORJUSDT', 'XRPBKRW', 'ADABKRW', 'BTCAUD', 'ETHAUD',
                       'AUDBUSD',
                       'FIOBNB', 'FIOBTC', 'FIOBUSD', 'BNBUPUSDT', 'BNBDOWNUSDT', 'XTZUPUSDT', 'XTZDOWNUSDT', 'AVABNB',
                       'AVABTC', 'AVABUSD', 'USDTBKRW', 'BUSDBKRW', 'IOTABUSD', 'MANAUSDT', 'XRPAUD', 'BNBAUD',
                       'AUDUSDT',
                       'BALBNB', 'BALBTC', 'BALBUSD', 'YFIBNB', 'YFIBTC', 'YFIBUSD', 'YFIUSDT', 'BLZBUSD', 'KMDBUSD',
                       'BALUSDT', 'BLZUSDT', 'IRISUSDT', 'KMDUSDT', 'BTCDAI', 'ETHDAI', 'BNBDAI', 'USDTDAI', 'BUSDDAI',
                       'JSTBNB', 'JSTBTC', 'JSTBUSD', 'JSTUSDT', 'SRMBNB', 'SRMBTC', 'SRMBUSD', 'SRMUSDT', 'ANTBNB',
                       'ANTBTC', 'ANTBUSD', 'ANTUSDT', 'CRVBNB', 'CRVBTC', 'CRVBUSD', 'CRVUSDT', 'SANDBNB', 'SANDBTC',
                       'SANDUSDT', 'SANDBUSD', 'OCEANBNB', 'OCEANBTC', 'OCEANBUSD', 'OCEANUSDT', 'NMRBNB', 'NMRBTC',
                       'NMRBUSD', 'NMRUSDT', 'DOTBNB', 'DOTBTC', 'DOTBUSD', 'DOTUSDT', 'LUNABNB', 'LUNABTC', 'LUNABUSD',
                       'LUNAUSDT', 'IDEXBTC', 'IDEXBUSD', 'RSRBNB', 'RSRBTC', 'RSRBUSD', 'RSRUSDT', 'PAXGBNB',
                       'PAXGBTC',
                       'PAXGBUSD', 'PAXGUSDT', 'WNXMBNB', 'WNXMBTC', 'WNXMBUSD', 'WNXMUSDT', 'TRBBNB', 'TRBBTC',
                       'TRBBUSD',
                       'TRBUSDT', 'ETHNGN', 'DOTBIDR', 'LINKAUD', 'SXPAUD', 'BZRXBNB', 'BZRXBTC', 'BZRXBUSD',
                       'BZRXUSDT',
                       'WBTCBTC', 'WBTCETH', 'SUSHIBNB', 'SUSHIBTC', 'SUSHIBUSD', 'SUSHIUSDT', 'YFIIBNB', 'YFIIBTC',
                       'YFIIBUSD', 'YFIIUSDT', 'KSMBNB', 'KSMBTC', 'KSMBUSD', 'KSMUSDT', 'EGLDBNB', 'EGLDBTC',
                       'EGLDBUSD',
                       'EGLDUSDT', 'DIABNB', 'DIABTC', 'DIABUSD', 'DIAUSDT', 'RUNEUSDT', 'FIOUSDT', 'UMABTC', 'UMAUSDT',
                       'EOSUPUSDT', 'EOSDOWNUSDT', 'TRXUPUSDT', 'TRXDOWNUSDT', 'XRPUPUSDT', 'XRPDOWNUSDT', 'DOTUPUSDT',
                       'DOTDOWNUSDT', 'SRMBIDR', 'ONEBIDR', 'LINKTRY', 'USDTNGN', 'BELBNB', 'BELBTC', 'BELBUSD',
                       'BELUSDT',
                       'WINGBNB', 'WINGBTC', 'SWRVBNB', 'SWRVBUSD', 'WINGBUSD', 'WINGUSDT', 'LTCUPUSDT', 'LTCDOWNUSDT',
                       'LENDBKRW', 'SXPEUR', 'CREAMBNB', 'CREAMBUSD', 'UNIBNB', 'UNIBTC', 'UNIBUSD', 'UNIUSDT',
                       'NBSBTC',
                       'NBSUSDT', 'OXTBTC', 'OXTUSDT', 'SUNBTC', 'SUNUSDT', 'AVAXBNB', 'AVAXBTC', 'AVAXBUSD',
                       'AVAXUSDT',
                       'HNTBTC', 'HNTUSDT', 'BAKEBNB', 'BURGERBNB', 'SXPBIDR', 'LINKBKRW', 'FLMBNB', 'FLMBTC',
                       'FLMBUSD',
                       'FLMUSDT', 'SCRTBTC', 'SCRTETH', 'CAKEBNB', 'CAKEBUSD', 'SPARTABNB', 'UNIUPUSDT', 'UNIDOWNUSDT',
                       'ORNBTC', 'ORNUSDT', 'TRXNGN', 'SXPTRY', 'UTKBTC', 'UTKUSDT', 'XVSBNB', 'XVSBTC', 'XVSBUSD',
                       'XVSUSDT', 'ALPHABNB', 'ALPHABTC', 'ALPHABUSD', 'ALPHAUSDT', 'VIDTBTC', 'VIDTBUSD', 'AAVEBNB',
                       'BTCBRL', 'USDTBRL', 'AAVEBTC', 'AAVEETH', 'AAVEBUSD', 'AAVEUSDT', 'AAVEBKRW', 'NEARBNB',
                       'NEARBTC',
                       'NEARBUSD', 'NEARUSDT', 'SXPUPUSDT', 'SXPDOWNUSDT', 'DOTBKRW', 'SXPGBP', 'FILBNB', 'FILBTC',
                       'FILBUSD', 'FILUSDT', 'FILUPUSDT', 'FILDOWNUSDT', 'YFIUPUSDT', 'YFIDOWNUSDT', 'INJBNB', 'INJBTC',
                       'INJBUSD', 'INJUSDT', 'AERGOBTC', 'AERGOBUSD', 'LINKEUR', 'ONEBUSD', 'EASYETH', 'AUDIOBTC',
                       'AUDIOBUSD', 'AUDIOUSDT', 'CTKBNB', 'CTKBTC', 'CTKBUSD', 'CTKUSDT', 'BCHUPUSDT', 'BCHDOWNUSDT',
                       'BOTBTC', 'BOTBUSD', 'ETHBRL', 'DOTEUR', 'AKROBTC', 'AKROUSDT', 'KP3RBNB', 'KP3RBUSD', 'AXSBNB',
                       'AXSBTC', 'AXSBUSD', 'AXSUSDT', 'HARDBNB', 'HARDBTC', 'HARDBUSD', 'HARDUSDT', 'BNBBRL', 'LTCEUR',
                       'RENBTCBTC', 'RENBTCETH', 'DNTBUSD', 'DNTUSDT', 'SLPETH', 'ADAEUR', 'LTCNGN', 'CVPETH',
                       'CVPBUSD',
                       'STRAXBTC', 'STRAXETH', 'STRAXBUSD', 'STRAXUSDT', 'FORBTC', 'FORBUSD', 'UNFIBNB', 'UNFIBTC',
                       'UNFIBUSD', 'UNFIUSDT', 'FRONTETH', 'FRONTBUSD', 'BCHABUSD', 'ROSEBTC', 'ROSEBUSD', 'ROSEUSDT',
                       'AVAXTRY', 'BUSDBRL', 'AVAUSDT', 'SYSBUSD', 'XEMUSDT', 'HEGICETH', 'HEGICBUSD', 'AAVEUPUSDT',
                       'AAVEDOWNUSDT', 'PROMBNB', 'PROMBUSD', 'XRPBRL', 'XRPNGN', 'SKLBTC', 'SKLBUSD', 'SKLUSDT',
                       'BCHEUR',
                       'YFIEUR', 'ZILBIDR', 'SUSDBTC', 'SUSDETH', 'SUSDUSDT', 'COVERETH', 'COVERBUSD', 'GLMBTC',
                       'GLMETH',
                       'GHSTETH', 'GHSTBUSD', 'SUSHIUPUSDT', 'SUSHIDOWNUSDT', 'XLMUPUSDT', 'XLMDOWNUSDT', 'LINKBRL',
                       'LINKNGN', 'LTCRUB', 'TRXTRY', 'XLMEUR', 'DFETH', 'DFBUSD', 'GRTBTC', 'GRTETH', 'GRTUSDT',
                       'JUVBTC',
                       'JUVBUSD', 'JUVUSDT', 'PSGBTC', 'PSGBUSD', 'PSGUSDT', 'BUSDBVND', 'USDTBVND', '1INCHBTC',
                       '1INCHUSDT', 'REEFBTC', 'REEFUSDT', 'OGBTC', 'OGUSDT', 'ATMBTC', 'ATMUSDT', 'ASRBTC', 'ASRUSDT',
                       'CELOBTC', 'CELOUSDT', 'RIFBTC', 'RIFUSDT', 'CHZTRY', 'XLMTRY', 'LINKGBP', 'GRTEUR', 'BTCSTBTC',
                       'BTCSTBUSD', 'BTCSTUSDT', 'TRUBTC', 'TRUBUSD', 'TRUUSDT', 'DEXEETH', 'DEXEBUSD', 'EOSEUR',
                       'LTCBRL',
                       'USDCBUSD', 'TUSDBUSD', 'PAXBUSD', 'CKBBTC', 'CKBBUSD', 'CKBUSDT', 'TWTBTC', 'TWTBUSD',
                       'TWTUSDT',
                       'FIROBTC', 'FIROETH', 'FIROUSDT', 'BETHETH', 'DOGEEUR', 'DOGETRY', 'DOGEAUD', 'DOGEBRL',
                       'DOTNGN',
                       'PROSETH', 'LITBTC', 'LITBUSD', 'LITUSDT', 'BTCVAI', 'BUSDVAI', 'SFPBTC', 'SFPBUSD', 'SFPUSDT',
                       'DOGEGBP', 'DOTTRY', 'FXSBTC', 'FXSBUSD', 'DODOBTC', 'DODOBUSD', 'DODOUSDT', 'FRONTBTC',
                       'EASYBTC',
                       'CAKEBTC', 'CAKEUSDT', 'BAKEBUSD', 'UFTETH', 'UFTBUSD', '1INCHBUSD', 'BANDBUSD', 'GRTBUSD',
                       'IOSTBUSD', 'OMGBUSD', 'REEFBUSD', 'ACMBTC', 'ACMBUSD', 'ACMUSDT', 'AUCTIONBTC', 'AUCTIONBUSD',
                       'PHABTC', 'PHABUSD', 'DOTGBP', 'ADATRY', 'ADABRL', 'ADAGBP', 'TVKBTC', 'TVKBUSD', 'BADGERBTC',
                       'BADGERBUSD', 'BADGERUSDT', 'FISBTC', 'FISBUSD', 'FISUSDT', 'DOTBRL', 'ADAAUD', 'HOTTRY',
                       'EGLDEUR',
                       'OMBTC', 'OMBUSD', 'OMUSDT', 'PONDBTC', 'PONDBUSD', 'PONDUSDT', 'DEGOBTC', 'DEGOBUSD',
                       'DEGOUSDT',
                       'AVAXEUR', 'BTTTRY', 'CHZBRL', 'UNIEUR', 'ALICEBTC', 'ALICEBUSD', 'ALICEUSDT', 'CHZBUSD',
                       'CHZEUR',
                       'CHZGBP', 'BIFIBNB', 'BIFIBUSD', 'LINABTC', 'LINABUSD', 'LINAUSDT', 'ADARUB', 'ENJBRL', 'ENJEUR',
                       'MATICEUR', 'NEOTRY', 'PERPBTC', 'PERPBUSD', 'PERPUSDT', 'RAMPBTC', 'RAMPBUSD', 'RAMPUSDT',
                       'SUPERBTC', 'SUPERBUSD', 'SUPERUSDT', 'CFXBTC', 'CFXBUSD', 'CFXUSDT', 'ENJGBP', 'EOSTRY',
                       'LTCGBP',
                       'LUNAEUR', 'RVNTRY', 'THETAEUR', 'XVGBUSD', 'EPSBTC', 'EPSBUSD', 'EPSUSDT', 'AUTOBTC',
                       'AUTOBUSD',
                       'AUTOUSDT', 'TKOBTC', 'TKOBIDR', 'TKOBUSD', 'TKOUSDT', 'PUNDIXETH', 'PUNDIXUSDT', 'BTTBRL',
                       'BTTEUR',
                       'HOTEUR', 'WINEUR', 'TLMBTC', 'TLMBUSD', 'TLMUSDT', '1INCHUPUSDT', '1INCHDOWNUSDT', 'BTGBUSD',
                       'BTGUSDT', 'HOTBUSD', 'BNBUAH', 'ONTTRY', 'VETEUR', 'VETGBP', 'WINBRL', 'MIRBTC', 'MIRBUSD',
                       'MIRUSDT', 'BARBTC', 'BARBUSD', 'BARUSDT', 'FORTHBTC', 'FORTHBUSD', 'FORTHUSDT', 'CAKEGBP',
                       'DOGERUB', 'HOTBRL', 'WRXEUR', 'EZBTC', 'EZETH', 'BAKEUSDT', 'BURGERBUSD', 'BURGERUSDT',
                       'SLPBUSD',
                       'SLPUSDT', 'TRXAUD', 'TRXEUR', 'VETTRY', 'SHIBUSDT', 'SHIBBUSD', 'ICPBTC', 'ICPBNB', 'ICPBUSD',
                       'ICPUSDT', 'BTCGYEN', 'USDTGYEN', 'SHIBEUR', 'SHIBRUB', 'ETCEUR', 'ETCBRL', 'DOGEBIDR', 'ARBTC',
                       'ARBNB', 'ARBUSD', 'ARUSDT', 'POLSBTC', 'POLSBNB', 'POLSBUSD', 'POLSUSDT', 'MDXBTC', 'MDXBNB',
                       'MDXBUSD', 'MDXUSDT', 'MASKBNB', 'MASKBUSD', 'MASKUSDT', 'LPTBTC', 'LPTBNB', 'LPTBUSD',
                       'LPTUSDT',
                       'ETHUAH', 'MATICBRL', 'SOLEUR', 'SHIBBRL', 'AGIXBTC', 'ICPEUR', 'MATICGBP', 'SHIBTRY',
                       'MATICBIDR',
                       'MATICRUB', 'NUBTC', 'NUBNB', 'NUBUSD', 'NUUSDT', 'XVGUSDT', 'RLCBUSD', 'CELRBUSD', 'ATMBUSD',
                       'ZENBUSD', 'FTMBUSD', 'THETABUSD', 'WINBUSD', 'KAVABUSD', 'XEMBUSD', 'ATABTC', 'ATABNB',
                       'ATABUSD',
                       'ATAUSDT', 'GTCBTC', 'GTCBNB', 'GTCBUSD', 'GTCUSDT', 'TORNBTC', 'TORNBNB', 'TORNBUSD',
                       'TORNUSDT',
                       'MATICTRY', 'ETCGBP', 'SOLGBP', 'BAKEBTC', 'COTIBUSD', 'KEEPBTC', 'KEEPBNB', 'KEEPBUSD',
                       'KEEPUSDT',
                       'SOLTRY', 'RUNEGBP', 'SOLBRL', 'SCBUSD', 'CHRBUSD', 'STMXBUSD', 'HNTBUSD', 'FTTBUSD', 'DOCKBUSD',
                       'ADABIDR', 'ERNBNB', 'ERNBUSD', 'ERNUSDT', 'KLAYBTC', 'KLAYBNB', 'KLAYBUSD', 'KLAYUSDT',
                       'RUNEEUR',
                       'MATICAUD', 'DOTRUB', 'UTKBUSD', 'IOTXBUSD', 'PHAUSDT', 'SOLRUB', 'RUNEAUD', 'BUSDUAH',
                       'BONDBTC',
                       'BONDBNB', 'BONDBUSD', 'BONDUSDT', 'MLNBTC', 'MLNBNB', 'MLNBUSD', 'MLNUSDT', 'GRTTRY', 'CAKEBRL',
                       'ICPRUB', 'DOTAUD', 'AAVEBRL', 'EOSAUD', 'DEXEUSDT', 'LTOBUSD', 'ADXBUSD', 'QUICKBTC',
                       'QUICKBNB',
                       'QUICKBUSD', 'C98USDT', 'C98BUSD', 'C98BNB', 'C98BTC', 'CLVBTC', 'CLVBNB', 'CLVBUSD', 'CLVUSDT',
                       'QNTBTC', 'QNTBNB', 'QNTBUSD', 'QNTUSDT', 'FLOWBTC', 'FLOWBNB', 'FLOWBUSD', 'FLOWUSDT',
                       'XECBUSD',
                       'AXSBRL', 'AXSAUD', 'TVKUSDT', 'MINABTC', 'MINABNB', 'MINABUSD', 'MINAUSDT', 'RAYBNB', 'RAYBUSD',
                       'RAYUSDT', 'FARMBTC', 'FARMBNB', 'FARMBUSD', 'FARMUSDT', 'ALPACABTC', 'ALPACABNB', 'ALPACABUSD',
                       'ALPACAUSDT', 'TLMTRY', 'QUICKUSDT', 'ORNBUSD', 'MBOXBTC', 'MBOXBNB', 'MBOXBUSD', 'MBOXUSDT',
                       'VGXBTC', 'VGXETH', 'FORUSDT', 'REQUSDT', 'GHSTUSDT', 'TRURUB', 'FISBRL', 'WAXPUSDT', 'WAXPBUSD',
                       'WAXPBNB', 'WAXPBTC', 'TRIBEBTC', 'TRIBEBNB', 'TRIBEBUSD', 'TRIBEUSDT', 'GNOUSDT', 'GNOBUSD',
                       'GNOBNB', 'GNOBTC', 'ARPATRY', 'PROMBTC', 'MTLBUSD', 'OGNBUSD', 'XECUSDT', 'C98BRL', 'SOLAUD',
                       'SUSHIBIDR', 'XRPBIDR', 'POLYBUSD', 'ELFUSDT', 'DYDXUSDT', 'DYDXBUSD', 'DYDXBNB', 'DYDXBTC',
                       'ELFBUSD', 'POLYUSDT', 'IDEXUSDT', 'VIDTUSDT', 'SOLBIDR', 'AXSBIDR', 'BTCUSDP', 'ETHUSDP',
                       'BNBUSDP',
                       'USDPBUSD', 'USDPUSDT', 'GALAUSDT', 'GALABUSD', 'GALABNB', 'GALABTC']
        if symbol in ALL_TICKERS:
            recent_price = float(client.get_recent_trades(symbol=symbol)[0]['price'])
            this_coin['new_trade'] = client.get_my_trades(symbol=symbol)
            # Calc totole_costs and totle_amount
            for trade in this_coin['new_trade']:
                if trade['isBuyer']:
                    this_coin['totle_costs'] += float(trade['quoteQty'])
                    this_coin['totle_amount'] += float(trade['qty'])
                else:
                    this_coin['realized_profit'] += float(trade['quoteQty'])
                    this_coin['totle_amount'] -= float(trade['qty'])
            # Convert timestamp to datatime
            for timestamp in this_coin['new_trade']:
                new_date = datetime.fromtimestamp((timestamp['time']) / 1000)
                timestamp['time'] = str(new_date).split(' ')[0]
            this_coin['unrealized_profit'] = recent_price * this_coin['totle_amount']
            this_coin['profit'] = this_coin['realized_profit'] + this_coin['unrealized_profit'] - this_coin[
                'totle_costs']
            return this_coin
        else:
            return False

    def get_asset(self):
        client = Client(self.api_key, self.secret_key)
        user_asset = client.get_account()['balances']
        user_own_asset = []
        for item in user_asset:
            if float(item['free']) > 0:
                user_own_asset.append(item)
        return user_own_asset


def home(request):
    return render(request, 'index.html', {'RQST_FROM_GECKO': RQST_FROM_GECKO})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'RQST_FROM_GECKO': RQST_FROM_GECKO})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                user_id = User.objects.get(username=request.POST['username']).id
                api_info = Website_users(user_id=user_id, api_key=request.POST['api_key'], secret_key=request.POST['secret_key'])
                api_info.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                return render(request, 'signup.html', {'RQST_FROM_GECKO': RQST_FROM_GECKO, 'error': 'That username has already been taken \n try another one.'})
        else:
            return render(request, 'signup.html', {'RQST_FROM_GECKO': RQST_FROM_GECKO, 'error': 'Password did not match.'})
    # Design from Bryan lin: https://github.com/bryanlin16899


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'RQST_FROM_GECKO': RQST_FROM_GECKO})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'RQST_FROM_GECKO': RQST_FROM_GECKO, 'error': 'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('dashboard')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def dashboard(request):
    user = GetUserInfo()
    try:
        user_key_info = Website_users.objects.get(user=request.user)
        user.api_key = user_key_info.api_key
        user.secret_key = user_key_info.secret_key
        if request.method == 'GET':
            return render(request, 'dashboard.html',
                          {
                           'RQST_FROM_GECKO': RQST_FROM_GECKO,
                           'this_coin': user.get_trades_info(),
                           'user_asset': user.get_asset()
                          })
        elif request.method == 'POST':
            new_symbol = request.POST.get('inputTicker')
            if user.get_trades_info(symbol=new_symbol):
                return render(request, 'dashboard.html',
                              {
                               'RQST_FROM_GECKO': RQST_FROM_GECKO,
                               'this_coin': user.get_trades_info(symbol=new_symbol),
                               'user_asset': user.get_asset()
                              })
            else:
                return render(request, 'dashboard.html',
                              {
                               'RQST_FROM_GECKO': RQST_FROM_GECKO,
                               'error': 'Invalid Ticker',
                               'user_asset': user.get_asset()
                              })
        else:
            return render(request, 'dashboard.html',
                          {
                           'RQST_FROM_GECKO': RQST_FROM_GECKO,
                           'this_coin': user.get_trades_info(),
                           'user_asset': user.get_asset()
                          })
    except BinanceAPIException:
        return render(request, 'dashboard.html',
                      {
                          'RQST_FROM_GECKO': RQST_FROM_GECKO,
                          'error': 'Your API KEY or SECRET KEY did not correct.',
                          'user_asset': user.get_asset()
                      })


@login_required
def change_api_key(request):
    user_key_info = Website_users.objects.get(user=request.user)
    api_key = user_key_info.api_key
    secret_key = user_key_info.secret_key
    if request.method == 'GET':
        return render(request, 'change_user_api_key.html', {'RQST_FROM_GECKO': RQST_FROM_GECKO, 'api_key': api_key, 'secret_key': secret_key})
    else:
        user_key_info.api_key = request.POST['api_key']
        user_key_info.secret_key = request.POST['secret_key']
        user_key_info.save()
        return redirect('dashboard')
