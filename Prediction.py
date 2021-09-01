from detecto import utils
from detecto.core import Model
from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import numpy as np
import cv2

import Validate

model = Model.load('./train.pth',[
    'Name', 'Date', 'Faculty', 'Classroom', 'Scholastic', 'ID'
])
def resize_image(path):
    img = cv2.imread(path,cv2.IMREAD_UNCHANGED)
    dim = (500,350)
    resized = cv2.resize(img,dim,interpolation = cv2.INTER_AREA)
    cv2.imwrite('./static/out.png',resized)
def non_max_suppression_fast(boxes, labels, overlapThresh):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
    #
    # initialize the list of picked indexes
    pick = []

    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],
                                               np.where(overlap > overlapThresh)[0])))

    # return only the bounding boxes that were picked using the
    # integer data type

    final_labels = [labels[idx] for idx in pick]
    final_boxes = boxes[pick].astype("int")

    return final_boxes, final_labels
def detector_vietorc():
    config = Cfg.load_config_from_name('vgg_transformer')
    config['weights'] = 'https://drive.google.com/uc?id=13327Y1tz1ohsm5YZMyXVMPIOjoOA0OaA'
    config['cnn']['pretrained'] = False
    config['device'] = 'cpu'
    config['predictor']['beamsearch'] = False
    detector = Predictor(config)
    return detector
def readImage(path):
    img = Image.open(path)
    s = detector_vietorc().predict(img)
    return s
def prediction(path):
    resize_image(path)
    fname = './static/out.png'
    image = utils.read_image(fname)
    labels,boxes,score = model.predict(image)
    final_boxes,final_labels = non_max_suppression_fast(boxes.numpy(),labels,0.005)
    list = []
    for i,bbox in enumerate(final_boxes):
        x_min, y_min, x_max, y_max = bbox
        if (x_max < 130):
            img = image[y_min:y_max, 0:x_max]
        else:
            img = image[y_min:y_max + 3, 130:x_max + 3]
        f = './static/info' + str(i) + '.png'
        cv2.imwrite(f, img)
        list.append(readImage(f))
    return list
