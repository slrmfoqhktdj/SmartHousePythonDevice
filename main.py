# import asyncio
# import websockets
# import json

# async def hello():
#     uri = "ws://192.168.0.7:8299/ws/device01"
#     async with websockets.connect(uri,subprotocols=["sh1.0"],ping_interval=60,ping_timeout=(60*9)/10) as websocket:
#         # name = input("What's your name? ")

#         # await websocket.send(name)
#         # print(f"> {name}")

#         # greeting = await websocket.recv()
#         # print(f"< {greeting}")

#         while True:
#             p = json.loads('{"PING":0}')
#             await websocket.send(p)
#             print("Send ping")

#             msg =  await websocket.recv()
#             print(msg)
#             msgjson = json.dumps(msg)
#             print(msgjson)

#             await asyncio.sleep(5)


# asyncio.get_event_loop().run_until_complete(hello())




import json
from websocket import WebSocketApp, WebSocketConnectionClosedException
import logging
import time
import uuid
from pytz import timezone
from datetime import datetime
import schedule
import threading


#기기 id
deviceid = "device01"

#자동수동       - True, 1: 자동    False,0 : 수동
auto = True

#센서값
temp_val = 13
humi_val = 60
co2_sensor_val = 15
ph_ec_sensor_val = 35

#onoff 여부
comp_onoff = False
pump_onoff = False
ffan_onoff = False
efan_onoff = False
aircon_onoff = False
co2creator_onoff = False
led_onoff = False



#cctv url
cctv_url = "https://www.naver.com/"

#예약 여부
appoint_compump_onoff = False
appoint_ffan_onoff = False
appoint_efan_onoff = False
appoint_aircon_onoff = False
appoint_co2creator_onoff = False
appoint_led_onoff = False

#예약 시간
appoint_compump_startTime = "03:14"
appoint_compump_stopTime = "03:14"
appoint_ffan_startTime = "03:14"
appoint_ffan_stopTime = "03:14"
appoint_efan_startTime = "03:14"
appoint_efan_stopTime = "03:14"
appoint_aircon_startTime = "03:14"
appoint_aircon_stopTime = "03:14"
appoint_co2creator_startTime = "03:14"
appoint_co2creator_stopTime = "03:14"
appoint_led_startTime = "03:14"
appoint_led_stopTime = "03:14"


def create_unique_id():
        unique_id = uuid.uuid4()
        return str(unique_id)

# def PeriodicReportFuntion():
#         while True:
#                 schedule.run_pending()
#                 time.sleep(1)


# PeriodicReport = schedule.every(1).seconds.do(PeriodicReportFuntion)
# PeriodicReportThread = threading.Thread(target=PeriodicReportFuntion)

