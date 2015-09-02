"""djang-filer config for harshp.com

"""

"""For easy_thumbnails to support retina displays (recent MacBooks, iOS)"""
THUMBNAIL_HIGH_RESOLUTION = True

"""enable automatic subject location aware cropping of images"""
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    # 'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
