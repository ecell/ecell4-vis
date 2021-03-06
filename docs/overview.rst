============
概要
============

ec4vis パッケージは、E-Cell System Version 4に対する可視化統合環境です。
ec4vis には、下記の機能が備わっています。

#. 可視化統合環境の操作画面となる、クロスプラットフォームな GUI。
#. 可視化対象データの操作を行うためのファイルエクスプローラ。
#. データに対する修飾・可視化を行うためのパイプラインシステムと、パイプラインエディタ。
#. データを可視化するためのビジュアライザフレームワーク。
#. ソフトウェアを拡張するためのプラグインシステム。


可視化統合環境
=================

ec4vis の可視化統合環境は、主に データソース、パイプライン、インスペクタ、ビジュアライザという概念で説明できます。

データソースは、処理対象のデータの場所です（データ本体ではなく、データの場所を表す識別子です）。
ファイルシステムやデータベース、ネットワーク上のサーバのポートなどが、データソースになりえます。

パイプラインは、可視化対象のデータを処理するためのフローです。パイプラインは、一つ以上のノードと呼ばれる要素で構成された有向グラフです。
パイプライン上のノードは、ルートを親とするツリー上の構造になっています（一つの親ノードに複数の子ノードを連結できるので、パイプラインは分岐してツリー構造になることがあります）。
ノードは親のノードに対して可視化対象のデータを要求し、親のノードは子ノードからの要求に応じてデータを提供します。
各ノードは、親から受け取ったデータに対して、何らかの処理を行えます。
ツリーの始点には、ルートノードと呼ばれるノードが存在し、ルートノードから、データソースの現在の値を取り出せます。

インスペクタとビジュアライザは、パイプライン上のノードの状態を表示するための機能です。これらの二つは、機能はほとんど同じですが、GUI上の役割で区別しています。
インスペクタは、ノードの状態を検査したり、調整したりするためのものです。例えば、ある処理を行うノードが、処理の際に使うパラメタを設定したり、現在使っているパラメタを表示したりするのは、インスペクタの役目です。
ビジュアライザは、ノードの保持しているデータを可視化するためのものです。ビジュアライザには、ユーザが可視化結果として見たいものだけを表示します。


プラグインシステム
=====================

ec4vis には、プラグインによって機能を拡張する仕組みがあります。
プラグインは、Python のモジュールまたはパッケージとして実装し、ec4vis がプラグインをサーチするディレクトリ上に配置します。
プラグインは起動時に読み込まれます。
プラグイン上には、Python のスクリプトとして実行できることなら何でも記述できます。ec4vis のパイプラインやインスペクタなどを追加する場合には、予め提供された登録用のAPIを呼び出します。


動作環境
================

OS: Ubuntu 12.10 (x86 64bit)
Python: 2.7.3 以降
wxPython: 2.8.12.1 以降
h5py: 2.0.1 以降
numpy: 1.6.2 以降
vtk: 5.8.0 以降


ec4vis パッケージの構成
===========================

ec4vis パッケージの構成は、下記の通りです。
::

  ec4vis                 パッケージ・トップレベル
  |-- console            ログコンソール関連モジュール群
  |-- datasource         データソース関連モジュール群
  |-- inspector          インスペクタ関連モジュール群
  |   `-- datasource     データソースインスペクタ実装
  |-- pipeline           パイプライン関連モジュール群
  |-- plugins            プラグインディレクトリ
  |-- registry           レジストリ関連モジュール群
  |-- resources          リソースファイル（アイコンなど）
  |-- utils              ユーティリティモジュール
  |   `-- wx_            wxPython固有のユーティリティ
  `-- visualizer         ビジュアライザ関連モジュール群
      `-- vtk3d          vtkを使ったビジュアライザクラス
