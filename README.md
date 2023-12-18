# ImageTriangulation
## Abstract
While triangulating an image is a relatively simple process, difficulties arise when determining which vertices to include such that the output image remains recognizable and visually pleasing. Here, we develop an image triangulation algorithm in Python that utilizes Sobel edge detection and point cloud sparsification to determine final vertices for Delaunay triangulation. We find that the algorithm successfully triangulates all images. However, the algorithm does not produce consistent results across all images, and the edge detection threshold parameter and sparsification parameter must be varied according to original image detail.

## Introduction
Image triangulation creates an abstract representation of an image as a form of art, which can be defined by four primary principles. The output image must divide the original image into a set of non-overlapping triangles, simplify the original image, approximate original image features as triangles, and retain the integrity of the original image.

There are several existing algorithms to perform image triangulation. [Marwood et. al. (2018)](https://arxiv.org/pdf/1809.02257.pdf) discuss a greedy algorithm that calculates a least important vertex as well as a stochastic process that mutates vertices according to a probability distribution. The primary goal of the algorithm is to compress images as opposed to create art. However, both least important vertices and stochastic processes are relavent in creating artwork. For instance, filtering out less important vertex is one approach to sparsifying the image point cloud. In addition, the point cloud can be generated using a stochastic process as an alternative triangulation method.

Endre Simo also details an image triangulation process in his blog post titled [Delaunay Image Triangulation](https://www.esimov.com/2019/04/image-triangulation-in-go). While both Simo's algorithm and our algorithm use Sobel edge detection and Delaunay triangulation, the two processes were devloped independently without reference. Simo's method does not include a density reduction parameter or sharpening step and retains the vertices output by edge detection. Instead, similar edges are removed to clean up the appearance.

## Installation
In order to run the program, download imageTriangulation.ipynb and open in a code editor such as Visual Studio code. Ensure that `python` as well as the following dependencies are installed:
- math
- matplotlib
- numpy
- os
- PIL
- random
- scipy

To select which image is triangulated, replace the string `image_path` with the file path for the desired image. The optimal `threshold` and `densityReduction` parameters vary depending on the image, but a general guideline is to use lower thresholds for more detailed images. In order to run the program, use the Terminal navigate to the directory where the project is stored.

```cd file_path/ImageTriangulation/```

Run

```python imageTriangulation.py```

to triangulate the image. Once the window displays the uncolored triangulation, close the window to view the final result.

Run

```python delaunayTriangulation.py```

to create a randomized Delaunay triangulation.

## Included Folders and Files
The originalImages folder contains sample images. In order to use them, replace the string `tajMahal.jpg` with the name of the desired image.

The triangulatedImages folder contains the triangulated versions of the images in the originalImages folder for reference.

imageTriangulation.ipynb contains the Python script for creating an image triangulation with vertices chosen with Sobel edge detection. The commented out code randomly generates final vertices instead of using Sobel edge detection.

delaunayTriangulation.py contains a Python script for determining the Delaunay triangulation for a randomized point cloud. Due to time constraints, the algorithm currently only works for relatively sparse point clouds. The algorithm is loosely based off of the pseudocode provided by [Mount 2020](https://www.cs.umd.edu/class/spring2020/cmsc754/Lects/lect13-delaun-alg.pdf).

## Algorithm
The algorithm consists of six steps:
1. Set Initial Values
2. Convert to Grayscale
3. Sharpen Image
4. Apply Sobel Operator
5. Triangulate Points
6. Color in Triangles

### 1. Set Initial Values
![Original image](/readmeImages/tajMahal_orig.jpg)
__Figure 1__ Original image

The first step is to input the original image as well as set the threshold value and density reduction parameter to determine the total number of triangles. The threshold value must be between 0 and 255, and the density reduction parameter must be greater than or equal to 1. Figure 1 displays an image of the Taj Mahal as an example. The threshold value is set to 50, and the density reduction parameter is set to 20.

### 2. Convert to Grayscale
![Grayscale image](/readmeImages/tajMahal_grey.jpg)
__Figure 2__ Grayscale image.

The second step is to convert the image to grayscale so that image processing operators can be applied in the next two steps. For each pixel in the image, the rgb value can be inserted into the following equation to find the output grayscale value ([Pham 2022](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9783180)):
$$c=0.299r+0.587g+0.114b$$
$$rgb=(c,c,c)$$
Notice that the defining feature of a gray color is $r=g=b$. This number is then rounded to the nearest integer to produce a valid rgb value. For example, Figure 3 shows the conversion of blue to gray. 
![Blue conversion to gray](/readmeImages/blueToGrey.png)
__Figure 3__ Blue to gray using the grayscale equation.

The blue color has rgb values (100, 180, 255), and the output value rounded to the nearest integer is (165, 165, 165).

After iterating over each pixel, Figure 2 displays the output grayscale image.

### 3. Sharpen Image
![Sharpened image](/readmeImages/tajMahal_sharpened.jpg)
__Figure 4__ Sharpened image.

The third step is to sharpen the image using a two-directional sharpening kernel in order to more clearly define the edges in the image. The sharpening kernel includes two separate kernels with one for the x-direction and the other for the y-direction. In order to sharpen the image evenly in both directions, $H_1=H_2$. The value $\alpha$ controls the degree of sharpening. Here, we use 4, though 1 is also a standard value.
$$H_1=\begin{matrix}0 & -1 & 0 \\-1 & \alpha + 4 & -1 \\0 & -1 & 0 \\\end{matrix}$$
$$H_2=\begin{matrix}0 & -1 & 0 \\-1 & \alpha + 4 & -1 \\0 & -1 & 0 \\\end{matrix}$$

![Image convolution process for x-direction](/readmeImages/convolution.png)
__Figure 5__ Image convolution process.

Figure 5 demonstrates the image convolution process for the x-direction. To perform the convolution, the kernel is overlaid on each pixel in the image. The values in the $H_1$ are multiplied by their corresponding values in the overlay region then summed in a method similar to the dot product. The output 
is equal to $H_x$. Because we are using a two-directional kernel, the same process must repeated with $H_2$.
$$H_x=\sum_{i=1}^9 H_{1,i}P_i$$
$$H_y=\sum_{i=1}^9 H_{2,j}P_j$$
where $H_{1,i}$ is the $i$th value in the $H_1$ kernel, $H_{2,j}$ is the $i$th value in the $H_2$ kernel, and $P_i$ is the $i$th pixel in the overlay region.

The final grayscale value for the central pixel in the overlay region is calculated as follows:
$$H=\sqrt{H_x^2+H_y^2}$$
The sharpened image is displayed im Figure 4. The primary difference between the grayscale and sharpened images is the definition of edges. The boundary between the trees and the sky, for instance, becomes much sharper.

### 4. Apply Sobel Operator
![Image after Sobel operator is applied](/readmeImages/tajMahal_sobel.jpg)
__Figure 6__ Image after Sobel processing.

The fourth step is to apply the Sobel operator. Like the sharpening kernel, the Sobel operator uses image convolution with the following x and y kernels ([Tian 2021](https://www.mdpi.com/2079-9292/10/6/655)).
$$G_x=\begin{matrix}1 & 0 & -1 \\2 & 0 & -2 \\1 & 0 & -1 \\\end{matrix}$$
$$G_y=\begin{matrix}1 & 2 & 1 \\0 & 0 & 0 \\-1 & -2 & -1 \\\end{matrix}$$
The Sobel operator picks out the edges in the image and sets their grayscale value according to their definition, with 255 being more defined. As a result, the image displays the skeleton of the original image, similar to an x-ray in appearance. Figure 6 shows the image after the Sobel operator is applied.

The vertices in the point cloud come from the set of pixels that meet the threshold value. If a pixel is part of a well-defined edge, the rgb value will be closer to white and fulfill the threshold. Less important points that are not sufficiently white, on the other hand, are filtered out. 

### 5. Triangulate Points
![Triangulation of image point cloud](/readmeImages/tajMahal_triangulation.png)
__Figure 7__ Triangulation of image point cloud after density reduction.

The fifth step is to triangulate the point cloud. Even with a threshold value, though, the points are still too densely packed to create a visually appealing image. If S is the point cloud, `len(S)/densityReduction` points can be sampled from $S$ to reduce the density. The Delaunay triangulation of the final point cloud is then calculated using `scipy.spatial.Delaunay`. Figure 7 shows the uncolored triangulation of the image.

### 6. Color in Triangles
![Final triangulated image](/readmeImages/tajMahal_final.png)
__Figure 8__ Final triangulated image after coloring in triangles.

The sixth and final step is to color in the triangles. For each triangle, we calcuate centroid $(x,y)$ and round to the nearest integer. The final color of the triangle is equal to the rgb value at pixel $(x,y)$ in the original image. Figure 8 depicts the final image triangulation.

## Varying Triangulation Parameters
The two varying parameters in the algorithm are the threshold value and density reduction parameter.

### Varying Thresholds
![Image triangulation for varying thresholds](/readmeImages/thresholdVariation.png)
__Figure 9__ Point cloud triangulation and final image triangulation for thresholds of 25, 50, and 75.

The threshold value is directly related to the number of vertices in the triangulation. As Figure 9 shows, the number of vertices and triangles decreases as the threshold increases.

### Varying Density
![Image triangulation for varying point cloud densities](/readmeImages/densityVariation.png)
__Figure 10__ Point cloud triangulation and final image triangulation for density reductions of 1, 20, and 40.

Changing the density reduction does not significantly alter the appearance of the final image trianglulation compared to varying the threshold. In other words, the output images in Figure 9 do not look very different from the ones in Figure 10. The image in the leftmost panel in Figure 10, though, demonstrates the extent to which density reduction declutters the points. As a result, the main purpose of density reduction is to decrease run time and avoid clusters of very small triangles.

### Ramdomized Point Cloud
![Image triangulation using a random point cloud](/readmeImages/densityVariation.png)
__Figure 11__ Point cloud triangulation and final image triangulation for a randomized point cloud.

If we use random points as the vertices for the triangulation, the integrity of the image is lost. The image becomes quite unrecognizable. Figure 11, for example, shows the image triangulation using 1200 randomly generated points, which is slightly more than the number of vertices that the edge detection method finds. Many of the features are lost, and the image becomes garbled. By using edge detection, though, we can reduce the number of points needed to make a recognizable image and preserve the underlying skeleton.

## Conclusion
While the algorithm we outline successfully triangulates any image, the ideal threshold value and density reduction parameter are subjective. If a user desires a more abstract image, a higher threshold value, higher density reduction parameter, or randomized point cloud is suitable. However, if a user is aspiring for a triangulated image closer to the original image, the opposite holds true.

There are multiple future directions for this algorithm. The first is to consider the dual graph of the Delaunay triangulation. Each Voronoi region would then be colored accordingly instead of each triangle. The output would be more similar to a mosaic and could be considered a separate form of art. Another direction is to debug and implement `delaunayTriangulation.py` for use in `imageTriangulation.py`. Due to time constraints, there are still several errors in the code that arise with dense point clouds. Finally, a website that includes a drag and drop box for image upload as well as adjustable parameters could make the program more user-friendly and interactive. Since the website would be coded in HTML, CSS, and JavaScript, both `delaunayTriangulation.py` and `imageTriangulation.py` would need translation from Python. Each of these extensions could significantly improve user experience.

## References
Marwood, D., Massimino, M., Covell, M., Baluja, S., "Representing Images in 200 Bytes: Compression via Triangulation," IEEE ICIP, 2018.

Mount, D., "CMSC 754: Lecture 13 - Delaunay Triangulations: Incremental Construction," 2020.

Pham, T., "Kriging-Weighted Laplacian Kernels for Grayscale Image Sharpening," IEEE, vol. 10, 2022.

Simo, E., "Delaunay Image Triangulation," 2019.

Tian, R., Sun, G., Liu, X., Zheng, B., "Sobel Edge Detection Based on Weighted Nuclear Norm Minimization Image Denoising," Electronics, vol. 10, no. 6, 2021.