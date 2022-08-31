# from PySide2.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.Qt import *
import sys
import random
import pygame
pygame.mixer.init()

class Window(QWidget):  # 此处需注意ui使用的是QMainWindow还是QWidget，本例是QWidget.
    def __init__(self):
        super().__init__()
        self.tank_index = 1
        self.create_timer = QTimer(self)
        self.create_timer.timeout.connect(self.CreateTank)
        self.setup_func()


    def setup_func(self):
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)  # 窗口置顶，无边框，在任务栏不显示图标
        self.desktop = QApplication.desktop()
        self.boundary_x = self.desktop.width()
        self.boundary_y = self.desktop.height()
        self.resize(self.boundary_x, self.boundary_y)
        self.create_timer.start(5000)
        self.CreateTank()


    def CreateTank(self):
        group = random.choice('gr')
        self.tank_dict = {}
        self.tank_dict['tank%d'%self.tank_index] = Tank(self, self.tank_index, self.boundary_x, self.boundary_y, group)
        self.tank_index += 1
        # self.block1 = block1


class Tank(QLabel):
    def __init__(self, Window, tank_index, boundary_x, boundary_y, group):
        super().__init__(Window)
        self.window = Window
        self.tank_index = tank_index
        self.bullet_power = 100
        self.group = group
        self.xrange = 1200
        self.yrange = 800
        self.boundary_x = boundary_x
        self.boundary_y = boundary_y
        self.tanksize = 90
        self.directxy = random.choice(['x+', 'x-', 'y+', 'y-'])
        self.health = 100
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.TankMove)
        self.fire_timer = QTimer(self)
        self.fire_timer.timeout.connect(self.TankFire)
        self.SetupTank()


    def SetupTank(self):
        self.move(random.randint(100, self.xrange - 100), random.randint(100, self.yrange - 100))
        # color_num = str(hex(random.randint(0, 15)))[2:] + str(hex(random.randint(0, 15)))[2:] + str(hex(random.randint(0, 15)))[2:] + str(hex(random.randint(0, 15)))[2:] + str(hex(random.randint(0, 15)))[2:] + str(hex(random.randint(0, 15)))[2:]
        # self.setStyleSheet('background-color: #%s' % color_num)
        self.resize(self.tanksize, self.tanksize)
        # self.setText(str(self.tank_index))
        self.setScaledContents(True) # 设置label内容可自动调节
        if self.group == 'g':
            self.pic = QPixmap(r".\PIC\tank_g.JPG").scaled(self.width(), self.height())
        else:
            self.pic = QPixmap(r".\PIC\tank_r.JPG").scaled(self.width(), self.height())
        self.setPixmap(self.pic)
        self.TankOrientation()
        self.move_timer.start(10)
        self.fire_timer.start(2000)


    def TankMove(self):
        # 判断坦克是否移出了屏幕
        if self.x() < 0:
            self.directxy = 'x+'
        elif self.x() > (self.boundary_x - self.tanksize):
            self.directxy = 'x-'
        if self.y() < 0:
            self.directxy = 'y+'
        elif self.y() > (self.boundary_y - self.tanksize):
            self.directxy = 'y-'
        movexy = random.randint(1, 10000)
        if movexy > 9960 and movexy <= 9970:
            self.move(self.x() + 1, self.y())
            self.directxy = 'x+'
        elif movexy > 9970 and movexy <= 9980:
            self.move(self.x() - 1, self.y())
            self.directxy = 'x-'
        elif movexy > 9980 and movexy <= 9990:
            self.move(self.x(), self.y() + 1)
            self.directxy = 'y+'
        elif movexy > 9990 and movexy <= 10000:
            self.move(self.x(), self.y() - 1)
            self.directxy = 'y-'
        else:
            # 判断前方是否有障碍物
            # print('开始判断')
            is_block = self.IsBlock(self.directxy, self.x(), self.y(), self.width(), self.height())
            if is_block == 1:
                pass
            else:
                if self.directxy == 'x+':
                    self.move(self.x() + 1, self.y())
                elif self.directxy == 'x-':
                    self.move(self.x() - 1, self.y())
                elif self.directxy == 'y+':
                    self.move(self.x(), self.y() + 1)
                elif self.directxy == 'y-':
                    self.move(self.x(), self.y() - 1)

        self.TankOrientation()
        # 判断坦克是否被击毁
        if self.health <= 0:
            # self.deleteLater()
            self.TankExplore(self.x(), self.y(), 90)
        self.show()

    def TankExplore(self, x_axis, y_axis, explore_size):
        self.resize(explore_size, explore_size)
        self.pic = QPixmap(r".\PIC\explode.jpg").scaled(self.width(), self.height())
        self.setPixmap(self.pic)
        self.show()
        self.explore_timer = QTimer(self)
        self.explore_timer.timeout.connect(self.ExploreDelete)
        self.explore_timer.start(100)

    def ExploreDelete(self):
        sound = pygame.mixer.Sound(r'.\sound\explore.mp3')
        sound.play()
        self.deleteLater()


    def IsBlock(self, directxy, obj_x, obj_y, obj_width, obj_height):
        if directxy == 'x+':
            point1_x = obj_x + obj_width + 1
            point1_y = obj_y + 1
            point2_x = obj_x + obj_width + 1
            point2_y = obj_y + obj_height -1
        elif directxy == 'x-':
            point1_x = obj_x - 1
            point1_y = obj_y + 1
            point2_x = obj_x - 1
            point2_y = obj_y + obj_height - 1
        elif directxy == 'y+':
            point1_x = obj_x + 1
            point1_y = obj_y + obj_height + 1
            point2_x = obj_x + obj_width - 1
            point2_y = obj_y + obj_height + 1
        else:
            point1_x = obj_x + 1
            point1_y = obj_y - 1
            point2_x = obj_x + obj_width - 1
            point2_y = obj_y - 1
        # 获取这两个坐标前面有什么东西
        # print(point1_x, point1_y)
        block_obj1 = self.window.childAt(point1_x, point1_y)
        block_obj2 = self.window.childAt(point2_x, point2_y)
        # print(str(block_obj1), str(block_obj2))
        if block_obj1 is None and block_obj2 is None:
            return 0
        else:
            return 1


    def TankOrientation(self):
        if self.group == 'g':
            tank_pic = 'tank_g.jpg'
        else:
            tank_pic = 'tank_r.jpg'
        transform = QTransform()  ##需要用到pyqt5中QTransform函数
        if self.directxy == 'x+':
            pic_degree = 270
        elif self.directxy == 'x-':
            pic_degree = 90
        elif self.directxy == 'y-':
            pic_degree = 180
        else:
            pic_degree = 0

        transform.rotate(pic_degree)  ##设置旋转角度
        self.pic = QPixmap(r".\PIC\%s" % tank_pic).scaled(self.width(), self.height()).transformed(transform)  #对image进行旋转
        self.setPixmap(self.pic)


    def TankFire(self):
        bspeed = 5
        if self.directxy == 'x+':
            bdirect = 'x+'
            bx = self.x() + self.width() + 3
            by = self.y() + self.height()/2
        elif self.directxy == 'x-':
            bdirect = 'x-'
            bx = self.x() - 3
            by = self.y() + self.height() / 2
        elif self.directxy == 'y-':
            bdirect = 'y-'
            bx = self.x() + self.width() / 2
            by = self.y() - 3
        else:
            bdirect = 'y+'
            bx = self.x() + self.width() / 2
            by = self.y() + self.height() + 3
        # self.bullet_list = []
        # self.bullet_list.append(Bullet(self.window, self.group, bx, by, bdirect, bspeed, self.boundary_x, self.boundary_y))
        # print(self.bullet_list)
        sound = pygame.mixer.Sound(r'.\sound\fire.mp3')
        sound.play()
        Bullet(self.window, self.group, bx, by, bdirect, bspeed, self.boundary_x, self.boundary_y, self.bullet_power)


