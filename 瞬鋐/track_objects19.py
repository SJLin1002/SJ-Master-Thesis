import os
# comment out below line to enable tensorflow logging outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from core.config import cfg
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as misc
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from imutils.video import FPS
# deep sort imports
from deep_sort import preprocessing, nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
#from easytello import tello
from time import sleep
from threading import Thread
from djitellopy import Tello
#KMeans
from sklearn.cluster import KMeans
#from sklearn_extra.cluster import KMedoids
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn import datasets
from matplotlib import markers
import KeyPressModule as kp
import pygame

#myTello = tello.Tello()
#print(myTello.get_battery())
#myTello.streamon() # Turning on stream
#sleep(15)
#myTello.streamoff()

kp.init()
tello = Tello()
tello.connect(False)   #連線空拍機
print("電量:")
print(tello.get_battery())
tello.streamoff()      #關閉空拍機鏡頭
tello.streamon()       #開啓空拍機鏡頭
sleep(5)  #  等待鏡頭初始化
print("5秒後鏡頭初始化...") 

flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags.DEFINE_string('weights', './checkpoints/yolov4-416',
                    'path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_string('video', './data/japan.mp4', 'path to input video or set to 0 for webcam')
flags.DEFINE_string('output', None, 'path to output video')
flags.DEFINE_string('output_format', 'MJPG', 'codec used in VideoWriter when saving video to file, MJPG or XVID')
flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags.DEFINE_float('score', 0.50, 'score threshold')
flags.DEFINE_boolean('dis_cv2_window', False, 'disable cv2 window during the process') # this is good for the .ipynb
flags.DEFINE_boolean('info', False, 'show detailed info of tracked objects')
flags.DEFINE_boolean('count', False, 'count objects being tracked on screen')

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 40

    if kp.getKey("LEFT"):lr = -speed
    elif kp.getKey("RIGHT"):lr = speed


    if kp.getKey("UP"):fb = speed
    elif kp.getKey("DOWN"):fb = -speed
    
    if kp.getKey("w"):ud = speed
    elif kp.getKey("s"):ud = -speed

    if kp.getKey("d"):yv = speed
    elif kp.getKey("a"):yv = -speed

    if kp.getKey("e"):yv = tello.land()   #無人機降落    
    #if kp.getKey("e"):yv = tello.takeoff()#起飛囉

    return [lr , fb ,ud ,yv]


def main(_argv):
    max_cosine_distance = 0.4
    nn_budget = None
    nms_max_overlap = 1.0

    carbox = dict() # { "key": [] }
    x1 = []
    x2 = []
    #UAV_Location
    UAV_Center = (475,350)
    UAV_Centerup = int(475)
    UAV_Centerright = int(350)

    #Vehicle_Location
    C_Center = (0,0) 
    C_CenterX = 0
    C_CenterY = 0

    #UAV_Move
    Vehicle_distance = 0
    UAVmove_UpAndDown = int(0)
    UAVmove_RightAndLeft = int(0)
    tello.left_right_velocity = 0
    tello.up_down_velocity= 0

    with open("data/classes/tracking.names", "r", encoding='utf-8') as f:
        tracked_classes = f.read().strip().split("\n")

    # read in all class names from config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)
    
    # initialize deep sort model
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)
    # calculate cosine distance metric
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    # initialize tracker
    tracker = Tracker(metric)

    # load configuration for object detector
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
    input_size = FLAGS.size
    video_path = FLAGS.video

    # load tflite model if flag is set
    if FLAGS.framework == 'tflite':
        interpreter = tf.lite.Interpreter(model_path=FLAGS.weights)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        print(input_details)
        print(output_details)
    # otherwise load standard tensorflow saved model
    else:
        saved_model_loaded = tf.saved_model.load(FLAGS.weights, tags=[tag_constants.SERVING])
        infer = saved_model_loaded.signatures['serving_default']

    # begin video capture 開始讀取影像
    try:
        
        cap = cv2.VideoCapture(tello.get_udp_video_address())
        #cap = cv2.VideoCapture(tello.get_frame_read().frame)
        #vid = cv2.VideoCapture(int(video_path))
        #cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
    except:
        vid = cv2.VideoCapture(video_path)

    out = None

    # get video ready to save locally if flag is set
    '''
   if FLAGS.output:
        # by default VideoCapture returns float instead of int
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
        out = cv2.VideoWriter(FLAGS.output, codec, fps, (width, height))
        '''
    frame_num = 0
    #grabbed, frame = vid.read()
    grabbed, frame = cap.read()
    fps = FPS().start()
    #tello.takeoff()#起飛囉
    
    # while video is running
    while grabbed:
        print(tello.get_battery())
        if not grabbed:
            print("Cannot receive frame")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # 轉換成灰階
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 轉換成灰階
        frame = cv2.medianBlur(frame, 5)  
        gray = cv2.medianBlur(frame, 5)                  # 模糊化去除雜訊
        image = Image.fromarray(frame)

        frame_num +=1
        frame_size = frame.shape[:2]
        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        start_time = time.time()

        # run detections on tflite if flag is set
        if FLAGS.framework == 'tflite':
            interpreter.set_tensor(input_details[0]['index'], image_data)
            interpreter.invoke()
            pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
            # run detections using yolov3 if flag is set
            if FLAGS.model == 'yolov3' and FLAGS.tiny == True:
                boxes, pred_conf = filter_boxes(pred[1], pred[0], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
            else:
                boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
        else:
            batch_data = tf.constant(image_data)
            pred_bbox = infer(batch_data)
            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=FLAGS.iou,
            score_threshold=FLAGS.score
        )

        # convert data to numpy arrays and slice out unused elements
        num_objects = valid_detections.numpy()[0]
        bboxes = boxes.numpy()[0]
        bboxes = bboxes[0:int(num_objects)]
        scores = scores.numpy()[0]
        scores = scores[0:int(num_objects)]
        classes = classes.numpy()[0]
        classes = classes[0:int(num_objects)]

        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, width, height
        original_h, original_w, _ = frame.shape
        bboxes = utils.format_boxes(bboxes, original_h, original_w)

        # store all predictions in one parameter for simplicity when calling functions  為簡單起見，在調用函數時將所有預測存儲在一個參數中
        pred_bbox = [bboxes, scores, classes, num_objects]
        names = []
        deleted_indx = []
        for i in range(num_objects):
            class_indx = int(classes[i])
            class_name = class_names[class_indx]
            if class_name not in tracked_classes:
                deleted_indx.append(i)
            else:
                names.append(class_name)
        names = np.array(names)
        count = len(names)
        if FLAGS.count:
            cv2.putText(frame, "Objects being tracked: {}".format(count), (5, 35), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 255, 0), 2)
            print("Objects being tracked: {}".format(count))
        # delete detections that are not in tracked_classes
        bboxes = np.delete(bboxes, deleted_indx, axis=0)
        scores = np.delete(scores, deleted_indx, axis=0)

        # encode yolo detections and feed to tracker  編碼 yolo 檢測並提供給跟踪器
        features = encoder(frame, bboxes)
        detections = [Detection(bbox, score, class_name, feature) for bbox, score, class_name, feature in zip(bboxes, scores, names, features)]

        #initialize color map 初始化顏色映射
        cmap = plt.get_cmap('tab20b')
        colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]

        # run non-maxima supression 運行非最大抑制
        boxs = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        classes = np.array([d.class_name for d in detections])
        indices = preprocessing.non_max_suppression(boxs, classes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]   

        #持續飛行
        tello.send_rc_control( 0 ,0 , 0 , 0 )  
          
        #UAV移動
        #vals = getKeyboardInput()
        #tello.send_rc_control(vals[0],vals[1],vals[2],vals[3])

        # Call the tracker 呼叫追蹤
        tracker.predict()
        tracker.update(detections)

        # update tracks 更新追蹤#

        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue 
            bbox = track.to_tlbr()
            class_name = track.get_class()
            
        #中心點#

            cx = int ((bbox[0]+bbox[2])/2)
            cy = int ((bbox[1]+bbox[3])/2)

        #顯示Vehicles中心點#
            #cv2.circle(frame, (cx, cy), 8, (1, 227, 254), -1)

        #無人機中心點
            cv2.circle( frame, UAV_Center, 10, (255, 150, 0), -1)
        
        #紀錄偵測到的車輛中心點位置/如果以記錄過該車量則改為更新座標#

            carbox[track.track_id] = {'x': cx, 'y': cy}
            
            if( len(carbox)>4):
                carbox.clear()

            #print(carbox)

            data = [[value['x'], value['y']]for _, value in carbox.items()]
            #print(data)

       #k-means分群
        
            try:
                
                Short_distance = 9999
                #vehicle = len(KM.labels_)
                vehicle = len(data)
                print("number of vehicles: "+ str(vehicle))
                
                if(vehicle == 1):
                    C_Center  = (cx,cy)
                    print("Vehicle only one!")

                if(vehicle == 2):
                    Vehicle_distance = float(((data[0][0]-data[1][0])**2 + (data[0][1]-data[1][1])**2)**0.5) 
                    x1 = data[0]
                    x2 = data[1]
                    C_CenterX = int((x1[0]+x2[0])/2)
                    C_CenterY = int((x1[1]+x2[1])/2)
                    C_Center  = (C_CenterX,C_CenterY)
                    print(C_Center)

                if(vehicle > 2):

                    KM = KMeans(n_clusters=2,init='random',max_iter=vehicle*10,n_init=10,tol=0.0001)
                    KM.fit(data)
                    #KM.predict(carbox)
                    #n_clusters:k值
                    #init: ‘random’ / ‘k-means++’ /自行給定
                    #max_iter:最多迭代次數
                    #tol:中心點誤差忍受 (最好不要設0)
                    #random_state:隨機種子
                    #print(KM.labels_)

                    for i in range(0,vehicle):
                        if(KM.labels_[i]==0):
                            for j in range(0,vehicle):
                                if(KM.labels_[j]==1):
                                    #print(data[i])
                                    #print(data[j])
                                    Vehicle_distance = float(((data[i][0]-data[j][0])**2 + (data[i][1]-data[j][1])**2)**0.5)
                                    #print(a) 
                                    if(Short_distance > Vehicle_distance):
                                        x1 = data[i]
                                        x2 = data[j]
                                        #print(x1)
                                        #print(x2)
                                        Short_distance = Vehicle_distance
                    C_CenterX = int((x1[0]+x2[0])/2)
                    C_CenterY = int((x1[1]+x2[1])/2)
                    C_Center  = (C_CenterX,C_CenterY)
                    #print(C_CenterX)
                    #print(C_CenterY)
                    print("Center: " + str(C_Center))

            except:
                print('Some thing wrong!')
                    
        #分群後中心點
            cv2.circle( frame, C_Center, 8, (0, 255, 0), -1)

        #移動判斷
            UAVmove_RightAndLeft = int(C_CenterX - UAV_Centerright)
            UAVmove_UpAndDown = int(C_CenterY - UAV_Centerup)
            
            #print("X須移動 "+ str(UAVmove_RightAndLeft))
            #print("Y須移動 "+ str(UAVmove_UpAndDown))
            print(" ")
            
            
        # draw bbox on screen 在屏幕上繪製 bbox
            color = colors[int(track.track_id) % len(colors)]
            color = [i * 255 for i in color]
            color  = (123,104,238) #固定邊框顏色
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1]-30)), (int(bbox[0])+(len(class_name)+len(str(track.track_id)))*17, int(bbox[1])), color, -1)
            #cv2.putText(frame, class_name + "-" + str(track.track_id),(int(bbox[0]), int(bbox[1]-10)),0, 0.75, (255,255,255),2)
            cv2.putText(frame, class_name, (int(bbox[0]), int(bbox[1]-10)),0, 0.75, (255,255,255),2)

        # if enable info flag then print details about each track   如果啟用信息標誌，則打印有關每個軌道的詳細信息
            if FLAGS.info:
                print("Tracker ID: {}, Class: {},  BBox Coords (xmin, ymin, xmax, ymax): {}".format(str(track.track_id), class_name, (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))))
        
        result = np.asarray(frame)
        result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        fps.update()
        #cv2.waitKey(15)

        if not FLAGS.dis_cv2_window:
            #cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
            cv2.namedWindow("result", cv2.WINDOW_FREERATIO)
            cv2.imshow("result", result)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                tello.land() #無人機降落 
                break
        # if output flag is set, save video file 如果設置了輸出標誌，則保存視頻文件
        if FLAGS.output:
            out.write(result)
        grabbed, frame = cap.read()

    cv2.destroyAllWindows() # 關閉視窗和連接
    tello.streamoff()   #停止影像串流
    tello.end  #斷開連線
    fps.stop()
    print("Elasped time: {:.2f}".format(fps.elapsed()))
    print("FPS: {:.2f}".format(fps.fps()))

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
