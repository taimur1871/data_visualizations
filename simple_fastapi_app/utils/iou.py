# check for duplicate detections
import numpy as np

def iou(box1, box2):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(box1[0], box2[0])
    yA = max(box1[1], box2[1])
    xB = min(box1[2], box2[2])
    yB = min(box1[3], box2[3])

    # compute the area of intersection rectangle
    intersction = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if intersction == 0:
        return 0
    # compute the area of both the prediction and ground-truth
    # rectangles
    box1_Area = abs((box1[2] - box1[0]) * (box1[3] - box1[1]))
    box2_Area = abs((box2[2] - box2[0]) * (box2[3] - box2[1]))

    # compute the intersection over union
    # union is sum of areas of two boxes - intersection
    iou = intersction / float(box1_Area + box2_Area - intersction)

    # return the intersection over union value
    return iou


def iou_check(cutter_list):
    # record indices of duplicates
    dupl_temp = []
    for i in range(len(cutter_list)):
        for j in range(len(cutter_list)):
            if i == j:
                continue
            elif iou(cutter_list[i], cutter_list[j]) > 0.5:
                dupl_temp.append(i)

    # get only first half of indices
    if len(dupl_temp) != 0:
        # remove the indices from original list
        to_remove = []
        for i in dupl_temp[len(dupl_temp)//2:]:
            to_remove.append(cutter_list[i])
        
        for j in to_remove:
            cutter_list.remove(j)
        return cutter_list
    else:
        return cutter_list
