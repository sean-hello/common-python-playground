import sys, random, argparse
import numpy as np
import math
import turtle
import random
from PIL import Image
from datetime import datetime
from fractions import gcd

# a class that draws a Spirograph
class Spiro:
    # constructor
    def __init__(self, xc, yc, col, R, r, l):

        # create the turtle object
        self.t = turtle.Turtle()	#创建新的turtle对象，有助于同时绘制多条螺线
        # set the cursor shape
        self.t.shape('turtle')	#光标设置为海龟，--shapes: “arrow”, “turtle”, “circle”, “square”, “triangle”, “classic”

        # set the step in degrees
        self.step = 5	#绘图角度的增量
        # set the drawing complete flag
        self.drawingComplete = False	#标志，动画中使用它，会产生一组螺线

        # set the parameters
        self.setparams(xc, yc, col, R, r, l)

        # initialize the drawing
        self.restart()

    # set the parameters
    def setparams(self, xc, yc, col, R, r, l):		#初始化Spiro对象
        # the Spirograph parameters
        self.xc = xc	
        self.yc = yc	#保存曲线中心的坐标
        self.R = int(R)	#每个圆的半径（R，r）转换为整数并保存
        self.r = int(r)
        self.l = l
        self.col = col
        # reduce r/R to its smallest form by dividing with the GCD
        gcdVal = gcd(self.r, self.R)	#模块fractions内置的gcd()来计算半径的GCD
        self.nRot = self.r//gcdVal		#
        # get ratio of radii
        self.k = r/float(R)
        # set the color
        self.t.color(*col)
        # store the current angle
        self.a = 0			#保存当前的角度，用来创建动画

    # restart the drawing
    def restart(self):
        # set the flag
        self.drawingComplete = False	#初始化标志，绘制多个spiro时，可以追踪某个特定的螺线是否完成
        # show the turtle
        self.t.showturtle()				#显示海龟光标，以防被隐藏
        # go to the first point
        self.t.up()						#提起笔，这样就可以在移动到第一笔的位置而不画线
        R, k, l = self.R, self.k, self.l 	#局部变量，保持代码紧凑
        a = 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))		#计算角度a设为0的x坐标和y坐标，以获得曲线的起点
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)		# >--<但移动到第一个位置而不画线
        self.t.down()	#落笔，Setpos()调用将绘制实际的线

    # draw the whole thing
    def draw(self):
        # draw the rest of the points
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360*self.nRot + 1, self.step):			#遍历i的完整范围，以度作单位，是360*nRot
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))		#计算参数i的每个值对应的x坐标和y坐标
            y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc + x, self.yc + y)
            # drawing is now done so hide the turtle cursor
            self.t.hideturtle()										#完成绘制，隐藏光标

    # update by one step
    def update(self):						#创建动画
        # skip the rest of the steps if done
        if self.drawingComplete:			#检查drawingCompelete标志是否设置，如果没有就继续执行代码其余的部分
            return
        # increment the angle
        self.a += self.step					#增加当前的角度
        # draw a step
        R, k, l = self.R, self.k, self.l
        # set the angle
        a = math.radians(self.a)			#计算当前角度对应的(x,y)位置并将海龟移动到那里，在这个过程中画出线段
        x = self.R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = self.R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        # if drawing is complete, set the flag
        if self.a >= 360*self.nRot:			#检查角度是否达到这条特定曲线计算的完整范围，如果true就设置drawingComplete=true，因为完成绘画
            self.drawingComplete = True
            # drawing is now done so hide the turtle cursor
            self.t.hideturtle()				#完成绘制，隐藏光标

    # clear everything
    def clear(self):
        self.t.clear()

