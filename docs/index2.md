
#####やること
win8 の gitbash から　ubuntu へ　秘密鍵で　ｓｓｈログインします。
おまけで、踏み台サーバー経由で目的サーバーへｓｓｈログインします（同じく秘密鍵使用）。
※ssh-agentを使います。gitbashのセッションに秘密鍵を覚えさせる。
#####前提
既に、サーバーへはポート２２でssh接続可能とします。（パスワード認証）
(※個人環境のサーバーでは既定のままでたぶんOK。)

```bash:win8
$ssh user1@ubuntu_server
password:########
```

##### opensshで鍵生成
公開鍵 test.rsa.pub と秘密鍵 test.rsa　が生成される。
※オプションのパスフレーズを入力した場合は忘れないこと。（使う度に聞かれるから！）

```bash:win8
cd ~/ && ls
#.sshが存在しない場合
mkdir .ssh
cd ~/.ssh && ssh-keygen
Enter file in which to save the key: test.rsa
#カレントディレクトリに　test.rsa と test.rsa.pubが生成される。
```

（※自分はやっていないのでgitbashでの結果は不明、未明だが）AWSのssh接続関連ドキュメントによると「秘密鍵ファイルの権限を自身のみに設定しておいた方がよい」かもしれない。
https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html

```bash:win8
chmod 400 test.rsa
```

##### gitbash ssh 用の設定ファイル　config を作成
serverへの接続情報やtest.rsaのパスなどを記入。

```yml:config
Host server1                    #hostName or 略称
    HostName 111.111.111.111    #ip or hostName
    Port 22
    User user1　　　　　　　　　　#server1のユーザー
    IdentityFile ~/.ssh/test.rsa  #上記で作成した秘密鍵              
```
##### 公開鍵　test.rsa.pub をサーバ―に転送
scpでサーバーに転送。

```bash:win8
cd ~/.ssh
scp test.rsa.pub user1@server1:~/.ssh
#一般には、server1上に、~/.ssh は既定で存在する。
#以降、この手の注釈は付けない予定。
```
##### サーバー側で、転送済　test.rsa.pub の内容を他のファイルに追記
サーバーにユーザー名とパスワードでsshログイン。
転送しておいたtest.rsa.pubの内容を別ファイルに追記。
最後に追記先のファイルとそのフォルダの権限を変更。

```bash:win8
ssh user1@server1
password: #####
```

```bash:server1
cd ~/.ssh
cat $test.rsa.pub >> authorized_keys
chmod 600 authorized_keys

cd ~/
chmod 700 .ssh
```
設定完了。

#####ssh で公開鍵を使ってサーバーにログイン
```bash:win8
ssh server1
#config で指定した hostの略称
```

####おまけ
#####ここからはgitbashのセッションに秘密鍵を記憶させる方法です。
ここまででserver1へのssh秘密鍵ログインの設定をして来ました。server1を踏み台サーバーだとします。その先に目的のサーバーserver2があります。
#####前提
server1を踏み台にしてserver2に同じユーザー名とパスワードでログインできるとします。更に、server2にもserver1の場合と同じ手順（※）で、同じ公開鍵を設置してあるとします。
※server2への接続はserver1を踏み台にするので全く同じではないですね。

問題は、踏み台サーバーにセキュリティ上の理由で秘密鍵を設置したくないことです。
手段としては、❶ローカルでssh-agentを使って秘密鍵を事前に登録しておき。❷win8からserver1へsshする際に、秘密鍵をセッションに記憶させます。

```bash:win8
ssh-agent bash
eval `ssh-agent`
cd ~/.ssh
ssh-add test.rsa       #秘密鍵を登録
ssh -A server1     #秘密鍵を記憶させるオプションでssh接続
```

server1からserver2へｓｓｈでログインします。（またはｓｃｐでファイル転送。）
※server2の~/.ssh/authorized_keysに公開鍵 test.rsa.pubの内容を追記済みとします。

```bash:server1
ssh user1@server2
# or scp my.txt user1@server2:~/
```



##参照
#####ssh-agent
https://www.gfd-dennou.org/arch/morikawa/memo/ssh-agent.txt
#####ssh-keygen
https://qiita.com/_kshara/items/fdf53a337fb9b9c4677b
#####サーバーに設置する公開鍵とそのフォルダの権限設定
https://qiita.com/ir-yk/items/af8550fea92b5c5f7fca
