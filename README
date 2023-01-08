# 基于Flask的基础Web框架，用于快速搭建服务


## 使用

1. 拉代码

``` bash
git@github.com:zkity/baseServer.git
```

2. 安装依赖

    1. python3.x

    2. python依赖库

    ``` bash
    pip install -r requirements.txt
    ```

3. 修改配置

    1. config/flask.yaml
    用户登陆需要数据库，修改为自己的数据库连接

    2. config/role.yaml
    更改权限配置

    3. config/user.yaml
    修改JWT密钥

4. 初始化成员表

    1. 建表
    ```bash
    python app.py
    ```

    2. 新增成员
    在数据库的`user`表中新增成员

5. 启动

    1. 测试环境

    ```bash
    flask run --host=0.0.0.0 --port=1234 --reload
    ```
    
    2. 生产环境

    生产环境需修改`run.ini`文件中的`chdir`,`logto`为服务器本地目录，以及`virtualenv`为本地虚拟环境
    ```
    ./run.sh
    ```

    在生产环境下，使用nginx配置可参考如下

    ```
    server {
        listen       443 ssl http2;
        listen       [::]:443 ssl http2;
        # 域名
        server_name  server.name;

        # 前端页面
        root /home/nginx/www/ipa;
        index index.html;

        # ssl 配置
        ssl_certificate "/path/to/file.crt";
        ssl_certificate_key "/path/to/file.key";
        ssl_session_cache shared:SSL:1m;
        ssl_session_timeout  10m;
        ssl_ciphers PROFILE=SYSTEM;
        ssl_prefer_server_ciphers on;

        gzip on;

        # 网页路径
        location / {
            try_files $uri $uri/ /index.html;
        }

        # 后台服务
        location /server {
            rewrite /ul/(.+) /$1 break;
            include uwsgi_params;
            # flask 的uwsgi路径
            uwsgi_pass 127.0.0.1:port;
        }
    }

    server {
        listen       80;
        # 域名
        server_name  server.name;

        return       301 https://$host$request_uri;
    }
    ```

## 基础功能

1. 鉴权

接口的访问需要token，使用`jwt`实现，并通过角色来决定对应用户的接口访问权限

2. 登陆

`user`表中记录了用户的账号，密码sha256摘要，以及角色

3. 接口限频

通过`/src/lib/limitFun.py`实现对接口的访问频率限制

4. 定时任务

通过`/src/lib/schedulerJob.py`实现定时任务

5. 文件上传/下载

对应的功能在`/src/controllers/file.py`中

## 新接口开发

1. 定义路由

在`/src/routers/page`下新建文件，参考如下写法定义路由

```python
from src.controllers.hi import sayHi
from src.controllers.hi import sayHello

def router(b1):
    b1.route('/hi', methods=['GET'])(sayHi)
    b1.route('/hello', methods=['POST'])(sayHello)
```

2. 定义功能实现

在`/src/controllers`下新建和路由对应的文件，实现功能，参考如下

```python
from flask import request
from src.lib.resp import Resp
from src.lib.respCode import RespCode

def sayHi():
    resp = Resp(code=RespCode.HI_OK.value, data={'res': 'hi'})
    return resp.res()

def sayHello():
    data = request.get_json()
    who = data.get('greet')

    resp = Resp(code=RespCode.HELLO_OK.value, data={'res': f'hello {who} !'})
    return resp.res()
```

3. 配置权限

在`/config/role.yaml`中为新建的接口设置权限

> 统一的返回格式定义在`/src/lib/resp.py`中，返回的错误码统一定义在`/src/lib/respCode.py`中