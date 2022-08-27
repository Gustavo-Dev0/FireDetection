import os
from unittest import result
import zipfile
import urllib.request
import numpy as np
from PIL import Image, ImageOps
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns


from skimage.feature import local_binary_pattern
from sklearn import preprocessing, metrics
from sklearn.svm import LinearSVC


def compute_lbp(arr):

    radius = 3
    n_points = 8 * radius
    n_bins = n_points + 2
    lbp = local_binary_pattern(arr, n_points, radius, 'uniform')
    lbp = lbp.ravel()

    feature = np.zeros(n_bins)
    for i in lbp:
        feature[int(i)] += 1
    feature /= np.linalg.norm(feature, ord=1)
    return feature

def load_data(tag='train'):

    tag_dir = Path.cwd() / tag
    vec = []
    cat = []
    for cat_dir in tag_dir.iterdir():
        cat_label = cat_dir.stem
        for img_path in cat_dir.glob('*.png'):
            print(img_path)
            img = Image.open(img_path.as_posix())
            if img.mode != 'L':
                img = ImageOps.grayscale(img)
                img.save(img_path.as_posix())
            arr = np.array(img)
            feature = compute_lbp(arr)
            vec.append(feature)
            cat.append(cat_label)
    return vec, cat


vec_test, cat_test   = load_data('predict')


import pickle
from tabulate import tabulate

filename = "lbp_svm.sav"

loaded_model = pickle.load(open(filename, 'rb'))
clf = loaded_model

prediction = clf.predict(vec_test)

prediction = prediction.tolist()
prediction_labels = []

for j in prediction:
    temp = "fire"
    if j == 1:
        temp = "non_fire"
    prediction_labels[len(prediction_labels):] = [temp]


results = []
ind = 0
for i in prediction:
    results[len(results):] = [[prediction_labels[ind], cat_test[ind]]]
    ind = ind+1

print(tabulate(results, headers=["Valor predicho", "Valor esperado"]))




