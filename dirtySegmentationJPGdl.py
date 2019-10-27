import pandas as pd
import os
from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool

#READ THE COMMENTS BEFORE RUNNING THIS!!!! THERE IS PREP TO BE DONE

#download the below csv for the training annotations for all of the images with segmentation data
# https://storage.googleapis.com/openimages/v5/train-annotations-object-segmentation.csv
#move or copy it into a new folder name "oiv5segmentation" in your home directory along with this script
#change the <user_name_here> to your username
f=pd.read_csv("/home/<user_name_here>/oiv5segmentation/train-annotations-object-segmentation.csv")


#download the "class-descriptions-boxable.csv" from the OIDV5 downloads page here: 
# https://storage.googleapis.com/openimages/web/download.html  
#you can find a list of LabelNames for classes that have segmentation data here:
# https://storage.googleapis.com/openimages/v5/classes-segmentation.txt
#open "class-descriptions-boxable.csv" it in a text editor 
#search for the name of the class you want
#copy the '/m/<LabelName>' LabelName for the class you want 
#check to see if it is in "classes-segmentation.txt", and if so paste it over the one I used.
#'/m/01599' below is just the LabelName for "Beer", as an example.
numClasses = ['/m/01599']

u = f.loc[f['LabelName'].isin(numClasses)]
threads = 20
commands = []
pool = ThreadPool(threads)

for ind in u.index:	
	image = u['ImageID'][ind]
	
	#change the <user_name_here> below to your username
	#add a directory called "/BeerJPGs" in the "/oiv5segmentation" directory.  that's where it will download the jpg's to
	#if you named it something else change that below
	download_dir = "/home/<user_name_here>/oiv5segmentation/BeerJPGs/"

	#change "train" below to "test" or "validation" if you want the jpg images for those
	path = "train" + '/' + str(image) + '.jpg ' + '"' + download_dir + '"'
	command = 'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/' + path 
	commands.append(command)

list(tqdm(pool.imap(os.system, commands), total = len(commands) ))

print('Done!')
pool.close()
pool.join()

#YOU STILL NEED TO DOWNLOAD THE MASK PNG's FROM THE DOWNLOADS PAGE!! 
#go here:
#  https://storage.googleapis.com/openimages/web/download.html
#click "train" by "segmentations" and download all of the zip files (0 1 2 3 4 5 6 7 8 9 a b c d e and f)
#It's not that big of a set of files, just download all of them by clicking on the links
