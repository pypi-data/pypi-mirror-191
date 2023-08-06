import numpy as np
import cv2
from itertools import chain
from typing import Optional, Union
import statistics as stats
import attr
import numpy as np
import math


@attr.s(auto_attribs=True)
class Line:

    x0: int
    y0: int
    x1: int
    y1: int
    is_ver: bool
    is_hor: bool
    line_id: int


@attr.s(auto_attribs=True)
class Lines:
    """class for image as a np pixel array, and its row dim, and col dim"""

    page_number: int
    page_height: float
    page_width: int
    lines: Union[np.ndarray, list]
    img: np.ndarray = None

    def as_dict(self):
        return attr.asdict(self)


def get_random_rgb_color():
    np_color = np.random.choice(range(256), size=3)
    color = (int(val) for val in np_color)
    return tuple(color)


#! thats the main function
def get_lines_object(img: np.array):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, lines = get_hor_ver_lines_from_image(img, length_threshold=50)
    lines = convert_to_line_objects(lines)
    # lines_object = Lines(
    #     page_number=self.page_number,
    #     page_height=img.shape[0],
    #     page_width=img.shape[1],
    #     lines=lines,
    #     img=img,
    # )
    return lines


def get_hor_ver_lines_from_image(img: np.array, length_threshold: int):
    line_detector = cv2.ximgproc.createFastLineDetector(
        # length_threshold=length_threshold,
        canny_th1=50,
        canny_th2=150,
        do_merge=True,
    )
    lines = line_detector.detect(img)
    lines = lines.squeeze()
    lines = filter_non_hor_ver_lines(lines=lines)
    return line_detector, lines


def filter_non_hor_ver_lines(lines: np.array) -> np.array:
    bad_index = []
    if lines is None or lines.size < 1:
        return lines
    for i, line in enumerate(lines):
        line_angle = get_line_angle(line)
        print(line_angle)
        if not is_hor_ver_angle(line_angle):
            bad_index.append(i)
    filtered_lines = np.delete(lines, bad_index, axis=0)
    return filtered_lines


def is_hor_angle(angle: float) -> bool:
    return -3 < angle < 3


def is_ver_angle(angle: float) -> bool:
    return 87 < angle < 93


def is_hor_ver_angle(angle: float) -> bool:
    is_hor = is_hor_angle(angle)
    is_ver = is_ver_angle(angle)
    return is_hor or is_ver


def get_line_angle(line: np.array) -> float:
    x0, y0, x1, y1 = line
    delta_x = abs(x0 - x1)
    delta_y = abs(y0 - y1)
    line_angle = math.degrees(math.atan2(delta_y, delta_x))
    return line_angle


def left_to_right_line(line):
    if line.x0 <= line.x1:
        return line
    return Line(line.x1, line.y1, line.x0, line.y0)


def bottom_up_line(line):
    if line.y0 <= line.y1:
        return line
    return Line(line.x1, line.y1, line.x0, line.y0)


def hor_intersection(l1, l2):
    l1 = left_to_right_line(l1)
    l2 = left_to_right_line(l2)
    eps = 20
    if abs(l1.y0 - l2.y0) >= eps and abs(l1.y1 - l2.y1) >= eps:
        return False
    if l1.x0 > l2.x0:
        l1, l2 = l2, l1

    return l1.x1 >= l2.x0 - eps


def ver_intersection(l1, l2):
    l1 = bottom_up_line(l1)
    l2 = bottom_up_line(l2)
    eps = 20
    if abs(l1.x0 - l2.x0) >= eps and abs(l1.x1 - l2.x1) >= eps:
        return False
    if l1.y0 > l2.y0:
        l1, l2 = l2, l1
    return l1.y1 >= l2.y0 - eps


def get_intersection(lines: list[Line], is_hor: bool = True) -> dict[int]:
    """method to compute all the intersecting lines in one orientation
    Args:
        lines (list[Line]): _description_
        is_hor (bool, optional): _description_. Defaults to True.
    Returns:
        dict[int]: _description_
    """
    intersection_function = hor_intersection if is_hor else ver_intersection
    intersecting_lines = {}
    for line in lines:
        for line2 in lines:
            if line.line_id == line2.line_id:
                continue
            if intersection_function(line, line2):
                results_list = intersecting_lines.get(line.line_id, [])
                results_list.append(line2.line_id)
                intersecting_lines[line.line_id] = results_list
    return intersecting_lines


