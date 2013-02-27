===================
プラグイン
===================

ec4vis では、以下のプラグインを提供しています。

* demo_cone_visualizer 
* filesystem_datasource_page.py
* hdf5_bundle_loader.py
* particle_constructor.py
* particle_visualizer.py
* sequential_selector.py
* simple_hdf5_loader.py
* simple_hdf5_loader_inspector.py
* simple_hdf5_tree_visualizer.py
* simple_particle_loader.py


demo_cone_visualizer
--------------------------------------------

何もしないダミーのノードと、 Vtk3dVisualizerPage を使って VTK ウィンドウに円錐を描画するデモです。


filesystem_datasource_page
--------------------------------------------

ファイルシステムからデータソースを選択するためのデータソースページです。

hdf5_bundle_loader
--------------------------------------------

ファイルシステムデータソースから受け取った URI をもとに、指定ディレクトリ以下、または指定ファイルの HDF データをロードします。

sequential_selector
--------------------------------------------

HDF データのリストから、特定のインデクスのデータを選択して、子ノードに渡します。

particle_constructor
--------------------------------------------

HDF データから、パーティクルデータを読み出します。

particle_visualizer
--------------------------------------------

particle_constructor の読みだしたパーティクルデータを表示する Vtk3dVisualizerPage です。Visual インスタンスを使っています。

simple_hdf5_loader
--------------------------------------------

URI を受け取り、指定パスの HDF ファイルを読み出すノードです。

simple_hdf5_loader_inspector
--------------------------------------------

simple_hdf5_loader のインスペクタです。


simple_hdf5_tree_visualizer
--------------------------------------------

HDF5データを受け取り、ツリー構造に表示するビジュアライザと、ツリーで選択したノードの情報を表示するインスペクタの例です。
インスペクタとビジュアライザの協調のサンプルです。


