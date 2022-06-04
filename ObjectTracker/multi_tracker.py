import cv2
import numpy as np
from os.path import abspath, dirname, join
import logging


MODELS_DIR = join(dirname(abspath(__file__)), 'models')


def inside_frame(frame, bbox):
    """
    Return the intersection rectangle between frame_rect and bbox
    """
    H, W, _ = frame.shape
    x1, y1, w, h = bbox
    x2, y2 = x1+w-1, y1+h-1
    x1 = max(x1, 0)
    y1 = max(y1, 0)
    x2 = min(x2, W-1)
    y2 = min(y2, H-1)

    out = x1, y1, x2-x1+1, y2-y1+1
    return out


class ObjectTracked:
    def __init__(self, id, name, bbox) -> None:
        self.id = id
        self.name = name
        self.bbox = bbox


class MultiTracker:

    supported_algoritms = ('CSRT', 'KCF', 'DaSiamRPN')

    def __init__(self, initial_objects: list,  frame0: np.ndarray, algo_name: str = 'KCF') -> None:
        """Initialize multitracker

        Args:
            initial_objects (list): Initial conditions. List of `ObjectTracked` objects
            frame0 (np.ndarray): Initial frame 
            algo_name (str, optional): Method use for tracking. Defaults to 'KCF'.
        """

        if algo_name not in MultiTracker.supported_algoritms:
            raise("Unknow algoritm: {}".format(algo_name))

        n = len(initial_objects)
        self._curr_objects = initial_objects
        self._trackers = [MultiTracker._create_tracker(
            algo_name) for _ in range(n)]
        for tracker, obj in zip(self._trackers, self._curr_objects):
            tracker.init(frame0, inside_frame(frame0, obj.bbox))

    def update(self, frame):
        n = len(self._curr_objects)
        index_to_delete = []
        for i in range(n):
            ok, bbox = self._trackers[i].update(frame)
            if ok:
                self._curr_objects[i].bbox = bbox
            else:                
                index_to_delete.append(i)

        for i in reversed(index_to_delete):
            logging.warning("  Tracking for object {} ended!".format(i))
            del self._curr_objects[i]
            del self._trackers[i]

    def draw(self, frame, title):
        cv2.putText(img=frame, text=title, org=(10, 60), fontFace=2,
                    fontScale=1.5, color=(255, 255, 0), thickness=2)
        for obj in self._curr_objects:
            x, y, w, h = map(int, obj.bbox)
            cv2.rectangle(img=frame, pt1=(x, y), pt2=(
                x+w-1, y+h-1), color=(0, 0, 0), thickness=4)
            cv2.putText(img=frame, text=str(obj.id), org=(
                x, y), fontFace=2, fontScale=1.5, color=(255, 255, 0), thickness=2)

    @staticmethod
    def _create_tracker(name: str):
        """Create a Tracker object with default parameters.
        """
        #TODO(rbt): Allow passing tracker parameters
        if name == 'KCF':
            return cv2.TrackerKCF_create()
        if name == 'CSRT':
            return cv2.TrackerCSRT_create()
        if name == 'DaSiamRPN':
            param = cv2.TrackerDaSiamRPN_Params()
            param.model = join(MODELS_DIR, "dasiamrpn_model.onnx")
            param.kernel_cls1 = join(MODELS_DIR, "dasiamrpn_kernel_cls1.onnx")
            param.kernel_r1 = join(MODELS_DIR, "dasiamrpn_kernel_r1.onnx")
            return cv2.TrackerDaSiamRPN_create(param)
