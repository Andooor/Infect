import pygame

# 导入所需的模块
import sys
import pygame

SCREEN_WEIGTHT = 1500
SCREEN_HEIGHT = 770
BG_COLOR = pygame.Color(0, 0, 0)
TEXT_COLOR = pygame.Color(255, 255, 255)


class MainGame:
    window = None
    gameName = "Infect"
    version = "V1.1"
    my_Ball = None

    def __init__(self):
        pass

    def startGame(self):

        self.initGame()

        while True:
            MainGame.window.fill(BG_COLOR)
            MainGame.window.blit(self.getTextSurface(), (SCREEN_WEIGTHT / 2 - 50, 10))
            MainGame.my_Ball.move()
            MainGame.my_Ball.displayBall()

            # 循环获取事件，监听事件状态
            for event in pygame.event.get():
                # 判断用户是否点了"X"关闭按钮,并执行if代码段
                if event.type == pygame.QUIT:
                    self.endGame()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mousePosition = event.pos
                    mouse_x = float(mousePosition[0])
                    mouse_y = float(mousePosition[1])

                    # Ball的位置范围
                    ballPositionRange = MainGame.my_Ball.ballPositionRange()
                    # 判断鼠标位置是否在Ball内
                    if (mouse_x >= ballPositionRange[0] and mouse_x <= ballPositionRange[2]) and (
                            mouse_y >= ballPositionRange[1] and mouse_y <= ballPositionRange[3]):
                        if MainGame.my_Ball.state == 'unselected':
                            MainGame.my_Ball.state = 'selected'
                        elif MainGame.my_Ball.state == 'selected':
                            MainGame.my_Ball.state = 'unselected'
                elif event.type == pygame.MOUSEMOTION:
                    mousePosition = event.pos
                    mouse_x = float(mousePosition[0])
                    mouse_y = float(mousePosition[1])

                    ballPositionRange = MainGame.my_Ball.ballPositionRange()

                    if mouse_x != ballPositionRange[4] or mouse_y != ballPositionRange[5]:
                        MainGame.my_Ball.moving = True

                        MainGame.my_Ball.xSpeedRatio = (mouse_x - ballPositionRange[4])*(
                            mouse_x - ballPositionRange[4]) / ((mouse_x - ballPositionRange[4])*(
                            mouse_x - ballPositionRange[4]) + (mouse_y - ballPositionRange[5])*(
                            mouse_y - ballPositionRange[5]))

                        MainGame.my_Ball.ySpeedRatio = (mouse_y - ballPositionRange[5])*(
                            mouse_y - ballPositionRange[5]) / ((mouse_x - ballPositionRange[4])*(
                            mouse_x - ballPositionRange[4]) + (mouse_y - ballPositionRange[5])*(
                            mouse_y - ballPositionRange[5]))

                        if mouse_x > ballPositionRange[4]:
                            MainGame.my_Ball.moveDirection_Left = False
                        elif mouse_x < ballPositionRange[4]:
                            MainGame.my_Ball.moveDirection_Left = True
                        if mouse_y > ballPositionRange[5]:
                            MainGame.my_Ball.moveDirection_Up = False
                        elif mouse_y < ballPositionRange[5]:
                            MainGame.my_Ball.moveDirection_Up = True

                    elif (mouse_x >= ballPositionRange[0] and mouse_x <= ballPositionRange[2]) and (
                            mouse_y >= ballPositionRange[1] and mouse_y <= ballPositionRange[3]):
                        MainGame.my_Ball.moving = False

            pygame.display.flip()  # 更新屏幕内容

    def initGame(self):
        # 使用pygame之前必须初始化
        pygame.init()
        # 设置主屏窗口
        MainGame.window = pygame.display.set_mode([SCREEN_WEIGTHT, SCREEN_HEIGHT])
        # 初始化Ball
        MainGame.my_Ball = Ball(SCREEN_WEIGTHT / 2, SCREEN_HEIGHT / 2)
        # 设置窗口的标题，即游戏名称
        pygame.display.set_caption(MainGame.gameName + "   " + MainGame.version)

    def getTextSurface(self):

        # 引入字体类型
        font = pygame.font.SysFont("kaiti", 18)
        # 生成文本信息，第一个参数文本内容；第二个参数，字体是否平滑；
        # 第三个参数，RGB模式的字体颜色；第四个参数，RGB模式字体背景颜色；
        textSurface = font.render("时间", True, TEXT_COLOR)
        # # 获得显示对象的rect区域坐标
        # textRect = textSurface.get_rect()
        # # 设置显示对象居中
        # textRect.center = (200, 200)
        return textSurface

    def endGame(self):
        # 卸载所有模块
        pygame.quit()
        # 终止程序，确保退出程序
        sys.exit()


class Ball:
    # 位置初始化
    def __init__(self, left, top):
        self.images = {
            'selected': pygame.image.load('images/greenBall.png'),
            'unselected': pygame.image.load('images/greyBall.png')
        }
        # 选中状态
        self.state = "unselected"
        # 根据选中状态加载图片
        self.image = self.images[self.state]
        # 根据图片获取区域
        self.rect = self.image.get_rect()
        # 获取图片的尺寸
        self.size = self.image.get_size()
        # 初始化位置
        self.left = left
        self.top = top
        self.rect.left = left
        self.rect.top = top
        # 移动状态
        self.moving = False
        self.moveDirection_Up = False
        self.moveDirection_Left = False
        self.speed = 1
        self.xSpeedRatio = float(0)
        self.ySpeedRatio = float(0)

    def move(self):

        if self.moving:
            if self.moveDirection_Up:
                if self.rect.top >= 0:
                    self.rect.top -= self.speed * self.ySpeedRatio
            else:
                if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                    self.rect.top += self.speed * self.ySpeedRatio
            if self.moveDirection_Left:
                if self.rect.left >= 0:
                    self.rect.left -= self.speed * self.xSpeedRatio
            else:
                if self.rect.left + self.rect.height < SCREEN_WEIGTHT:
                    self.rect.left += self.speed * self.xSpeedRatio

    def displayBall(self):
        # 获取展示的对象
        self.image = self.images[self.state]
        self.size = self.image.get_size()
        # 调用blit方法展示
        MainGame.window.blit(self.image, self.rect)

    def ballPositionRange(self):
        #  [最左方，最上方，最右方，最下方，中心点x，中心点y]
        PositionRange = [
            self.rect.left,
            self.rect.top,
            self.rect.left + self.size[0],
            self.rect.top + self.size[1],
            self.rect.left + self.size[0] / 2,
            self.rect.top + self.size[1] / 2
        ]
        return PositionRange


if __name__ == '__main__':
    MainGame().startGame()
