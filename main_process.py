# import asyncio
# import json

# async def ex_websocket():
#         async for ws in websockets.connect("ws://192.168.0.7:8299/ws/device01",ping_interval=None,subprotocols=["sh1.0"],ping_timeout=30):
#                 try:
#                         await ws.send(json.dumps([2,create_unique_id(),"BOOTDEVICE",{"id":deviceid , "comp":comp_onoff , "pump":pump_onoff , "temp": temp_val, "humi":humi_val , "f_fan":ffan_onoff , "e_fan":efan_onoff , "aircon":aircon_onoff , "co2_sensor":co2_sensor_val,"co2_creator":co2creator_onoff , "ph_ec_sensor": ph_ec_sensor_val, "led":led_onoff , "cctv":cctv_url , "auto":auto}]))
#                         while True:
#                                 response = await ws.recv()
#                                 print(f"Recevice msg : {response}")
#                 except websockets.ConnectionClosed:
#                         continue


# asyncio.get_event_loop().run_until_complete(ex_websocket())



import json
from websocket import WebSocketApp
import logging
import time
import uuid
from pytz import timezone
from datetime import datetime
import schedule
# import asyncio
import requests
import os
import threading
from dateutil import parser
from glob import glob
from natsort import natsorted
from multiprocessing.connection import Client
import sys

#기기 id
deviceid = "device01"

#웹소켓
ws_app = None

#웹소켓 쓰레딩
thread_websocket = None
#정기기록 및 보고 쓰레딩
thread_schedule_report = None

#쓰레드 전역변수 충돌 방지
lock = threading.Lock()

#웹소켓 서버 주소
websocket_server_url = "ws://192.168.0.7:8299/ws/"

#로그 업로드 서버 주소 
logupload_server_url = "http://localhost:5025/"

#로그 파일 저장소 주소
log_file_url = "./logs/"

#로그 업로드 서버 주소 
program_update_server_url = "http://localhost:5025/"

#업데이트 파일 저장소 주소
update_file_url = "./update_programs/"

#업데이트 명령어 커멘드
upgradeProgram = "upgradeProgram"


#자동수동       - True, 1: 자동    False,0 : 수동
auto = True

