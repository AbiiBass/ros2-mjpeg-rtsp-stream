# Camera Topic Streamed in MJPEG and RTSP
This project streams ROS 2 camera topics as MJPEG over HTTP and forwards them as RTSP using FFmpeg. (Built for Ubuntu 22.04 and ROS 2 Humble)
This project and instructions are based on **Ubuntu 22.04** and **Python 3.10**.  
**Note:** Any **lower** versions **may** cause errors.

---

## Camera Topic to MJPEG Streamer

### Prerequisites

Install ROS 2 Humble:  
https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html

Install required packages:

```bash
sudo apt install python3-pip
```
```bash
pip3 install opencv-python
```
```bash
pip3 install mjpeg-streamer
```
```bash
sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade
```

### Troubleshooting Tips

To check if a topic has active publishers:

```bash
ros2 topic info <topic_name>
```

To inspect the topic and see the image encoding:

```bash
ros2 topic echo <topic_name> --once
```

Look at the `encoding` field. Common types include:

- `bgr8` - OpenCV-compatible BGR image
- `rgb8` - Standard RGB format
- `mono8` - Grayscale image
- `yuv422` - YUV format
- `compressed` - Compressed image (requires `image_transport`)

Make sure your streamer or subscriber script can handle the encoding format used.

---

## Streaming to RTSP

### Prerequisites

Install `ffmpeg`:

```bash
sudo apt update
```
```bash
sudo apt install ffmpeg
```

Download and extract appropriate package **MediaMTX**:  
(Visit https://github.com/bluenviron/mediamtx/releases if you need a different build)

```bash
wget https://github.com/bluenviron/mediamtx/releases/download/v1.12.3/mediamtx_v1.12.3_linux_arm64.tar.gz
tar -xzf mediamtx_v1.12.3_linux_arm64.tar.gz
cd mediamtx
./mediamtx
```

This will start the RTSP server locally on port `8554`.

### Forward MJPEG Stream to RTSP

In a separate terminal, run:

```bash
ffmpeg -i http://<robot-ip>:<port-nuber>/my_camera -c:v copy -f rtsp rtsp://localhost:8554/mystream
```

Replace the placeholders:
- `<robot-ip>` - IP address of the robot running the MJPEG stream
- `my_camera` - MJPEG stream path (adjust if different)
- `mystream` - Desired RTSP stream name

---

## Viewing the Streams

- MJPEG (browser-compatible):  
  `http://<robot-ip>:8080/my_camera`

- RTSP (VLC or any RTSP-compatible client):  
  `rtsp://localhost:8554/mystream`

You can view the RTSP video stream using either `ffplay` or VLC:

### Option 1: Using ffplay

```bash
ffplay rtsp://<ip>:<port>/mystream
```
### Option 2: USing VLC Media Player
1. Download and install [VLC Media Player](https://www.videolan.org/vlc/).
2. Open VLC.
3. Go to **Media > Open Network Stream**.
4. Enter the following RTSP URL: rtsp://<ip>:<port>/mystream
5. Click Play



---

## Description

Streams ROS 2 camera topics as MJPEG over HTTP and forwards them as RTSP using FFmpeg and MediaMTX. Built for Ubuntu 22.04 and ROS 2 Humble.

