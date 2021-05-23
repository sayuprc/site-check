import inspect
import os
import shutil
import cv2
import numpy

def mkdir(path):
  if not os.path.isdir(path):
    os.makedirs(path)

def move_file(src, dest):
  shutil.move(src, dest)

def is_file_exists(path):
  return os.path.isfile(path)

def diff_image(src_path, dest_path):
  src = cv2.imread(src_path)
  dest = cv2.imread(dest_path)

  return numpy.array_equal(src, dest)