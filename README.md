# PKUAutoElective 2024 Spring Version

![Start-Elective](./assets/bark-notification.jpeg)

## 小白版教程

参见 [Arthals' Docs](https://docs.arthals.ink/docs/pku-auto-elective)

## 更新日志

**感谢 zhongxinghong, Mzhhh, KingOfDeBug, Totoro-Li 等同学**

> **Update at Feb 17, 2024**：修改通知方式为 Bark，并修复了一个 Numpy 版本更新带来的类型 Bug，添加了 `requirements.txt` 以便安装依赖。
>
> **Update at Feb 21, 2022**: 验证码错误时，少数情况下重试会出现`NoneType' object has no attribute 'tobytes'`报错，且 exceptions 中并未提供处理机制。考虑到 Captcha 类成员函数 save()对主要功能并无影响，故删除 loop.py 中相关调用以避免程序异常停止。
>
> **Update at Feb 20, 2022**: 对 KingOfDebug 同学的 repo 出现`[104] unable to parse HTML content`的问题，对 parsing.py, captcha/等部分进行了替换，同步修改了 loop.py
> 同时对 captcha/online.py 中的 TTShituRecognizer 类进行修改，对 data 增加 typeid==7，调用平台的无感学习模型，规避 TT 平台默认的英文数字混合，在改版后识别率欠佳的问题。
>
> **Update at Mar 7, 2022**: 修改了 `get_supplement` 的 API 参数，已经可以实现课程列表页面的正常跳转，请更新至最新 commit 版本。

本项目基于 [PKUElective2022Spring](https://github.com/Totoro-Li/PKUElective2022Spring)，原仓库对 2021 春季学期的选课网站 API 改动进行了调整。并针对验证码系统的改动，将识别系统转为在线商用平台 [TT 识图](http://www.ttshitu.com)（打钱！打钱！），目前识别准确度仍然略微堪忧（但是可用）。

本项目在此基础上，修改通知方式为 Bark，并修复了一个 Numpy 版本更新带来的类型 Bug，添加了 `requirements.txt` 以便安装依赖。

## 安装

```bash
git clone https://github.com/zhuozhiyongde/PKUElective2024Spring.git
cd PKUElective2024Spring
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## Bark 进度通知（可选）

在 [Bark App](https://bark.day.app/) （仅限 iOS）的示例请求中获得推送 Key（注意不是设置里的 Device Token），然后修改 `config.ini` 中的 `notification` 部分：

```ini
[notification]
disable_push = 0  (默认为1，即不接收)
token = xxxxx  (你的 Bark key)
verbosity = 1 (推送消息详细级别，1为推送选课成功、失败；2为在此基础上推送所有ERROR类型消息)
minimum_interval = -1 (最小消息时间间隔，单位为秒，若消息产生时，距离上次成功发送不足这一时间，则取消发送。-1为不设置)
```

保存后，重启刷课机生效。

可以通过 notification/bark_push.py 中的 test_notify()以测试设置是否正确。

## 配置文件

### config.ini

参考 [PKUAutoElective](https://github.com/zhongxinghong/PKUAutoElective) 项目中的 `config.ini` 配置说明。

你也可以使用我写的 [可视化配置文件生成器](https://docs.arthals.ink/docs/pku-auto-elective)

### apikey.json

**请首先将 apikey.sample.ini 复制一份并改名为 apikey.ini，并按照以下说明进行配置。**

该文件为 [TT 识图](http://www.ttshitu.com) 平台的 API 密钥，在平台注册后，填入用户名与密码即可。由于该 API 需要收费，须在平台充值后方可使用（1 RMB 足够用到天荒地老了）。

```json
{
    "username": "xiaoming",
    "password": "xiaominghaoshuai"
}
```

## 使用说明

### 基本用法

将项目 clone 至本地后，切换至项目根目录下并运行 `main.py` 即可。

```
cd PKUElective2024Spring
python3 main.py
```

使用 `Ctrl + C` 输送 `KeyboardInterrupt`，可以终止程序运行。

### 高级用法

关于支持的命令行参数，参见 [PKUAutoElective](https://github.com/zhongxinghong/PKUAutoElective) 的使用说明。

一个比较常用的示例是，使用多个配置文件：

```bash
python main.py -c another-config.ini
```

### 测试识图平台

配置好 `apikey.json` 后，在命令行运行以下指令以测试在线识图是否正常工作

```
python -c "import base64; from autoelective.captcha import TTShituRecognizer;
c = TTShituRecognizer().recognize(base64.b64decode(
'iVBORw0KGgoAAAANSUhEUgAAAIIAAAA0CAMAAABxThCnAAADAFBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAz'
'AABmAACZAADMAAD/AAAAMwAzMwBmMwCZMwDMMwD/MwAAZgAzZgBmZgCZZgDMZgD/ZgAAmQAzmQBmmQCZmQDMmQD/mQAAzAAzzABm'
'zACZzADMzAD/zAAA/wAz/wBm/wCZ/wDM/wD//wAAADMzADNmADOZADPMADP/ADMAMzMzMzNmMzOZMzPMMzP/MzMAZjMzZjNmZjOZ'
'ZjPMZjP/ZjMAmTMzmTNmmTOZmTPMmTP/mTMAzDMzzDNmzDOZzDPMzDP/zDMA/zMz/zNm/zOZ/zPM/zP//zMAAGYzAGZmAGaZAGbM'
'AGb/AGYAM2YzM2ZmM2aZM2bMM2b/M2YAZmYzZmZmZmaZZmbMZmb/ZmYAmWYzmWZmmWaZmWbMmWb/mWYAzGYzzGZmzGaZzGbMzGb/'
'zGYA/2Yz/2Zm/2aZ/2bM/2b//2YAAJkzAJlmAJmZAJnMAJn/AJkAM5kzM5lmM5mZM5nMM5n/M5kAZpkzZplmZpmZZpnMZpn/ZpkA'
'mZkzmZlmmZmZmZnMmZn/mZkAzJkzzJlmzJmZzJnMzJn/zJkA/5kz/5lm/5mZ/5nM/5n//5kAAMwzAMxmAMyZAMzMAMz/AMwAM8wz'
'M8xmM8yZM8zMM8z/M8wAZswzZsxmZsyZZszMZsz/ZswAmcwzmcxmmcyZmczMmcz/mcwAzMwzzMxmzMyZzMzMzMz/zMwA/8wz/8xm'
'/8yZ/8zM/8z//8wAAP8zAP9mAP+ZAP/MAP//AP8AM/8zM/9mM/+ZM//MM///M/8AZv8zZv9mZv+ZZv/MZv//Zv8Amf8zmf9mmf+Z'
'mf/Mmf//mf8AzP8zzP9mzP+ZzP/MzP//zP8A//8z//9m//+Z///M//////8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACP6ykAAAOH0lEQVR4nJWZ'
'PXbkOBKE6bejvsiM0+w2VnORojGAo7oI6DDp6BZrDcpp0CFvsRbgoG6yXySq36yx7+1bSS3VD4tIREZGRqKnetX/76eYvkKM//lT'
'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'
'lSfnQz3/Dc7xKmEJtRLLAAAAAElFTkSuQmCC')); print(c, c.code == 'vfg8')"
```

如正常运行，将输出

```
Captcha('vfg8') True
```

## 注意事项

-   作者可能无视 issue 和 PR，如果您有更好的改进想法，请最好 clone 一份后自行改动
-   请不要在公开场合传播此项目，以免造成不必要的麻烦
-   刷课有风险 USE AT YOUR OWN RISK!
-   **暂时不能给你明确的答复，这个需要你自己衡量！**
