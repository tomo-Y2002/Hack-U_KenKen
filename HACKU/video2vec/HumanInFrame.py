import ultralytics
from ultralytics import YOLO
import numpy as np
import cv2



def HumanInFrame(frame:np.array)->bool:
    # モデル選択
    '''
    yolov8n.pt   処理:200ms/frame
    yolov8s.pt   処理:?/frame
    '''
    model = YOLO(f'yolov8n.pt')

    # 推論
    '''
    project : 保存先
    save : セグメンテーション結果を動画として保存するか
    '''
    results = model.predict(source = frame,
                            conf = 0.50,
                            name = 'my_predict',
                            save_txt = False,
                            save_conf = False,
                            retina_masks = False,
                            classes = 0,
                            exist_ok = True,
                            save = False)

    if len(results[0].boxes.cls) == 0:
        return False
    else :
        return True

if __name__=='__main__':
    frame = cv2.imread('/content/drive/MyDrive/HackU/data/test.jpg')
    print(HumanInFrame(frame))
