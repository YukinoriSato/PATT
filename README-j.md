# PATT

PATT: Polyhedral compilation-based AuTo Tile size optimizer

Copyright (C) 2018-2019, Yukinori Sato All Rights Reserved.




英語版のドキュメントは[こちら](README.md).


PATT (Polyhedral compilation-based AuTo Tile size optimizer) は、計算ループをタイリングして、タイリングサイズを最適化するプログラムです。


技術的な詳細は、[ACM TACO 2019に掲載された論文](https://dl.acm.org/citation.cfm?id=3293449)をご覧ください.



## PATTの構成

+ src ： PATT プログラム
  + src/patt.py：PATT 起動プログラム
  + src/modes/*_modes.py：各モードにおける最適化プログラム
  + src/util/*.py：コンパイル、計測を実行するプログラム
+ polybench4.2_mainNit ： ベンチマークプログラム
+ TACO2018 ： サンプルプログラム



## PATTのシステム概略図

![Overview](patt_overview.jpg)



## PATTの利用環境

PATT を利用するには、llvm + clang + polly、python2 が必要です。論文のデータは、LLVM5.0.0を用いています。

環境変数に、llvm の bin のパスを追加します。  
`ex. $ export PATH=llvm5.0/build/bin:$PATH`


## PATTのダウンロード

   $ git clone https://github.com/YukinoriSato/PATT



## PATT の実行方法 その1 ローカルでの実行

サンプルプログラム1に移動します。

    $ cd TACO2018/haswell

CPU スレッド数、PATT プログラム先、ベンチマークプログラム先を設定します。

```
$ vi run_all.sh
threads=8
CC="PATT/src/patt.py"
SRC_DIR="PATT/polybench4.2_mainNit"
```

サンプルプログラムを実行します。

    $ ./run_all.sh


## PATT の実行方法 その2 リモートでの実行

リモートで実行する計算機は、ssh によるリモート実行を行います。  
リモートで実行する計算機では、ファイル共有などで、PATT 以下のディレクトリがホストと同じようにアクセス可能でなければなりません。

サンプルプログラム2に移動します。

    $ cd TACO2018/remote-ssh

CPU スレッド数、リモート実行するホスト名、PATT プログラム先、ベンチマークプログラム先を設定します。

```
$ vi run_all.sh
threads=8
remote=hostname
CC="PATT/src/patt.py"
SRC_DIR="PATT/polybench4.2_mainNit"
```

サンプルプログラムを実行します。

    $ ./run_all.sh


## run_all.sh の実行内容

サンプルプログラム run_all.sh は、以下の処理を実行します。

+ kernels_info.sh の読み込み：ベンチマークプログラム情報の取得
+ 計測実行条件設定ファイルの作成：ファイル名は、export PATT_SETTING_FILE="patt_setting"で設定
+ src/patt.py の実行：タイリングサイズ最適化プログラムの実行
  + 下記部分で、patt.py が実行される。kernel は、ベンチマーク名。rep回繰り返し実行。<br>
    `${CC} ${CC_OPTION} ${SRC1} ${SRC2} &> ./result/${kernel}/${mode}_${rep}`
  + psize は、Polybench のデータクラス。
  + ベンチマークプログラムコンパイル時に、--polly-tile-sizes で、タイルサイズを指定しています。
+ ./extract_data.py の実行：ログファイルから、計測条件と時間を抜粋して、ログファイル_extracted に記録
+ ./align_this_time.py の実行：ログファイル_extracted から、計測時間のみを抽出して、ログファイル_extracted_aligned に記録


## PATT の実行結果

PATT のログファイル。

+ result / カーネル / モード _ 繰り返し番号：最適化実行ログファイル
+ result / カーネル / モード _ 繰り返し番号 _extracted：計測条件と実行時間ログ
+ result / カーネル / モード _ 繰り返し番号 _extracted_aligned：実行時間ログ

実行時間は、'[measure] this time' で出力されます。9999 は、ベストタイムより遅い、9997 はエラーです。  
--polly-tile-sizes は、指定したタイルサイズです。

