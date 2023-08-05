# 介绍

[Gitee](https://gitee.com/bluepang2021/qrunner_new)

![](Qrunner_logo.jpg)

[![PyPI version](https://badge.fury.io/py/qrunner.svg)](https://badge.fury.io/py/qrunner) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qrunner)
![visitors](https://visitor-badge.glitch.me/badge?page_id=qrunner_new.qrunner)

AppUI/WebUI/HTTP automation testing framework based on pytest.

> 基于pytest 的 App UI/Web UI/HTTP自动化测试框架。

## 特点

* 集成`facebook-wda`/`uiautomator2`/`selenium`/`requests`，支持安卓 UI/IOS UI/Web UI/HTTP测试。
* 集成`allure`, 支持HTML格式的测试报告。
* 提供脚手架，快速生成自动化测试项目。
* 提供强大的`数据驱动`。
* 提供丰富的断言。
* 支持生成随机测试数据。
* 支持设置用例依赖。


## 三方依赖

* Allure：https://github.com/allure-framework/allure2
* WebDriverAgent：https://github.com/appium/WebDriverAgent

## Install

```shell
> pip install -i https://pypi.tuna.tsinghua.edu.cn/simple qrunner
```

## 🤖 Quick Start

1、查看帮助：
```shell
usage: qrunner [-h] [-v] [-n PROJECT_NAME] [-p PLATFORM] [-i INSTALL]

全平台自动化测试框架

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         版本号
  -n PROJECT_NAME, --project_name PROJECT_NAME
                        项目名称
  -p PLATFORM, --platform PLATFORM
                        所属平台
  -i INSTALL, --install INSTALL
                        浏览器驱动名称

```

2、创建项目：
```shell
> qrunner -p android -n android_test
```
目录结构如下：
```shell
android_test/
├── test_dir/
│   ├── __init__.py
│   ├── test_android.py
├── test_data/
│   ├── data.json
└── run.py
```

3、运行项目：

* ✔️ 在`pyCharm`中右键执行。

* ✔️ 通过命令行工具执行。

```shell
> python run.py

2022-09-29 11:02:40,206 - root - INFO - 执行用例
2022-09-29 11:02:40,206 - root - INFO - 用例路径: test_adr.py
2022-09-29 11:02:40,206 - root - INFO - ['test_adr.py', '-sv', '--reruns', '0', '--alluredir', 'allure-results', '--clean-alluredir']
================================================================================================================================================= test session starts ==================================================================================================================================================
platform darwin -- Python 3.9.10, pytest-6.2.5, py-1.11.0, pluggy-1.0.0 -- /Users/UI/PycharmProjects/qrunner_new_gitee/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/UI/PycharmProjects/qrunner_new_gitee
plugins: xdist-2.5.0, forked-1.4.0, allure-pytest-2.9.45, rerunfailures-10.2, dependency-0.5.1, ordering-0.6
collecting ... 2022-09-29 11:02:40,294 - root - INFO - [UJK0220521066836] Create android driver singleton
2022-09-29 11:02:40,303 - root - INFO - 启动 android driver for UJK0220521066836
2022-09-29 11:02:40,309 - urllib3.connectionpool - DEBUG - Starting new HTTP connection (1): ujk0220521066836:7912
2022-09-29 11:02:40,357 - urllib3.connectionpool - DEBUG - Starting new HTTP connection (1): 127.0.0.1:62522
2022-09-29 11:02:40,377 - urllib3.connectionpool - DEBUG - http://127.0.0.1:62522 "GET /wlan/ip HTTP/1.1" 200 11
collected 1 item                                                                                                                                                                                                                                                                                                       

test_adr.py::TestLogin::test_login 2022-09-29 11:02:40,381 - root - DEBUG - [start_time]: 2022-09-29 11:02:40
2022-09-29 11:02:40,381 - root - INFO - 强制启动应用: com.qizhidao.clientapp
2022-09-29 11:02:40,496 - urllib3.connectionpool - DEBUG - http://127.0.0.1:62522 "POST /shell HTTP/1.1" 200 39
2022-09-29 11:02:40,792 - urllib3.connectionpool - DEBUG - http://127.0.0.1:62522 "GET /packages/com.qizhidao.clientapp/info HTTP/1.1" 200 221
2022-09-29 11:02:40,893 - urllib3.connectionpool - DEBUG - http://127.0.0.1:62522 "POST /shell HTTP/1.1" 200 184
2022-09-29 11:02:40,895 - root - INFO - 存在才点击元素: {'resourceId': 'com.qizhidao.clientapp:id/bottom_btn'},0
2022-09-29 11:02:40,895 - root - INFO - 判断元素是否存在: {'resourceId': 'com.qizhidao.clientapp:id/bottom_btn'},0
2022-09-29 11:02:40,895 - root - INFO - 查找元素: {'resourceId': 'com.qizhidao.clientapp:id/bottom_btn'},0
2022-09-29 11:02:54,106 - urllib3.connectionpool - DEBUG - http://127.0.0.1:62522 "POST /jsonrpc/0 HTTP/1.1" 200 90
2022-09-29 11:02:54,179 - root - WARNING - 【exists:257】未找到元素 {'resourceId': 'com.qizhidao.clientapp:id/bottom_btn'}
2022-09-29 11:02:54,179 - root - INFO - 点击元素: {'resourceId': 'com.qizhidao.clientapp:id/bottom_view'},3
2022-09-29 11:02:54,179 - root - INFO - 查找元素: {'resourceId': 'com.qizhidao.clientapp:id/bottom_view'},3
2022-09-29 11:02:54,332 - urllib3.connectionpool - DEBUG - http://127.0.0.1:62522 "POST /jsonrpc/0 HTTP/1.1" 200 89
2022-09-29 11:02:54,685 - urllib3.connectionpool - DEBUG - http://127.0.0.1:62522 "GET /screenshot/0 HTTP/1.1" 200 236334
2022-09-29 11:02:55,619 - urllib3.connectionpool - DEBUG - http://127.0.0.1:62522 "POST /jsonrpc/0 HTTP/1.1" 200 290
2022-09-29 11:02:55,822 - urllib3.connectionpool - DEBUG - http://127.0.0.1:62522 "POST /jsonrpc/0 HTTP/1.1" 200 89
2022-09-29 11:02:55,822 - root - DEBUG - 点击成功
2022-09-29 11:02:55,822 - root - INFO - 判断元素是否存在: {'text': '登录/注册'},0
2022-09-29 11:02:55,823 - root - INFO - 查找元素: {'text': '登录/注册'},0
2022-09-29 11:03:00,253 - urllib3.connectionpool - DEBUG - http://127.0.0.1:62522 "POST /jsonrpc/0 HTTP/1.1" 200 90
2022-09-29 11:03:00,254 - root - WARNING - 【exists:257】未找到元素 {'text': '登录/注册'}
2022-09-29 11:03:00,254 - root - INFO - 已登录成功
2022-09-29 11:03:00,255 - root - DEBUG - 等待: 3s
PASSED2022-09-29 11:03:03,621 - urllib3.connectionpool - DEBUG - http://127.0.0.1:62522 "GET /screenshot/0 HTTP/1.1" 200 175495
2022-09-29 11:03:03,624 - root - INFO - 退出应用: com.qizhidao.clientapp
2022-09-29 11:03:03,782 - urllib3.connectionpool - DEBUG - http://127.0.0.1:62522 "POST /shell HTTP/1.1" 200 39
2022-09-29 11:03:03,783 - root - DEBUG - [end_time]: 2022-09-29 11:03:03
2022-09-29 11:03:03,783 - root - DEBUG - [run_time]: 23.40 s
```

4、查看报告

运行`allure server allure-results`浏览器会自动调起报告（需先安装配置allure）

![test report](./test_report.jpg)

## 🔬 Demo

[demo](/demo) 提供了丰富实例，帮你快速了解qrunner的用法。

### 安卓APP 测试

```shell
import qrunner
from qrunner import story, title


class HomePage(qrunner.Page):
    LOC_AD_CLOSE = {'id_': 'id/bottom_btn', 'desc': '首页广告关闭按钮'}
    LOC_MY = {'id_': 'id/bottom_view', 'index': 3, 'desc': '首页底部我的入口'}
    
    def go_my(self):
        self.elem(**self.LOC_AD_CLOSE).click()
        self.elem(**self.LOC_MY).click()


@story('首页')
class TestClass(qrunner.TestCase):
    
    def start(self):
        self.hp = HomePage(self.driver)
        self.elem_close = self.elem(id_='id/bottom_btn', desc='首页广告关闭按钮')
        self.elem_my = self.elem(id_='id/bottom_view', index=3, desc='首页底部我的入口')
    
    @title('pom模式用例')
    def test_pom(self):
        self.start_app()
        self.hp.go_my()
        self.assertText('我的订单')
        self.stop_app()
    
    @title('普通模式用例')
    def test_normal(self):
        self.start_app()
        self.elem_close.click()
        self.elem_my.click()
        self.assertText('我的订单')
        self.stop_app()


if __name__ == '__main__':
    qrunner.main(
        platform='android',
        device_id='UJK0220521066836',
        pkg_name='com.qizhidao.clientapp'
    )
```

__说明：__

* 创建测试类必须继承 `qrunner.TestCase`。
* 测试用例文件命名必须以 `test` 开头。
* qrunner的封装了`assertText`、`assertElement` 等断言方法。
* 如果用例间有耦合关系，建议使用pom模式，方便复用；否则，使用普通模式即可
  - pom模式需要继承qrunner.Page
  - 页面初始化的时候需要传入driver

### IOS APP 测试

```shell
import qrunner
from qrunner import story, title


class HomePage(qrunner.Page):
    LOC_AD_CLOSE = {'label': 'close white big', 'desc': '首页广告关闭按钮'}
    LOC_MY = {'label': '我的', 'desc': '首页底部我的入口'}
    
    def go_my(self):
        self.elem(**self.LOC_AD_CLOSE).click()
        self.elem(**self.LOC_MY).click()


@story('首页')
class TestClass(qrunner.TestCase):

    def start(self):
        self.hp = HomePage(self.driver)
        self.elem_close = self.elem(label='close white big', desc='首页广告关闭按钮')
        self.elem_my = self.elem(label='我的', desc='首页底部我的入口')

    @title('pom模式用例')
    def test_pom(self):
        self.start_app()
        self.hp.go_my()
        self.assertText('我的订单')
        self.stop_app()
    
    @title('普通模式用例')
    def test_normal(self):
        self.start_app()
        self.elem_close.click()
        self.elem_my.click()
        self.assertText('我的订单')
        self.stop_app()


if __name__ == '__main__':
    qrunner.main(
        platform='ios',
        device_id='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company'
    )
```

__说明：__

* 创建测试类必须继承 `qrunner.IosTestCase`。
* 测试用例文件命名必须以 `test` 开头。
* qrunner的封装了`assertText`、`assertElement` 等断言方法。
* 如果用例间有耦合关系，建议使用pom模式，方便复用；否则，使用普通模式即可
  - pom模式需要继承qrunner.Page
  - 页面初始化的时候需要传入driver

### Web 测试

```shell
import qrunner
from qrunner import story, title


class PatentPage(qrunner.Page):
    url = None
    LOC_SEARCH_INPUT = {'id_': 'driver-home-step1', 'desc': '查专利首页输入框'}
    LOC_SEARCH_SUBMIT = {'id_': 'driver-home-step2', 'desc': '查专利首页搜索确认按钮'}
    
    def simple_search(self):
        self.elem(**self.LOC_SEARCH_INPUT).set_text('无人机')
        self.elem(**self.LOC_SEARCH_SUBMIT).click()


@story('专利检索')
class TestClass(qrunner.TestCase):
    
    def start(self):
        self.pp = PatentPage(self.driver)
        self.elem_input = self.elem(id_='driver-home-step1', desc='查专利首页输入框')
        self.elem_submit = self.elem(id_='driver-home-step2', desc='查专利首页搜索确认按钮')
    
    @title('pom模式代码')
    def test_pom(self):
        self.pp.open()
        self.pp.simple_search()
        self.assertTitle('无人机专利检索-企知道')
    
    @title('普通模式代码')
    def test_normal(self):
        self.open()
        self.elem_input.click()
        self.elem_submit.click()
        self.assertTitle('无人机专利检索-企知道')


if __name__ == '__main__':
    qrunner.main(
        platform='web',
        base_url='https://patents.qizhidao.com/'
    )
```

__说明：__

* 创建测试类必须继承 `qrunner.WebTestCase`。
* 测试用例文件命名必须以 `test` 开头。
* qrunner的封装了`assertTitle`、`assertUrl` 和 `assertText`等断言方法。
* 如果用例间有耦合关系，建议使用pom模式，方便复用；否则，使用普通模式即可
  - pom模式需要继承qrunner.Page
  - 页面初始化的时候需要传入driver

### HTTP 测试

```python
import qrunner
from qrunner import title, file_data, story


@story('PC站首页')
class TestClass(qrunner.TestCase):

    @title('查询PC站首页banner列表')
    @file_data('card_type', 'data.json')
    def test_getToolCardListForPc(self, card_type):
        path = '/api/qzd-bff-app/qzd/v1/home/getToolCardListForPc'
        payload = {"type": card_type}
        self.post(path, json=payload)
        self.assertEq('code', 0)


if __name__ == '__main__':
    qrunner.main(
        platform='api',
        base_url='https://www-pre.qizhidao.com'
    )
```

__说明：__

* 创建测试类必须继承 `qrunner.TestCase`。
* 测试用例文件命名必须以 `test` 开头。
* qrunner的封装了`assertEq`、`assertLenEq` 和 `assertLenGt`等断言方法。

### Run the test

```python
import qrunner

qrunner.main()  # 当前文件，pycharm中需要把默认的测试框架从pytest改成unittest，才能右键run
qrunner.main(case_path="./")  # 当前目录下的所有测试文件
qrunner.main(case_path="./test_dir/")  # 指定目录下的所有测试文件
qrunner.main(case_path="./test_dir/test_api.py")  # 指定目录下的测试文件
```

### 感谢

感谢从以下项目中得到思路和帮助。

* [seldom](https://github.com/SeldomQA/seldom)

* [selenium](https://www.selenium.dev/)

* [uiautomator2](https://github.com/openatx/uiautomator2)
  
* [facebook-wda](https://github.com/openatx/facebook-wda)

* [requests](https://github.com/psf/requests)

# 开始

## 快速开始

### 基本规范

`qrunner`继承`pytest`单元测试框架，所以他的编写规范与[pytest](https://www.osgeo.cn/pytest/contents.html#full-pytest-documentation)
基本保持一致。

```shell
# test_sample.py
import qrunner

class TestYou(qrunner.TestCase):
    def test_case(self):
        """a simple test case """
        assert 1+1 == 2

if __name__ == '__main__':
    qrunner.main()
```

基本规范：
1. 创建测试类`TestYou`并继承`qrunner.TestCase`类，必须以`Test`开头
2. 创建测试方法`test_case`, 必须以`test`开头。
3. `qrunner.mian()`是框架运行的入口方法，接下来详细介绍。

### `main()` 方法
`main()`方法是qrunner运行测试的入口, 它提供了一些最基本也是最重要的配置。

```python
import qrunner
# ...
if __name__ == '__main__':
    qrunner.main(
      platform=None,
      device_id=None,
      pkg_name=None,
      base_url=None,
      headers=None,
      browser='chrome',
      timeout=10,
      case_path=None,
      rerun=0,
      concurrent=False,
    )
```

__参数说明__

* platform: 支持的平台，包括android、ios、web、api
* device_id: IOS设备id，通过tidevice list命令获取
* pkg_name: IOS应用包名，通过tidevice applist命令获取
* browser: 浏览器类型，默认chrome，还支持firefox、edge、safari等
* case_path: 测试用例路径
* rerun: 失败重试次数
* concurrent: 是否并发执行用例
* base_url: 默认域名
* headers: 默认请求头, {
    "login_headers": {},
    "visit_headers": {}
}
* timeout: 超时时间

### 运行测试

1. 运行当前文件中的用例

创建 `test_sample.py` 文件，在要文件中使用`main()`方法，如下：

```py
# test_sample.py
import qrunner

class TestYou(qrunner.TestCase):
    
    def test_case(self):
        """a simple test case """
        assert 1+1 == 2
        
if __name__ == '__main__':
    qrunner.main()  # 默认运行当前文件中的用例
```

`main()`方法默认运行当前文件中的所有用例。

```shell
> python test_sample.py      # 通过python命令运行
```

2. 指定运行目录、文件

可以通过`path`参数指定要运行的目录或文件。
   
```py
# run.py
import qrunner

qrunner.main(case_path="./")  # 指定当前文件所在目录下面的用例。
qrunner.main(case_path="./test_dir/")  # 指定当前目录下面的test_dir/ 目录下面的用例。
qrunner.main(case_path="./test_dir/test_sample.py")  # 指定测试文件中的用例。
qrunner.main(case_path="D:/qrunner_sample/test_dir/test_sample.py")  # 指定文件的绝对路径。
```
* 运行文件
```shell
> python run.py
```

### 失败重跑

qrunner支持`错误`&`失败`重跑。

```python
# test_sample.py
import qrunner

class TestYou(qrunner.TestCase):
  
    def test_error(self):
        """error case"""
        assert a == 2
        
    def test_fail(self):
        """fail case """
        assert 1+1 == 3
        
if __name__ == '__main__':
    qrunner.main(rerun=3)
```

参数说明：

* rerun: 指定重跑的次数，默认为 `0`。

```shell
> python test_sample.py

/Users/UI/PycharmProjects/qrunner_new_gitee/venv/bin/python /Users/UI/PycharmProjects/qrunner_new_gitee/test_api.py
2022-10-08 11:59:24,673 - root - INFO - 执行用例
2022-10-08 11:59:24,738 - root - INFO - 用例路径: /Users/UI/PycharmProjects/qrunner_new_gitee/test_api.py
2022-10-08 11:59:24,738 - root - INFO - ['/Users/UI/PycharmProjects/qrunner_new_gitee/test_api.py', '-sv', '--reruns', '3', '--alluredir', 'allure-results', '--clean-alluredir']
============================= test session starts ==============================
platform darwin -- Python 3.9.10, pytest-6.2.5, py-1.11.0, pluggy-1.0.0 -- /Users/UI/PycharmProjects/qrunner_new_gitee/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/UI/PycharmProjects/qrunner_new_gitee
plugins: xdist-2.5.0, forked-1.4.0, allure-pytest-2.9.45, rerunfailures-10.2, dependency-0.5.1, ordering-0.6
collecting ... collected 2 items

test_api.py::TestYou::test_error 2022-10-08 11:59:24,833 - root - DEBUG - [start_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,838 - root - DEBUG - [end_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,838 - root - DEBUG - [run_time]: 0.00 s
RERUN
test_api.py::TestYou::test_error 2022-10-08 11:59:24,839 - root - DEBUG - [start_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,841 - root - DEBUG - [end_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,841 - root - DEBUG - [run_time]: 0.00 s
RERUN
test_api.py::TestYou::test_error 2022-10-08 11:59:24,842 - root - DEBUG - [start_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,844 - root - DEBUG - [end_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,844 - root - DEBUG - [run_time]: 0.00 s
RERUN
test_api.py::TestYou::test_error 2022-10-08 11:59:24,845 - root - DEBUG - [start_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,846 - root - DEBUG - [end_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,846 - root - DEBUG - [run_time]: 0.00 s
FAILED
test_api.py::TestYou::test_fail 2022-10-08 11:59:24,848 - root - DEBUG - [start_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,849 - root - DEBUG - [end_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,850 - root - DEBUG - [run_time]: 0.00 s
RERUN
test_api.py::TestYou::test_fail 2022-10-08 11:59:24,851 - root - DEBUG - [start_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,853 - root - DEBUG - [end_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,853 - root - DEBUG - [run_time]: 0.00 s
RERUN
test_api.py::TestYou::test_fail 2022-10-08 11:59:24,855 - root - DEBUG - [start_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,856 - root - DEBUG - [end_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,856 - root - DEBUG - [run_time]: 0.00 s
RERUN
test_api.py::TestYou::test_fail 2022-10-08 11:59:24,858 - root - DEBUG - [start_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,860 - root - DEBUG - [end_time]: 2022-10-08 11:59:24
2022-10-08 11:59:24,860 - root - DEBUG - [run_time]: 0.00 s
FAILED

=========================== short test summary info ============================
FAILED test_api.py::TestYou::test_error - NameError: name 'a' is not defined
FAILED test_api.py::TestYou::test_fail - assert 2 == 3
========================== 2 failed, 6 rerun in 0.04s ==========================
```

### 测试报告

qrunner 默认在运行测试文件下自动创建`allure-results`目录，需要通过allure serve命令生成html报告

* 运行测试用例前
```shell
mypro/
└── test_sample.py
```
* 运行测试用例后
```shell
mypro/
├── allure-results/
│   ├── 0a1430a7-aafd-4d4a-984c-b2b435835fba-container.json
│   ├── 5c1bbb85-afd5-4f7a-a470-17ad4b0a2870-attachment.txt
└── test_sample.py
```
命令行执行allure serve allure-results，自动调起浏览器打开测试报告，查看测试结果。
![](./test_report.jpg)

## 高级用法

### 随机测试数据

测试数据是测试用例的重要部分，有时不能把测试数据写死在测试用例中，比如注册新用户，一旦执行过用例那么测试数据就已经存在了，所以每次执行注册新用户的数据不能是一样的，这就需要随机生成一些测试数据。

qrunner 提供了随机获取测试数据的方法。

```python
import qrunner
from qrunner import testdata


class TestYou(qrunner.TestCase):
    
    def test_case(self):
        """a simple test case """
        word = testdata.get_word()
        print(word)
        
if __name__ == '__main__':
    qrunner.main()
```

通过`get_word()` 随机获取一个单词，然后对这个单词进行搜索。

**更多的方法**

```python
from qrunner.testdata import *
# 随机一个名字
print("名字：", first_name())
print("名字(男)：", first_name(gender="male"))
print("名字(女)：", first_name(gender="female"))
print("名字(中文男)：", first_name(gender="male", language="zh"))
print("名字(中文女)：", first_name(gender="female", language="zh"))
# 随机一个姓
print("姓:", last_name())
print("姓(中文):", last_name(language="zh"))
# 随机一个姓名
print("姓名:", username())
print("姓名(中文):", username(language="zh"))
# 随机一个生日
print("生日:", get_birthday())
print("生日字符串:", get_birthday(as_str=True))
print("生日年龄范围:", get_birthday(start_age=20, stop_age=30))
# 日期
print("日期(当前):", get_date())
print("日期(昨天):", get_date(-1))
print("日期(明天):", get_date(1))
# 数字
print("数字(8位):", get_digits(8))
# 邮箱
print("邮箱:", get_email())
# 浮点数
print("浮点数:", get_float())
print("浮点数范围:", get_float(min_size=1.0, max_size=2.0))
# 随机时间
print("当前时间:", get_now_datetime())
print("当前时间(格式化字符串):", get_now_datetime(strftime=True))
print("未来时间:", get_future_datetime())
print("未来时间(格式化字符串):", get_future_datetime(strftime=True))
print("过去时间:", get_past_datetime())
print("过去时间(格式化字符串):", get_past_datetime(strftime=True))
# 随机数据
print("整型:", get_int())
print("整型32位:", get_int32())
print("整型64位:", get_int64())
print("MD5:", get_md5())
print("UUID:", get_uuid())
print("单词:", get_word())
print("单词组(3个):", get_words(3))
print("手机号:", get_phone())
print("手机号(移动):", get_phone(operator="mobile"))
print("手机号(联通):", get_phone(operator="unicom"))
print("手机号(电信):", get_phone(operator="telecom"))
```

* 运行结果

```shell
名字： Hayden
名字（男）： Brantley
名字（女）： Julia
名字（中文男）： 觅儿
名字（中文女）： 若星
姓: Lee
姓（中文）: 白
姓名: Genesis
姓名（中文）: 廉高义
生日: 2000-03-11
生日字符串: 1994-11-12
生日年龄范围: 1996-01-12
日期（当前）: 2022-09-17
日期（昨天）: 2022-09-16
日期（明天）: 2022-09-18
数字(8位): 48285099
邮箱: melanie@yahoo.com
浮点数: 1.5315717275531858e+308
浮点数范围: 1.6682402084146244
当前时间: 2022-09-17 23:33:22.736031
当前时间(格式化字符串): 2022-09-17 23:33:22
未来时间: 2054-05-02 11:33:47.736031
未来时间(格式化字符串): 2070-08-28 16:38:45
过去时间: 2004-09-03 12:56:23.737031
过去时间(格式化字符串): 2006-12-06 07:58:37
整型: 7831034423589443450
整型32位: 1119927937
整型64位: 3509365234787490389
MD5: d0f6c6abbfe1cfeea60ecfdd1ef2f4b9
UUID: 5fd50475-2723-4a36-a769-1d4c9784223a
单词: habitasse
单词组（3个）: уж pede. metus.
手机号: 13171039843
手机号(移动): 15165746029
手机号(联通): 16672812525
手机号(电信): 17345142737
```

### 用例的依赖

**depend**

`depend` 装饰器用来设置依赖的用例。

```python
import qrunner
from qrunner import depend


class TestDepend(qrunner.TestCase):
    
    @depend(name='test_001')
    def test_001(self):
        print("test_001")
        
    @depend("test_001", name='test_002')
    def test_002(self):
        print("test_002")
        
    @depend(["test_001", "test_002"])
    def test_003(self):
        print("test_003")
        
if __name__ == '__main__':
    qrunner.main()
```

* 被依赖的用例需要用name定义被依赖的名称，因为本装饰器是基于pytest.mark.dependency，它会出现识别不了被装饰的方法名的情况
  ，所以通过name强制指定最为准确
  ```@depend(name='test_001')```
* `test_002` 依赖于 `test_001` , `test_003`又依赖于`test_002`。当被依赖的用例，错误、失败、跳过，那么依赖的用例自动跳过。
* 如果依赖多个用例，传入一个list即可
```@depend(['test_001', 'test_002'])```
  
### 发送邮件

```python
import qrunner
from qrunner import Mail


if __name__ == '__main__':
    qrunner.main()
    mail = Mail(host='xx.com', user='xx@xx.com', password='xxx')
    mail.send_report(title='Demo项目测试报告', report_url='https://www.baidu.com', receiver_list=['xx@xx.com'])
```

- title：邮件标题
- report_url: 测试报告的url
- receiver_list: 接收报告的用户列表


### 发送钉钉

```python
import qrunner
from qrunner import DingTalk


if __name__ == '__main__':
    qrunner.main()
    dd = DingTalk(secret='xxx',
                  url='xxx')
    dd.send_report(msg_title='Demo测试消息', report_url='https://www.baidu.com')
```

- `secret`: 如果钉钉机器人安全设置了签名，则需要传入对应的密钥。
- `url`: 钉钉机器人的Webhook链接
- `msg_title`: 消息标题
- `report_url`: 测试报告url

## 数据驱动

数据驱动是测试框架非常重要的功能之一，它可以有效的节约大量重复的测试代码。qrunner针对该功能做强大的支持。

### @data()方法

当测试数据量比较少的情况下，可以通过`@data()`管理测试数据。


**参数化测试用例**

```python
import qrunner
from qrunner import data


class TestDataDriver(qrunner.TestCase):
    @data('name,keyword', [
        ("First case", "qrunner"),
        ("Second case", "selenium"),
        ("Third case", "unittest"),
    ])
    def test_tuple_data(self, name, keyword):
        """
        Used tuple test data
        :param name: case desc
        :param keyword: case data
        """
        print(f"test data: {name} + {keyword}")

    @data('name,keyword', [
        ["First case", "qrunner"],
        ["Second case", "selenium"],
        ["Third case", "unittest"],
    ])
    def test_list_data(self, name, keyword):
        """
        Used list test data
        """
        print(f"test data: {name} + {keyword}")

    @data('json', [
        {"scene": 'First case', 'keyword': 'qrunner'},
        {"scene": 'Second case', 'keyword': 'selenium'},
        {"scene": 'Third case', 'keyword': 'unittest'},
    ])
    def test_dict_data(self, json):
        """
        used dict test data
        """
        print(f"case desc: {json['scene']}")
        print(f"test data: {json['keyword']}")
    
    @data('param', [
            ("First case", "qrunner"),
            ("Second case", "selenium"),
            ("Third case", "unittest"),
        ])
    def test_tuple_single_param(self, param):
        """
        Used tuple test data
        :param name: case desc
        :param keyword: case data
        """
        print(f"test data: {param[0]} + {param[1]}")
    
    @data('param_a', [1, 2])
    @data('param_b', ['c', 'd'])
    def test_cartesian_product(self, param_a, param_b):
        """
        笛卡尔积
        :param param_a: case desc
        :param param_b: case data
        """
        print(f"test data: {param_a} + {param_b}")
```

通过`@data()` 装饰器来参数化测试用例。

### @file_data() 方法

当测试数据量比较大的情况下，可以通过`@file_data()`管理测试数据。

**JSON 文件参数化**

qrunner 支持将`JSON`文件的参数化。

json 文件：

```json
{
  "login1": [
    [1, 2],
    [3, 4]
  ],
  "login2": [
    {"username":  1, "password":  2},
    {"username":  3, "password": 4}
  ]
}

```

> 注：`login1` 和 `login2` 的调用方法一样。 区别是前者更简洁，后者更易读。
```python
import qrunner
from qrunner import file_data


class TestYou(qrunner.TestCase):

    @file_data("login1")
    def test_default(self, login1):
        """文件名使用默认值
        file: 'data.json'
        """
        print(login1[0], login1[1])

    @file_data(key="login2", file='data.json')
    def test_full_param(self, login2):
        """参数都填上"""
        print(login2["username"], login2["password"])
```

- key: 指定字典的 key，默认不指定解析整个 JSON 文件。
- file : 指定 JSON 文件的路径。

# Web UI 测试

## 浏览器与驱动

### 下载浏览器驱动

> qrunner集成webdriver_manager管理浏览器驱动。
和Selenium一样，在使用qrunner运行自动化测试之前，需要先配置浏览器驱动，这一步非常重要。

qrunner 集成 [webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager) ，提供了`chrome/firefox/edge`浏览器驱动的自动下载。

__自动下载__

如果你不配置浏览器驱动也没关系，qrunner会根据你使用的浏览器版本，自动化下载对应的驱动文件。

* 编写简单的用例

```python
import qrunner


class TestBing(qrunner.TestCase):

    def start(self):
        self.url = 'https://www.bing.com'
        self.elem_input = self.elem(id_='sb_form_q', desc='输入框')

    def test_bing_search(self):
        """selenium api"""
        self.open(self.url)
        self.elem_input.set_text('无人机')
        self.sleep(2)
        self.assertTitle("qrunner - 搜索")


if __name__ == '__main__':
    qrunner.main(platform='web')
```

qrunner 检测到的`Chrome`浏览器后，自动化下载对应版本的驱动，并保存到本地，以便于下次执行的时候就不需要下载了。
并且，非常贴心的将`chromedriver`的下载地址从 google 切换成了 taobao 的镜像地址。

__手动下载__

通过`qrunner`命令下载浏览器驱动。
```shell
> qrunner --install chrome
> qrunner --install firefox
> qrunner --install ie
> qrunner --install edge
```
1. 默认下载到当前的`C:\Users\username\.wdm\drivers\` 目录下面。
2. Chrome: `chromedriver` 驱动，众所周知的原因，使用的taobao的镜像。
3. Safari: `safaridriver` （macOS系统自带，默认路径:`/usr/bin/safaridriver`）

指定浏览器驱动

```python
import qrunner
from qrunner import ChromeConfig


if __name__ == '__main__':
    ChromeConfig.command_executor = '/Users/UI/Documents/chromedriver'
    qrunner.main(platform='web', browser="chrome")
```

### 指定不同的浏览器

我们运行的自动化测试不可能只在一个浏览器下运行，我们分别需要在chrome、firefox浏览器下运行。在qrunner中需要只需要修改一个配置即可。

```python
import qrunner
# ……
if __name__ == '__main__':
    qrunner.main(browser="chrome") # chrome浏览器,默认值
    qrunner.main(browser="gc")     # chrome简写
    qrunner.main(browser="firefox") # firefox浏览器
    qrunner.main(browser="ff")      # firefox简写
    qrunner.main(browser="edge")    # edge浏览器
    qrunner.main(browser="safari")  # safari浏览器
```
在`main()`方法中通过`browser`参数设置不同的浏览器，默认为`Chrome`浏览器。

## qrunner API

### 查找元素

* id_
* name
* class_name
* tag
* link_text
* partial_link_text
* css
* xpath

__使用方式__

```python
import qrunner


class TestDemo(qrunner.TestCase):
    
    def test_demo(self):
        self.elem(id_="kw", desc='xxx')
        self.elem(name="wd", desc="xxx")
        self.elem(class_name="s_ipt", desc="xxx")
        self.elem(tag_name="input", desc="xxx")
        self.elem(xpath="//input[@id='kw']", desc="xxx")
        self.elem(css="#kw", desc="xxx")
        self.elem(link_text="hao123", desc='xxx')
        self.elem(partial_link_text="hao", desc='xxx')
```

__帮助信息__

* [CSS选择器](https://www.w3school.com.cn/cssref/css_selectors.asp)
* [xpath语法](https://www.w3school.com.cn/xpath/xpath_syntax.asp)

__使用下标__

有时候无法通过一种定位找到单个元素，那么可以通过`index`指定一组元素中的第几个。

```python
self.elem(tag_name="input", index=7, desc="xxx")

```

通过`tag_name="input"`匹配出一组元素， `index=7` 指定这一组元素中的第8个，`index`默认下标为`0`。

### fixture

- 有时自动化测试用例的运行需要一些前置&后置步骤，qrunner提供了相应的方法。
- 只要继承了WebTestCase，每个用例类执行之前都会打开浏览器，类结束之后关闭浏览器

__start & end__

针对每条用例的fixture，可以放到`start()/end()`方法中。

```python
import qrunner


class TestCase(qrunner.TestCase):
    def start(self):
        print("一条测试用例开始")
        
    def end(self):
        print("一条测试结果")
        
    def test_search(self):
        self.open('https://www.baidu.com')
        self.elem(id_='kw', desc='输入框').set_and_enter('无人机')

```

__start_class & end_class__

针对每个测试类的fixture，可以放到`start_class()/end_class()`方法中。

```python
import qrunner


class TestCase(qrunner.TestCase):
    
    @classmethod
    def start_class(cls):
        print("测试类开始执行")
        
    @classmethod
    def end_class(cls):
        print("测试类结束执行")
        
    def test_search(self):
        pass
```

> 警告：不要把用例的操作步骤写到fixture方法中! 因为它不属于某条用例的一部分，一旦里面的操作步骤运行失败，测试报告都不会生成。
### 断言

qrunner 提供了一组针对Web页面的断言方法。

__使用方法__

```
# 断言标题是否等于"title"
self.assertTitle("title")

# 断言标题是否包含"title"
self.assertInTitle("title")

# 断言URL是否等于
self.assertUrl("url")

# 断言URL是否包含
self.assertInUrl("url")

# 断言页面包含“text”
self.assertText("text")

# 断言页面不包含“text”
self.assertNotText("text")

# 断言警告是否存在"text" 提示信息
self.assertAlertText("text")

# 断言元素是否存在
self.assertElement(css="#kw")

# 断言元素是否不存在
self.assertNotElement(css="#kwasdfasdfa")
```

### WebDriverAPI

qrunner简化了selenium中的API，使操作Web页面更加简单。

大部分API都由`WebDriver`类提供：

```python
import qrunner


class TestCase(qrunner.TestCase):
    
    def test_case(self):
        self.driver.open_url("https://www.baidu.com") # 打开页面
        self.driver.back() # 返回上一页
        self.driver.screenshot("登录页") # 截屏
        self.driver.max_window() # 页面全屏
        self.driver.set_window(1920, 1080) # 设置页面宽高
        old = self.driver.get_windows() # 获取当前页面句柄列表
        self.driver.switch_window(old) # 切换当前页面句柄
        self.driver.window_scroll(1920, 1080) # 设置页面滚动范围
        self.driver.switch_to_frame('xxx_id') # 切换到iframe
        self.driver.switch_to_frame_out() # 从iframe退回顶层页面
        self.driver.execute_js('alert("hell")') # 执行js脚本
        self.driver.click(self.elem(id_='kw', desc='xxx').get_element()) # 强制点击一个元素，在元素本阻挡等情况下使用
        self.driver.quit() # 退出浏览器
        self.driver.close() # 关闭当前页签
        self.driver.add_cookies([{"name": "xxx", "value": "xxx"}]) # 添加cookie
        self.driver.get_cookies() # 获取当前cookie列表
        self.driver.get_cookie('cookie_name') # 获取指定的cookie
        self.driver.delete_all_cookies() # 清空所有cookie
        self.driver.delete_cookie('cookie_name') # 删除指定的cokkie
        self.driver.refresh() # 刷新页面
        print(self.driver.get_page_content()) # 获取当前页面xml
        self.driver.get_title() # 获取页面标题
        self.driver.get_url() # 获取页面链接
        self.driver.get_alert_text() # 获取alert中的文本
        self.driver.accept_alert() # 同意
        self.driver.dismiss_alert() # 拒绝
```

### WebElement操作

qrunner把控件都封装成了WebElement对象，控件的操作封装成了WebElement对象的方法

```python
import qrunner


class TestCase(qrunner.TestCase):

    def start(self):
        self.element = self.elem(id_='kw', desc='xxx')

    def test_case(self):
        self.element.get_elements()  # 获取定位到的控件列表
        self.element.get_element()  # 获取第一个定位到的控件
        self.element.exists()  # 判断控件是否存在
        self.element.click()  # 单击
        self.element.click_exists()  # 如果控件存在才单击
        self.element.slow_click()  # 慢慢移动到控件上，然后单击
        self.element.right_click()  # 右键单击
        self.element.move_to_elem()  # 鼠标移动到控件上
        self.element.click_and_hold()  # 长按
        self.element.drag_and_drop(100, 100)  # 拖动到
        self.element.double_click()  # 双击
        self.element.set_text('xxx')  # 单击控件并输入
        self.element.set_and_enter('xxx')  # 输入后点击enter
        self.element.clear_text()  # 清空输入框
        self.element.enter()  # 选中控件，点击enter
        self.element.select_all()  # 全选操作
        self.element.cut()  # 剪切
        self.element.copy()  # 复制
        self.element.paste()  # 粘贴
        self.element.backspace()  # 退格
        self.element.delete()  # 删除一个字符
        self.element.tab()  # 点一下tab
        self.element.space()  # 点击space建
        print(self.element.rect) # 返回控件左上角坐标和宽高
        print(self.element.get_attr('xxx')) # 控件的属性
        print(self.element.get_display()) # 控件的display属性
        print(self.element.text) # 控件的文本
        self.element.select_index(0) # 下拉列表选择
        self.element.select_text('xx') # 下拉列表选择
        self.element.submit() # 表单提交
```

## 更多配置

### 开启headless模式

Firefox和Chrome浏览器支持`headless`模式，即将浏览器置于后台运行，这样不会影响到我们在测试机上完成其他工作。

```python
import qrunner
from qrunner import ChromeConfig

#...

if __name__ == '__main__':
    ChromeConfig.headless = True
    qrunner.main(browser="chrome")
```

### 开放浏览器配置能力

qrunner为了更加方便的使用驱动，屏蔽了浏览器的配置，为了满足个性化的需求，比如禁用浏览器插件，设置浏览器代理等。所以，通过ChromeConfig类的参数来开放这些能力。

* 浏览器忽略无效证书

```python
import qrunner
from qrunner import ChromeConfig
from selenium.webdriver import ChromeOptions


if __name__ == '__main__':
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')  # 忽略无效证书的问题
    ChromeConfig.options = chrome_options
    qrunner.main(browser="chrome")
```

将要`ChromeOption`添加的设置赋值给`ChromeConfig`的`options`变量。

* 浏览器关闭沙盒模式

```python
import qrunner
from qrunner import ChromeConfig
from selenium.webdriver import ChromeOptions


if __name__ == '__main__':
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--no-sandbox')  # 关闭沙盒模式
    ChromeConfig.options = chrome_options
    ChromeConfig.headless = True
    qrunner.main(browser="chrome")
```

* 开启实验性功能

chrome开启实验性功能参数 `excludeSwitches`。

```python
import qrunner
from qrunner import ChromeConfig
from selenium.webdriver import ChromeOptions


if __name__ == '__main__':
    option = ChromeOptions()
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    ChromeConfig.options = option
    qrunner.main(browser="chrome")
```

### Selenium Grid

首先，安装Java环境，然后下载 `selenium-server`。

```shell
> java -jar .\selenium-server-4.3.0.jar standalone
00:25:28.023 INFO [LoggingOptions.configureLogEncoding] - Using the system default encoding
00:25:28.029 INFO [OpenTelemetryTracer.createTracer] - Using OpenTelemetry for tracing
00:25:36.978 INFO [NodeOptions.getSessionFactories] - Detected 16 available processors
00:25:37.012 INFO [NodeOptions.discoverDrivers] - Discovered 3 driver(s)
00:25:37.043 INFO [NodeOptions.report] - Adding Chrome for {"browserName": "chrome"} 16 times
00:25:37.045 INFO [NodeOptions.report] - Adding Firefox for {"browserName": "firefox"} 16 times
00:25:37.046 INFO [NodeOptions.report] - Adding Edge for {"browserName": "MicrosoftEdge"} 16 times
00:25:38.260 INFO [Node.<init>] - Binding additional locator mechanisms: id, name, relative
00:25:38.281 INFO [GridModel.setAvailability] - Switching Node 373df045-cf78-4d52-84c0-d99fd2c7a374 (uri: http://10.2.212.3:4444) from DOWN to UP
00:25:38.282 INFO [LocalDistributor.add] - Added node 373df045-cf78-4d52-84c0-d99fd2c7a374 at http://10.2.212.3:4444. Health check every 120s
00:25:42.503 INFO [Standalone.execute] - Started Selenium Standalone 4.3.0 (revision a4995e2c09*): http://10.2.212.3:4444
```

```python
import qrunner
from qrunner import ChromeConfig


# ……
if __name__ == '__main__':
    ChromeConfig.command_executor = "http://10.2.212.3:4444"
    qrunner.main(browser="chrome")
```

* 设置远程节点，[selenium Grid doc](https://www.selenium.dev/documentation/grid/getting_started/)。

# HTTP接口测试

## 开始使用

### 前言

HTTP接口测试很简单，不管工具、框架、还是平台，只要很的好的几个点就是好工具。

1. 测试数据问题：比如删除接口，重复执行还能保持结果一致，必定要做数据初始化。
2. 接口依赖问题：B接口依赖A的返回值，C接口依赖B接口的返回值。
3. 加密问题：不同的接口加密规则不一样。有些用到时间戳、md5、base64、AES，如何提供种能力。
4. 断言问题：有些接口返回的结构体很复杂，如何灵活的做到断言。

对于以上问题，工具和平台要么不支持，要么很麻烦，然而框架是最灵活的。 

> unittest/pytest + requests/https 直接上手写代码就好了，既简单又灵活。

那么同样是写代码，A框架需要10行，B框架只需要5行，然而又不失灵活性，那我当然是选择更少的了，毕竟，人生苦短嘛。

qrunner适合个人接口自动化项目，它有以下优势。

* 可以写更少的代码
* 自动生成HTML测试报告
* 支持参数化，减少重复的代码
* 支持生成随机数据
* 支持数据库操作

这些是qrunner支持的功能，我们只需要集成HTTP接口库，并提供强大的断言即可。

qrunner 兼容 [Requests](https://docs.python-requests.org/en/master/) API 如下:

|  qrunner   | requests  |
|  ----  | ----  |
| self.get()  | requests.get() |
| self.post()  | requests.post() |
| self.put()  | requests.put() |
| self.delete()  | requests.delete() |

### qrunner VS Request+unittest

先来看看unittest + requests是如何来做接口自动化的：

```python
import unittest
import requests


class TestAPI(unittest.TestCase):

    def test_get_method(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = requests.get("http://httpbin.org/get", params=payload)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
```

这其实已经非常简洁了。同样的用例，用qrunner实现。

```python
# test_req.py
import qrunner


class TestAPI(qrunner.TestCase):

    def test_get_method(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        self.get("http://httpbin.org/get", params=payload)
        self.assertStatusCode(200)


if __name__ == '__main__':
    qrunner.main()
```

主要简化点在，接口的返回数据的处理。当然，qrunner真正的优势在断言、日志和报告。


### 运行测试

```shell
/Users/UI/PycharmProjects/qrunner_new_gitee/venv/bin/python /Users/UI/PycharmProjects/qrunner_new_gitee/test_api.py
2022-10-10 09:07:25,350 - root - INFO - 执行用例
2022-10-10 09:07:25,418 - root - INFO - 用例路径: /Users/UI/PycharmProjects/qrunner_new_gitee/test_api.py
2022-10-10 09:07:25,418 - root - INFO - ['/Users/UI/PycharmProjects/qrunner_new_gitee/test_api.py', '-sv', '--reruns', '0', '--alluredir', 'allure-results', '--clean-alluredir']
============================= test session starts ==============================
platform darwin -- Python 3.9.10, pytest-6.2.5, py-1.11.0, pluggy-1.0.0 -- /Users/UI/PycharmProjects/qrunner_new_gitee/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/UI/PycharmProjects/qrunner_new_gitee
plugins: xdist-2.5.0, forked-1.4.0, allure-pytest-2.9.45, rerunfailures-10.2, dependency-0.5.1, ordering-0.6
collecting ... collected 1 item

test_api.py::TestAPI::test_get_method 2022-10-10 09:07:25,542 - root - DEBUG - [start_time]: 2022-10-10 09:07:25


2022-10-10 09:07:25,543 - root - INFO - -------------- Request -----------------[🚀]
2022-10-10 09:07:25,543 - root - DEBUG - [method]: GET      [url]: http://httpbin.org/get 

2022-10-10 09:07:25,548 - urllib3.connectionpool - DEBUG - Starting new HTTP connection (1): httpbin.org:80
2022-10-10 09:07:26,064 - urllib3.connectionpool - DEBUG - http://httpbin.org:80 "GET /get?key1=value1&key2=value2 HTTP/1.1" 200 376
2022-10-10 09:07:26,065 - root - DEBUG - [headers]:
 {"User-Agent": "python-requests/2.28.1", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "keep-alive"} 

2022-10-10 09:07:26,065 - root - DEBUG - [params]:
 {"key1": "value1", "key2": "value2"} 

2022-10-10 09:07:26,065 - root - INFO - -------------- Response ----------------
2022-10-10 09:07:26,065 - root - DEBUG - [type]: json 

2022-10-10 09:07:26,065 - root - DEBUG - [response]:
 {"args": {"key1": "value1", "key2": "value2"}, "headers": {"Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Host": "httpbin.org", "User-Agent": "python-requests/2.28.1", "X-Amzn-Trace-Id": "Root=1-6343704e-1dbe48bc4eb003ef007efe05"}, "origin": "58.251.23.66", "url": "http://httpbin.org/get?key1=value1&key2=value2"} 

PASSED2022-10-10 09:07:26,065 - root - DEBUG - [end_time]: 2022-10-10 09:07:26
2022-10-10 09:07:26,066 - root - DEBUG - [run_time]: 0.52 s


============================== 1 passed in 0.54s ===============================
```

通过日志/报告都可以清楚的看到。

* 请求的方法
* 请求url
* 响应的类型
* 响应的数据

## 更强大的断言

断言接口返回的数据是我们在做接口自动化很重要的工作。

### assertPath

`assertPath` 是基于 `jmespath` 实现的断言，功能非常强大。

jmespath: https://jmespath.org/specification.html

接口返回数据如下：

```json
{
  "args": {
    "hobby": 
      ["basketball", "swim"], 
    "name": "tom"
  }
}
```

qrunner中可以通过path进行断言：

```python
import qrunner


class TestAPI(qrunner.TestCase):

    def test_assert_path(self):
        payload = {'name': 'tom', 'hobby': ['basketball', 'swim']}
        self.get("http://httpbin.org/get", params=payload)
        self.assertPath("args.name", "tom")
        self.assertPath("args.hobby[0]", "basketball")
        self.assertIn("args.hobby[0]", "ball")

```

* `args.hobby[0]` 提取接口返回的数据。
* `assertPath()` 判断提取的数据是否等于`basketball`; 
* `assertIn()` 判断提取的数据是否包含`ball`。

### 更多断言方法

```python
def assertStatusCode(status_code):
    """
    断言状态码
    """

def assertPath(path, value):
    """
    功能同assertEq，用于兼容历史代码
    doc: https://jmespath.org/
    """

def assertNotEq(path, value):
    """
    值不等于
    doc: https://jmespath.org/
    """

def assertLenEq(path, value):
    """
    断言列表长度等于多少
    doc: https://jmespath.org/
    """

def assertLenGt(path, value):
    """
    断言列表长度大于多少
    doc: https://jmespath.org/
    """

def assertLenGtOrEq(path, value):
    """
    断言列表长度大于等于多少
    doc: https://jmespath.org/
    """

def assertLenLt(path, value):
    """
    断言列表长度小于多少
    doc: https://jmespath.org/
    """

def assertLenLtOrEq(path, value):
    """
    断言列表长度小于等于多少
    doc: https://jmespath.org/
    """

def assertGt(path, value):
    """
    值大于多少
    doc: https://jmespath.org/
    """

def assertGtOrEq(path, value):
    """
    值大于等于
    doc: https://jmespath.org/
    """

def assertLt(path, value):
    """
    值小于多少
    doc: https://jmespath.org/
    """

def assertLtOrEq(path, value):
    """
    值小于等于多少
    doc: https://jmespath.org/
    """

def assertRange(path, start: int, end: int):
    """值在(start, end)范围内
    doc: https://jmespath.org/
    """

def assertIn(path, value):
    """
    断言匹配结果被value_list包含
    doc: https://jmespath.org/
    """

def assertNotIn(path, value):
    """
    断言匹配结果不被value_list包含
    doc: https://jmespath.org/
    """

def assertNotExists(path):
    """断言字段不存在"""

def assertContains(path, value):
    """
    断言匹配结果包含value
    doc: https://jmespath.org/
    """

def assertNotContains(path, value):
    """
    断言匹配结果不包含value
    doc: https://jmespath.org/
    """

def assertTypeMatch(path, value_type):
    """
    类型匹配
    doc: https://jmespath.org/
    """

def assertStartsWith(path, value):
    """
    以什么开头
    doc: https://jmespath.org/
    """

def assertEndsWith(path, value):
    """
    以什么结尾
    doc: https://jmespath.org/
    """

def assertRegexMatch(path, value):
    """
    正则匹配
    doc: https://jmespath.org/
    """
```

## 更多功能

### 接口数据依赖

在场景测试中，我们需要利用上一个接口的数据，调用下一个接口。

* 简单的接口依赖

```python
import qrunner

class TestRespData(qrunner.TestCase):

    def test_data_dependency(self):
        """
        Test for interface data dependencies
        """
        headers = {"X-Account-Fullname": "bugmaster"}
        self.get("/get", headers=headers)
        self.assertStatusCode(200)

        username = self.response["headers"]["X-Account-Fullname"]
        self.post("/post", data={'username': username})
        self.assertStatusCode(200)
```

qrunner提供了`self.response`用于记录上个接口返回的结果，直接拿来用即可。

* 封装接口依赖

1. 创建公共模块

```python
# common.py
from qrunner import HttpRequest


class Common(HttpRequest):
    
    def get_login_user(self):
        """
        调用接口获得用户名
        """
        headers = {"Account": "bugmaster"}
        r = self.get("http://httpbin.org/get", headers=headers)
        return r


if __name__ == '__main__':
    c = Common()
    c.get_login_user()
```

2. 引用公共模块

```python
import qrunner
from common import Common


class TestRequest(qrunner.TestCase):

    def start(self):
        self.c = Common()

    def test_case(self):
        # 调用 get_login_user() 获取
        user = self.c.get_login_user()
        self.post("http://httpbin.org/post", data={'username': user})
        self.assertStatusCode(200)


if __name__ == '__main__':
    qrunner.main()

```

### 共享登录态

```python
import qrunner


def get_headers():
    return {
        "login_headers": {
            "token": "xxx"
        },
        "visit_headers": {
            "visit_id": "xxx"
        }
    }


if __name__ == '__main__':
    qrunner.main(headers=get_headers())
```

只要按格式传入登录和游客态的请求头，所有的请求就可以自动带上对应的请求头，以实现携带登录态的功能

# APP UI 测试

## 公共依赖

* [weditor](https://github.com/alibaba/web-editor)
  - 用于查看控件属性
    
* 手机通过usb连接电脑

## 安卓 UI 测试

### 依赖环境

* [adb](https://formulae.brew.sh/cask/android-platform-tools)
    - 用于查看手机设备id
    
### qrunner API

#### 查找元素

* id_
* class_name
* text
* xpath

__使用方式__

```python
self.elem(id_="kw", desc='xxx')
self.elem(class_name="wd", desc="xxx")
self.elem(text="s_ipt", desc="xxx")
self.elem(xpath="input", desc="xxx")

```

__帮助信息__

* [xpath语法](https://www.w3school.com.cn/xpath/xpath_syntax.asp)

__省略包名__

安卓控件的resourceId都是以com.qi.xxx的包名开头的，只要在main方法传入android_pkg即可

__使用下标__

有时候无法通过一种定位找到单个元素，那么可以通过`index`指定一组元素中的第几个。

```python
self.elem(class_name="input", index=7, desc="xxx")

```

通过`class_name="input"`匹配出一组元素， `index=7` 指定这一组元素中的第8个，`index`默认下标为`0`。

#### fixture

- 有时自动化测试用例的运行需要一些前置&后置步骤，qrunner提供了相应的方法。
- 只要继承了AndroidTestCase，每条用例执行之前都会启动应用，结束之后会停止应用

__start & end__

针对每条用例的fixture，可以放到`start()/end()`方法中。

```python
import qrunner


class TestCase(qrunner.TestCase):
    def start(self):
        print("一条测试用例开始")
        self.elem1 = self.elem(xpath='xx', desc='xx')
        
    def end(self):
        print("一条测试结果")
        
    def test_search(self):
        self.elem1.click()
```

__start_class & end_class__

针对每个测试类的fixture，可以放到`start_class()/end_class()`方法中。

```python
import qrunner


class DemoPage(qrunner.Page):
    LOC_INPUT = {'id_': 'kw', 'desc': '输入框'}
    
    def input(self):
      self.elem(**self.LOC_INPUT).set_text('xx')


class TestCase(qrunner.TestCase):
    
    @classmethod
    def start_class(cls):
        print("测试类开始执行")
        cls.dp = DemoPage(cls.driver)
        
    @classmethod
    def end_class(cls):
        print("测试类结束执行")
        
    def test_search(self):
        self.dp.input()
```

> 警告：不要把用例的操作步骤写到fixture方法中! 因为它不属于某条用例的一部分，一旦里面的操作步骤运行失败，测试报告都不会生成。
#### 断言

qrunner 提供了一组针对安卓页面的断言方法。

__使用方法__

```
def assertText(self, expect_value, timeout=5):
    """断言页面包含文本"""

def assertNotText(self, expect_value, timeout=5):
    """断言页面不包含文本"""

def assertElement(self, timeout=5, **kwargs):
    """断言元素存在"""

def assertNotElement(self, timeout=5, **kwargs):
    """断言元素不存在"""
```

#### AndroidDriverAPI

qrunner简化了uiautomator2中的API，使操作安卓页面更加简单。

大部分API都由`AndroidDriver`类提供：

```python

def uninstall_app(self, pkg_name=None):
    """卸载应用"""

def install_app(self, apk_path):
    """安装应用"""

def new_install_app(self, apk_path, pkg_name=None):
    """先卸载再安装应用"""

def start_app(self, pkg_name=None):
    """启动应用"""

def force_start_app(self, pkg_name=None):
    """重启应用"""

def stop_app(self, pkg_name=None):
    """停止指定应用"""

def stop_all_app(self):
    """停止所有应用"""

def stop_app_list(self, app_list: list):
    """退出指定多个应用"""

def clear_app(self, pkg_name=None):
    """清除应用缓存"""

def get_driver_info(self):
    """设备连接信息"""

def get_app_info(self, pkg_name=None):
    """获取指定应用信息"""

def get_current_app(self):
    """获取当前应用信息"""

def save_app_icon(self, pkg_name=None):
    """保存应用icon"""

def get_running_apps(self):
    """获取正在运行的应用"""

def get_app_list(self):
    """获取所有已安装的应用"""

def wait_app_running(self, pkg_name=None, front=True, timeout=20):
    """
    等待应用运行
    @param pkg_name: 应用包名
    @param front: 是否前台运行
    @param timeout: 等待时间
    @return: 应用pid
    """

def wait_activity(self, activity_name, timeout=10):
    """
    等待activity运行
    @param activity_name: activity名称，.ApiDemos
    @param timeout: 超时时间
    @return: True or False
    """

def push(self, src_path, target_path, mode=None):
    """
    把电脑本地文件上传到手机上
    @param src_path: 电脑本地文件，foo.txt
    @param target_path: 手机目录，/sdcard/
    @param mode: 需要修改的权限，0o755
    @return:
    """

def pull(self, src_path, target_path):
    """
    把手机上的文件下载到电脑
    @param src_path: 手机文件，/sdcard/tmp.txt
    @param target_path: 电脑目录，tmp.txt
    @return:
    """

def check(self):
    """检查设备连接状态"""

def open_url(self, url):
    """
    通过url打开web页面或者app schema
    @param url: 页面url，https://www.baidu.com，taobao://taobao.com
    @return:
    """

def shell(self, cmd, timeout=60):
    """
    执行短周期shell脚本
    @param cmd: shell字符串或list，pwd，["ls", "-l"]
    """

def start_session(self, pkg_name=None):
    """
    启动应用并生成session
    """

def stop_session(self):
    """关闭session并停止应用"""

def check_session(self):
    """检查session是否可用"""

def screenshot(self, file_name):
    """
    截图并保存到预定路径
    @param file_name: foo.png or fool
    @return:
    """

def upload_pic(self, file_name):
    """截图并上传allure"""

def get_page_content(self):
    """获取页面xml内容"""

def get_window_size(self):
    """获取页面宽高"""

def get_serial(self):
    """获取设备id"""

def get_device_info(self):
    """获取设备信息"""

def screen_on(self):
    """点亮屏幕"""

def screen_off(self):
    """关闭屏幕"""

def get_screen_status(self):
    """获取屏幕点亮状态"""

def unlock(self):
    """解锁手机"""

def press(self, key):
    """
    点击原生自带按键
    @param key: 按键名，支持：home、back、left、right、up、down、center、menu、search、enter、delete、recent、volume_up、
                volume_down、volume_mute、camera、power
    """

def click(self, x, y):
    """点击坐标"""

def click_alert(self, alert_list: list):
    """点击弹窗"""

def double_click(self, x, y):
    """双击坐标"""

def long_click(self, x, y):
    """长按坐标"""

def swipe(self, sx, sy, ex, ey):
    """滑动"""

def swipe_left(self, scale=0.9):
    """往左滑动"""

def swipe_right(self, scale=0.9):
    """往右滑动"""

def swipe_up(self, scale=0.8):
    """往上滑动"""

def swipe_down(self, scale=0.8):
    """往下滑动"""

def scroll_down_fast(self):
    """快速往下滑动"""

def scroll_down_slow(self, step=50):
    """
    通过step控制滑动速度
    """

def scroll_up_fast(self):
    """快速往上滑动"""

def scroll_up_down(self, step):
    """
    通过step控制滑动速度
    """

def scroll_bottom_fast(self):
    """快速滑到底部"""

def scroll_bottom_slow(self, step=50):
    """
    通过step控制滑动速度
    """

def scroll_top_fast(self):
    """快速滑动到顶部"""

def scroll_top_slow(self, step=50):
    """
    通过step控制滑动速度
    """

def scroll_to(self, *args, **kwargs):
    """滑动到元素"""

def drag(self, sx, sy, ex, ey):
    """拖动"""

def set_password(self, text, clear=True):
    """输入密码"""

def set_ori_left(self):
    """屏幕向右边转动"""

def set_ori_right(self):
    """屏幕向左边转动"""

def set_ori_natural(self):
    """屏幕恢复原始转向"""

def start_record(self, file_name='output'):
    """开始录制"""

def stop_record(self):
    """停止录制"""
```

#### AndroidElement操作

qrunner把控件都封装成了AndroidElement对象，控件的操作封装成了AndroidElement对象的方法

```python

def get_elements(self, retry=3, timeout=3, alert_list=None):
    """
    获取元素列表
    """

def get_element(self, retry=3, timeout=3, alert_list=None):
    """
    获取指定一个元素
    """

@property
def info(self):
    """获取元素信息"""

@property
def text(self):
    """获取元素文本属性"""

@property
def bounds(self):
    """获取元素坐标"""

@property
def rect(self):
    """获取元素左上角的坐标以及宽高"""

@property
def visibleBounds(self):
    """获取元素可见坐标"""

@property
def focusable(self):
    """获取元素是否聚焦"""

@property
def selected(self):
    """获取元素是否选中"""

def child(self, *args, **kwargs):
    """获取元素儿子节点，不能用于PageObject，会导致在应用启动前进行元素识别"""

def brother(self, *args, **kwargs):
    """获取兄弟元素"""

def left(self, *args, **kwargs):
    """获取左边元素"""

def right(self, *args, **kwargs):
    """获取右边元素"""

def up(self, *args, **kwargs):
    """获取上边的元素"""

def down(self, *args, **kwargs):
    """获取下边的元素"""

def exists(self, timeout=1):
    """判断元素是否存在"""

def click(self, retry=3, timeout=3, alert_list=None):
    """单击"""

def click_exists(self, timeout=3):
    """元素存在才点击"""

def click_gone(self):
    """等元素消失后再点击"""

def wait_gone(self, timeout=3):
    """等待元素消失"""

def long_click(self):
    """长按"""

def set_text(self, text):
    """输入文本"""

def clear_text(self):
    """清除文本"""

def drag_to(self, *args, **kwargs):
    """拖动到另外一个元素的位置"""

def swipe_left(self):
    """向左滑动"""

def swipe_right(self):
    """向右滑动"""

def swipe_up(self):
    """向上滑动"""

def swipe_down(self):
    """向下滑动"""
```

## IOS UI 测试

### 依赖环境

* [WebDriverAgent](https://testerhome.com/topics/7220)
    - 把代码操作转化成原生操作
* [tidevice](https://github.com/alibaba/taobao-iphone-device)
    - 查看手机设备id
    - 启动WebDriverAgent
    
### qrunner API

#### 查找元素

* name
* label
* value
* text
* class_name
* xpath

__使用方式__

```python
self.elem(name="kw", desc='xxx')
self.elem(label="wd", desc="xxx")
self.elem(value="s_ipt", desc="xxx")
self.elem(text="input", desc="xxx")
self.elem(class_name="input", desc="xxx")
self.elem(xpath="input", desc="xxx")

```

__帮助信息__

* [xpath语法](https://www.w3school.com.cn/xpath/xpath_syntax.asp)


__使用下标__

有时候无法通过一种定位找到单个元素，那么可以通过`index`指定一组元素中的第几个。

```python
self.elem(class_name="input", index=7, desc="xxx")

```

通过`class_name="input"`匹配出一组元素， `index=7` 指定这一组元素中的第8个，`index`默认下标为`0`。

#### fixture

- 有时自动化测试用例的运行需要一些前置&后置步骤，qrunner提供了相应的方法。
- 只要继承了IosTestCase，每条用例执行之前都会启动应用，结束之后会停止应用

__start & end__

针对每条用例的fixture，可以放到`start()/end()`方法中。

```python
import qrunner


class TestCase(qrunner.TestCase):
    def start(self):
        print("一条测试用例开始")
        self.elem1 = self.elem(label='kw', desc='输入框')
        
    def end(self):
        print("一条测试结果")
        
    def test_search(self):
        self.elem1.click()
```

__start_class & end_class__

针对每个测试类的fixture，可以放到`start_class()/end_class()`方法中。

```python
import qrunner


class DemoPage(qrunner.Page):
    LOC_INPUT = {'label': 'kw', 'desc': '输入框'}
    
    def input(self):
      self.elem(**self.LOC_INPUT).set_text('xxx')


class TestCase(qrunner.TestCase):
    
    @classmethod
    def start_class(cls):
        print("测试类开始执行")
        cls.dp = DemoPage(cls.driver)
        
    @classmethod
    def end_class(cls):
        print("测试类结束执行")
        
    def test_search(self):
        self.dp.input()
```

> 警告：不要把用例的操作步骤写到fixture方法中! 因为它不属于某条用例的一部分，一旦里面的操作步骤运行失败，测试报告都不会生成。
#### 断言

qrunner 提供了一组针对IOS页面的断言方法。

__使用方法__

```
def assertText(self, expect_value, timeout=5):
    """断言页面包含文本"""

def assertNotText(self, expect_value, timeout=5):
    """断言页面不包含文本"""

def assertElement(self, timeout=5, **kwargs):
    """断言元素存在"""

def assertNotElement(self, timeout=5, **kwargs):
    """断言元素不存在"""
```

#### IosDriverAPI

qrunner简化了facebook-wda中的API，使操作IOS页面更加简单。

大部分API都由`IosDriver`类提供：

```python

def install_app(self, ipa_url):
    """安装应用"""

def new_install_app(self, ipa_url, bundle_id=None):
    """先卸载，再安装"""

def uninstall_app(self, bundle_id=None):
    """卸载应用"""

def start_app(self, bundle_id=None):
    """启动应用"""

def force_start_app(self, bundle_id=None):
    """重启应用"""

def stop_app(self, bundle_id=None):
    """停止应用"""

def app_current(self):
    """获取运行中的app列表"""

def app_launch(self, bundle_id=None):
    """将应用切到前台"""

def back(self):
    """返回上一页"""

def go_home(self):
    """返回手机主页"""

def send_keys(self, value):
    """输入内容"""

def screenshot(self, file_name):
    """
    截图并保存到预定路径
    @param file_name: foo.png or fool
    @return:
    """

@property
def page_content(self):
    """获取页面xml内容"""

def get_window_size(self):
    """获取屏幕尺寸"""

def click(self, x, y):
    """点击坐标"""

def double_click(self, x, y):
    """双击坐标"""

def tap_hold(self, x, y):
    """长按坐标"""

def click_alert(self, alert_list: list):
    """点击弹窗"""

def swipe(self, start_x, start_y, end_x, end_y, duration=0):
    """根据坐标滑动"""

def swipe_by_screen_percent(self, start_x_percent, start_y_percent, end_x_percent, end_y_percent, duration=0):
    """根据屏幕百分比滑动"""

def swipe_left(self, start_percent=1, end_percent=0.5):
    """往左滑动"""

def swipe_right(self, start_percent=0.5, end_percent=1):
    """往右滑动"""

def swipe_up(self, start_percent=0.8, end_percent=0.2):
    """往上滑动"""

def swipe_down(self, start_percent=0.2, end_percent=0.8):
    """往下滑动"""

def check(self):
    """检查设备连接状态"""

def locked(self):
    """检查手机是否锁屏"""

def lock(self):
    """锁屏"""

def unlock(self):
    """解锁"""

def open_url(self, url):
    """
    打开schema
    @param: url，schema链接，taobao://m.taobao.com/index.htm
    @return:
    """

@property
def battery_info(self):
    """电池信息"""

@property
def device_info(self):
    """设备信息"""

@property
def scale(self):
    """获取分辨率"""
```

#### IosElement操作

qrunner把控件都封装成了IosElement对象，控件的操作封装成了IosElement对象的方法

```python

def get_elements(self, retry=3, timeout=3, alert_list=None):
    """
    针对元素定位失败的情况，抛出NoSuchElementException异常
    @param retry:
    @param timeout:
    @param alert_list
    @return:
    """

# def __getitem__(self, index):
#     elements = self.get_elements()
#     return elements[index]

def get_element(self, retry=3, timeout=3, alert_list=None):
    """
    针对元素定位失败的情况，抛出NoSuchElementException异常
    @param retry:
    @param timeout:
    @param alert_list
    @return:
    """

@property
def info(self):
    """获取元素信息"""

@property
def text(self):
    """获取元素文本"""

@property
def className(self):
    """获取元素className"""

@property
def name(self):
    """获取元素name"""

@property
def visible(self):
    """获取元素visible属性"""

@property
def value(self):
    """获取元素value"""

@property
def label(self):
    """获取元素label"""

@property
def enabled(self):
    """获取元素enabled属性"""

@property
def displayed(self):
    """获取元素displayed属性"""

@property
def bounds(self):
    """获取元素bounds属性"""

@property
def rect(self):
    """获取元素左上角坐标和宽高"""

def exists(self, timeout=1):
    """
    判断元素是否存在当前页面
    @param timeout:
    @return:
    """

def wait_gone(self, timeout=10):
    """等待元素消失"""

def click(self, retry=3, timeout=3, alert_list=None):
    """
    单击
    @param: retry，重试次数
    @param: timeout，每次重试超时时间
    @param: alert_list，异常弹窗列表
    """

def click_exists(self, timeout=3):
    """元素存在时点击"""

def clear_text(self):
    """清除文本"""

def set_text(self, text):
    """输入内容"""

def scroll(self, direction=None):
    """
    scroll to make element visiable
    @param: direction，方向，"up", "down", "left", "right"
    @return:
    """

def swipe_left(self):
    """往左滑动"""

def swipe_right(self):
    """往右滑动"""

def swipe_up(self):
    """往上滑动"""

def swipe_down(self):
    """往下滑动"""

def child(self, *args, **kwargs):
    """获取兄弟节点，不能用于PageObject，会导致在应用启动前进行元素识别"""
```
