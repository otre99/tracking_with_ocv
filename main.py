import cv2
import json
from ObjectTracker import MultiTracker, ObjectTracked
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)

def build_parser():
    parser = argparse.ArgumentParser(prog="This program tracks multiple objects in a video")
    parser.add_argument("--video", help="Input video", default="development_assets/input.mkv")
    parser.add_argument("--json", help="JSON file containing initial bboxes", default="development_assets/initial_conditions.json")
    parser.add_argument("--method", help="Tracking method", default="KCF", choices=MultiTracker.supported_algoritms)
    parser.add_argument("--output", help="Output video", default="output.avi")
    parser.add_argument("--display", help="Show results in the screen",  default=False, action="store_true")
    return parser

def load_initial_detections(json_file):
    data = json.load(open(json_file))
    result = []
    for d in data:
        result.append(ObjectTracked(
            id=d["id"], name=d["object"], bbox=d["coordinates"]))
    return result



def main():
    ARGS = build_parser().parse_args()


    logging.info('  Opening input video "{}"...'.format(ARGS.video))
    video_cap = cv2.VideoCapture(ARGS.video)
    if not video_cap.isOpened():
        logging.error(' Error opening video "{}"'.format(ARGS.video))
        return 

    logging.info('  Reading JSON file "{}"...'.format(ARGS.json))
    initial_objects = load_initial_detections(json_file=ARGS.json)
    ok, frame = video_cap.read()
    mtracker = MultiTracker(initial_objects=initial_objects,
                            frame0=frame, algo_name=ARGS.method)

    h,w,_ = frame.shape
    ovideo = cv2.VideoWriter(ARGS.output, cv2.VideoWriter_fourcc(*'MJPG'), 24, (w,h))

    tictac = cv2.TickMeter()
    nframes=0
    logging.info("  Start tracking with {} objects".format(len(initial_objects)))
    while True:
        ok, frame = video_cap.read()
        if not ok:
            logging.info("  The video ended | Processed frames {} | Final tracked objects {}".format(nframes, len(mtracker._curr_objects)))
            break

        tictac.start()
        mtracker.update(frame=frame)
        tictac.stop()

        fps = int(tictac.getFPS())
        # draw the resuls 
        mtracker.draw(frame=frame, title="Method: {} | FPS={}".format(ARGS.method, fps))
        nframes+=1
        if nframes%100==0:
            logging.info("  Frames count {:05d} | FPS = {}".format(nframes, fps))

        # display the results 
        if ARGS.display:
            cv2.imshow("Tracking", cv2.resize(frame, dsize=None, fx=0.75, fy=0.75))
            cv2.waitKey(1)

        ovideo.write(frame)
    ovideo.release()

if __name__ == "__main__":
    main()