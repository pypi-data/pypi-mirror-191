import qrunner
from qrunner import Elem
from qrunner.core.ocr.element import OCRElem


class HomePage(qrunner.Page):
    """APP首页"""
    ad_close = Elem(res_id='bottom_btn', desc='广告关闭按钮')
    patent_entry = Elem(text='查专利', desc='查专利入口')

    def go_patent(self):
        self.elem(self.ad_close).click_exists()
        self.elem(self.patent_entry).click()


class PatentPage(qrunner.Page):
    """查专利首页"""
    report_entry = Elem(text='分析报告', desc='分析报告入口')
    tech_entry = Elem(text='技术全景报告', desc='技术全景报告入口')
    create_tech = Elem(text='创建技术全景报告', desc='创建技术报告标题')

    def go_tech_report(self):
        OCRElem(self.driver, **self.report_entry).click()
        OCRElem(self.driver, **self.tech_entry).click()
        assert OCRElem(self.driver, **self.create_tech).exists()


class TestAdvancedSearch(qrunner.TestCase):
    """高级搜索"""

    def start(self):
        self.hp = HomePage(self.driver)
        self.pp = PatentPage(self.driver)

    def test_01(self):
        self.hp.go_patent()
        self.pp.go_tech_report()


if __name__ == '__main__':
    qrunner.main(
        platform='android',
        device_id='UJK0220521066836',
        pkg_name='com.qizhidao.clientapp'
    )