#센서값
temp_val = 15
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
#현재 시간 포멧 리턴
def getNowTime():
        return datetime.now().astimezone(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')

#로그파일 이름 포멧 리턴
def getScheduleLogFIleName():
        return datetime.now().astimezone(timezone('Asia/Seoul')).strftime('%Y_%m_%d.txt')

#로그파일 기록 시간 포멧 리턴
def getScheduleLogFIleTime():
        return datetime.now().astimezone(timezone('Asia/Seoul')).strftime('%H:%M:%S')

# iso 8601 날짜 포멧을 datetime 포멧으로 변경
def getFindLogFileDate(isostr):
        return parser.isoparse(isostr).astimezone(timezone('Asia/Seoul'))



def on_message(ws, message):
        data = json.loads(message)  # JSON 데이터 파싱
        logging.info(data)
        print(data, flush=True)

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
        elif data[2]=="CMDLOGUPLOAD":#로그 업로드
                id = data[3]['id']
                upload_location = data[3]['location']
                log_starttime = getFindLogFileDate(data[3]['startTime'])
                log_stoptime = getFindLogFileDate(data[3]['stopTime'])
                 
                # logging.info(str(log_starttime)+","+str(log_stoptime))
                # 날짜에 해당하는 로그 파일 고르기
                selected_file_list = uploadfile_selected_returnlogfilelist(log_starttime,log_stoptime)

                # 파일 합치기
                log_file_name = uploadfile_create_returnName(selected_file_list,log_starttime,log_stoptime)

                # 파일 업로드
                with open("./"+log_file_name,'rb') as files :
                        upload = {'upload_log': files}
                        requests.post(logupload_server_url+upload_location,files=upload)

                # 파일 삭제
                os.remove("./"+log_file_name)
                
                senddata = json.dumps([3,data[1],{"fileName":log_file_name}])
                ws.send(senddata)
        elif data[2]=="CMDPRGUPLOAD":# 프로그램 업데이트
                id = data[3]['id']
                update_location = data[3]['location']
                file_name = update_location.split("/")[-1]

                # logging.info("update_location : "+update_location)
                # logging.info("file_name : "+file_name)

                #파일 다운로드
                result_status = updatefile_download(update_location,file_name)

                senddata = json.dumps([3,data[1],{"id":deviceid,"result":result_status}])
                ws.send(senddata)

                #entire.py에 업데이트 명령
                print(json.dumps({"cmd":upgradeProgram,"path":update_file_url+file_name}), flush=True)

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
        
        # 연결 시 boot 상태 보고 및 등록
        senddata = json.dumps([2,create_unique_id(),"BOOTDEVICE",{"id":deviceid , "comp":comp_onoff , "pump":pump_onoff , "temp": temp_val, "humi":humi_val , "f_fan":ffan_onoff , "e_fan":efan_onoff , "aircon":aircon_onoff , "co2_sensor":co2_sensor_val,"co2_creator":co2creator_onoff , "ph_ec_sensor": ph_ec_sensor_val, "led":led_onoff , "cctv":cctv_url , "auto":auto}])  
        ws.send(senddata)

def on_error(ws, err):
        logging.error(err)  # 에러 발생 시 에러 메시지 출력
        write_log("서버 에러 : "+str(err))

def on_close(ws, status_code, msg):
        logging.info("closed!")  # 연결 종료 시 메시지 출력

        lock.acquire()
        global ws_app

        ws_app = None
        lock.release()
        write_log("서버 종료")



# 로그 기록 
def write_log(msg):
        #폴더 없을시 생성
        make_folder(log_file_url)

        if not os.path.exists("".join([log_file_url,getScheduleLogFIleName()])):
                logging.info("not exist file!")
                open("".join([log_file_url,getScheduleLogFIleName()]),"w")

        with open("".join([log_file_url,getScheduleLogFIleName()]),"a") as wt:
                wt.write(getScheduleLogFIleTime()+" - "+msg+'\n')


# 업로드 파일에 속할 파일 리스트 반환
def uploadfile_selected_returnlogfilelist(log_starttime, log_stoptime):
        selected_file_list = []
        file_list = glob(log_file_url+'*.txt')
        file_list = natsorted(file_list)        # 파일 정렬
        for file in file_list:
                # logging.info(os.path.basename(file))  # 파일명만 추려오기
                file_date = datetime.strptime(os.path.basename(file),"%Y_%m_%d.txt").astimezone(timezone('Asia/Seoul'))
                # logging.info(file_date) # 파일명을 datetime으로 
                       
                if log_starttime <= file_date <= log_stoptime:
                        selected_file_list.append(file)
        
        return selected_file_list


# 업로드 파일 생성 및 이름 반환
def uploadfile_create_returnName(selected_file_list,log_starttime, log_stoptime):
        log_file_name = "&&".join([deviceid,log_starttime.strftime('%Y%m%d'),log_stoptime.strftime('%Y%m%d')])+".txt"
        with open("./"+log_file_name, 'w') as outfile:
                for filename in natsorted(selected_file_list):
                         with open(filename) as file:
                                outfile.write(os.path.basename(filename)+'\n')
                                for line in file:
                                        outfile.write(line)
        return log_file_name

# 파일 업데이트
def updatefile_download(update_location,file_name):

        # 업데이트 파일 없으면 생성
        make_folder(update_file_url)

        # 파일 다운로드
        with open(update_file_url+file_name,'wb') as files :
                response = requests.get(program_update_server_url+update_location)
                files.write(response.content)

                if not response.ok :
                        return False
        
        return True

# 정기보고 스케줄 실행 함수   
def schedule_report():
        logging.info("schedule_report!")

        write_log(",".join(["온도:"+str(temp_val),"습도:"+str(humi_val),"co2센서:"+str(co2_sensor_val),"ph_ec센서:"+str(ph_ec_sensor_val)]))


        # 시간별 정기보고 
        try:
                if not(ws_app is None) :
                        logging.info("report!")
                        senddata = json.dumps([2,create_unique_id(),"REPORTALLSENSOR",{"id":deviceid , "value":{"temp": temp_val, "humi":humi_val ,"co2_sensor":co2_sensor_val,"ph_ec_sensor": ph_ec_sensor_val , "time": getNowTime() } }])  
                        ws_app.send(senddata)
        except Exception as e:
                logging.info(e)

#  스케줄 실행
def run_schedule():
        while True:
                schedule.run_pending()
                time.sleep(1)

# 웹소켓 연결
def run_websocket():
        global ws_app

        ws_app = WebSocketApp(websocket_server_url+deviceid,
                        on_message=on_message,
                        on_error=on_error,
                                
                        on_close=on_close)
        ws_app.on_open = on_connect
        ws_app.subprotocols = ["sh1.0"]
        ws_app.run_forever(ping_interval=0, ping_timeout=30, reconnect=10)

# 로그 및 다운로드 폴더가 존재하지 않을 경우 생성
def make_folder(foldername):
        if not os.path.exists(foldername[:-1]):
                os.makedirs(foldername[:-1])
                
def main():        
        try:
                logging.basicConfig(level=logging.DEBUG)

                write_log("기기 프로그램 시작")

                #정기보고 스케줄 등록
                schedule.every().hour.at("00:10").do(schedule_report)
                # schedule.every(2).seconds.do(schedule_report)
                
                
                global thread_websocket
                global thread_schedule_report

                #쓰레드 등록
                thread_websocket = threading.Thread(target=run_websocket)
                thread_schedule_report = threading.Thread(target=run_schedule)

                thread_websocket.start()
                thread_schedule_report.start()

                logging.info("업데이트 버전 1 ")
                


                
        except Exception as e:
                write_log("메인 프로그램 에러 : "+str(e))
                logging.info("프로그램이 사용자에 의해 중단되었습니다.")


        

if __name__ == "__main__":
        main()
        
