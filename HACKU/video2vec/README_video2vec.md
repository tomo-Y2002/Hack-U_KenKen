## video2vec.py
```video2vec```関数に、動画ファイルのパスと、モデルの重みファイルのパスを渡して実行すれば、ベクトルが返ってくる
```
def video2vec(FILE_PATH, WEIGHT_PATH)-> np.array:
```
#### パッケージのインストール
```
pip install ultralytics
pip install --upgrade ultralytics
pip install Pillow torch torchvision matplotlib numpy 
```

#### 引数
**FILE_PATH** str: 動画ファイルが存在するパス。絶対パスを推奨  
**WEIGHT_PATH** str: モデルの重みファイルが存在するパス。ファイル名は同梱している```model_0.832.pth```

#### 返値
np.array : (1, 1024)の1024次元のベクトルが、numpy.ndarrayの形式で返ってくる。

#### 注意
二回目以降の実行では、```{HOME}/video.mp4```として動画を保存している場合、
```
rm -r {HOME}/my_predict/labels
```
みたいな感じで、labelsディレクトリをそのまま削除する必要がある。
同じファイル名の動画を複数回作成する時の動作として、各フレームの人間の位置を書き**加えて**いくので、
どんどん人間が追加されて行ってしまい誤作動につながる。

#### 今後の変更
・　入力をカメラ直結にする(バックエンドと要相談)  
・　処理の高速化


## HumanInFrame.py
人間がフレーム中にいるかどうかを返す関数
```
def HumanInFrame(frame:np.array)->bool:
```
#### 引数
**frame**  np.array: cv2でフレームを取得した結果を入力として利用可能

#### 返値
bool : 人がいたらTrue, いなかったらFalse

#### 注意
単純な実装なので、顔だけ写っていてもconfidenceが0.5以上なら人間と判断されるので、
結構敏感かも
敏感すぎたら、conf = 0.5の所を0.8とか0.9とかにしてもよいかも

