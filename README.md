# Image Triangulation
## [Image Triangulation Examples (Video)](https://youtu.be/PlOVQtR-gjY)

## Abstract
Image triangulation, the practice of decomposing images into triangles, deliberately employs simplification to create an abstracted piece of art. While triangulating an image is a relatively simple process, difficulties arise when determining which vertices produce recognizable and visually pleasing output images. Here, we discuss an image triangulation algorithm in Python that utilizes Sobel edge detection and point cloud sparsification to determine final vertices for a Delaunay triangulation, resulting in the creation of artistic triangulated compositions.

## Introduction
Image triangulation creates an abstract representation of an image as a form of art, which can be defined by four primary principles. The output image must divide the original image into a set of non-overlapping triangles, simplify the original image, approximate original image features as triangles, and retain the integrity of the original image.

There are several existing algorithms to perform image triangulation. [Marwood et al. (2018)](https://arxiv.org/pdf/1809.02257.pdf) discuss a greedy algorithm that calculates a least important vertex as well as a stochastic process that mutates vertices according to a probability distribution. The primary goal of the algorithm is compressing images as opposed to creating art. However, both least important vertices and stochastic processes are relevant in creating artwork. For instance, filtering out less important vertices is one approach to sparsifying the image point cloud. In addition, the point cloud can be generated using a stochastic process as an alternative triangulation method.

Endre Simo also details an image triangulation process in his blog post titled [Delaunay Image Triangulation](https://www.esimov.com/2019/04/image-triangulation-in-go). While both Simo's algorithm and our algorithm use Sobel edge detection and Delaunay triangulation, the two processes were developed independently without reference. Simo's method does not include a density reduction parameter or sharpening step and retains the vertex output by edge detection. Instead, similar edges are removed to clean up the appearance.

Other algorithms include those described by [Lawonn and G&uuml;nther (2019)](https://onlinelibrary.wiley.com/doi/abs/10.1111/cgf.13526) and [Onoja and Aboiyar (2020)](https://www.researchgate.net/publication/343188422_Digital_Image_Segmentation_Using_Delaunay_Triangulation_Algorithm).

## Installation
In order to run the program, download imageTriangulation.ipynb and open it in a code editor such as Visual Studio code. Ensure that `python` as well as the following dependencies are installed:
- math
- matplotlib
- numpy
- os
- PIL
- random
- scipy

The command line interface includes several options. 
1. `-d` Set density reduction parameter
2. `-f` Set file path to desired image
3. `-g` Set file name of the triangulated image
4. `-s` Save triangulated image to triangulatedImages folder with file name designated by `-g`
5. `-t` Set threshold parameter
Note that the optimal `threshold` and `densityReduction` parameters vary depending on the image, but a general guideline is to use lower thresholds for more detailed images. In order to run the program, use the Terminal to navigate to the directory where the project is stored.

```cd file_path/ImageTriangulation/```

Run

```python imageTriangulation.py```

to triangulate the image using the command line options as needed. For example:

```python imageTriangulation.py -d 50 -g finalImage.png -s -t 60```

Once the window displays the uncolored triangulation, close the window to view the final result.

## Included Folders and Files
The originalImages folder contains sample images. In order to use them, replace the string `waterLily.jpeg` with the name of the desired image. Any additional images uploaded to the originalImages folder may also be used.

The `triangulatedImages` folder contains the triangulated versions of the images in the originalImages folder for reference.

`imageTriangulation.py` contains the Python script for creating an image triangulation with vertices chosen with Sobel edge detection. The commented out code randomly generates final vertices instead of using Sobel edge detection.

## Algorithm
The algorithm consists of five steps:
1. Convert to Grayscale
2. Sharpen Image
3. Apply Sobel Operator
4. Triangulate Points
5. Color in Triangles

![Original image](/readmeImages/waterLily_orig.jpg)

__Figure 1__ Original image

Before the algorithm begins, we input the original image (all images taken by us) as well as set the threshold value and density reduction parameter to determine the total number of triangles. The threshold value must be between 0 and 255, and the density reduction parameter must be greater than or equal to 1. Figure 1 displays an example image. The threshold value is set to 50, and the density reduction parameter is set to 60.

### 1. Convert to Grayscale
![Grayscale image](/readmeImages/waterLily_grey.jpg)

__Figure 2__ Grayscale image.

The first step is to convert the image to grayscale so that image processing operators can be applied in the next two steps. For each pixel in the image, the rgb value can be inserted into the following equation to find the output grayscale value ([Pham (2022)](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9783180)):
$$c=0.299r+0.587g+0.114b$$
$$rgb=(c,c,c)$$
Notice that the defining feature of a gray color is $r=g=b$. This number is then rounded to the nearest integer to produce a valid rgb value. For example, if a pixel has $rgb=(100,180,255)$, inputting $rgb$ into the grayscale equation yields a final value of $(165,165,165)$. After iterating over each pixel, Figure 2 displays the output grayscale image.

### 2. Sharpen Image
![Sharpened image](/readmeImages/waterLily_sharpened.jpg)

__Figure 3__ Sharpened image.

The second step is to sharpen the image using a $3\times3$ kernel in order to more clearly define the edges in the image.
```math
L_1=\begin{bmatrix} 0 & -1 & 0 \\ -1 & 5 & -1 \\ 0 & -1 & 0 \end{bmatrix} \\
```
![Image convolution process for x-direction](/readmeImages/convolution.png)

__Figure 4__ Image convolution process.

Figure 4 demonstrates the image convolution process. To perform the convolution, the kernel is overlaid on each pixel in the image. The values in $L_1$ are multiplied by their corresponding values in the overlay region then summed in a method similar to the dot product. The output 
is equal to $H_{xy}$.
$$H_{xy}=\sum_{i=1}^9 I_iL_{1,i}$$
where $H_i$ is the *i*th value in kernel $L_1$ and $P_i$ is the *i*th pixel in the overlay region. Therefore, for the pixel shown in pink, $H_{xy}=-b-d+5e-f-h$.

The sharpened image is displayed in Figure 3. The primary difference between the grayscale and sharpened images is the definition of edges. The boundaries between each of the petals, for instance, become much sharper.

### 3. Apply Sobel Operator
![Image after Sobel operator is applied](/readmeImages/waterLily_sobel.jpg)

__Figure 5__ Image after Sobel processing.

The third step is to apply the Sobel operator, which utilizes an image convolution process with the following x and y kernels ([Tian (2021)](https://www.mdpi.com/2079-9292/10/6/655)).
```math
G_x=\begin{bmatrix} 1 & 0 & -1 \\ 2 & 0 & -2 \\ 1 & 0 & -1 \end{bmatrix} \\
G_y=\begin{bmatrix} 1 & 2 & 1 \\ 0 & 0 & 0 \\ -1 & -2 & -1 \end{bmatrix}
```
The x kernel whitens pixels to the left and right of each pixel, while the y kernel whitens pixels above and below each pixel. As a result, the Sobel operator picks out the edges in the image and sets their grayscale value according to their definition, with 255 being more defined. As a result, the image displays the skeleton of the original image, similar to an x-ray in appearance. Figure 5 shows the image after the Sobel operator is applied.

The vertices in the point cloud come from the set of pixels that meet the threshold value. If a pixel is part of a well-defined edge, the rgb value will be closer to white and fulfill the threshold. Less important points that are not sufficiently white, on the other hand, are filtered out.

### 4. Triangulate Points
![Triangulation of image point cloud](/readmeImages/waterLily_triangulation.png)

__Figure 6__ Triangulation of image point cloud after density reduction.

The fourth step is to triangulate the point cloud. Even with a threshold value, though, the points are still too densely packed to create a visually appealing image. If S is the point cloud, `len(S)/densityReduction` points can be sampled from $S$ to reduce the density. The Delaunay triangulation of the final point cloud is then calculated using `scipy.spatial.Delaunay`. Figure 6 shows the uncolored triangulation of the image.

### 5. Color in Triangles
![Final triangulated image](/readmeImages/waterLily_final.png)

__Figure 7__ Final triangulated image after coloring in triangles.

The fifth and final step is to color in the triangles. For each triangle, we calculate centroid $(x,y)$ as the average of the triangle's vertices and round to the nearest integer. The final color of the triangle is equal to the rgb value at pixel $(x,y)$ in the original image. Figure 7 depicts the final image triangulation.

## Varying Triangulation Parameters
The two varying parameters in the algorithm are the threshold value and density reduction parameter.

### Varying Thresholds
![t=25 triangulation](/readmeImages/waterLily_t25_triangulation.png) | ![t=25](/readmeImages/waterLily_t25.png)
:-------------------------:|:-------------------------:
![t=50 triangulation](/readmeImages/waterLily_triangulation.png) | ![t=50](/readmeImages/waterLily_final.png)
:-------------------------:|:-------------------------:
![t=75 triangulation](/readmeImages/waterLily_t75_triangulation.png) | ![t=75](/readmeImages/waterLily_t75.png)
__Figure 8__ Point cloud triangulation and final image triangulation for thresholds of 25, 50, and 75.

The threshold value is directly related to the number of vertices in the triangulation. As Figure 8 shows, the number of vertices and triangles decreases as the threshold increases.

### Varying Density
![d=35 triangulation](/readmeImages/waterLily_t25_triangulation.png) | ![d=35](/readmeImages/waterLily_t25.png)
:-------------------------:|:-------------------------:
![d=60 triangulation](/readmeImages/waterLily_triangulation.png) | ![d=60](/readmeImages/waterLily_final.png)
:-------------------------:|:-------------------------:
![d=85 triangulation](/readmeImages/waterLily_t75_triangulation.png) | ![d=85](/readmeImages/waterLily_t75.png)
__Figure 9__ Point cloud triangulation and final image triangulation for density reductions of 35, 60, and 85.

Changing the density reduction does not significantly alter the appearance of the final image triangulation. The image in the leftmost panel of Figure 9, though, demonstrates the extent to which density reduction declutters the points as opposed to changing the threshold. As a result, the main purpose of density reduction is to decrease run time and avoid clusters of very small triangles.

### Ramdomized Point Cloud
![Triangulation for random point cloud](/readmeImages/random.png) | ![Triangulated image using a randomized point cloud](/readmeImages/randomTriangulation.png)

__Figure 10__ Point cloud triangulation and final image triangulation for a randomized point cloud.

If we use random points as the vertices for the triangulation, the integrity of the image is lost. Figure 10, for example, shows the image triangulation using 1000 randomly generated points, which is slightly less than the number of vertices that the edge detection method finds. Many of the features are lost, and the image becomes garbled. By using edge detection, though, we can reduce the number of points needed to make a recognizable image and preserve the underlying skeleton.

## Conclusion
While the algorithm we outline successfully triangulates any image, the ideal threshold value and density reduction parameter are subjective. If a user desires a more abstract image, a higher threshold value, higher density reduction parameter, or randomized point cloud is suitable. However, if a user is aspiring for a triangulated image closer to the original image, the opposite holds true.

There are multiple future directions for this algorithm. The first is to consider the dual graph of the Delaunay triangulation. Each Voronoi region would then be colored accordingly instead of each triangle. The output would be more similar to a mosaic and could be considered a separate form of art. In addition, a website that includes a drag and drop box for image upload as well as adjustable parameters could make the program more user-friendly and interactive. Since the website would be coded in HTML, CSS, and JavaScript, `imageTriangulation.py` would need translation from Python. Each of these extensions could significantly improve user experience.

## References
Lawonn, K., G&uuml;nther, T., "Stylized Image Triangulation," *Computer Graphics Forum*, 2019.

Marwood, D., Massimino, M., Covell, M., Baluja, S., "Representing Images in 200 Bytes: Compression via Triangulation," *IEEE ICIP*, 2018.

Onoja, G., Aboiyar, P., "Digital Image Segmentation Using Delaunay Triangulation Algorithm," *Nigerian Annals of Pure and Applied Sciences*, vol. 3, pp. 268-283, 2020.

Pham, T., "Kriging-Weighted Laplacian Kernels for Grayscale Image Sharpening," *IEEE*, vol. 10, 2022.

Simo, E., "Delaunay Image Triangulation," 2019.

Tian, R., Sun, G., Liu, X., Zheng, B., "Sobel Edge Detection Based on Weighted Nuclear Norm Minimization Image Denoising," *Electronics*, vol. 10, no. 6, 2021.