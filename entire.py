
# 유닉스 기반 통신법
# import logging
# import os


# FIFO_FILENAME = './fifo-test'

# def main():        
#     logging.basicConfig(level=logging.DEBUG)
#     logging.info("child start!")

#     if not os.path.exists(FIFO_FILENAME):
#         os.mkfifo(FIFO_FILENAME)
#         if os.path.exists(FIFO_FILENAME):
#             fp_fifo = open(FIFO_FILENAME, "r")
#             i = 0
#             while True:
#                 with open(FIFO_FILENAME, 'r') as fifo:
#                     data = fifo.read()
#                     line = data.split('\n')
#                     for str in line:
#                         i = i+1
#                         print(str + "%4d" % i)   

# from multiprocessing.connection import Listener  
import zipfile  
import subprocess
import main_process
import os
import logging
import json
import time

def proc_terminate(proc): # 프로세스 main_process.py 종료
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        print("강제 종료 실행")
        proc.kill()
        proc.wait()

def proc_run(): # 프로세스로 main_process.py 실행
    return subprocess.Popen(['python','main_process.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text= True)

def run():
    logging.basicConfig(level=logging.DEBUG)
    
    proc = proc_run()

    try:
        while True:
            line = proc.stdout.readline()
            line = line.strip()
            print("receive msg : ", line)

            try:
                msg = json.loads(line)
                logging.info("data : "+ str(msg["cmd"]))

                if msg["cmd"] == main_process.upgradeProgram:
                    proc_terminate(proc)

                    with zipfile.ZipFile(msg["path"]) as zip_file :
                        #업데이트 파일 다운로드시 자신의 파일을 제외한 모든 파일 받기
                        ignore_file_name = os.path.basename(__file__)
                        for file_names in zip_file.namelist():
                            if file_names != ignore_file_name:
                                zip_file.extract(member=file_names,path="./")
                        
                        # 모든 파일 한번에 받기
                        # zip_file.extractall(path="./")
                        main_process.write_log("프로그램 업데이트")

                    # 파일 삭제
                    os.remove(msg["path"])
                    time.sleep(1)
                    proc = proc_run()
                    time.sleep(1)


                elif msg["cmd"] == main_process.rebootsoftware:
                    main_process.write_log("소프트웨어 재부팅을 요청했습니다.")
                    
                    proc_terminate(proc)

                    time.sleep(1)
                    proc = proc_run()
                    time.sleep(1)

                    

                elif msg["cmd"] == main_process.reboothardware:
                    main_process.write_log("하드웨어 재부팅을 요청했습니다.")
                    
                    proc_terminate(proc)
                    try:
                        result = subprocess.run(['sudo', 'reboot'], check=True, capture_output=True, text=True)
                        main_process.write_log("하드웨어 재부팅 : "+ str(result))
                    except subprocess.CalledProcessError as e:
                        main_process.write_log("하드웨어 재부팅 오류 : "+ str(e))
                        time.sleep(1)
                        proc = proc_run()
                        time.sleep(1)

            except json.JSONDecodeError:
                pass        



    finally:
        print("프로세스 종료 완료")


if __name__ == "__main__":
    run()