# 定義
# インポート
import os
import ultralytics
from ultralytics import YOLO
# from google.colab.patches import cv2_imshow
from PIL import Image 
import torch
import matplotlib.pyplot as plt
import numpy as np
import torch.nn as nn
from torchvision import transforms


# チェック
# display.clear_output()
# ultralytics.checks()

# Segmentation データ用のクラス
class SegData():
    def __init__(self, name, prob):
        self.name = name            # classname : int
        self.prob = prob            # prob of estimation : float
        self.area = []              # area of segmentation : list
        self.area_x = []
        self.area_y = []

    def add(self, x, y):
        self.area_x.append(x)
        self.area_y.append(y)
        self.area.append([x, y])

# シルエットのエッジの情報を保存するクラス
class SilhouetteEdge():
    def __init__(self, arr, width, height, edge_x, edge_y):
        self.width = width          #行列の幅
        self.height = height        #行列の高さ
        self.arr = arr              #行列 (最初は、中身がないものを持っているが、のちに計算を行う)
        self.edge_x = edge_x        #領域を囲むエッジのx座標 (重複なし, 一周できる順番)
        self.edge_y = edge_y        #領域を囲むエッジのy座標 (重複なし, 一周できる順番)

# GEI classの設定
class GEI():
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.arr = [[0 for i in range(width)] for j in range(height)]

    def aveBy(self, num:float):
        for y in range(self.height):
            for x in range(self.width):
                self.arr[y][x] /= num

    def image(self):
        arr_numpy = [[self.arr[y][x]*255 for x in range(self.width)] for y in range(self.height)]
        arr_numpy = np.array(arr_numpy, dtype=np.uint8)
        pil_img = Image.fromarray(arr_numpy)            # ここ本当はImage.fraomarrayにしたいけど、importで指定していた。
        # pil_img.save(f'{HOME}/test.jpg')
        plt.imshow(pil_img)

# エッジの補間アルゴリズム
def bresenham_line(x0, y0, x1, y1):
    # ブレゼンハムのアルゴリズム　ChatGPT出力
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points

