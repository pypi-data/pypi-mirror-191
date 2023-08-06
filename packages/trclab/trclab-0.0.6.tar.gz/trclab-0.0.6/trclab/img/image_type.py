from enum import Enum, unique

@unique
class ImageType(Enum):
    DICOM = "dcm"
    NII = "nii"
    JPEG = "jpg"
    PNG = "png"
    TIFF = "tiff"
    BMP = "bmp"
