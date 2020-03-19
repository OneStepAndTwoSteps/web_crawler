#author py chen
from selenium import webdriver
# 等待事件
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 页面对象定位
from selenium.webdriver.common.by import By
# 行为链：可以完成简单的交互行为，例如鼠标移动，鼠标点击事件，键盘输入，以及内容菜单交互。这对于模拟那些复杂的类似于鼠标悬停和拖拽行为很有用
from selenium.webdriver import ActionChains
# 异常
from selenium.common.exceptions import TimeoutException
import time
import base64
from PIL import Image
import json

with open('pass.json','r') as f:
    user_info =  json.load(f)
    username = user_info['username']
    password = user_info['password']


class BliBli_login():

    def __init__(self):

        self.url = 'https://passport.bilibili.com/login'
        self.username= username
        self.password = password
        self.driver = webdriver.Chrome()            # 实例化一个dirver
        self.wait = WebDriverWait(self.driver,20)   # 超时时间为20s
        self.INIT_LEFT = 60                         # 在查找缺口时 x 的坐标
        self.BORDER = 6                             # 滑块和验证码左侧的空隙为6px
        self.driver.get(self.url)                           # 进入页面


    def input_user_pass(self):

        # 判断是否至少有1个元素存在于dom树中。举个例子，如果页面上有n个元素的class都是'column-md-3'，那么只要有1个元素存在，这个方法就返回True
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))

        username.send_keys(self.username)
        password.send_keys(self.password)


    def get_login_button(self):

        # 判断某个元素中是否可见并且是enable的，这样的话才叫clickable
        login_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'btn-login')))
        print(login_button)
        return login_button

    def get_verification_image(self):   # 获取验证码的图片

        time.sleep(2)

        # 执行JS获取图片,base64格式
        JS = 'return document.getElementsByClassName("geetest_canvas_fullbg")[0].toDataURL("image/png");'  # 不带阴影的完整图片
        image_info = self.driver.execute_script(JS) # 执行JS代码获取图片

        print(image_info)

        # 拿到base64编码的图片信息
        im_base64 = image_info.split(',')[1]
        # 转为bytes类型
        captcha1 = base64.b64decode(im_base64)

        with open('captcha1.png','wb') as f:
            f.write(captcha1)

            JS = 'return document.getElementsByClassName("geetest_canvas_bg")[0].toDataURL("image/png");'  # 不带阴影的完整图片
            image_info = self.driver.execute_script(JS)  # 执行JS代码获取图片

            print(image_info)

            # 拿到base64编码的图片信息
            im_base64 = image_info.split(',')[1]
            # 转为bytes类型
            captcha2 = base64.b64decode(im_base64)

            with open('captcha2.png', 'wb') as f:
                f.write(captcha2)

        captcha1 = Image.open('captcha1.png')
        captcha2 = Image.open('captcha2.png')
        return captcha1, captcha2

    def get_slider(self):

        slider = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.geetest_slider_button')))
        return slider

    def move_slider(self, slider, track):
        """
        滑动滑块至缺口
        :param slider: 滑块对象
        :param track:  移动轨迹
        :return:
        """

        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in track:
            # 只进行水平移动
            ActionChains(self.driver).move_by_offset(xoffset=x,yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

    def get_offset(self,image1,image2):
        """
        获取缺口偏移量
        :param image1:不带缺口的图片
        :param image2: 带缺口的图片
        :return:
        """
        left = self.INIT_LEFT
        for i in range(left,image1.size[0]):                        # 从左到右 x方向
            for j in range(image1.size[1]):                         # 从上到下 y方向
                if not  self.judge_pixel_equel(image1,image2,i,j):
                    left = i                                        # 找到缺口的左侧边界 在x方向上的位置
                    print('缺口位置: ',left)
                    return left
        return left

    def judge_pixel_equel(self,image1,image2,x,y):    # 判断两张图片 各个位置的像素是否相同
        """
        # 获取两张图片指定位置的像素点
        :param image1: 不带缺口的图片
        :param image2: 带缺口的图片
        :return:
        """
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        # 设置一个阈值 允许有误差
        threshold = 60
        # 彩色图 每个位置的像素点有三个通道
        # 0，1，2 分别表示图片的RGB色值，这里的范围为60，如果三者相差都大于60，则认为是不一样的像素点，也就是缺口的位置，返回True
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self,offset):
        """
        根据偏移量 获取移动轨迹，使用加速度来构造

        极验验证码增加了机器轨迹识别，匀速移动、随机速度移动等方法都不能通过验证，只有完全模拟人的移动轨迹才可以通过验证。
        人的移动轨迹一般是先加速后减速，我们需要模拟这个过程才能成功。
        :param offset: 偏移量
        :return: 移动轨迹
        """

        track = []              # 移动轨迹
        current = 0             # 当前位置
        mid = offset / 5 * 4    # 前面4/5的距离加速，后面1/5的距离减速
        t = 0.2                 # 间隔时间
        v = 0                   # 速度

        while current < offset:
            if current < mid:
                a = 3
            else:
                a = -3
            v0 = v                          # 初速度
            v = v0 + t * a                  # 速度
            move = v0 + 1/2 * a * t * t     # 距离
            current += move                 # 当前位置
            track.append(round(move))       # 加入轨迹

        return track

    def check_login(self):
        """
        检查是否登录成功
        :return: 成功返回True，失败返回False
        """
        try:
            self.wait = WebDriverWait(self.driver, 5)  # 超时时间为20s
            if self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="internationalHeader"]/div[1]/div/div[3]/div[2]/div[3]/div/div[1]/a/span'))):
                return True

        except TimeoutException:
            return  False

    def login(self):
        """
        登录验证
        :return:
        """
        self.input_user_pass()  # 输入帐号和密码
        login_button = self.get_login_button()  # 返回登录按钮
        login_button.click()  # 点击登录
        captcha1, captcha2 = self.get_verification_image()  # 获取验证码图片
        offset = self.get_offset(captcha1, captcha2)  # 获取两张图片的偏移量
        offset = offset - self.BORDER                       # 减去滑块左侧所占的宽度
        track = self.get_track(offset)                      # 获取滑动轨迹，模拟人的滑动行为
        slider = self.get_slider()                          # 获取滑动按钮对象
        self.move_slider(slider,track)                      # 进行滑动滑块

        return offset

    def retry(self,offset):
        """
        重新进行滑动验证
        :param offset: 偏移量
        :return:
        """
        offset = offset - self.BORDER                       # 减去滑块左侧所占的宽度
        track = self.get_track(offset)                      # 获取滑动轨迹，模拟人的滑动行为
        slider = self.get_slider()                          # 获取滑动按钮对象
        self.move_slider(slider,track)                      # 进行滑动滑块



if __name__ == '__main__':

    B_login = BliBli_login()
    offset = B_login.login()

    # B_login.retry(offset)

    while True:
        if B_login.check_login():
            print('登录成功')
            break
        else:
            time.sleep(2)
            # 变化 offset 重新尝试
            offset = offset - 1
            B_login.retry(offset)