class Bullet(QLabel):
    def __init__(self, Window, group, bx, by, bdirect, bspeed, boundary_x, boundary_y, bullet_power):
        super().__init__(Window)
        self.window = Window
        self.group = group
        self.bx = bx
        self.by = by
        self.health = bullet_power
        self.bdirect = bdirect
        self.bspeed = bspeed
        self.boundary_x = boundary_x
        self.boundary_y = boundary_y
        self.move(int(bx), int(by)) # 子弹初始位置
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.BulletMove)
        self.SetupBullet()

    def SetupBullet(self):
        if self.group == "g":
            bullet_pic = 'bullet_g.jpg'
        else:
            bullet_pic = 'bullet_r.jpg'
        # 根据子弹方向加载子弹图片
        self.setScaledContents(True)  # 设置label内容可自动调节
        transform = QTransform()  #需要用到pyqt5中QTransform函数
        if self.bdirect == 'x+':
            pic_degree = 270
            self.resize(20, 10)
        elif self.bdirect == 'x-':
            pic_degree = 90
            self.resize(20, 10)
        elif self.bdirect == 'y-':
            pic_degree = 180
            self.resize(10, 20)
        else:
            pic_degree = 0
            self.resize(10, 20)
        transform.rotate(pic_degree)  ##设置旋转角度
        self.pic = QPixmap(r".\PIC\%s" % bullet_pic).scaled(self.width(), self.height()).transformed(transform)  # 对image进行旋转
        self.setPixmap(self.pic)
        self.move_timer.start(10)


    def BulletMove(self):
        # 判断子弹是否会发生撞击
        is_block, block_obj1, block_obj2 = self.IsBlock(self.bdirect, self.x(), self.y(), self.width(), self.height())
        if is_block == 1:
            try:
                if block_obj1 is not None:
                    if block_obj1.group != self.group:
                        block_obj1.health = block_obj1.health - self.health
                if block_obj2 is not None:
                    if block_obj2.group != self.group:
                        block_obj2.health = block_obj2.health - self.health
                self.health = 0
            except Exception as e:
                print(e)
        else:
            if self.bdirect == 'x+':
                self.move(self.x() + self.bspeed, self.y())
            elif self.bdirect == 'x-':
                self.move(self.x() - self.bspeed, self.y())
            elif self.bdirect == 'y+':
                self.move(self.x(), self.y() + self.bspeed)
            elif self.bdirect == 'y-':
                self.move(self.x(), self.y() - self.bspeed)
        # print(self.x(), self.y())
        # 判断子弹是否移出了屏幕
        if self.x() < 0:
            self.deleteLater()
        elif self.x() > self.boundary_x:
            self.deleteLater()
        if self.y() < 0:
            self.deleteLater()
        elif self.y() > self.boundary_y:
            self.deleteLater()
        # 判断子弹是否爆炸
        if self.health <= 0:
            # self.deleteLater()
            self.BulletExplore(self.x(), self.y(), 20)
        self.show()
        # print('执行了show')


    def BulletExplore(self, x_axis, y_axis, explore_size):
        self.resize(explore_size, explore_size)
        self.pic = QPixmap(r".\PIC\explode.jpg").scaled(self.width(), self.height())
        self.setPixmap(self.pic)
        self.show()
        self.explore_timer = QTimer(self)
        self.explore_timer.timeout.connect(self.ExploreDelete)
        self.explore_timer.start(100)


    def ExploreDelete(self):
        self.deleteLater()


    def IsBlock(self, directxy, obj_x, obj_y, obj_width, obj_height):
        if directxy == 'x+':
            point1_x = obj_x + obj_width + 1
            point1_y = obj_y + 1
            point2_x = obj_x + obj_width + 1
            point2_y = obj_y + obj_height -1
        elif directxy == 'x-':
            point1_x = obj_x - 1
            point1_y = obj_y + 1
            point2_x = obj_x - 1
            point2_y = obj_y + obj_height - 1
        elif directxy == 'y+':
            point1_x = obj_x + 1
            point1_y = obj_y + obj_height + 1
            point2_x = obj_x + obj_width - 1
            point2_y = obj_y + obj_height + 1
        else:
            point1_x = obj_x + 1
            point1_y = obj_y - 1
            point2_x = obj_x + obj_width - 1
            point2_y = obj_y - 1
        # 获取这两个坐标前面有什么东西
        # print(point1_x, point1_y)
        block_obj1 = self.window.childAt(point1_x, point1_y)
        block_obj2 = self.window.childAt(point2_x, point2_y)
        # print(str(block_obj1), str(block_obj2))
        if block_obj1 is None and block_obj2 is None:
            return 0, None, None
        else:
            return 1, block_obj1, block_obj2


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainw = Window()
    mainw.show()
    sys.exit(app.exec_())