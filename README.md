> 在資料夾路徑那邊輸入 cmd

> 主要教學參考

> reply

https://github.com/yaoandy107/line-bot-tutorial

> post

https://medium.com/@lukehong/%E5%88%9D%E6%AC%A1%E5%98%97%E8%A9%A6-line-bot-sdk-eaa4abbe8d6e

> in cmd

```javascript
git remote
echo "# linebot_test" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/howarder3/linebot_test.git
git push -u origin master

git add .
git commit -m 'update readme'
git push origin master
git push heroku master

doskey /history
```

> git 雙push

https://yami.io/git-multiple-origin/

```javascript
查看目前所有的路徑：
$ git remote -v
(push) 意味著會被推送的遠端
(fetch) 則是可供拉回的遠端，一般只有一個 fetch。

新增一個 Origin 的遠端：
$ git remote set-url origin --push --add https://github.com/howarder3/linebot_test.git

再檢查一次：
$ git remote -v
```
