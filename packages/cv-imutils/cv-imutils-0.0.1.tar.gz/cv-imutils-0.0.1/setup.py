from setuptools import setup, find_packages
VERSION = '0.0.1'
DESCRIPTION = 'Lightweight utility package for common computer vision tasks.'
LONG_DESCRIPTION = 'A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization, displaying Matplotlib images, sorting contours, detecting edges, and much more easier with OpenCV and both Python 2.7 and Python 3.'

# Setting up
setup(
    name="cv-imutils",
    version=VERSION,
    author="Emam_ahsour",
    author_email="emam54637@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["opencv-python", "numpy", "mediapipe",
                      "Pillow", "scipy", "imutils", "pdf2image", "pytesseract"],
    keywords=['python', 'cv2-utils', 'tools', 'pycv2',
              'cv2-functions', "cv2-most-used functions"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
