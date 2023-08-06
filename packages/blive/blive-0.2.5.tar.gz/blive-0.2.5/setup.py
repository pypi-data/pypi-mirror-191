# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blive']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler>=3.9.1.post1,<4.0.0',
 'aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.8.3,<4.0.0',
 'brotli>=1.0.9,<2.0.0',
 'pyee>=9.0.4,<10.0.0']

setup_kwargs = {
    'name': 'blive',
    'version': '0.2.5',
    'description': '',
    'long_description': '# B 站弹幕监听框架\n\n## 特点\n\n- 简单，只需房间号即可监听\n- 异步，io 不阻塞，及时获取消息\n\n## B 站直播弹幕 websocket 协议分析\n\n[PROTOCOL 分析](./PROTOCOL.md)\n\n## 快速开始\n\n1. 安装\n\n   `pip install blive`\n\n2. 创建 app\n\n   ```python\n   from blive import  BLiver\n\n   app = BLiver(123) #123为房间号\n   ```\n\n3. 创建处理器\n\n   ```python\n   from blive import  BLiver, Events, BLiverCtx\n   from blive.msg import DanMuMsg\n\n   app = BLiver(123)\n\n   # 标记该方法监听弹幕消息,更多消息类型请参考 Events 类源代码\n   @app.on(Events.DANMU_MSG)\n   async def listen_danmu(ctx: BLiverCtx):\n       danmu = DanMuMsg(ctx.body) #ctx.body 套上相应的消息操作类即可得到消息的基本内容,也可直接操作 ctx.body\n       print(danmu.content)\n       print(danmu.sender)\n       print(danmu.timestamp)\n   ```\n\n4. 运行\n\n   ```python\n\n   from blive import  BLiver, Events, BLiverCtx\n   from blive.msg import DanMuMsg\n\n   app = BLiver(123)\n\n   @app.on(Events.DANMU_MSG)\n   async def listen_danmu(ctx: BLiverCtx):\n       danmu = DanMuMsg(ctx.body)\n       print(danmu.content)\n       print(danmu.sender)\n       print(danmu.timestamp)\n\n   app.run() # 运行app!\n\n   ```\n\n## 同时监听多个直播间\n\n```python\nimport asyncio\nfrom blive import BLiver, Events, BLiverCtx\nfrom blive.msg import DanMuMsg\n\n\n# 定义弹幕事件handler\nasync def listen(ctx: BLiverCtx):\n   danmu = DanMuMsg(ctx.body)\n   print(\n      f\'\\n{danmu.sender.name} ({danmu.sender.medal.medal_name}:{danmu.sender.medal.medal_level}): "{danmu.content}"\\n\'\n   )\n\n\nasync def main():\n   # 两个直播间\n   ke = BLiver(605)\n   azi = BLiver(510)\n\n   # 注册handler\n   ke.on(Events.DANMU_MSG, listen)\n   azi.on(Events.DANMU_MSG, listen)\n\n   # 以异步task的形式运行\n   task1 = ke.run_as_task()\n   task2 = azi.run_as_task()\n\n   # await 两个任务\n   await asyncio.gather(*[task1, task2])\n\n\nif __name__ == "__main__":\n   loop = asyncio.get_event_loop()\n   loop.run_until_complete(main()) \n```\n\n## 作为协议解析工具在其他地方使用（伪代码）\n\n```python\nfrom blive.core import BWS_MsgPackage\n\npackman = BWS_MsgPackage() # 实例化一个消息包处理器\n\nwhile True:\n   data = ws.receive() # 当收到消息时\n   msg = packman.unpack(data) # 使用packman解析消息,返回一个形如 [(header,body), (header,body), ... ] 数组\n   print(msg)\n```\n\n## 与 fastapi (其他asyncio生态框架) 配合使用\n\n```python\nfrom fastapi import FastAPI\nfrom blive import BLiver,Events\nfrom blive.msg import DanMuMsg\n\napp = FastAPI()\n\nBLIVER_POOL = {}\n\n\n# 定义弹幕事件handler\nasync def handler(ctx):\n   danmu = DanMuMsg(ctx.body)\n   print(\n      f\'\\n{danmu.sender.name} ({danmu.sender.medal.medal_name}:{danmu.sender.medal.medal_level}): "{danmu.content}"\\n\'\n   )\n\ndef create_bliver(roomid):\n    b = BLiver(roomid)\n    b.on(Events.DANMU_MSG,handler)\n    return b\n\n\n@app.get("/create")\nasync def create_new_bliver(roomid:int):\n    room = BLIVER_POOL.get(roomid,None)\n    if not room:\n        b = create_bliver(roomid)\n        BLIVER_POOL[roomid] = b.run_as_task() # 启动监听\n    return {"msg":"创建一个新直播间弹幕监听成功"}\n\n\n@app.get("/del")\nasync def rm_bliver(roomid:int):\n    room = BLIVER_POOL.get(roomid,None)\n    if room:\n        room.cancel()\n        BLIVER_POOL.pop(roomid)\n    return {"msg":"移除直播间弹幕监听成功"}\n\n\n@app.get("/show")\nasync def show():\n    return list(BLIVER_POOL.keys())\n```\n\n## 项目简介\n\n- blive 文件夹为框架代码\n\n  - core.py 为B站ws直播聊天室协议包处理的核心代码\n\n  - eeframework.py 为框架代码\n\n  - msg.py 为消息操作类代码\n\n- example/app.py\n   以框架形式运行例子\n\n- example/multi_room.py\n   同时监听多个直播间的实现\n\n- example/with_fastapi.py\n   与fastapi 配合使用的例子\n\n\n## TODO\n\n- 更多的消息操作类（欢迎各位提pr）\n- 尝试加入中间件架构（目前感觉需求不大）\n',
    'author': 'Cam',
    'author_email': 'yulinfeng000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
