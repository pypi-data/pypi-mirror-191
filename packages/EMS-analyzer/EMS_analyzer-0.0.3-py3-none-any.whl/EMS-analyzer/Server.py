# import os
# os.add_dll_directory(r'C:\Users\kimyh\opencv\build\install\x64\vc16\bin')
# os.add_dll_directory(r'C:\opencv\build\x64\vc16\bin')
# os.add_dll_directory(r'C:\Program Files\VTK')
import cv2
import imagezmq
#import numpy as np
import time
#import timeit
# from PIL import Image
import traceback
#import threading
# import tensorflow as tf



# th=0

def port_split(ip_addr,hub,range,name_var_list):
    if hub==0:
        for i,var_n in enumerate(name_var_list):
            globals()[f"{var_n}"] =imagezmq.ImageHub(open_port=f"{ip_addr}:{range}{i}") 
    else:
        for i,var_n in enumerate(name_var_list):
            globals()[f"{var_n}"] =imagezmq.ImageSender(connect_to=f"{ip_addr}:{range}{i}",REQ_REP=False) 

def prediction_forward(h0, s0,cnt, class_name,model):
    for idx,h in enumerate(h0):
        rpi_name_tmp, images_tmp = globals()[h].recv_image()
        send_name_tmp, send_image_tmp,picked_image_tmp = Set_yolo(rpi_name_tmp
                                                                  ,images_tmp
                                                                  ,class_name
                                                                  ,model,cnt)
        globals()[h].send_reply(b'OK')
        Pub(send_name_tmp, send_image_tmp,picked_image_tmp,globals()[s0[idx]])

def init_yolo():
    # cfg='cfg/yolov4.cfg'
    # weights='cfg/yolov4.weights'
    # names='cfg/coco.names'
    
    cfg='cfg/fish_test.cfg'
    weights='cfg/fish.weights'
    names='cfg/fish.names'
    
    # cfg='cfg/trained_on_merge/yolo-fish-2.cfg'
    # weights='cfg/trained_on_merge/merge_yolo-fish-2.weights'
    # names='cfg/fish.names'

    # cfg='cfg/fish_test.cfg'
    # weights='cfg/yolov4-custom_last.weights'
    # names='cfg/custom.names'

    # cfg='cfg/yolov3-obj.cfg'
    # weights='cfg/yolov3-obj_30000.weights'
    # names='cfg/fish.names'

    net = cv2.dnn.readNet(cfg,weights)
    #net = cv2.cuda
    class_name = []
    with open(names, "r") as f:
        class_name = [line.strip() for line in f.readlines()]

    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416,416),scale=1/255, swapRB=True)
    return class_name,model
    
def Set_yolo(rpi_name, images,class_name,model,cnt):
    
    frame=images
    COLORS = [(255, 255, 0), (255, 0, 0),(0, 255, 255), (0, 255, 0)]
    #ret, frame = VideoSignal.read()
    h, w, c = frame.shape
    print(f'init_set :{h}x{w}x{c}')
    x=0;y=0
    picked_img=frame[y:y+h,x:x+w]
    conf_threshold=0.01
    nms_threshold=0.01
    classes, scores, boxes = model.detect(frame, conf_threshold, nms_threshold)
    #if classes:
    #print(classes, scores,boxes)
    label=''
    classid=0
    for (classid, score, box) in zip(classes,scores,boxes):
        color = COLORS[int(classid) % len(COLORS)]
        label = f"{class_name[classid]}-{score}"
        print("label===============",label)
        cv2.rectangle(frame, box, color,thickness=1)
        cv2.putText(frame, label, (box[0],box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,color, 1)
    t = time.localtime()
    print(t)
    current_time = time.strftime("%H-%M-%S", t)
    if len(classes)>0:
            cv2.imwrite(f"./label_img/t_11/{current_time}-{cnt}.jpg", frame)
    return rpi_name, frame, picked_img


def Pub(name, images, detect_data,sender):
    sender.send_image(name, images)
    
def init(ip_addr='tcp://192.168.1.3'
        ,h0=["image_hub0_0","image_hub0_1","image_hub0_2","image_hub0_3"]
        ,s0=["sender0_0","sender0_1","sender0_2","sender0_3"]
        ,img0=["image_origin0","image_origin1","image_origin2","image_origin3"]

        ,images=b''
        ,jpg_buffer=b''
        ,face_image=b''):
    
    port_split(ip_addr,0,566,h0)
    port_split(ip_addr,1,556,s0)
    return h0,s0

def main(class_name,model,h0,s0):
    cnt=0
    try:
        while True:
            # with tf.compat.v1.Session() as sess:
            start = time.time()
            prediction_forward(h0, s0,cnt,class_name, model)
            
            end = round(time.time()-start,3)
            second_start=time.time()
            cnt+=1
            second_end=round(time.time()-second_start,4)
            #print(f'{cnt}: Time for recevied a image: {end}sec, Time for aired a image: {second_end}sec')
    except(KeyboardInterrupt, SystemExit):
        print('Exit dut to keyboard interrupt')
    except Exception as ex:
        print('Traceback error:',ex)
        traceback.print_exc()
    finally:
        for h in h0:
            globals()[h].close()
        for s in s0:
            globals()[s].close()

if __name__ =="__main__":

    h0,s0=init()
    class_name, model=init_yolo()
    main(class_name,model,h0,s0)
