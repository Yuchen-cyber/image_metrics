import numpy as np
#https://matplotlib.org/
import matplotlib.pyplot as plt
#https://scikit-learn.org/stable/
from sklearn.cluster import KMeans
#https://opencv.org/
import cv2
import glob

# This file is written based on :https://www.kaggle.com/code/shivamburnwal/dominant-colour-extraction
def execute_dominant_colour(execute_number):
    for id in range(1, execute_number+1):
        get_dominant_colour(id=id)
        
        
# take first element for sort
def takeFirst(elem):
    return elem[0]
def get_dominant_colour(id):
    # Read image and print dimensions
    filename = './submissions/submission_' + str(id) + '/out1R.png'
    dir_save = './submissions/submission_' + str(id)
    image = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    r, c = image.shape[:2]
    out_r = 120
    image = cv2.resize(image, (int(out_r*float(c)/r), out_r))
    pixels = image.reshape((-1, 3))
    km = KMeans(n_clusters=6)
    km.fit(pixels)
    
    colors = np.asarray(km.cluster_centers_, dtype='uint8')
    # percentage of each extracted colour in the image
    percentage = np.asarray(np.unique(km.labels_, return_counts = True)[1], dtype='float32')
    percentage = percentage/pixels.shape[0]
    percentage_sort = list(-np.sort(-percentage))[:5]
    colour_list = list(zip(percentage,colors))
    colour_list.sort(key=takeFirst, reverse=True)
    colors_sort = np.array(list(zip(*colour_list))[1][:5])


    plt.title('Dominance Of Colours', size=16)
    plt.bar(range(1,6), percentage_sort, color=np.array(colors_sort)/255, edgecolor = "black")
    plt.ylabel('Percentage')
    plt.xlabel('Colours')
    dir_save = './submissions/submission_' + str(id) + '/RESULTS/dominant_color.png'
    command = dir_save
    plt.savefig(command)
    plt.clf()
    

        
def find_cluster_numbers():
    path = './submissions/submission_*/out1R.png'
    cluster_number= []
    all_k_scores = []
    for filename in glob.glob(path):
        get_dominant_colour(filename=filename)
        image = cv2.imread(filename)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        r, c = image.shape[:2]
        out_r = 120
        image = cv2.resize(image, (int(out_r*float(c)/r), out_r))
        pixels = image.reshape((-1, 3))
        X = pixels
        
        distorsions = []
        for k in range(2, 15):
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(X)
            distorsions.append(kmeans.inertia_)
        all_k_scores.append(distorsions) 
        pick_cluster_numbers = []
        for i in range(2, 15):
            if i >= 5:
                index = i - 2
                previous = distorsions[index - 1]
                elbow_value = float(previous - distorsions[index] )
                pick_cluster_numbers.append(elbow_value)
        pick_cluster_number = pick_cluster_numbers.index(max(pick_cluster_numbers)) + 5
        cluster_number.append(pick_cluster_number)
    data = np.array(all_k_scores)
    k_cores = list(np.average(data, axis=0))
    fig = plt.figure(figsize=(15, 5))
    plt.plot(range(2, 15), k_cores)
    plt.grid(True)
    plt.ylabel('K-means Score')
    plt.xlabel('Number of Clusters')
    plt.title('Elbow curve')
    dir_save = './submissions/elbow.png'
    command = dir_save
    plt.savefig(command)
    k_number = round(np.mean(np.array(cluster_number)))
    if k_number < np.mean(np.array(cluster_number)):
        k_number = k_number + 1
        
    print(k_number)
    


    


