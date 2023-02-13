import numpy as np
import scipy.misc
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from PIL import Image
from scipy import ndimage
import math
# import cv2
import plotly.graph_objects as go

# load image in grayscale
# eagle_horse_gray = cv2.imread("question5.jpg", cv2.IMREAD_GRAYSCALE)
# eagle_horse_gray_org = plt.imshow(eagle_horse_gray, cmap = "gray")
# plt.title("The original Gray Scale image")
# plt.savefig("results/grayscaleimage.jpg")
# plt.show()


def resize_image(image_file, percentage):
    image = Image.open(image_file)
    image_array = np.array(image)
    width = int(image_array.shape[1] * percentage / 100)
    height = int(image_array.shape[0] * percentage / 100)
    dim = (width, height)
    image = image.resize((dim))
    return image, dim

def cumsum(histogram):
    len_histogram = len(histogram)
    result = np.zeros(len_histogram)
    sum = 0
    for each in range(len_histogram):
        sum+=histogram[each]
        result[each] = sum
    normalized_result = result*(max(histogram)/max(result))
    return result, normalized_result, max(normalized_result), min(normalized_result)

def norm_to_pixel_range(cdf_normalized):
    equalized_histogram = []
    cdf_min = min(cdf_normalized)
    cdf_max = max(cdf_normalized)
    for each in cdf_normalized:
        eq = (each-cdf_min)*255/(cdf_max-cdf_min)
        equalized_histogram.append(eq)

    return np.array(equalized_histogram).astype("uint8")


# we get resized image by using resize_image function
eagle_horse, dimension = resize_image("../dataset/eagleHorse.jpg", 40)
eagle_horse_array = np.array(eagle_horse)
# transform it from rgb to gray scale
eagle_horse_gray = rgb2gray(eagle_horse_array)


eh_resized = plt.imshow(eagle_horse_gray, cmap = "gray")
plt.title("The grayscale image with reduced resolution")
plt.savefig("results/reducedresolution.jpg")
plt.show()
# applying Gaussian Filter

gaussian_result_eh = ndimage.gaussian_filter(eagle_horse_gray, sigma = 1)
# resulted image's pixels are in the range of 0 and 1. We scale it to 0 and 255
gaussian_result_eh *=255
gaussian_compare, images = plt.subplots(1,2)
images[0].imshow(eagle_horse_gray, cmap = "gray")
images[0].title.set_text("Resized gray scale image")
images[1].imshow(gaussian_result_eh, cmap = "gray")
images[1].title.set_text("Gaussian filter result")
gaussian_compare.suptitle("Gaussian results")
gaussian_compare.savefig("results/gaussianresults.jpg")

plt.show()


N = dimension[0]*dimension[1]
num_of_bins = int(math.log2(N)+1)

histogram_data_16bins, edges_16bins = np.histogram(gaussian_result_eh, 16)
histogram_data_256bins, edges_256bins = np.histogram(gaussian_result_eh, 256)

# print(edges)
plt.hist(gaussian_result_eh.flatten(),256,[0,256]); 
plt.savefig("results/histogram.jpg")
plt.show()
plt.hist(gaussian_result_eh.flatten(),16,[0,256]); 
plt.savefig("results/histogram16bins.jpg")
plt.show()




_, cdf16, cdf_max16, cdf_min16 = cumsum(histogram_data_16bins)
_, cdf, cdf_max, cdf_min = cumsum(histogram_data_256bins)

histogram_max = max(histogram_data_256bins)
# bin_edges = list(range(0,256))
plt.plot(edges_256bins[1:], cdf, color = "r")
plt.hist(gaussian_result_eh.ravel(),256,[0,256] )
plt.savefig("results/histogramandcdf")
plt.show()





normalized_cdf_to_pixel = norm_to_pixel_range(cdf)
eagle_horse_gray_equalized = normalized_cdf_to_pixel[gaussian_result_eh.astype("uint8")]
eagle_horse_gray_equalized = np.reshape(eagle_horse_gray_equalized,gaussian_result_eh.shape)


hist_eq, images = plt.subplots(1,2)
images[0].imshow(gaussian_result_eh, cmap = "gray")
images[0].title.set_text("Before")
images[1].imshow(eagle_horse_gray_equalized, cmap = "gray")
images[1].title.set_text("After")
hist_eq.suptitle("Equalization results")
hist_eq.savefig("results/equalizationresults.jpg")

plt.show()


# # calculate equalized histogram

histogram_data_16bins_eq, edges_16bins_eq = np.histogram(eagle_horse_gray_equalized, 16)
histogram_data_256bins_eq, edges_256bins_eq = np.histogram(eagle_horse_gray_equalized, 256)

plt.hist(eagle_horse_gray_equalized.flatten(), 256, [0,256])
plt.savefig("results/histogram_equalized_256.jpg")
plt.show()

plt.hist(eagle_horse_gray_equalized.flatten(), 16, [0,256])
plt.savefig("results/histogram_equalized_16.jpg")
plt.show()

cdf_org, cdf_table,cdf_table_min, cdf_table_max = cumsum(histogram_data_16bins)
cdf_org_eq, cdf_eq_table, cdf_eq_table_min, cdf_eq_table_min = cumsum(histogram_data_16bins_eq)

print(len(edges_16bins_eq))

edges_table = edges_16bins[1:]
edges_table_eq = edges_16bins_eq[1:]


L = 0
for each in edges_table:
    L+=each
edges_norm_eq = [round(x/L,4) for x in edges_table_eq]
edges_norm = [round(x/L,4) for x in edges_table]
edges_table = [round(x,3) for x in edges_table]
edges_table_eq = [round(x,3) for x in edges_table_eq]

print(L)
norm_cdf_org = cdf_org/max(cdf_org)
norm_cdf_org_eq = cdf_org_eq/max(cdf_org_eq)

fig = go.Figure(data=[go.Table(header=dict(values=['Normalized Values of H1', 'Normalized Values of H2', 'Values of H1', ' Values of H2', 'N of H1', 'N of H2', 'sum of N of H1', 'sum of N of H2']),
                 cells=dict(values=[edges_norm, edges_norm_eq, edges_table, edges_table_eq, histogram_data_16bins, histogram_data_16bins_eq, cdf_org, cdf_org_eq]))])
# fig.savefig("results/table.jpg")
fig.show()