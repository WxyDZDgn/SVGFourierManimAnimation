通过读取 SVG 的路径拟合傅里叶级数利用 Manim 生成绘制该路径的动画

生成步骤：
1. 将**含有** SVG 路径的文件放入 `res` 文件夹；
2. 打开根目录下 `animation.py` 文件，修改创建 `SVG` 对象的参数为对应的文件；
3. 在根目录下使用 `manimgl .\animation.py RotatingVectors -owl` 生成动画并完成后自动打开。

前提得有环境，请参考[此处](https://docs.manim.org.cn/getting_started/installation.html#python-manimgl)安装步骤，具体运行细节请自行调整。

注：若 `SVG` 文件中没有路径和`d`属性，不可转换。

___

文件细节：

1. `Curve.py`：`SVG` 路径的三种大类曲线（直线、二阶贝塞尔曲线、三阶贝塞尔曲线，但并没有对圆锥曲线适配，关于三种大类的指令请参考[此处](https://developer.mozilla.org/zh-CN/docs/Web/SVG/Attribute/d)）；
2. `SVG.py`：`SVG` 类，即多个 `Curve` 实例的组合，并提供解析 `SVG` 文件中的**路径**指令；
3. `Fourier.py`：傅里叶级数类，通过传入若干个复数参数 $c_{-L}, \cdots, c_{L}$ 得到对应函数 $f(t) = c_0 + \sum_{k=1}^{L}\left(c_{k}e^{2\pi ikt} + c_{-k}e^{-2\pi ikt}\right)$；
4. `svg_test.py`：其中一个拟合傅里叶级数的样例，并输出复数列表以便在平面直角坐标系上描点作图并查看效果；
5. `animation.py`：用于 `Manim` 的动画生成，想了解文件细节请转至[此处](https://docs.manim.org.cn/)。
