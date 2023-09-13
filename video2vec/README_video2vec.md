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
