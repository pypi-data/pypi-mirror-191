import os,sys
from PIL import Image
from PIL import ImageTk
import tkinter.font, tkinter.ttk
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import threading
import cv2
import traceback
import time 
import ftplib
import platform
import configparser
import logging

class Fk_viewer(object):
    
    def __init__(self,env):
        
        # logging.basicConfig(filename="recoding_file/em.log",filemode='w',
        #                     level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
        #                     datefmt="%m/%d/%Y %I:%M:%S %p %Z")
        self.env=env.upper()
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')
        self.file_name=""
        self.file_name_s=""
        self.path_file_name=""
        self.path_file_name_s=""
        self.path=self.config[self.env]['PATH']
        self.target_path=self.config[self.env]['TARGET_PATH']
        try:
            if self.env=="DEFAULT":
                self.view = cv2.VideoCapture(int(self.config[self.env]['VIDEOCAPTURE']))
            else:
                self.view = cv2.VideoCapture(self.config[self.env]['VIDEOCAPTURE'])
        except cv2.error as ex:
            logging.error(ex)
            time.sleep(5)
        w = round(self.view.get(cv2.CAP_PROP_FRAME_WIDTH)) # width
        h = round(self.view.get(cv2.CAP_PROP_FRAME_HEIGHT)) #height
        fps = self.view.get(cv2.CAP_PROP_FPS) #frame per second
        logging.info(f"Checking... for receivied IP camera info to being: ,{w},{h},{fps}")
        self.txt_idx=1
        self.image=None
        self.out=None
        self.t_img=None
        self.thread_seq=None
        self.thread_file_trans=None
        self.file_exist=False
        self.out_set=None
        self.num=0
        self.start_recoding()
  
    def start_recoding(self):
        # print("kkkkk")
        if self.thread_seq is None or not self.thread_seq.is_alive():
            self.thread_on=True
            self.out_set=True
            self.thread_seq=threading.Thread(target=self.start_recoding1, args=())
            # self.thread_seq.daemon=True
            self.thread_seq.start()
        # print("shit!!\n")
        if self.thread_file_trans is None or not self.thread_file_trans.is_alive():
            self.thread_file_trans=threading.Thread(target=self.file_conveyance, args=())
            # self.thread_file_trans.daemon=True
            self.thread_file_trans.start()

    def start_recoding1(self):
        ii=0
        while True:
            if self.out_set==False:
                break
            time.sleep(1)
            if self.thread_on==False:
                break
            if self.out is None or not self.out.isOpened():
                if self.t_img is None or not self.t_img.is_alive():
                    # logging.info(f"cnt: {ii+1}")
                    try:
                        if not self.view.isOpened():
                            if self.env=="DEFAULT":
                                self.view = cv2.VideoCapture(0)
                            else:
                                self.view = cv2.VideoCapture(self.config[self.env]['VIDEOCAPTURE'])
                    except cv2.error as ex:
                        logging.error(f'Traceback error: {ex},{traceback.print_exc()}')
                        # traceback.print_exc()
                    self.t_img = threading.Thread(target=self.sample_viewThread, args=())
                    # self.t_img.daemon =True
                    self.t_img.start()
                                
    def sample_viewThread(self):
        fr =[]
        idx=1
        mbyte_cnt=0
        snap_freq = int(self.config[self.env]['SNAP_FREQ'])
        setting_frame_cnt=int(self.config[self.env]['SETTING_FRAME_CNT'])
        (file_name, file_name_s,path_file_name,path_file_name_s)=self.setting_file_name()
        
        w = round(self.view.get(cv2.CAP_PROP_FRAME_WIDTH)) # width
        h = round(self.view.get(cv2.CAP_PROP_FRAME_HEIGHT)) #height
        if self.config[self.env]['FPS']=="AUTO":
            fps = self.view.get(cv2.CAP_PROP_FPS) #frame per second
        else: fps = int(self.config[self.env]['FPS_SET']) 
        codec_tmp=self.config[self.env]['CODEC']
        fourcc = cv2.VideoWriter_fourcc(*codec_tmp) #fourcc
        delay = round(1000/fps)
        logging.info(f"{file_name} Checking... for going to be saved file")
            
        if not self.view.isOpened() and not self.out.isOpened():
            logging.error("Check to IP camera states or File isn't opend!!")
            self.stop_recoding_btn()
        try:
            if self.out is None or not self.out.isOpened():
                if not self.out is None:
                    self.out.release()
                self.out = cv2.VideoWriter(
                    filename=path_file_name,
                    fourcc=fourcc,
                    # apiPreference=cv2.CAP_FFMPEG,
                    fps=float(fps),
                    frameSize=(w, h),
                    isColor=True)#path_file_name, fourcc, fps, (w,h))
                # logging.error(self.out.isOpened())
        except cv2.error as ex:
            logging.exception(f'Traceback error: {ex}, {traceback.print_exc()}')
            
        try:
            while True:
                ret, fr = self.view.read()
                if not ret:
                    fr=[]
                    self.view.release()
                    self.out.release()
                    break
                if ret and idx <=setting_frame_cnt and self.out_set==True:#self.out.isOpened():
                    self.update_progress(idx/setting_frame_cnt,file_name)
                    if self.out.isOpened():
                        self.out.write(fr)
                    else:
                        break
                    cv2.waitKey(delay=delay)
                else:
                    self.stop_recoding(file_name,file_name_s,path_file_name,path_file_name_s)
                    file_size=(os.path.getsize(path_file_name_s))/1024/1024
                    print(f'\nThe file {file_name}({round(file_size,2)}MB) saved sucessfully')
                    break
                idx+=1
            
        except(KeyboardInterrupt, SystemExit):
                logging.exception('Exit dut to keyboard interrupt')
        except Exception as ex:
            logging.exception(f'Traceback error: {ex}')
            traceback.print_exc()
        finally:
            #self.view.release()
            self.out.release()
            
    def setting_file_name(self):
        d=datetime.now()
        file_name= f"f{d.strftime('%Y%m%d%H%M%S')}.mp4"
        file_name_s= f"fc{d.strftime('%Y%m%d%H%M%S')}.mp4"
        self.file_name=file_name
        self.file_name_s=file_name_s
        self.path_file_name=os.path.join(self.path,file_name)
        self.path_file_name_s=os.path.join(self.path,file_name_s)
        
        path_file_name=os.path.join(self.path,file_name)
        path_file_name_s=os.path.join(self.path,file_name_s)
        return file_name,file_name_s,path_file_name,path_file_name_s       
    
    def stop_recoding_btn(self):
        self.thread_on=False
        self.out_set=False
            
    def stop_recoding(self,file_name,file_name_s,path_file_name,path_file_name_s):
        self.out.release()
        if platform.system()=="Windows":
            os.system(f"rename {path_file_name} {file_name_s}")    
        else: os.system(f"mv {path_file_name} {path_file_name_s}")
            
    def update_progress(self,progress,file_name):
        barLength = 10 # Modify this to change the length of the progress bar
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float"
        if progress < 0:
            progress = 0
            status = "Halt..."
        if progress >= 1:
            progress = 1
            status = "Done..."
        block = int(round(barLength*progress))
        text = " \r{3} is [{0}] {1}% in process {2}".format( "#"*block + "-"*(barLength-block),
                                                            round(progress*100,2), status,file_name)
        sys.stdout.write(text)
        sys.stdout.flush()
        
    def sumof_progress(self,num,total,file_tr_name):
        self.num = self.num+num
        # print(self.num)
        self.update_progress(self.num/total,file_tr_name)
  
    def file_conveyance(self):
        while True:
            try:
                time.sleep(1)
                # print("aaa")
                file_tmp=[]
                file_tmp=[f for (dirpath, dirnames, filenames) in os.walk(self.path) for f in filenames if "fc" in f]
                # print(len(file_tmp))
                if len(file_tmp):
                    logging.info(f"file_name : {file_tmp} and cnt:{len(file_tmp)}")
                if len(file_tmp):#self.file_exist:
                    file_tr_name=file_tmp[0]
                    #for file_tr_name in file_tmp:
                    try:
                        with ftplib.FTP() as session:
                            session.connect(self.config[self.env]['FTP_SERVER_IP'], 21) 
                            session.login(self.config[self.env]['FTP_ID'],
                                        self.config[self.env]['FTP_PASS'])

                            
                            file_path = os.path.join(self.path,file_tr_name)
                            
                            with open(file_path ,mode='rb') as uploadfile:
                                session.encoding='utf-8'
                                total=os.path.getsize(file_path)
                                # print(total)
                                # sent=0
                                session.storbinary("STOR " + f"{self.target_path}/{file_tr_name}",
                                                uploadfile,20480,
                                                callback=lambda sent: self.sumof_progress(len(sent),total,file_tr_name))
                                self.num=0
                            
                            try:
                                if platform.system()=="Windows":
                                    os.system(f"del {os.path.join(self.path,file_tr_name)} /F /Q")
                                else: os.system(f"rm {os.path.join(self.path,file_tr_name)}")
                                print(f"{file_tr_name} was transfered successfully.\n")
                    
                            except Exception as ex:
                                logging.exception(f'Traceback error: {ex}')
                                traceback.print_exc()
                    except(KeyboardInterrupt, SystemExit):
                        logging.exception('Exit dut to keyboard interrupt')
                    except Exception as ex:
                        logging.exception(f'Traceback error: {ex}')
                else:
                    pass
               
            except(KeyboardInterrupt, SystemExit):
                    logging.exception('Exit dut to keyboard interrupt')
            except Exception as ex:
                logging.exception(f'Traceback error: {ex}')
                traceback.print_exc()
                

if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) >= 2 else "DEFAULT"
    t = Fk_viewer(env)
