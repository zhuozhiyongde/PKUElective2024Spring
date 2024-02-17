#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : bark_push
# @Date : 2022-02-22
# @Project: PKUElective2022Spring-main
# @AUTHOR : Totoro / Arthals

import requests
from timeit import default_timer as timer
from socket import gaierror as GetAddressError


class Notify(object):
    @property
    def disable_push(self):
        return self._disable_push

    @property
    def get_token(self):
        return self._token

    @property
    def get_verbosity(self):
        return self._verbosity

    @property
    def get_interval_lock(self):
        return self._interval_lock

    def get_time_stamp(self):
        return self._time_stamp

    def get_elapsed_time(self):
        return timer() - self.get_time_stamp()

    def output_ready(self):
        return self.get_elapsed_time() >= self.get_interval_lock

    def __init__(self, _token, _interval_lock, _disable_push=0, _verbosity=2):
        self._disable_push = _disable_push
        self._token = _token
        self._time_stamp = timer()
        self._interval_lock = _interval_lock
        self._verbosity = _verbosity

    def send_bark_push(
        self,
        token=None,
        msg: str = "",
        prefix: str = "",
    ):
        try:
            # https://api.day.app/JnQH697v85queQS4iTaj8A/PKUAutoElective/这里改成你自己的推送内容
            if self.disable_push == 1:
                return
            if token is None:
                token = self.get_token
            if not token or not msg or not self.output_ready():
                return

            data = {
                "title": "PKUAutoElective",
                "body": f"{prefix}{msg}",
                "icon": "https://cdn.arthals.ink/pku.jpg",
                "level": "timeSensitive",
            }

            req = requests.post(f"https://api.day.app/{token}/", data=data)

            rs = req.json()
            assert int(rs["code"] / 100) == 2, rs

        except AssertionError:
            print("网络连接错误\n")

        except ValueError:
            print(self.get_token)
            print("公众号提醒设置有误，请检查您传入的token值\n")

        except GetAddressError:
            print("网络连接错误\n")

        except BaseException:
            print("公众号提醒设置有误,推送发送失败\n")

        finally:
            self._time_stamp = timer()


def test_notify(_token_: str):
    notify = Notify(_token=_token_, _interval_lock=0, _disable_push=0, _verbosity=2)
    notify.send_bark_push(msg="This is a test.", prefix="[测试]")


test_notify("")  # 在单引号内填入您的token