# 重複なしの二次元リストを取得する関数 nkmkより
def get_unique_list(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

# 二次元配列を塗りつぶす関数 ChatGPT
'''
ちなみに、pythonでは二次元リストなどのイミュータブルなものは参照で渡されるから、
return arrとしなくていい
'''
def flood_fill(array, start_point, old_value, new_value, width, height):
    """
    Execute flood fill on a 2D array starting from a specific point.

    Parameters:
    - array: 2D numpy array
    - start_point: tuple (x, y)
    - old_value: value to be replaced
    - new_value: value to replace with
    - height: 行列の高さ y
    - width: 行列の幅 x
    """
    if array[start_point[1]][start_point[0]] != old_value:
        return

    stack = [start_point]
    while stack:
        x, y = stack.pop()
        if array[y][x] == old_value:
            array[y][x] = new_value
            if y > 0: stack.append((x, y-1))
            if y < height-1: stack.append((x, y+1))
            if x > 0: stack.append((x-1, y))
            if x < width-1: stack.append((x+1, y))

def video2vec(FILE_PATH, WEIGHT_PATH)->np.array:
    HOME, FILE_NAME = os.path.split(FILE_PATH)
    BASE_NAME, _ = os.path.splitext(FILE_NAME)

    #　定数の定義
    # HOME = '/content/drive/MyDrive/HackU/data'

    # モデル選択
    '''
    yolo8n-seg.pt   処理:30秒/90frames
    yolo8s-seg.pt   処理:1分/90frame
    '''
    model = YOLO(f'{HOME}/yolov8n-seg.pt')

    # 推論
    '''
    project : 保存先
    save : セグメンテーション結果を動画として保存するか
    '''
    # 実行時は以下のようにして、labelsを消すこと
    results = model.predict(source = f'{HOME}/{FILE_NAME}',
                            project = f'{HOME}',
                            conf = 0.50,
                            name = 'my_predict',
                            save_txt = True,
                            save_conf = True,
                            retina_masks = True,        
                            classes = 0,
                            exist_ok = True,
                            save = False)

    # 動画のフレームの中に、人間が映っているフレームはどこにあるかを判定する
    """
    インデックスを1スタートで記述していることに注意
    画面の両端いっぱいに人間が移動できることを仮定している。
    これはカメラ固定ならば達成できる条件。
    もし高度なことをするのならば、pose estimationを用いて
    keypoints の箇所を監視することで、人間が完全に写っているフレームを把握する。
    """
    frame_human = []
    for idx, result in enumerate(results):
        if len(result.boxes.cls) == 1:
            xleft = result.boxes.xyxyn[0][0]       #左端のx座標
            xright = result.boxes.xyxyn[0][2]      #右端のx座標
            if xleft > 0.05 and xright < 0.95:
                frame_human.append(idx+1)
    print('---frame_human---\n', frame_human)


    # 検出物体の情報を取得 動画 実装時には変更必須
    '''
    Objs_timeseq : 要素がObjsのリスト
    num_frame_accum : 一秒間のフレーム枚数　30fpsを仮定
    clip_name : 保存される動画ファイルの名前　
    '''
    Objs_timeseq = []
    num_frame_accum = 30
    clip_name = BASE_NAME     #walk1.mp4ならwalk1
    for idx in frame_human[0:num_frame_accum]:        # frame_accumの最初から30枚を取得
        Objs = []
        path = '{}/my_predict/labels/{}_{}.txt'.format(HOME, clip_name, idx)       #このpathは写真を変えるごとに変更が必要
        with open(path) as f:
            for s_line in f:
                s_list = s_line[:-1]        #各行の最後の文字が\nなので除去している。
                s_list = s_line.split()
                name = int(s_list[0])
                prob = float(s_list[-1])
                obj = SegData(name, prob)
                for i in range(1, len(s_list)-1, 2):    # yolov8-seg の出力txtの構造から、idx 0:class, -1:probでその間に領域
                    obj.add(float(s_list[i]), float(s_list[i+1]))     # segmentation 領域の座標を追加
                Objs.append(obj)
        Objs_timeseq.append(Objs)

    # 検出結果のチェック　動画
    frame_height, frame_width = results[0].orig_shape   #これは必要
    ## 以下はデプロイ時にコメントアウト推奨
    # plt.figure(dpi = 200)
    # for Objs in Objs_timeseq:               # フレームごとの取得
    #     for obj in Objs:                    # 一枚のフレーム内のオブジェクトの取得
    #         if obj.name == 0:               # 人間かの判断(まあ人間だけ選んでいるんだけども)
    #             x = []
    #             y = []
    #             for i in range(len(obj.area)):
    #                 x.append(obj.area_x[i]*frame_width)
    #                 y.append((1 - obj.area_y[i])*frame_height)
    #             x.append(obj.area_x[0]*frame_width)
    #             y.append((1 - obj.area_y[0])*frame_height)
    #             plt.plot(x, y, linewidth=1)

    # plt.xlim(0, frame_width)
    # plt.ylim(0, frame_height)
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.show()



    # セグメンテーション結果について、任意のサイズでbounding boxで切り出す 動画版
    frame_ratio = frame_width / float(frame_height)
    arr_height = 128    # 保存する行列の高さ
    arr_width = 0       # 保存する行列の幅
    SilhouetteEdges_timeseq = []

    for Objs in Objs_timeseq:
        SilhouetteEdges = []           # 行列を保存するリスト(一つの画像に複数人がいた場合にも対応)

        for obj in Objs:
            if obj.name == 0:
                x = []
                y = []
                for i in range(len(obj.area)):
                    x.append(obj.area_x[i]*frame_ratio)    # アスペクト比を守って存在
                    y.append(obj.area_y[i])

                # obj の領域を把握(bounding box)
                xmax = max(x)
                xmin = min(x)
                ymax = max(y)
                ymin = min(y)
                obj_width = xmax - xmin
                obj_height = ymax - ymin
                obj_ratio = obj_width / obj_height
                # results[0].boxes.xyxyn[0]でも出た

                # 行列の幅の導出
                arr_width = int(arr_height * obj_ratio)

                # 行列の定義
                arr = [[0 for i in range(arr_width)] for j in range(arr_height)]

                # 行列に挿入する作業
                edge_points = []        #エッジの点を保存するリスト 一時的 %%
                for i in range(len(x)):
                    arr_x = int((x[i]-xmin)*(arr_width-1)/obj_width)        # index out of range対策で-1している
                    arr_y = int((y[i]-ymin)*(arr_height-1)/obj_height)
                    edge_points.append([arr_x, arr_y])      # %%
                    arr[arr_y][arr_x] = 1

                # SilhouetteEdgeクラスのインスタンス化 とエッジの座標抽出
                edge_points = get_unique_list(edge_points)
                edge_x = [i[0] for i in edge_points]
                edge_y = [i[1] for i in edge_points]
                # edge_x.append(edge_points[0][0])
                # edge_y.append(edge_points[0][1])
                s = SilhouetteEdge(arr, arr_width, arr_height, edge_x, edge_y)
                SilhouetteEdges.append(s)

                # 画像にしてみる　
                ##実行時コメントアウト推奨
                # arr_numpy = np.array(arr, dtype=np.uint8) * 255
                # # print(arr_numpy.shape)
                # pil_img = Image.fromarray(arr_numpy)            # ここ本当はImage.fraomarrayにしたいけど、importで指定していた。
                # # pil_img.save(f'{HOME}/test.jpg')
                # plt.figure()
                # plt.imshow(pil_img)

        SilhouetteEdges_timeseq.append(SilhouetteEdges)
    # plt.show()

    # シルエットのエッジの欠けているところをつなぐ　動画
    for SilhouetteEdges in SilhouetteEdges_timeseq:
        for S in SilhouetteEdges:
            num_points = len(S.edge_x)
            idx = 0                                     #途中で要素の数を足すので、for文のiではインデックスにならない
            for i in range(num_points):
                # print(i, idx)
                x0 = S.edge_x[idx]
                y0 = S.edge_y[idx]
                x1 = S.edge_x[(idx+1) % num_points]
                y1 = S.edge_y[(idx+1) % num_points]
                points_between = bresenham_line(x0, y0, x1, y1)     #点と点の間の線形補間　:　点のtupleが返ってくる
                for d_idx, point in enumerate(points_between[1:len(points_between)-1]):                  # (x0, y0), (x1, y1)は除けているはず
                    x = point[0]
                    y = point[1]
                    S.arr[y][x] = 1
                    S.edge_x.insert(idx+d_idx+1, x)
                    S.edge_y.insert(idx+d_idx+1, y)

                idx += (len(points_between)-1)      # 挿入した分だけidxにインクリメント
                num_points += (len(points_between)-2)   # 追加した分だけnum_pointsを増やす

    # シルエットのエッジがかけていないかチェック 動画版　
    ## 以下実行時コメントアウト推奨
    # for SilhouetteEdges in SilhouetteEdges_timeseq:
    #     for s in SilhouetteEdges:
    #         # 画像にしてみる
    #         arr_numpy = np.array(s.arr, dtype=np.uint8) * 255
    #         pil_img = Image.fromarray(arr_numpy)            # ここ本当はImage.fraomarrayにしたいけど、importで指定していた。
    #         # pil_img.save(f'{HOME}/test.jpg')
    #         plt.figure()
    #         plt.imshow(pil_img)


    # シルエットの塗りつぶし 動画
    for SilhouetteEdges in SilhouetteEdges_timeseq:
        for s in SilhouetteEdges:
            start_point = (s.width//2, s.height//2)         # シルエット画像の中心が0であると仮定 →これがずれているとミスる
            old_value = 0
            new_value = 1
            flood_fill(s.arr, start_point, old_value, new_value, s.width, s.height)

    # 塗りつぶせているかをチェック 動画
    ## 以下実行時コメントアウト推奨
    # for SilhouetteEdges in SilhouetteEdges_timeseq:
    #     for s in SilhouetteEdges:
    #         # 画像にしてみる
    #         arr_numpy = np.array(s.arr, dtype=np.uint8) * 255
    #         pil_img = Image.fromarray(arr_numpy)            # ここ本当はImage.fraomarrayにしたいけど、importで指定していた。
    #         # pil_img.save(f'{HOME}/test.jpg')
    #         plt.figure()
    #         plt.imshow(pil_img)

    # GEIの生成
    """
    SilhouetteEdgesの中に一人しかいない前提で作っているので、
    もし動画の中に人間が二人以上いたら、
    GEIの作り方が変になってしまう
    """
    gei = GEI(arr_height, 88)     #arr_height = 128である前提
    for SilhouetteEdges in SilhouetteEdges_timeseq:
        if (len(SilhouetteEdges) == 1):
            for s in SilhouetteEdges:
                pad_x = (gei.width-s.width)//2
                if (gei.height == s.height):
                    for y in range(s.height):
                        for x in range(s.width):
                            if(x+pad_x < gei.width):
                                gei.arr[y][x+pad_x] += s.arr[y][x]
                else:
                    print("error:GEITとsilhouetteの高さがあっていません")
                    break
        else:
            print("error:複数の物体が検出されました。対応不可です")
            break

    gei.aveBy(len(SilhouetteEdges_timeseq))

    # GEIT画像のチェック
    gei.image()

    # ベクトル生成のモデル定義
    '''
    0.2m parram
    '''
    GEINet2 = nn.Sequential(
        nn.Conv2d(1, 18, kernel_size=3, stride=1, padding=1),
        nn.BatchNorm2d(18),
        nn.ReLU(inplace=True),
        nn.Conv2d(18, 18, kernel_size=3, stride=1, padding=1),
        nn.BatchNorm2d(18),
        nn.ReLU(inplace=True),
        nn.MaxPool2d(kernel_size=2, stride=2),

        nn.Conv2d(18, 45, kernel_size=3, stride=1, padding=1),
        nn.BatchNorm2d(45),
        nn.ReLU(inplace=True),
        nn.Conv2d(45, 45, kernel_size=3, stride=1, padding=1),
        nn.BatchNorm2d(45),
        nn.ReLU(inplace=True),
        nn.MaxPool2d(kernel_size=2, stride=2),

        nn.AdaptiveAvgPool2d(1),
        nn.Flatten(),
        nn.Dropout(0.27),
        nn.Linear(45, 1024),
        nn.ReLU(inplace=True),
        nn.Linear(1024, 124)
    )

    # モデルのパラメタ読み込み
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = GEINet2
    model.to(device)
    model.load_state_dict(torch.load(WEIGHT_PATH, map_location=device))
    # model.load_state_dict(torch.load(f'/content/drive/MyDrive/HackU/data/weight/model_{0.834}.pth', map_location=device))

    # ベクトル抽出の関数定義
    def extract_features(model, input_data, layer_index):
        """
        指定されたモデルの特定の層から特徴量を抽出します。

        :param model: モデル (nn.Module)
        :param input_data: モデルの入力データ (torch.Tensor)
        :param layer_index: 特徴量を取り出したい層のインデックス (int)
        :return: 抽出された特徴量 (torch.Tensor)
        """

        # 出力を保存するリスト
        features = []
        # フック関数
        def hook_fn(module, input, output):
            features.append(output)
        # 指定された層にフックをアタッチ
        hook = model[layer_index].register_forward_hook(hook_fn)
        # モデルを評価モードにする
        model.eval()
        # データをモデルに供給
        with torch.no_grad():
            model(input_data)
        # フックを削除
        hook.remove()
        # 最初の特徴量の出力を返す
        return features[0]

    #ベクトル抽出
    gei_np = (np.array(gei.arr, dtype=np.float32))
    gei_tensor = transforms.ToTensor()(gei_np)
    features = extract_features(model, gei_tensor.reshape(1,1,128,88), -3)
    print(features.shape)       #関数化して、numpy配列をリターンするようにするとか
    return features.numpy()

if __name__=='__main__':
    weight_path = f"C:/Users/denjo/Desktop/HackU/data/model_{0.848}.pth"
    video_path = "C:/Users/denjo/Desktop/HackU/data/shimizu.MP4"
    vector = video2vec(video_path, weight_path)
    print(type(vector))
    print(vector.shape)
