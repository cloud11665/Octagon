# -*- coding: utf-8 -*-
from typing import Iterable, Union, Tuple, List

import cv2
import numpy as np


def img_stack(src:Union[Tuple, List], scale:float) -> np.ndarray:
	rows:int = len(src)
	cols:int = len(src[0])
	height:int = src[0][0].shape[0]
	width:int = src[0][0].shape[1]

	if isinstance(src[0], list):
		for x in range(0, rows):
			for y in range(0, cols):
				if src[x][y].shape[:2] == src[0][0].shape[:2]:
					src[x][y] = cv2.resize(src[x][y], (0, 0), fx=scale, fy=scale)
				else:
					src[x][y] = cv2.resize(src[x][y], (src[0][0].shape[1], src[0][0].shape[0]), fx=scale, fy=scale)
				if len(src[x][y].shape) == 2: src[x][y] = cv2.cvtColor(src[x][y], cv2.COLOR_GRAY2BGR)

		img_blank = np.zeros((height, width, 3), np.uint8)
		hor = [img_blank] * rows
		hor_con = [img_blank] * rows
		for x in range(0, rows):
			hor[x] = np.hstack(src[x])

		return np.vstack(hor)

	for x in range(0, rows):
		if src[x].shape[:2] == src[0].shape[:2]:
			src[x] = cv2.resize(src[x], (0, 0), fx=scale, fy=scale)
		else:
			src[x] = cv2.resize(src[x], (src[0].shape[1], src[0].shape[0]), fx=scale, fy=scale)

		if len(src[x].shape) == 2:
			src[x] = cv2.cvtColor(src[x], cv2.COLOR_GRAY2BGR)
		
	return np.hstack(src)
