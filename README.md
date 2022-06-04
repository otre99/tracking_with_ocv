# Object tracking with python

This program tracks multiple objects in a video

![Demo](development_assets/demo.gif)

## Dependences
It only depends on OpenCV 4.5. You can use pip3 to install the dependencies:

```
pip3 install -r ./requirements.txt
```

## Run the program

Run this to see the input options:
```
python3 main.py --help

usage: This program tracks multiple objects in a video [-h] [--video VIDEO] [--json JSON] [--method {CSRT,KCF,DaSiamRPN}] [--output OUTPUT] [--display]

options:
  -h, --help            show this help message and exit
  --video VIDEO         Input video
  --json JSON           JSON file containing initial bboxes
  --method {CSRT,KCF,DaSiamRPN}
                        Tracking method
  --output OUTPUT       Output video
  --display             Show results in the screen

```

The program expects a video (`--video` ) and a JSON file (`--json`) containing the starting position coordinates ( `[x,y,w,h]` rectangle) of each object you want to track (see this [example](development_assets/initial_conditions.json)).

### Examples:
- Run with default parameters. It will use the video and JSON file inside folder [development_assets](development_assets/):
    ```
    python3 main.py
    ```
- Show results on the screen:
    ```
    python3 main.py --display 
    ```
- Use ``DaSiamRPN`` method (based on Deep Learning):
    ```
    python3 main.py --display --method=DaSiamRPN
    ```
- Use custom data:
    ```
    python3 main.py --display --method=DaSiamRPN --video=sample1.mp4  --json=sample1.json --output=results.avi 
    ```

### Using docker 
Create docker image:
 ```
 docker build -f Dockerfile -t obj_tracking:v01 .
 ``` 

Run this command to execute the program inside the container. Replace ``python3 main.py --help`` with your own command.
 ```
docker run -it --rm --net=host -e DISPLAY=$DISPLAY -w /app -v /tmp/.X11-unix/:/tmp/.X11-unix -v $HOME:/data obj_tracking:v01 python3 main.py --help
 ```

If you want to use the ``--display`` option make sure to run this command on the terminal:
```
xhost +
``` 