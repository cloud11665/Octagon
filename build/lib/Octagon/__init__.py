# -*- coding: utf-8 -*-
import time
from typing import Union, Tuple, List
import sys
import click

import cv2
import numpy as np

CANNY_TH1 = 60
CANNY_TH2 = 120


def img_stack(src: Union[Tuple, List], scale: float) -> np.ndarray:
	rows: int = len(src)
	cols: int = len(src[0])
	height: int = src[0][0].shape[0]
	width: int = src[0][0].shape[1]

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


def contours(src: Union[Tuple, List], mask: Union[Tuple, List]):
	cntrs, weight = cv2.findContours(src, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	for cnt in cntrs:
		area = cv2.contourArea(cnt)
		if area > 750:
			perim = cv2.arcLength(cnt, closed=True)
			approx = cv2.approxPolyDP(cnt, 0.02 * perim, closed=True)
			corners = len(approx)
			x, y, w, h = cv2.boundingRect(approx)
			if corners == 8:
				cv2.drawContours(mask, cnt, -1, (0, 0, 255), 5)
				cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 255, 0), 2)
				cv2.putText(mask, 'Octagon', (x, y - 5), cv2.QT_FONT_NORMAL, 1, (0, 255, 0), 2)
	return mask


def compute(img: Union[Tuple, List], scale: float = 0.75, debug: bool = False):
	img_mask = img.copy()
	img_bl = np.zeros_like(img)
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img_prep = cv2.GaussianBlur(img_gray, (5, 5), 1)
	img_prep = cv2.bilateralFilter(img_prep, 7, 40, 35)
	img_canny = cv2.Canny(img_prep, CANNY_TH1, CANNY_TH2)
	img_mask = contours(img_canny, img_mask)

	if debug:
		return img_stack(([img, img_gray, img_prep],
						[img_canny, img_mask, img_bl]), scale)
	else:
		return img_mask
	
	
@click.command()
@click.option('-d', '--debug', is_flag=True, help="Debug mode, shows the process of edge detection.")
@click.option('--nogui', is_flag=True, help="FLAG, doesn't show the default gui.")
@click.option('-w', '--webcam', is_flag=True, help="FLAG, can only choose one.")
@click.option('--wres', nargs=2, type=int, default=(640, 480), help="Size of output, <x, y>, defaults to 640x480px")
@click.option('--wid', nargs=1,type=int, default=0, help="webcam ID, defaults to 0")
@click.option('--fps', nargs=1,type=int, default=10, help="Webcam FPS, defaults to 10")
@click.option('-i', '--image', '--img',  nargs=1, default='',  type=str, help="Input image path.")
@click.option('-v', '--video',           nargs=1, default='',  type=str, help="Input video path.")
@click.option('-o', '--output', '--out', nargs=1, default='',  type=str, help="Output path.")
@click.option('-s', '--scale',           nargs=1, default=0.75, type=float, help="Gui scale.")
def main(webcam, wres, wid, fps, image, video, debug, output, scale, nogui):
	if webcam:
		cam = cv2.VideoCapture(wid)
		cam.set(3, wres[0])
		cam.set(4, wres[1])
		cam.set(10, 100)
		while True:
			time.sleep(1/fps)
			_, img = cam.read()
			cv2.imshow('Octagon', compute(img, scale, debug))

			if cv2.waitKey(1) & 0xFF == ord('q'):
				sys.exit(2)
	if image:
		img = cv2.imread(image)
		if output:
			cv2.imwrite(output, compute(img, 1.0, debug))
		if not nogui:
			cv2.imshow('Octagon', compute(img, scale, debug))
			cv2.waitKey(0)
		sys.exit(2)

	if video:
		print('Not implemented yet')
		sys.exit(2)

	else:
		print('Invalid arguments.')
		sys.exit(2)


main()
