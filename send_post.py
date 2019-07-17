import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def process():
    options = Options()
    options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错
    options.add_argument('window-size=1920x3000') #指定浏览器分辨率
    options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
    options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    broswer = webdriver.Chrome(os.path.abspath('./drivers/chromedriver_linux'), options=options)
    
    broswer.set_page_load_timeout(20)
    broswer.set_script_timeout(20)
    try:
        print('try opening website...')
        broswer.get('https://vip.anjuke.com/login/')
    except:
        print('timeout...stop page loading')
        broswer.execute_script("window.stop()")

    # 切换账号密码登录
    span = broswer.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[1]/span[2]')
    span.click()
    time.sleep(1)

    # 登录
    print('try login...')
    broswer.find_element_by_id('loginName').send_keys('13928753569')
    broswer.find_element_by_id('loginPwd').send_keys('YZXyzx123456')
    broswer.find_element_by_id('loginSubmit').submit()
    time.sleep(1)

    # 发布房源
    print('switch to publish rent page')
    broswer.get('https://vip.anjuke.com/house/publish/rent/?from=manage')
    time.sleep(2)

    # 阅读条款
    print('readed button')
    readBtn = broswer.find_element_by_xpath('//*[@id="publishHouse"]/div[2]/div/button')
    if readBtn is not None:
        readBtn.click()

    # 小区名称
    print('fill community unite...')
    broswer.find_element_by_id('community_unite').send_keys('中汇城')
    time.sleep(3)
    broswer.find_element_by_xpath('//*[@id="publish_form"]/div[3]/div/ul/li[1]').click()

    # 室
    print('fill shi...')
    broswer.find_element_by_name('shi').send_keys('1')

    # 厅
    print('fill ting...')
    broswer.find_element_by_name('ting').send_keys('1')

    # 卫
    print('fill wei...')
    broswer.find_element_by_name('wei').send_keys('1')

    # 所在楼层
    print('fill current floor')
    broswer.find_element_by_name('suoZaiLouCeng').send_keys('5')

    # 总共楼层
    print('fill total floors')
    broswer.find_element_by_name('zongLouCeng').send_keys('11')

    # 电梯
    print('select dianti')
    broswer.find_element_by_xpath('//*[@id="publish_form"]/div[8]/label[2]').click()

    # 总面积
    broswer.find_element_by_name('mianJi').send_keys('35')

    # 已出租
    broswer.find_element_by_name('params_101').send_keys('0')

    # 共几户
    broswer.find_element_by_name('params_196').send_keys('2')

    # 房屋类型
    print('selectting house type...')
    broswer.find_element_by_xpath('//*[@id="select-housetype"]/div').click()
    time.sleep(0.2)
    broswer.find_element_by_xpath('//*[@id="select-housetype"]/div/ul/li[3]').click()

    # 装修情况
    print('selectting house fit...')
    broswer.find_element_by_xpath('//*[@id="select-housefit"]/div').click()
    time.sleep(0.2)
    broswer.find_element_by_xpath('//*[@id="select-housefit"]/div/ul/li[4]').click()

    # 朝向
    print('selectting exposure')
    broswer.find_element_by_xpath('//*[@id="select-exposure"]/div').click()
    time.sleep(0.2)
    broswer.find_element_by_xpath('//*[@id="select-exposure"]/div/ul/li[3]').click()

    # 公共设施
    broswer.find_element_by_xpath('//*[@id="publish_form"]/div[12]/div/div/label[1]').click()

    # 待租卧室 - 类型
    print('select bedroom')
    broswer.find_element_by_xpath('//*[@id="select-bedroom"]/div').click()
    time.sleep(0.2)
    broswer.find_element_by_xpath('//*[@id="select-bedroom"]/div/ul/li[3]').click()

    # 待租卧室 - 朝向
    broswer.find_element_by_xpath('//*[@id="select-roomorient"]/div').click()
    time.sleep(0.2)
    broswer.find_element_by_xpath('//*[@id="select-roomorient"]/div/ul/li[3]').click()

    # 待租卧室 - 限制
    broswer.find_element_by_xpath('//*[@id="select-sex"]/div').click()
    time.sleep(0.2)
    broswer.find_element_by_xpath('//*[@id="select-sex"]/div/ul/li[2]').click()

    # 待租卧室 - 面积
    broswer.find_element_by_name('params_12').send_keys('23')

    # 价格
    print('fill price...')
    broswer.find_element_by_name('jiaGe').send_keys('1500')

    # 付款方式
    print('fill pay type...')
    broswer.find_element_by_xpath('//*[@id="select-paymode"]/div').click()
    time.sleep(0.2)
    broswer.find_element_by_xpath('//*[@id="select-paymode"]/div/ul/li[2]').click()

    # 标题
    print('fill title...')
    broswer.find_element_by_name('title').send_keys('这里是标题这里是标题这里是标题这里是标题这里是标题')

    # 详细介绍
    # broswer.find_element_by_name('content_fangyuanxiangqing').send_keys('这里是描述')
    # broswer.execute_script('document.getElementsByName("content_fangyuanxiangqing").value = "这里是描述"')
    # 选择房源模板
    print('openning house templete window...')
    broswer.find_element_by_xpath('//*[@id="template_ctrl"]/a[2]').click()
    time.sleep(2)
    print('select house templete...')
    broswer.find_element_by_xpath('//*[@id="house_template"]/div[2]/div[1]/dl/dd/label').click()
    print('close templete window')
    broswer.find_element_by_xpath('//*[@id="house_template"]/div[2]/div[2]/a[1]').click()

    print('uploading images...')

    # 上传室内图
    file_path = os.path.abspath('./data/images/2019-07-06/38697195167240/99aef1d1a0b7f43ce138d167690f206a5399c003.jpg')
    broswer.find_element_by_id('room_fileupload').send_keys(file_path)
    file_path = os.path.abspath('./data/images/2019-07-06/38697195167240/863b66bd9453b8d31fa36056fc08d39fe98bacd6.jpg')
    broswer.find_element_by_id('room_fileupload').send_keys(file_path)
    file_path = os.path.abspath('./data/images/2019-07-06/38697195167240/89039b0f8a95ab6e82c493976062393c4a4f2453.jpg')
    broswer.find_element_by_id('room_fileupload').send_keys(file_path)

    # 上传户型图
    file_path = os.path.abspath('./data/images/2019-07-16/34824689599151/a2f67dab78b86a93e1a600998d515d21229540bb.jpg')
    broswer.find_element_by_id('model-fileupload').send_keys(file_path)

    # 等待图片上传完成
    print('waiting for upload images')
    time.sleep(20)

    # 设置封面
    broswer.find_element_by_xpath('//*[@id="room-upload-display"]/div[1]/div/i[1]').click()
    time.sleep(2)

    # 发布房源
    print('publish rent info...')
    broswer.find_element_by_id('publish-rent-add').click()
    time.sleep(5)

    # 结果检测
    if broswer.find_element_by_xpath('/html/body/div[4]/div[2]/dl/dd').text == '操作成功':
        print('发布成功')
    else:
        print('发布失败')

    time.sleep(3)
    broswer.quit()


if __name__ == '__main__':
    process()
