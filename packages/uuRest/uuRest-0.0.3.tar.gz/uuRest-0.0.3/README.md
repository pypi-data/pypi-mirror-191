# uuTS
Library that allows developers to easily integrate their application(s) with Unicorn Systems solutions and products using REST API.
## Examples of How To Use (uuREST)
Simple Request
```python
text
```

Iterating through the list of items
```python
from vidstream import CameraClient
from vidstream import VideoClient
from vidstream import ScreenShareClient

# Choose One
client1 = CameraClient('127.0.0.1', 9999)
client2 = VideoClient('127.0.0.1', 9999, 'video.mp4')
client3 = ScreenShareClient('127.0.0.1', 9999)

client1.start_stream()
client2.start_stream()
client3.start_stream()
```

Check out: https://www.youtube.com/