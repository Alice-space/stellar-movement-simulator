<!--
 * @Author: Alicespace
 * @Date: 2019-12-24 12:18:22
 * @LastEditTime : 2019-12-24 13:19:51
 -->

# 星体运动模拟器文档


本页面是程序的在线文档，本项目遵循``` GNU GENERAL PUBLIC LICENSE Version 3```执照，开源地址[Github](https://github.com/Alice-space/stellar-movement-simulator)。  

.. tip::
        发布版本于[Github](https://github.com/Alice-space/stellar-movement-simulator/releases),同时提供`Alice_space博客`下载来提高速度。
        #### 镜像下载地址：
        Alice_space博客
.. note::
        广告时间！[Alice_space博客](https://alicespace.cn/)（虽然好久没更新）

本项目使用[Panda3D](https://www.panda3d.org/)引擎开发。

## 模块概览

1. 计算部分：  
    `stellarMovementSimulator.Mem`：实现队列数据结构，用于存取计算数据。
    `stellarMovementSimulator.calculateloop`：实现计算过程，碰撞判定。
2. 绘图过程：  
    `stellarMovementSimulator.world`：实现3D世界的绘制，更新。  
    `stellarMovementSimulator.starGui`：实现2D的用户界面绘制。
3. 发布  
    `stellarMovementSimulator.setup`：用于打包成二进制，分发

.. note::
        发现BUG请及时在[github Issues](https://github.com/Alice-space/stellar-movement-simulator/issues)上报告，感谢您的反馈。
