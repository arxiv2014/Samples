#### named mutex
https://github.com/vburenin/nsync

#### daemontools
http://keisyu.hateblo.jp/entry/2014/02/12/234834

#### setlock
https://qiita.com/mogulla3/items/0a955196c524712f48ba

##### go-setlock
http://sig9.hatenablog.com/entry/2016/10/18/120000

```bash
$ setlock -N /c/temp/st.tmp sh test.sh
# -N ロックを取得できるまで待機。
# -X ロックを取得できないとエラー。
```
#### named pipe
https://stackoverflow.com/questions/39407592/named-pipes-in-go-for-both-windows-and-linux
#### golang namedMutex library(異プロセス間は不可？)
https://github.com/vburenin/nsync

#### golang 引数取得
https://qiita.com/uokada/items/f0e069a751679dcf616d

```golang:
import(flags)
fmt.Println("flag.Args: ", flag.Args())
```

#### sample

```golang

//GOOS=linux build go

package main

import ("fmt";"flag";"time";"os";"encoding/base64";"log";"runtime")

func base64Encode(str string) string {
    return base64.StdEncoding.EncodeToString([]byte(str))
}

func base64Decode(str string) (string, bool) {
    data, err := base64.StdEncoding.DecodeString(str)
    if err != nil {
        return "", true
    }
    return string(data), false
}
func main() {
    println( runtime.GOOS)
     time.Sleep(time.Millisecond * 1)
    flag.Parse()
    len := l
    en(flag.Args())
    println("flag.Args(): ")
    println(flag.Args())
    if(len<1){
        println("len(flag.Args())<1")
        os.Exit(1)        
    }
    
    //arg2 := flag.Args()[0:3]
    s, err := base64Decode(flag.Args()[0])
    if err {
                log.Fatal("error:", err)      
    }
     fmt.Printf("%q\n", s)
     
}

```


