# colors
built to select top n most common colors in an image

## usage
drop images to analyzed into directory ./images (currently set up for .jpg files)
requires the file "benchmark_colors.csv" to provide a set of possible colors for output
run in shell: >python colors.py
program will read all images in ./images and create csv file results.csv
showing top n most frequent colors for each image
program defaults to n=3, which may be changed via optional argument
ex: >python colors.py 4 

requirements:
  python 3.8.0
  numpy 1.21.2
  pandas 1.3.3
  Pillow 8.3.2
