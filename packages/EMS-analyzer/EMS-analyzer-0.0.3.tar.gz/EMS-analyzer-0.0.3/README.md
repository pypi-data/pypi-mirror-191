
# EMS-analyzer
EMS(electronic monitoring system)-analyzer is collecting the image data and detecting the object
using Yolo. And stitching the images which is already detected image of consist to quadrant image.
And it train the this images


## Installing

Install from PyPI

    pip install EMS-analyzer

## Usage

1. Setting and run Server ans Client

```python
from EMS-analyzer import Server
Server.init(ip_addr='server_ip'
            ,h0=['ha','hb','hc','hd']
            ,s0=['sa','sb','sc','sd'])
class_name, model=init_yolo()
Server.main(class_name, model)

from EMS-analyzer import Client
Client.main(ip_addr='sever_ip', input_image='image or video')

```

## TODO
