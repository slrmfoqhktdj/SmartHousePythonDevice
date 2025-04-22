
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
                    proc.terminate()
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        print("강제 종료 실행")
                        proc.kill()
                    finally:
                        proc.wait()
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

                    proc = proc_run()
            except json.JSONDecodeError:
                pass        



    finally:
        print("프로세스 종료 완료")


if __name__ == "__main__":
    run()