
## node.js 最新版安装

[http://nodejs.cn/download/package-manager/#debian-and-ubuntu-based-linux-distributions](http://nodejs.cn/download/package-manager/#debian-and-ubuntu-based-linux-distributions)

安装 nodejs
```
✗ curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
✗ sudo apt-get install -y nodejs
```

查看 nodejs 版本
```
✗ node -v
v4.4.7
```

查看 npm 版本(新版 nodejs　自带 npm)
```
✗ npm -v
2.15.8
```

## weui

安装 weui
```
✗ cd app/static
✗ npm install --save weui
weui@0.4.2 node_modules/weui
```
当前目录会生成 node_modules/weui

weui 页面示例：[node_modules/weui/dist/example/index.html](node_modules/weui/dist/example/index.html)


[微信网页开发样式库](http://mp.weixin.qq.com/wiki/2/ae9782fb42e47ad79eb7b361c2149d16.html)


## jQuery WeUI

[jQuery WeUI](http://lihongxun945.github.io/jquery-weui/)

[https://github.com/lihongxun945/jquery-weui](https://github.com/lihongxun945/jquery-weui)

安装
```
✗ cd app/static
✗ npm install jquery-weui
```

插件修改, 增加输入框原始参数显示
node_modules/jquery-weui/dist/js/jquery-weui.js
```
  $.prompt = function(text, title, callbackOK, callbackCancel, inputValue, inputType) {
    if (typeof title === 'function') {
      callbackCancel = arguments[2];
      callbackOK = arguments[1];
      title = undefined;
    }

    return $.modal({
      text: "<p class='weui-prompt-text'>"+(text || "")+"</p><input type='"+(inputType || "text")+"' class='weui_input weui-prompt-input' id='weui-prompt-input' value='"+(inputValue || "")+"'/>",
      title: title,
      buttons: [
      {
        text: defaults.buttonCancel,
        className: "default",
        onClick: callbackCancel
      },
      {
        text: defaults.buttonOK,
        className: "primary",
        onClick: function() {
          callbackOK && callbackOK($("#weui-prompt-input").val());
        }
      }]
    });
  };
```