import numpy as np
from matplotlib.image import imread
from PIL import Image
from sklearn.cluster import KMeans

def most_frequest_colors(image_file):
    
    img = Image.open(image_file)
        
    # Convert the image to a NumPy array
    img_array = np.array(img)
    
    # Print the shape of the image array for debugging
    print(f"Original image shape: {img_array.shape}")
    
    # Reshape the image array to a 2D array where each row is a pixel (R, G, B)
    pixels = img_array.reshape(-1, 3)
    
    # Print the reshaped image array for debugging
    print(f"Reshaped image shape: {pixels.shape}")
    
    # Picks the most common colors
    num_clusters = 10
    
    kmeans = KMeans(n_clusters=num_clusters)
    
    # Fit the KMeans object into the reshaped array
    kmeans.fit(pixels)
    
    # Grabs the most common colors
    cluster_centers = kmeans.cluster_centers_
    cluster_centers = cluster_centers.astype(int)
    
    return cluster_centers