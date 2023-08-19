
### 前提条件

- スタートの都市はどこでもいい
- 終わったらスタートに戻る必要がある

### 現時点での方針

- 16 までは bruteforce か DP (メモ化再帰) で厳密解を得る
- それ以上のときは 貪欲法 + 2-opt or 3-opt を複数回繰り返したうち、最も良い経路を採用する（データセットのサイズによって変更）

### TODO

- simulated annealing の実装
  - 仮想的に温度を設定して、温度が下がるような経路の変更を行う
- 禁断探索法を試してみる
  - 2-opt と似ていて初期解を更新するらしい

### for_small.py

- 都市数 5, 8 のときに bruteforce attack ができる
- スタートを 0 に固定することで、都市数 N に対して O((N-1)!) になってちょっとだけ良い
- 逆順の経路は同じなので、半分だけ探索すれば良い
- 16 で試したらターミナルが落ちた

### dp.py

- 都市数 16 まで
- メモ化再帰によって厳密なスコアを得られる
- メモから経路を復元

### 2-opt

- 512, 2048 に対して 2-optを行った
- 初期経路を貪欲法で決定し、10回試した内で最も良い経路を採用
- 2-opt は2組の都市のペアをとってきて、ひっくり返したほうが経路が短くなるならひっくり返して、距離の差分を返す
- 差分が負にならない（これ以上よくできない）なら終わる
### 3-opt

- 64, 128 に対して 3-opt を行った
- 考え方は 2-opt と同様
- 初期経路を貪欲法で決定し、10回試した内で最も良い経路を採用

### 4-opt

- input_0で正しい答えは出たが、input_1からとても遅いため断念
- 何か間違っているのかもしれない

### links

- https://en.wikipedia.org/wiki/2-opt
- https://en.wikipedia.org/wiki/3-opt
- https://en.wikipedia.org/wiki/Simulated_annealing
- https://atcoder.jp/contests/abc180/tasks/abc180_e

### results

- output_0.csv

![image](https://user-images.githubusercontent.com/82920808/244947895-491ccf4b-3564-4992-818f-52c42e3fd2c7.png)

- output_1.csv

![image](https://user-images.githubusercontent.com/82920808/244948003-e7401e46-5c9f-4b4d-acd1-f71d1f6d0e33.png)

- output_2.csv

![image](https://user-images.githubusercontent.com/82920808/244948514-9f92091e-41b1-457e-917b-a22d702fb6c6.png)

- output_3.csv

![Alt text](image.png)

- output_4.csv

![image](https://user-images.githubusercontent.com/82920808/244956890-1ac87180-5450-4468-8115-3abf6ddf56d5.png)

- output_5.csv

![image](https://user-images.githubusercontent.com/82920808/244961874-47ee78bb-9400-40bd-b6cf-044bc43a892b.png)

- output_6.csv

![image](https://user-images.githubusercontent.com/82920808/244954751-ade22057-3f14-4d2b-ac68-7a2244dd359a.png)
