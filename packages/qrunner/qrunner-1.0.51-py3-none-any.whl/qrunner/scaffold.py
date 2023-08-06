import os.path
import sys


case_content_android = """import qrunner
from qrunner import Elem


class HomePage(qrunner.Page):
    ad_close = Elem(res_id='bottom_btn', desc='广告关闭按钮')
    search_entry = Elem(res_id='banner', desc='搜索入口')

    def go_search(self):
        self.elem(self.ad_close).click_exists()
        self.elem(self.search_entry).click()


class SearchPage(qrunner.Page):
    search_input = Elem(res_id='cet_search_key', desc='搜索框')
    search_confirm = Elem(res_id='tv_search_cancel', desc='搜索确认按钮')

    def search(self, keyword: str):
        self.elem(self.search_input).set_text(keyword)
        self.elem(self.search_confirm).click()


class TestSearch(qrunner.TestCase):

    def start(self):
        self.hp = HomePage(self.driver)
        self.sp = SearchPage(self.driver)

    def test_pom(self):
        self.hp.go_search()
        self.sp.search('无人机')
        self.assert_in_page('航天彩虹无人机股份有限公司')


if __name__ == '__main__':
    qrunner.main(
        platform='android',
        device_id='UJK0220521066836',
        pkg_name='com.qizhidao.clientapp'
    )
"""

case_content_ios = """import qrunner
from qrunner import Elem


class HomePage(qrunner.Page):
    ad_close = Elem(label='close white big', desc='广告关闭按钮')
    search_entry = Elem(xpath='//*[@label="空列表"]/Other[2]', desc='搜索入口')
    
    def go_search(self):
        self.elem(self.ad_close).click_exists()
        self.elem(self.search_entry).click()


class SearchPage(qrunner.Page):
    search_input = Elem(class_name='TextField', desc='搜索框')
    search_confirm = Elem(class_name='StaticText', label='搜索', desc='搜索确认按钮')

    def search(self, keyword: str):
        self.elem(self.search_input).set_text(keyword)
        self.elem(self.search_confirm).click()


class TestSearch(qrunner.TestCase):

    def start(self):
        self.hp = HomePage(self.driver)
        self.sp = SearchPage(self.driver)

    def test_pom(self):
        self.hp.go_search()
        self.sp.search('无人机')
        self.assert_in_page('航天彩虹无人机股份有限公司')


if __name__ == '__main__':
    qrunner.main(
        platform='ios',
        device_id='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company'
    )

"""

case_content_web = """import qrunner
from qrunner import Elem


class PatentPage(qrunner.Page):
    search_input = Elem(id_='driver-home-step1', desc='查专利首页输入框')
    search_submit = Elem(id_='driver-home-step2', desc='查专利首页搜索确认按钮')
    
    def simple_search(self, keyword: str):
        self.elem(self.search_input).set_text(keyword)
        self.elem(self.search_submit).click()


class TestPatentSearch(qrunner.TestCase):

    def start(self):
        self.pp = PatentPage(self.driver)

    def test_pom(self):
        self.driver.open_url()
        self.pp.simple_search('无人机')
        self.assert_in_page('王刚毅')


if __name__ == '__main__':
    qrunner.main(
        platform='web',
        base_url='https://patents.qizhidao.com/'
    )
"""

case_content_api = """import qrunner


class TestGetToolCardListForPc(qrunner.TestCase):

    def test_getToolCardListForPc(self):
        path = '/api/qzd-bff-app/qzd/v1/home/getToolCardListForPc'
        payload = {"type": 1}
        self.post(path, json=payload)
        self.assert_eq('code', 0)


if __name__ == '__main__':
    qrunner.main(
        platform='api',
        base_url='https://www.qizhidao.com'
    )
"""

data_content = """{
  "card_type": [0, 1, 2]
}
"""


def create_scaffold(platform):
    """create scaffold with specified project name."""

    def create_folder(path):
        os.makedirs(path)
        msg = f"created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    # 新增测试数据目录
    create_folder(os.path.join("test_data"))
    create_file(
        os.path.join("test_data", "data.json"),
        data_content,
    )
    if platform == "android":
        # 新增安卓测试用例
        create_file(
            os.path.join("test_android.py"),
            case_content_android,
        )

    elif platform == "ios":
        # 新增ios测试用例
        create_file(
            os.path.join("test_ios.py"),
            case_content_ios,
        )
    elif platform == "web":
        # 新增web测试用例
        create_file(
            os.path.join("test_web.py"),
            case_content_web,
        )
    elif platform == "api":
        # 新增接口测试用例
        create_file(
            os.path.join("test_api.py"),
            case_content_api,
        )
    else:
        print("请输入正确的平台: android、ios、web、api")
        sys.exit()
