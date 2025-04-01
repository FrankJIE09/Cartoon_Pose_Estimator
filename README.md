# 相机结合 MediaPipe 姿态估计和卡通化

这个 Python 项目使用奥比中光 3D 相机捕获视频，并使用 MediaPipe 处理视频以检测人体姿态，然后应用卡通效果。

## 主要功能

* **奥比中光相机集成:** 使用 `pyorbbecsdk` 库与奥比中光深度相机进行交互。
* **姿态估计:** 使用 MediaPipe Pose 实时检测和跟踪人体姿态。
* **卡通效果:** 使用 OpenCV 将卡通滤镜应用于视频流。
* **模块化设计:** 相机接口封装在 `OrbbecCamera` 类中，便于重用。

## 环境要求

* Python 3.x
* `pyorbbecsdk`
* `opencv-python`
* `mediapipe`
* `numpy`
* `pyyaml`

您可以使用 pip 安装 Python 依赖：

```bash
pip install pyorbbecsdk opencv-python mediapipe numpy pyyaml
```

## 硬件要求

* 奥比中光 3D 相机

## 安装步骤

1.  克隆代码仓库：

2.  安装所需的 Python 包（见“环境要求”）。

## 使用方法

1.  确保您的奥比中光相机已连接到计算机。
2.  运行 `main.py` 脚本：

    ```bash
    python main.py
    ```

3.  脚本将显示一个窗口，其中显示处理后的视频流，包含姿态关键点和卡通效果。
4.  按 `q` 键退出应用程序。

## 代码说明

* `main.py`:
    * 应用程序的主要入口点。
    * 使用 `OrbbecCamera` 类初始化奥比中光相机。
    * 捕获视频帧。
    * 处理每一帧，使用 MediaPipe 检测姿态。
    * 使用 OpenCV 应用卡通效果。
    * 显示处理后的视频。
* `orbbec_camera.py`:
    * 包含 `OrbbecCamera` 类，该类处理与奥比中光相机的通信。
    * 提供以下方法：
        * 启动和停止相机流。
        * 检索彩色和深度帧。
        * 访问相机参数。
        * 调整相机设置（例如，曝光）。
* `utils.py` (如果存在):
    * 包含实用函数，例如帧转换 (例如，`frame_to_bgr_image`)。
* `hand_eye_config.yaml` (可选):
    * 一个 YAML 文件（如果使用），用于存储外部标定参数（例如，用于手眼标定）。

## 优化技巧

由于姿态估计和卡通化的计算强度，项目可能会遇到性能瓶颈。以下是一些优化技巧：

* **降低处理负载:**
    * 使用更简单的 MediaPipe 姿态模型 (`model_complexity`)。
    * 降低输入帧分辨率。
    * 优化卡通化参数 (例如, `ksize`)。
* **硬件加速:**
    * 如果可用，请确保 OpenCV 和 MediaPipe 使用 GPU 加速。
* **代码优化:**
    * 减少不必要的数据复制。

## 故障排除

* **相机未检测到:**
    * 确保奥比中光相机已正确连接。
    * 确保已正确安装 `pyorbbecsdk` 库。
    * 检查是否有其他应用程序正在使用相机。
* **性能问题:**
    * 请参阅“优化技巧”部分。
* **错误:**
    * 检查控制台输出中的错误消息。


## 许可证

MIT 