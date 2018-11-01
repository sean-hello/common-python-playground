#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-31 14:52:56
# @Author  : LiYu ()
# @Link    : ${link}
# @Version : $Id$

import sys, random, argparse
import numpy as np
import math
from PIL import Image

#70 levels of gray
gscale1 =  "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
#10 levels of gray
gscale2 = '@%#*+=-:. '

def getAvergeL(image):			#PIL Image对象传入
	"""Given PIL Image, return average value of grayscale value"""
	#get image as numpy array
	im = np.array(image)		#Image转成numpy数组，成为一个二维数组，包含每个像素的高度
	#get the dimensions
	w,h = im.shape				#保存图像的尺寸
	#get the average
	return np.average(im.reshape(w*h))		#average()计算图像中亮度的平均值，先使用numpy.reshape()先将维度为宽高的二维数组转成扁平的一维，numpy.average()调用对这些数组值求和并计算平均值

def coverImageToAscii(fileName, cols, scale, moreLevels):
	"""Given Image and dimensions(rows, cols),returns an m*n list of Image"""
	#declare globals
	global gscale1, gscale2
	#open image and convert to grayscale
	image = Image.open(fileName).convert('L')		#打开文件，转为灰度图像，L：luminancce是图像亮度单位
	#store the image dimensions
	W, H = image.size[0],image.size[1]				#保存图像的宽度和高度
	print("input image dims :%d x %d" %(W,H))
	#compute tile width
	w = W/cols 										#使用浮点而不是整数除法，避免在计算小块尺寸时的截断误差
	#compute tile height based on the aspect ratio ratio and scale of the font
	h = w/scale										#垂直比例系数，计算高度
	#compute number of rows touse in the final grid 
	rows = int(H/h)									#用网格计算高度

	print("cols: %d ,rows: %d" %(cols,rows))
	print("tile dims: %d x %d" %(w, h))	

	#check if image size is too small
	if cols > W or rows > H:
		print("Image too small for specified cols!")
		exit(0)
	#an ASCII image is a list of character strings
	aimg = []						#初始化，按计算好的图像小块行数迭代遍历
	#generate the list of tile dimentsions
	for j in range(rows):
		y1 = int(j*h)				#计算每个图像
		y2 = int((j+1)*h)
		#correct the last tile 
		if j == rows-1:
			y2 = H
		#append an empty string
		aimg.append("")
		for i in range(cols):
			#crop the image to fit the tile 
			x1 = int(i*w)
			x2 = int((i+1)*w)
			#correct the last tile
			if i == cols-1:
				x2 = W
			img = image.crop((x1,y1,x2,y2))
			#get the average luminance
			avg = int(getAvergeL(img))
			#look up the ASCII character for gratscale value(avg)
			if moreLevels:
				gsval = gscale1[int((avg*69)/255)]
			else:
				gsval = gscale2[int((avg*9)/255)]
			#append the ASCII character to the string
			aimg[j] += gsval
	return aimg

def main():
	#create parser
	descStr = "This program converts an image into ASCII art."
	parser = argparse.ArgumentParser(description=descStr)
	#add expected arguments
	parser.add_argument('--file', dest='imgFile', required=True)		#路径
	parser.add_argument('--scale', dest='scale', required=False)		#垂直比例因子
	parser.add_argument('--out', dest='outFile', required=False)		#输出文件名
	parser.add_argument('--cols', dest='cols', required=False)			#ASCII输出文本列数
	parser.add_argument('--moreLevels', dest='moreLevels', action='store_true')	#让用户选择更多层次的灰度梯度
	#parse arguments
	args = parser.parse_args()
	
	imgFile = args.imgFile
	#set output file
	outFile = 'out.txt'
	if args.outFile:
		outFile = args.outFile
	#set scale default as 0.43, which suits a Courier font
	scale = 0.43
	if args.scale:
		scale = float(args.scale)
	#set cols
	cols = 80
	if args.cols:
		cols = int(args.cols)
	print('generating ASCII art...')
	#convert image to ASCII text
	aimg = coverImageToAscii(imgFile, cols, scale, args.moreLevels)

	#open a new text file
	f = open(outFile, 'w')			#写入文件
	#write each string in the list to the new file 
	for row in aimg:
		f.write(row + '\n')
	#clean up
	f.close()
	print("ASCII art writen to %s" % outFile)

if __name__ == '__main__':
	main()