def dfs_visit(G, v, found, cc):
    # TODO change dfs_visit to using stack instead of recursive call
    for u in G[v]:
        if u not in found:
            found.add(u)
            cc.append(u)
            if u in G.keys():
                dfs_visit(G, u, found, cc)


def dfs(G):
    found = set()
    all_cc = []
    for v in G.keys():
        if v not in found:
            found.add(v)
            cc = [v]
            dfs_visit(G, v, found, cc)
            all_cc.append(cc)
    return all_cc


def get_combined_lines(cc: list, line_dict: dict, line_id: int, is_hor: bool = False):
    lines = [line_dict[key] for key in cc]
    if is_hor:
        x0 = min(lines, key=lambda x: x.x0).x0
        x1 = max(lines, key=lambda x: x.x1).x1
        y0 = np.mean([y.y0 for y in lines])
        y1 = np.mean([y.y1 for y in lines])
        return Line(
            x0=x0, x1=x1, y0=y0, y1=y1, line_id=line_id, is_hor=True, is_ver=False
        )
    y0 = min(lines, key=lambda x: x.y0).y0
    y1 = max(lines, key=lambda x: x.y1).y1
    x0 = np.mean([x.x0 for x in lines])
    x1 = np.mean([x.x1 for x in lines])
    return Line(
        x0=x0, x1=x1, y0=y0, y1=y1, line_id=line_id, is_hor=is_hor, is_ver=not is_hor
    )


def convert_to_line_objects(lines: np.array) -> list[Line]:
    if lines is None or lines.size < 1:
        return [], []
    hor_lines = []
    ver_lines = []
    for i, line in enumerate(lines):
        is_hor = is_ver = False
        delta_x = abs(line[0] - line[2])
        delta_y = abs(line[1] - line[3])
        if delta_x > delta_y:
            is_hor = True
            line[1] = line[3] = stats.mean([line[1], line[3]])
            hor_lines.append(
                Line(
                    x0=min(line[0], line[2]),
                    y0=line[1],
                    x1=max(line[0], line[2]),
                    y1=line[3],
                    is_ver=is_ver,
                    is_hor=is_hor,
                    line_id=i,
                )
            )
        else:
            is_ver = True
            line[0] = line[2] = stats.mean([line[0], line[2]])
            ver_lines.append(
                Line(
                    x0=line[0],
                    y0=min(line[1], line[3]),
                    x1=line[2],
                    y1=max(line[1], line[3]),
                    is_ver=is_ver,
                    is_hor=is_hor,
                    line_id=i,
                )
            )

    ver_line_dict = {x.line_id: x for x in ver_lines}
    hor_line_dict = {x.line_id: x for x in hor_lines}
    ver_line_inter = get_intersection(ver_lines, is_hor=False)
    ver_connected_components = dfs(ver_line_inter)
    hor_line_inter = get_intersection(hor_lines, is_hor=True)
    hor_connected_components = dfs(hor_line_inter)
    new_ver = []
    new_hor = []
    inter_hor_line_ids = set(list(chain(*hor_connected_components)))
    inter_ver_line_ids = set(list(chain(*ver_connected_components)))

    for i, cc in enumerate(ver_connected_components):
        new_ver.append(
            get_combined_lines(cc=cc, line_id=i, line_dict=ver_line_dict, is_hor=False)
        )
    for i, cc in enumerate(hor_connected_components):
        new_hor.append(
            get_combined_lines(cc=cc, line_id=i, line_dict=hor_line_dict, is_hor=True)
        )
    old_hor = [x for x in hor_lines if x.line_id not in inter_hor_line_ids]
    new_hor.extend(old_hor)
    for i, line in enumerate(new_hor):
        line.line_id = i * 2
    old_ver = [y for y in ver_lines if y.line_id not in inter_ver_line_ids]
    new_ver.extend(old_ver)
    for i, line in enumerate(new_ver):
        line.line_id = i * 2 + 1
    lines = new_hor + new_ver
    return lines
