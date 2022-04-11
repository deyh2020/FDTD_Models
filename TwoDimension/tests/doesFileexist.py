from os.path import exists

fileDir = "../data/2022-03-30/Laptop_Debug_1/"
files = ["fields.h5","structure.h5"]

for file in files:
    print(os.path.exists(fileDir + file))