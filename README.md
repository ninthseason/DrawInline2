## DrawInline2 - 控制鼠标，自动绘画

[查看展示视频](./docs/vrc.mp4)

---

本项目是 [DrawInline](https://github.com/ninthseason/drawinline) 的改进，将鼠标控制器由 PyAutoGUI 换为驱动级的 [pyinterception](https://github.com/kennyhml/pyinterception)，从而能在更多场景中工作。此外，精简了大量代码。

## 使用方法

1. 必须安装 [Interception 驱动](https://github.com/oblitum/Interception)，否则本工具不会起作用。
2. 如果发现线条位置不对或具备随机性，尝试 设置->蓝牙与设备->鼠标->关闭 增强指针精确度 (set Settings->Bluetooth & device->Mouse->Enhance pointer precision to OFF)
   - 这疑似是 pyinterception 或 Interception 的特性，尽管本工具的代码已经最大程度规避了该特性的影响
3. 克隆仓库后安装虚拟环境 `uv install`
4. 用任意截图工具将想绘制的图片存入剪切板
5. 运行 main.py，等待5秒后即会开始控制鼠标绘制 `uv run main.py`

## 原理

1. 使用 Canny 算法提取线稿
2. 对线稿进行 thin 处理以精简线稿
3. 使用深度优先搜索+广度优先搜索由线稿生成鼠标位移绝对坐标数组
4. 将绝对坐标转换为相对坐标
5. 根据相对坐标移动鼠标即可

## 备注
`./third_party/pyinterception` 与原版本的唯一差别在于实现了 [issue#42](https://github.com/kennyhml/pyinterception/issues/42)