def getNowTime():
        return datetime.now().astimezone(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')

def on_message(ws, message):
        data = json.loads(message)  # JSON 데이터 파싱
        logging.info(data)

        global auto

        global comp_onoff
        global pump_onoff
        global ffan_onoff 
        global efan_onoff 
        global aircon_onoff 
        global co2creator_onoff 
        global led_onoff 

        global appoint_compump_onoff
        global appoint_ffan_onoff
        global appoint_efan_onoff
        global appoint_aircon_onoff 
        global appoint_co2creator_onoff 
        global appoint_led_onoff
        global appoint_compump_startTime
        global appoint_compump_stopTime
        global appoint_ffan_startTime
        global appoint_ffan_stopTime 
        global appoint_efan_startTime 
        global appoint_efan_stopTime 
        global appoint_aircon_startTime 
        global appoint_aircon_stopTime 
        global appoint_co2creator_startTime 
        global appoint_co2creator_stopTime
        global appoint_led_startTime 
        global appoint_led_stopTime 

        if auto :   # 자동일때만 명령듣기
                        if data[2]=="CMDCOMP":# 컴프 onoff
                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": data[3]['value']}])
                                ws.send(senddata)
                        elif data[2]=="CMDPUMP":#펌프 onoff
                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": data[3]['value']}])
                                ws.send(senddata)
                        elif data[2]=="CMDFFAN":#유동팬 onoff
                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": data[3]['value']}])
                                ws.send(senddata)
                        elif data[2]=="CMDEFAN":#배기팬 onoff
                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": data[3]['value']}])
                                ws.send(senddata)
                        elif data[2]=="CMDAIRCON":#냉난방기 onoff
                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": data[3]['value']}])
                                ws.send(senddata)
                        elif data[2]=="CMDCO2CREATOR": #co2발생기 onoff
                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": data[3]['value']}])
                                ws.send(senddata)
                        elif data[2]=="CMDLED":#LED onoff
                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": data[3]['value']}])
                                ws.send(senddata)
                        elif data[2]=="CMDALLONOFF":#모든 onoff (웹)
                                onoff_id = data[3]['id']
                                
                                if onoff_id == deviceid :
                                        onoff_key = data[3]['key'].split(",")
                                        onoff_value = data[3]['value'].split(",")
                                        for k in range(len(onoff_key)) :
                                                v_val = (onoff_value[k] == 'true')

                                                if onoff_key[k] == "comp_val" :         # 컴프  onoff
                                                        if comp_onoff  != v_val :    #기존 값과 다르면 실행
                                                                comp_onoff = v_val
                                                elif onoff_key[k] == "pump_val" :       #펌프 onoff
                                                        if pump_onoff  != v_val :    #기존 값과 다르면 실행
                                                                pump_onoff = v_val
                                                elif onoff_key[k] == "f_fan_val" :      #유동팬 onoff
                                                        if ffan_onoff  != v_val :    #기존 값과 다르면 실행
                                                                ffan_onoff = v_val
                                                elif onoff_key[k] == "e_fan_val" :      #배기팬 onoff
                                                        if efan_onoff  != v_val :    #기존 값과 다르면 실행
                                                                efan_onoff = v_val
                                                elif onoff_key[k] == "aircon_val" :     #냉난방기 onoff
                                                        if aircon_onoff  != v_val :    #기존 값과 다르면 실행
                                                                aircon_onoff = v_val
                                                elif onoff_key[k] == "co2_creator_val" :#co2발생기 onoff
                                                        if co2creator_onoff  != v_val :    #기존 값과 다르면 실행
                                                                co2creator_onoff = v_val
                                                elif onoff_key[k] == "led_val" :        #LED onoff
                                                        if led_onoff  != v_val :    #기존 값과 다르면 실행
                                                                led_onoff = v_val
                                                   
                                        senddata = json.dumps([3,data[1],{"id":deviceid,"result": True}])
                                        ws.send(senddata)
                                else :
                                        senddata = json.dumps([3,data[1],{"id":deviceid,"result": False}])
                                        ws.send(senddata)
                        elif data[2]=="ACMDCOMPUMP":#예약 컴프펌프 onoff
                                if not data[3]['startt'] and not data[3]['stopt'] and data[3]['onoff'] :
                                        senddata = json.dumps([3,data[1],{"id":deviceid,"result": False}])
                                        ws.send(senddata)
                                        return

                                appoint_compump_startTime = data[3]['startt']
                                appoint_compump_stopTime = data[3]['stopt']
                                appoint_compump_onoff = data[3]['onoff']

                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": True}])
                                ws.send(senddata)
                        elif data[2]=="ACMDFFAN":#예약 유동팬 onoff
                                if not data[3]['startt'] and not data[3]['stopt'] and data[3]['onoff'] :
                                        senddata = json.dumps([3,data[1],{"id":deviceid,"result": False}])
                                        ws.send(senddata)
                                        return

                                appoint_ffan_startTime = data[3]['startt']
                                appoint_ffan_stopTime = data[3]['stopt']
                                appoint_ffan_onoff = data[3]['onoff']

                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": True}])
                                ws.send(senddata)
                        elif data[2]=="ACMDEFAN":#예약 배기팬 onoff
                                if not data[3]['startt'] and not data[3]['stopt'] and data[3]['onoff'] :
                                        senddata = json.dumps([3,data[1],{"id":deviceid,"result": False}])
                                        ws.send(senddata)
                                        return

                                appoint_efan_startTime = data[3]['startt']
                                appoint_efan_stopTime = data[3]['stopt']
                                appoint_efan_onoff = data[3]['onoff']

                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": True}])
                                ws.send(senddata)
                        elif data[2]=="ACMDAIRCON":#예약 냉난방기 onoff
                                if not data[3]['startt'] and not data[3]['stopt'] and data[3]['onoff'] :
                                        senddata = json.dumps([3,data[1],{"id":deviceid,"result": False}])
                                        ws.send(senddata)
                                        return

                                appoint_aircon_startTime = data[3]['startt']
                                appoint_aircon_stopTime = data[3]['stopt']
                                appoint_aircon_onoff = data[3]['onoff']

                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": True}])
                                ws.send(senddata)
                        elif data[2]=="ACMDCO2CREATOR": #예약 co2발생기 onoff
                                if not data[3]['startt'] and not data[3]['stopt'] and data[3]['onoff'] :
                                        senddata = json.dumps([3,data[1],{"id":deviceid,"result": False}])
                                        ws.send(senddata)
                                        return

                                appoint_co2creator_startTime = data[3]['startt']
                                appoint_co2creator_stopTime = data[3]['stopt']
                                appoint_co2creator_onoff = data[3]['onoff']

                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": True}])
                                ws.send(senddata)
                        elif data[2]=="ACMDLED":#예약 LED onoff
                                if not data[3]['startt'] and not data[3]['stopt'] and data[3]['onoff'] :
                                        senddata = json.dumps([3,data[1],{"id":deviceid,"result": False}])
                                        ws.send(senddata)
                                        return

                                appoint_led_startTime = data[3]['startt']
                                appoint_led_stopTime = data[3]['stopt']
                                appoint_led_onoff = data[3]['onoff']

                                senddata = json.dumps([3,data[1],{"id":deviceid,"result": True}])
                                ws.send(senddata)
                
        # 자동수동 상관없는 명령

        if data[2]=="AppointList": #예약정보 리스트
                senddata = json.dumps([3,data[1],{"id":deviceid,"auto":1 if auto else 0,"items": [{"name":"compump","startt":appoint_compump_startTime,"stopt":appoint_compump_stopTime,"onoff":appoint_compump_onoff},
                                                                                                        {"name":"ffan","startt":appoint_ffan_startTime,"stopt":appoint_ffan_stopTime,"onoff":appoint_ffan_onoff},
                                                                                                        {"name":"efan","startt":appoint_efan_startTime,"stopt":appoint_efan_stopTime,"onoff":appoint_efan_onoff},
                                                                                                        {"name":"aircon","startt":appoint_aircon_startTime,"stopt":appoint_aircon_stopTime,"onoff":appoint_aircon_onoff},
                                                                                                        {"name":"co2creator","startt":appoint_co2creator_startTime,"stopt":appoint_co2creator_stopTime,"onoff":appoint_co2creator_onoff},
                                                                                                        {"name":"led","startt":appoint_led_startTime,"stopt":appoint_led_stopTime,"onoff":appoint_led_onoff}]}])
                ws.send(senddata)

def on_connect(ws):
        logging.info("connected!")  # 연결됨 메시지 출력
        # 연결 시 서버에 보낼 메시지 전송
        # ws.send('[{"ticket": "test" }, {"type": "trade", "codes": ["KRW-BTC" ] }, {"format": "DEFAULT" } ]')
        # datauuid = create_unique_id()
        # logging.info(datauuid)
        # senddata = json.dumps([2,datauuid,"REPORTCOMP",{"id":"device01","value":comp_onoff}]) # 컴프 보고
        # senddata = json.dumps([2,datauuid,"REPORTPUMP",{"id":"device01","value":pump_onoff}])   # 펌프 보고
        # senddata = json.dumps([2,datauuid,"REPORTFFAN",{"id":"device01","value":ffan_onoff}])   # 유동팬 보고
        # senddata = json.dumps([2,datauuid,"REPORTEFAN",{"id":"device01","value":efan_onoff}])   # 배기팬 보고
        # senddata = json.dumps([2,datauuid,"REPORTAIRCON",{"id":"device01","value":aircon_onoff}])       # 냉난방기 보고
        # senddata = json.dumps([2,datauuid,"REPORTCO2CREATOR",{"id":"device01","value":co2creator_onoff}])       # co2발생기 보고
        # senddata = json.dumps([2,datauuid,"REPORTLED",{"id":"device01","value":led_onoff}])     # led 보고
        # senddata = json.dumps([2,datauuid,"REPORTTEMP",{"id":"device01","value":temp_val}])     # 온도 보고
        # senddata = json.dumps([2,datauuid,"REPORTHUMI",{"id":"device01","value":humi_val}])     # 습도 보고
        # senddata = json.dumps([2,datauuid,"REPORTCO2SENSOR",{"id":"device01","value":co2_sensor_val}])  # co2센서 보고
        # senddata = json.dumps([2,datauuid,"REPORTPHECSENSOR",{"id":"device01","value":ph_ec_sensor_val}])       # ph_ec센서 보고
        # senddata = json.dumps([2,datauuid,"REPORTAuto",{"id":"device01","value":1 if auto else 0}])  # 자동 수동 바뀔때 
        # ws.send(senddata)
        
        # 연결 시 boot 상태 보고
        senddata = json.dumps([2,create_unique_id(),"BOOTDEVICE",{"id":deviceid , "comp":comp_onoff , "pump":pump_onoff , "temp": temp_val, "humi":humi_val , "f_fan":ffan_onoff , "e_fan":efan_onoff , "aircon":aircon_onoff , "co2_sensor":co2_sensor_val,"co2_creator":co2creator_onoff , "ph_ec_sensor": ph_ec_sensor_val, "led":led_onoff , "cctv":cctv_url , "auto":auto}])  
        ws.send(senddata)

        # 시간별 정기보고 
        # senddata = json.dumps([2,create_unique_id(),"REPORTALLSENSOR",{"id":deviceid , "value":{"temp": temp_val, "humi":humi_val ,"co2_sensor":co2_sensor_val,"ph_ec_sensor": ph_ec_sensor_val , "time": getNowTime() } }])  
        # ws.send(senddata)




def on_error(ws, err):
        logging.error(err)  # 에러 발생 시 에러 메시지 출력


def on_close(ws, status_code, msg):
        logging.info("closed!")  # 연결 종료 시 메시지 출력


def run_websocket():
        while True:
                ws_app = WebSocketApp("ws://192.168.0.7:8299/ws/device01",
                                on_message=on_message,
                                on_error=on_error,
                                
                                on_close=on_close)
                ws_app.on_open = on_connect
                ws_app.subprotocols = ["sh1.0"]
                ws_app.run_forever(ping_interval=0, ping_timeout=30)
                time.sleep(10)  # 연결이 끊어진 후 재시도 전 대기 시간

try:
        logging.basicConfig(level=logging.DEBUG)
        run_websocket()
except KeyboardInterrupt:
        logging.info("프로그램이 사용자에 의해 중단되었습니다.")
        
