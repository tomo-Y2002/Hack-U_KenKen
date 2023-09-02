# Hack-U_KenKen
チームKenKenのレポジトリです。

9/2　風澤

プロジェクト名HACKU,アプリ名hoyouとおきます

hoyou内にurls.pyを立てて、HACKU/urls.pyにincludeする。(hoyou内のurls.pyをいじる)

プロジェクト内にHTMLをまとめるtemplatesというフォルダをつくった

HTMLでは一応メイン用にhome.htmlをまず作成
```
path('', views.home, name="home"),
```

人のデータベースへの登録のためにmodelsのクラスの作成(写真はできたらやります)


adminのsuperuser

名前/kenken

email/kenken@gmail.com

password/hackukenken


PersonクラスにKoki Mitukeを登録してみました

動画と同時に通った人、物を認証し結果を示すrealtime.htmlを作り、viewsにrealtime関数を作った(まだテスト段階)→出力は今の所は名前のみ(写真はあと回し、もし必要そうなら加える)




人の登録のフォームのためにforms.py,person_register.htmlを作った。必要な情報、属性については後々改善する(forms.pyはなくてもいける)