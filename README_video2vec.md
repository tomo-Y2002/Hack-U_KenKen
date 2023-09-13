## video2vec.py

```
def video2vec(FILE_PATH, WEIGHT_PATH)-> np.array:
```
#### 引数
FILE_PATH : 動画ファイルが存在するパス。絶対パスを推奨
WEIGHT_PATH : モデルの重みファイルが存在するパス。ファイル名は同梱している```model_0.832.pth```

#### 返値
np.array : (1, 1024)の1024次元のベクトルが、numpy.ndarrayの形式で返ってくる。

#### 今後の変更
・　入力をカメラ直結にする(バックエンドと要相談)  
・　処理の高速化
