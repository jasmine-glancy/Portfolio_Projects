import numpy as np
from matplotlib.image import imread
from PIL import Image
from sklearn.cluster import KMeans

def most_frequest_colors(image_file):
    
    img = Image.open(image_file)
        
    # Convert the image to a NumPy array
    img_array = np.array(img)
    
    # # Print the shape of the image array for debugging
    # print(f"Original image shape: {img_array.shape}")
    
    # Reshape the image array to a 2D array where each row is a pixel (R, G, B)
    pixels = img_array.reshape(-1, 3)
    
    # # Print the reshaped image array for debugging
    # print(f"Reshaped image shape: {pixels.shape}")
    
    # Picks the most common colors
    num_clusters = 10
    
    kmeans = KMeans(n_clusters=num_clusters)
    
    # Fit the KMeans object into the reshaped array
    kmeans.fit(pixels)
    
    # Grabs the most common colors
    cluster_centers = kmeans.cluster_centers_
    cluster_centers = cluster_centers.astype(int)
    
    # print(type(cluster_centers))
    return cluster_centers

def first_5_colors(color_dict):
    """Grabs the first 5 colors in the dictionary"""

    return color_dict[:5]

def last_5_colors(color_dict):
    """Grabs the first 5 colors in the dictionary"""

    return color_dict[5:]

def individual_rgb_values(color_dict):
    """Grabs the individual RGB values from the array"""
    
    rgb_values = []
    
    for color in color_dict:
        r, g, b = color
        
        rgb_values.append(f"R: {r} G: {g} B: {b}")
        
    return rgb_values


def format_colors(color_dict):
    """Outputs colors as R: x G: x B: x"""
    
    formatted_colors = []
    
    for color in color_dict:
        print(f"Color: {color}")
        
        r, g, b = color
        
        formatted_colors.append(f"rgb({r}, {g}, {b})")

    return formatted_colors