import os
import random
import shutil
from shutil import copyfile
import matplotlib.pyplot as plt

#Definimos la ruta del dataset
root_dir = "dataset2"

#Verificamos si existe
if os.path.exists(root_dir):
  shutil.rmtree(root_dir)

#Creamos directorios
def create_train_val_dirs(root_path):

    os.makedirs(os.path.join(root_dir,"train"))
    os.makedirs(os.path.join(f"{root_dir}/train", "fire"))
    os.makedirs(os.path.join(f"{root_dir}/train", "non_fire"))
    os.makedirs(os.path.join(root_dir,"test"))
    os.makedirs(os.path.join(f"{root_dir}/test", "fire"))
    os.makedirs(os.path.join(f"{root_dir}/test", "non_fire"))

try:
    create_train_val_dirs(root_path=root_dir)
except FileExistsError:
    print("You should not be seeing this since the upper directory is removed beforehand")

for rootdir, dirs, files in os.walk(root_dir):
    for subdir in dirs:
        print(os.path.join(rootdir, subdir))


#funcion que divide el dataset para entrenamiento y test
def split_data(SOURCE_DIR, TRAINING_DIR, VALIDATION_DIR, SPLIT_SIZE):

    processed_data = []
    
    for filename in os.listdir(SOURCE_DIR) :
        file = SOURCE_DIR + filename
        if os.path.getsize(file) > 0 :
            processed_data.append(filename)
        else :
            print(f"{filename} is zero length, so ignoring.")

    randomized_data = random.sample(processed_data, len(processed_data))

    training_length = int(len(randomized_data)*SPLIT_SIZE)
    validation_length = int(len(randomized_data) - training_length)

    training_data = randomized_data[:training_length]
    validation_data = randomized_data[-validation_length:]

    #Copiar a nuevos directorios
    for filename in training_data :
        present_file = SOURCE_DIR + filename
        destination = TRAINING_DIR + filename
        copyfile(present_file, destination)


    for filename in validation_data :
        present_file = SOURCE_DIR + filename
        destination = VALIDATION_DIR + filename
        copyfile(present_file, destination)

#Se guardan rutas de directorios
FIRE_SOURCE_DIR = "fire_dataset/fire_images/"
NON_FIRE_SOURCE_DIR = "fire_dataset/non_fire_images/"

TRAINING_DIR = "dataset/train/"
VALIDATION_DIR = "dataset/test/"

TRAINING_FIRE_DIR = os.path.join(TRAINING_DIR, "fire/")
VALIDATION_FIRE_DIR = os.path.join(VALIDATION_DIR, "fire/")

TRAINING_NON_FIRE_DIR = os.path.join(TRAINING_DIR, "non_fire/")
VALIDATION_NON_FIRE_DIR = os.path.join(VALIDATION_DIR, "non_fire/")

#Eliminamos si ya existen
if len(os.listdir(TRAINING_FIRE_DIR)) > 0:
  for file in os.scandir(TRAINING_FIRE_DIR):
    os.remove(file.path)
if len(os.listdir(TRAINING_NON_FIRE_DIR)) > 0:
  for file in os.scandir(TRAINING_NON_FIRE_DIR):
    os.remove(file.path)
if len(os.listdir(VALIDATION_FIRE_DIR)) > 0:
  for file in os.scandir(VALIDATION_FIRE_DIR):
    os.remove(file.path)
if len(os.listdir(VALIDATION_NON_FIRE_DIR)) > 0:
  for file in os.scandir(VALIDATION_NON_FIRE_DIR):
    os.remove(file.path)

#Para separar 70% para entrenamiento y 30% para test
split_size = .7

#Llamamos a splitdata para realizar la separación
split_data(FIRE_SOURCE_DIR, TRAINING_FIRE_DIR, VALIDATION_FIRE_DIR, split_size)
split_data(NON_FIRE_SOURCE_DIR, TRAINING_NON_FIRE_DIR, VALIDATION_NON_FIRE_DIR, split_size)

#Imprimimos mensajes informativos
print(f"There are {len(os.listdir(TRAINING_FIRE_DIR))} images of fire for training")
print(f"There are {len(os.listdir(TRAINING_NON_FIRE_DIR))} images of non_fire for training")
print(f"There are {len(os.listdir(VALIDATION_FIRE_DIR))} images of fire for validation")
print(f"There are {len(os.listdir(VALIDATION_NON_FIRE_DIR))} images of non_fire for validation")