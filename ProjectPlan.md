<!--
* @Author: Alicespace
* @Date: 2019-11-18 08:28:36
 * @LastEditTime: 2019-12-12 10:52:54
-->

# 星体运动模拟器开发笔记

## 1.开发目标

使用```Panda3D```引擎，构建三维行星运动的模型，并提供可视化的形象。

## 2.人员分工

- 李志昊：draw3DWorld，controller，RenderPipeline
- 邢景琪、龙俊：calculate、drawGUI
- 刘承恩：测试，演示样例，3D模型、res、DBmanager

## 3.开发需求

- 实现可视化的3D界面，实现“WASD”和“鼠标”控制的“前后左右”和“视角变化”。
- 实现内部GUI控制球体的数量，贴图，贴图颜色，运动初始坐标，运动初始速度矢量，球体数量小于$100$。
- 在计算中实现球体的碰撞判定
- 实现时间比例尺，做到```1:10^n(5<n<10)```
- 实现使用```Panda3D```低于```1.10.0```的版本创建网页版，使用```1.10.4```构建跨PC平台的可分发的免安装应用程序

## 4.测试需求

- 创建三体模型演示
- 创建太阳系行星模型
- 创建引力弹弓效应的演示

## 5.架构设计
  
分7大模块

1. 计算模块(**calculate**)：负责轨迹的计算，碰撞判定  

	#### 要求
	- 计算快而准确，时间不大于现成已有最优算法的３倍，保证在３体任意初始条件的运动至少有60fps

	- 碰撞准确，星体不得穿模，碰撞要符合物理规律（注意洛希极限，密度）
		- "固－固":
			- 碰撞
			- 撞碎
		- "固－气"
			- 摩擦
		- "气－气"
			- 融合
			- 摩擦  
	- 可以改变运动矢量参数  
	#### 输入
	```
	calculate.start(startT,endT,Tsclar,whichStep)
	```
	#### 输出
	```
	bool True
	bool False
	```
2. 控制器模块(**controller**)：负责处理键盘鼠标输入  

	#### 要求：
	- 实现"WASD"和"鼠标”控制的“前后左右"和"视角变化"
	- 实现"ESC"召唤菜单，等快捷键功能
	- 响应菜单快捷键
	- 控制背景音乐的启停，音量
	- 注册鼠标单击3D实体的响应

3. 3D绘图模块(**draw3DWorld**):绘制3D世界  

	#### 要求：
	- 正确渲染3D世界，宇宙背景贴图
	- 标示轨迹和星体

4. 用户界面绘制模块(**drawGUI**):绘制2D的悬浮GUI  

	#### 要求：
	- 设置
		- 音量控制
		- 比例尺
	- 侧边栏新对象创建，托拽矢量给出初始速度
	- 更改对象属性

5. 渲染着色器管线(**RenderPipeline**):渲染管线，使画面精美  

	#### 要求:
	- 目前尚未考虑
6. 资源文件(**res**):  

	#### 要求：
	- 包括3D模型，egg文件，背景音乐，贴图
7. 数据库管理类(DBmanager):将SQL对象化
	#### 要求:
	- 维护一个数据库:
	```
	class stars:
		list get_all_stars()
		star get_Star_by_id(int id)
		bool addStar(class star)
		bool deleteStar(int id)
		bool configStar(class star)
	class star:
		int star.id
		str star.name
		float star.mass
		float star.radius
		str star.texture
		str star.model
		list star.position
		list star.velocity
		#list star.route_0
		#list star.route_1
	```
