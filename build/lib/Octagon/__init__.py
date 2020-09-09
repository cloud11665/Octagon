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
	img_prep = cv2.bilateralFilter(img_prep, 7, 40, 35)
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
@click.option('--wid', nargs=1,type=int, default=0)
@click.option('--fps', nargs=1,type=int, default=10)
@click.option('-i', '--image', '--img', nargs=1, type=str, default='^')
@click.option('-v', '--video', nargs=1, default='^', type=str)
@click.option('-d', '--debug', is_flag=True)
@click.option('-o', '--output', '--out', nargs=1, default='^', type=str)
@click.option('-s', '--scale', nargs=1, default=0.75, type=float)
def main(webcam, wres, wid, fps, image, video, debug, output, scale):
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
			cv2.imwrite(output, compute(img, 1.0))

		cv2.imshow('Octagon', compute(img, scale, debug))
		cv2.waitKey(0)

	if video:
		print('Not implemented yet')
		sys.exit(2)

	else:
		print('Invalid arguments.')
		sys.exit(2)

main()
