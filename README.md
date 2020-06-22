# MaskGenerator
Easy-to-use python script that can generate black and white mask images from JSON files that are created by [VGG Image Annotator](http://www.robots.ox.ac.uk/~vgg/software/via/via.html).

***Warning***: This script will only work as long as there is only one *type*, or one *dropdown* selection in the VGG app.

## Usage
Initialization requires the json file with annotations, directory of original images, and an ouput directory. **NOTE**: the output directories must already be present, this will not generate the directories.

To use, provide the paths to the required document/directories, and run .create_images()

```python
from MaskGenerator import MaskGenerator

generate_mask_imgs = MaskGenerator("my_annotations.json", "no_mask_imgs/imgs", "mask_imgs/imgs")

#To inspect the dataframe before generating the images
generate_mask_imgs.data

generate_mask_imgs.create_images()
```

or simply run
```python
MaskGenerator("image_annotations.json", "cats/imgs", "bandit_cats/imgs").create_images()
```