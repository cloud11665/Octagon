# -*- coding: utf-8 -*-
import time
from typing import Union, Tuple, List
import sys
import click

import cv2
import numpy as np

import stack

CANNY_TH1 = 60
CANNY_TH2 = 120
PATH = './../src/img/stop.png'


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
	img_prep = cv2.bilateralFilter(img_prep, 7, 50, 50)
	img_canny = cv2.Canny(img_prep, CANNY_TH1, CANNY_TH2)
	img_mask = contours(img_canny, img_mask)

	if debug:
		return stack.img_stack(([img, img_gray, img_prep],
								[img_canny, img_mask, img_bl]), scale)
	else:
		return img_mask
	
	
@click.command()
@click.option('-w', '--webcam', is_flag=True)
@click.option('--wres', nargs=2, type=int, default=(640, 480))
@click.option('--wid', )
def main(photo, photo_path, film, film_path, wecam, webcam_id,webcam_fps, webcam_res):

	cam = cv2.VideoCapture(0)
	cam.set(10, 100)
	while True:
		time.sleep(0.1)
		stat, img = cam.read()

		cv2.imshow('Octagon', compute(img))

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

'''
@click.command()
@click.option('--webcam', '-w', default=False)
def main(webcam, path, debug, framewidth=640, frameheight=480):
	if webcam:
		cam = cv2.VideoCapture(0)
		cam.set(10, 100)
		cam.set(3, framewidth)
		cam.set(4, frameheight)
		while True:
			time.sleep(0.1)
			stat, img = cam.read()

			cv2.imshow('Octagon', compute(img))

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
	elif path:
		img = cv2.imread(path)
		cv2.imshow('Octagon', compute(img))'''
