> 在資料夾路徑那邊輸入 cmd

> 主要教學參考

https://github.com/yaoandy107/line-bot-tutorial

> git 雙push

https://yami.io/git-multiple-origin/

in cmd
```
查看目前所有的路徑：
$ git remote -v
(push) 意味著會被推送的遠端
(fetch) 則是可供拉回的遠端，一般只有一個 fetch。

新增一個 Origin 的遠端：
$ git remote set-url origin --push --add https://github.com/howarder3/linebot_test.git

再檢查一次：
$ git remote -v
```