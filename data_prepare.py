import os
path = "test_imgs/sequences/00/image_0"
for file in os.listdir(path):
    new_name = "000"+file
    os.rename(path+"/"+file, path+"/"+new_name)