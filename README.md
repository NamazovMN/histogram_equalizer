# Histogram Equalization
## What is that for?
Histogram is image processing technique to represent intensity values of an image. Equalization technique is utilized for spreading higher local contrasts in the image.
Thiss allows us to increase the global contrast of the image while pixels with the highest intensity values are decreased locally, after application.
## How do we apply?
Histogram equalization cannot be applied to the RGB image, since it can make strong modifications on image channels. So that we transform the image into gray-scale form, initially. At the next step we apply Gaussian filter to image, which reduces noise in the image and blures regions of the image. Following figure depicts the difference after applying Gaussian Filter to the image.
<p align="center">
<img src="examples_dir/eagleHorse.jpg/gaussian.png" >
</p>
