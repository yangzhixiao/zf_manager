import os
import time
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import db


def publish_house(fid, tid):
    num = db.query_count('select count(*) from publish_record where fid=? and status!=?', fid, '待发布')
    if num > 0:
        print('house is already published.', fid)
        db.close()
        return

    f_row = db.query_one('select * from house where id=?', fid)
    t_row = db.query_one('select * from template where id=?', tid)
    if f_row is None:
        print('house not found.', fid)
        db.close()
        return

    if t_row is None:
        print('template not found.', tid)
        db.close()
        return

    options = Options()
    driver_path = './drivers/chromedriver_mac'
    if sys.platform.startswith('linux'):
        options.add_argument('--no-sandbox')
        options.add_argument('window-size=1920x3000')
        options.add_argument('--disable-gpu')
        options.add_argument('--hide-scrollbars')
        options.add_argument('blink-settings=imagesEnabled=false')
        options.add_argument('--headless')
        driver_path = './drivers/chromedriver_linux'
    broswer = webdriver.Chrome(os.path.abspath(driver_path), options=options)
    
    broswer.set_page_load_timeout(5)
    broswer.set_script_timeout(20)
    try:
        print('try opening website...')
        broswer.get('https://vip.anjuke.com/login/')
    except Exception as ex:
        print('timeout...stop page loading: ', ex.__str__())
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
    broswer.find_element_by_id('community_unite').send_keys(t_row['community_unite'])
    time.sleep(3)
    broswer.find_element_by_xpath('//*[@id="publish_form"]/div[3]/div/ul/li[1]').click()

    # 室
    print('fill shi...')
    broswer.find_element_by_name('shi').send_keys(t_row['shi'])

    # 厅
    print('fill ting...')
    broswer.find_element_by_name('ting').send_keys(t_row['ting'])

    # 卫
    print('fill wei...')
    broswer.find_element_by_name('wei').send_keys(t_row['wei'])

    # 所在楼层
    print('fill current floor')
    broswer.find_element_by_name('suoZaiLouCeng').send_keys(t_row['suoZaiLouCeng'])

    # 总共楼层
    print('fill total floors')
    broswer.find_element_by_name('zongLouCeng').send_keys(t_row['zongLouCeng'])

    # 电梯
    print('select dianti')
    broswer.find_element_by_xpath('//*[@id="publish_form"]/div[8]/label[2]').click()

    # 总面积
    broswer.find_element_by_name('mianJi').send_keys(t_row['mianJi'])

    # 已出租
    broswer.find_element_by_name('params_101').send_keys(t_row['currentrent'])

    # 共几户
    broswer.find_element_by_name('params_196').send_keys(t_row['totalrent'])

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
    broswer.find_element_by_name('jiaGe').send_keys(t_row['jiaGe'])

    # 付款方式
    print('fill pay type...')
    broswer.find_element_by_xpath('//*[@id="select-paymode"]/div').click()
    time.sleep(0.2)
    broswer.find_element_by_xpath('//*[@id="select-paymode"]/div/ul/li[2]').click()

    # 标题
    print('fill title...')
    broswer.find_element_by_name('title').send_keys(t_row['title'])

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
    for img in str(f_row['imgs']).split(','):
        file_path = os.path.abspath(os.path.join('./data/images/', img))
        broswer.find_element_by_id('room_fileupload').send_keys(file_path)

    # 上传户型图
    file_path = os.path.abspath('./data/house_model.jpg')
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
    result = broswer.find_element_by_xpath('/html/body/div[4]/div[2]/dl/dd')
    if result is not None and result.text == '操作成功':
        print('发布成功')
        db.execute('update publish_record set status=? where fid=?', '已发布', fid)
    else:
        print('发布失败')
        db.execute('update publish_record set status=? where fid=?', '发布失败', fid)

    time.sleep(3)
    time.sleep(90000)
    broswer.quit()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        publish_house(sys.argv[1], sys.argv[2])
