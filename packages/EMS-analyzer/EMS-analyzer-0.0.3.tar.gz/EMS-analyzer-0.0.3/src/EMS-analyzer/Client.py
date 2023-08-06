#from imutils.video import VideoStream
# import os
# os.add_dll_directory(r'C:\Users\kimyh\opencv\build\install\x64\vc16\bin')
# os.add_dll_directory(r'C:\opencv\build\x64\vc16\bin')
import imagezmq
import cv2
import traceback
import sys

# ip_addr='tcp://192.168.1.3'
# input_image='D:\955.LINC3.0\img\IMG_1517.MP4'
# output_image='D:\955.LINC3.0\img\All_detectingIMG_1500.avi'

def port_split(ip_addr,hub,range,name_var_list):
    if hub==0:
        for i,var_n in enumerate(name_var_list):
            globals()[f"{var_n}"] \
            =imagezmq.ImageHub(open_port=f"{ip_addr}:{range}{i}", REQ_REP=False) 
    else:
        for i,var_n in enumerate(name_var_list):
            globals()[f"{var_n}"] \
            =imagezmq.ImageSender(connect_to=f"{ip_addr}:{range}{i}") 

def img_split(image_orign, img_name_list,quadrant):
    #match quadrant:
    if quadrant ==0: #1/4
        globals()[f"{img_name_list[quadrant]}"]\
            =image_orign[0:int(len(image_orign)*0.8),0:int(len(image_orign[0])*0.8)]
    if quadrant ==1: #2/4
        globals()[f"{img_name_list[quadrant]}"]\
        =image_orign[0:int(len(image_orign)*0.8),int(len(image_orign[0])*0.2):]
    if quadrant ==2: #3/4
        globals()[f"{img_name_list[quadrant]}"]\
        =image_orign[int(len(image_orign)*0.2):,0:int(len(image_orign[0])*0.8)]
    if quadrant ==3: #4/4
        globals()[f"{img_name_list[quadrant]}"]\
        =image_orign[int(len(image_orign)*0.2):,int(len(image_orign[0])*0.2):]
    if quadrant >=4:
        for idx,_ in enumerate(img_name_list):
            img_split(image_orign, img_name_list,idx)
        
def prediction_img(img0,s0,h0):

    for i, s in enumerate(s0):
        globals()[s].send_image(f"1/4_3_{i}", globals()[img0[i]])
    for i in h0:
            image_name0_0, image_tmp = globals()[i].recv_image()
            # out.write(image_tmp)
            print(image_tmp.shape)
            cv2.imshow(f"1/4_{i}", image_tmp)
        

def main(ip_addr='tcp://192.168.1.3',input_image='D:\955.LINC3.0\img\IMG_1517.MP4'):
    # ip_addr='tcp://192.168.1.3'
    input_image='D:\955.LINC3.0\img\IMG_1517.MP4'
    # output_image='D:\955.LINC3.0\img\All_detectingIMG_1500.avi'
    
    h0=["image_hub0_0","image_hub0_1","image_hub0_2","image_hub0_3"]
    port_split(ip_addr,0,556,h0)
    s0=["sender0_0","sender0_1","sender0_2","sender0_3"]
    port_split(ip_addr,1,566,s0)

    picam = cv2.VideoCapture(input_image) #0) #VideoStream(usePiCamera=True).start()

    # videoFileName = input_image+"out"
    w = round(picam.get(cv2.CAP_PROP_FRAME_WIDTH)) # width
    h = round(picam.get(cv2.CAP_PROP_FRAME_HEIGHT)) #height
    fps = picam.get(cv2.CAP_PROP_FPS) #frame per second
    fourcc = cv2.VideoWriter_fourcc(*'DIVX') #fourcc
    delay = round(1000/fps)		

    # out = cv2.VideoWriter(videoFileName, fourcc, fps, (w,h))
    # if not (out.isOpened()):
    #     print("File isn't opend!!")
    #     picam.release()
    #     sys.exit()


    #time.sleep(2.0)  # allow camera sensor to warm up
    try:
        while True:  # send images as stream until Ctrl-C
            ret,image_orign = picam.read(0)
            print("image_orign.shap: ",image_orign.shape, len(image_orign),len(image_orign[0]))
            if ret:
                img_=["image_origin0","image_origin1","image_origin2","image_origin3"]
                img3_=["image_origin3_0","image_origin3_1","image_origin3_2","image_origin3_3"]
                img3_2_=["image_origin3_2_0","image_origin3_2_1","image_origin3_2_2","image_origin3_2_3"]
                img3_2_1_=["image_origin3_2_1_0","image_origin3_2_1_1","image_origin3_2_1_2","image_origin3_2_1_3"]
                img_split(image_orign, img_, 0)
                img_split(globals()[img_[0]],img3_ , 3)
                img_split(globals()[img3_[3]],img3_2_ , 4)
                # img_split(globals()[img3_2_[3]],img3_2_1_ , 4)
                #prediction_img(img_,s0,h0)
                #prediction_img(img3_,s0,h0)
                prediction_img(img3_2_,s0,h0)
                
                # cv2.imshow("image_origin",globals()[img3_[2]])
                cv2.waitKey(delay)  # wait until a key is pressed
                if cv2.waitKey(delay) == 27:
                    break
            else:
                print("ret is false")
                break
    except(KeyboardInterrupt, SystemExit):
        print('Exit dut to keyboard interrupt')
    except Exception as ex:
        print('Traceback error:',ex)
        traceback.print_exc()
    finally:
        picam.release()
        # out.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    main()