# a class for animating Spirographs
class SpiroAnimator:
    # constructor
    def __init__(self, N):
        # set the timer value in milliseconds
        self.deltaT = 10						#时间隔间定时器，毫秒为单位，
        # get the window dimensions
        self.width = turtle.window_width()		#保存海龟的窗口尺寸
        self.height = turtle.window_height()
        # create the Spiro objects
        self.spiros = []						#创建一个空的数组，填入一些Spiro对象，这些封装的万花尺绘制，然后循环N次（N传入给构造函数SpiroAnimator）
        for i in range(N):
            # generate random parameters
            rparams = self.genRandomParams()	#辅助方法，生成随机参数
            # set the spiro parameters
            spiro = Spiro(*rparams)				#创建新的spiro对象并添加到数组（rparams是元组，需要传入Spiro构造函数，*运算符号将元组转参数列表）
            self.spiros.append(spiro)
        # call timer
        turtle.ontimer(self.update, self.deltaT)	#每隔deltaT毫秒调用update()

    # restart spiro drawing
    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters
            rparams = self.genRandomParams()
            # set the spiro parameters
            spiro.setparams(*rparams)
            # restart drawing
            spiro.restart()

    # generate random parameters
    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)	#将R设置为50至窗口短边一半长度的随机整数
        r = random.randint(10, 9*R//10)					#将r设置为R的10%~90%之间
        l = random.uniform(0.1, 0.9)					#将l设置为0.1至0.9之间的随机小数
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)		#在屏幕边界内随机选择x和y左边，选择一个随机点作为螺线的中心
        col = (random.random(),							#随机设置红绿蓝颜色的成分，曲线指定的随机颜色
               random.random(),
               random.random())
        return (xc, yc, col, R, r, l)					#所有计算的参数作为元组返回

    def update(self):
        # update all spiros
        nComplete = 0							#初始化后，用来遍历Spiro对象
        for spiro in self.spiros:
            # update
            spiro.update()						#更新
            # count completed spiros
            if spiro.drawingComplete:			#绘画完成
                nComplete += 1
        # restart if all spiros are complete
        if nComplete == len(self.spiros):		#检查计算器，若所有对象都完成，调用restart()重新开始新的螺线动画
            self.restart()
        # call the timer
        turtle.ontimer(self.update, self.deltaT)	#调用计时器方法，用在DeltaT毫秒后再次调用update()

    # toggle turtle cursor on and off
    def toggleTurtles(self):		#显示或隐藏光标
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()

# save drawings as PNG files
def saveDrawing():		#将绘制保存为PNG图像文件
    # hide the turtle cursor
    turtle.hideturtle()			#隐藏光标，这样就不会在最后的图形看到海龟
    # generate unique filenames
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    fileName = 'spiro-' + dateStr
    print('saving drawing to %s.eps/png' % fileName)
    # get the tkinter canvas		tkinter创建用户界面(UI)窗口
    canvas = turtle.getcanvas()			
    # save the drawing as a postscipt image
    canvas.postscript(file = fileName + '.eps')		#利用tkinter创建canvas对象，将窗口嵌入PostScript(EPS)文件格式，是矢量格式，可以用高分辨率打印
    # use the Pillow module to convert the poscript image file to PNG
    img = Image.open(fileName + '.eps')
    img.save(fileName + '.png', 'png')
    # show the turtle cursor
    turtle.showturtle()			#取消隐藏海龟光标

# main() function
def main():
    # use sys.argv if needed
    print('generating spirograph...')
    # create parser
    descStr = """This program draws Spirographs using the Turtle module.
    When run with no arguments, this program draws random Spirographs.

    Terminology:

    R: radius of outer circle
    r: radius of inner circle
    l: ratio of hole distance to r
    """

    parser = argparse.ArgumentParser(description=descStr)			#创建参数解析对象

    # add expected arguments
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help="The three arguments in sparams: R, r, l.")			#向解析器添加--sparams可选参数

    # parse args
    args = parser.parse_args()			#调用函数进行实际的解析

    # set the width of the drawing window to 80 percent of the screen width
    turtle.setup(width=0.8)				#创建绘图窗口的宽度设置为80%的屏幕宽度

    # set the cursor shape to turtle
    turtle.shape('turtle')

    # set the title to Spirographs!
    turtle.title("Spirographs!")		#窗口标题
    # add the key handler to save our drawings
    turtle.onkey(saveDrawing, "s")		#按s键保存图画，需要安装ghostscript
    # start listening
    turtle.listen()						#让窗口监听用户事件

    # hide the main turtle cursor
    turtle.hideturtle()

    # check for any arguments sent to --sparams and draw the Spirograph
    if args.sparams:					#检查是否有参	数
        params = [float(x) for x in args.sparams]	#用‘列表解析’将参数转换浮点数，(列表解析式python结构，以紧凑而强大的方式创建列表)
        # draw the Spirograph with the given parameters
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)			#利用任何提取的参数来构造Spiro对象
        spiro.draw()								#开始表演
    else:
        # create the animator object
        spiroAnim = SpiroAnimator(3)				#没有参数就随机创建图画，参数为图画的幅数
        # add a key handler to toggle the turtle cursor
        turtle.onkey(spiroAnim.toggleTurtles, "t")	#按T切换海龟图标
        # add a key handler to restart the animation
        turtle.onkey(spiroAnim.restart, "space")	#按空格键重新启动动画

    # start the turtle main loop
    turtle.mainloop()								#告诉tkinter窗口保持打开，监听事件

# call main
if __name__ == '__main__':
    main()

# 带参例子 $ pyhton spiro.py --sparams 300 100 0.5