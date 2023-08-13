import pathlib
import sys
import numpy as np
from PIL import Image
from pydicom import dcmread



def convert_all_subdirectories(path):
    pathLib_parent = pathlib.Path(path)

    for img_path in pathLib_parent.rglob(f"*.dcm"):
        png_path = img_path.with_suffix('.png')
        if not png_path.exists():
            png = convert_dcm_png(img_path)
            png.save(png_path)
            print("Wrote " + png_path.as_posix())

def convert_dcm_png(path):
    
    im = dcmread(path)

    im = im.pixel_array.astype(float)

    rescaled_image = (np.maximum(im,0)/im.max())*255 # float pixels
    final_image = np.uint8(rescaled_image) # integers pixels

    final_image = Image.fromarray(final_image)

    return final_image

def main():

    if len(sys.argv) != 2:
        print("Usage: python3 dicom-to-png.py path_of_dicom_folder")
        return 0
    else:
        convert_all_subdirectories(sys.argv[1])

if __name__ == "__main__":
    main()
    