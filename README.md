# HubbleVision
**Estimating Hubble's constant (H₀) via photometric redshift through a CNN & a visualizer through ManimGL in Python.**

This project was submitted as a final project for Physics 20B - Cosmology: Humanity's Place in the Universe at the University of California, Irvine.

## How To Run

### Clone the Repository
```
git clone https://github.com/sidsun1/HubbleVision.git
cd HubbleVision
```

### Set up a Virtual Environment
Ensure that Python 3.12 is used for the virtual environment.

```
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Run the ```download_sdss_images.py``` Script
Simply click play on the module, or run it with 
```
python -m download_sdss_images.py
```

### Run the Notebook
Click `run all` in the Jupyter notebook interface in the file ```redshift_cnn.ipynb```.

### Run the Manim Animations
Play the video files in the `videos` subdirectory, or run the commands:

```
python -m manimlib hubble_scene.py HubbleIntro -w --uhd
python -m manimlib hubble_scene.py HubbleLawComparison -w --uhd
python -m manimlib hubble_scene.py RedShiftScene -w --uhd
```

## Citations (Tools and References Used)
### Tools
- https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch (Sloan Digital Sky Survey - Data Release 18) [Used for image downloads through SQL queries]
- https://www.tensorflow.org/guide/keras/sequential_model [Tensorflow CNN development docs to calculate Hubble's Constant]
- https://3b1b.github.io/manim/ [Docs for development of python animations on Hubble's Constant + RedShift / The Doppler Effect]
### References
- https://cosmo.nyu.edu/mb144/manyd.html [Used to determine a standardized value for M_r]
- https://academic.oup.com/mnras/article/392/3/1060/1062734 [Also used to find a standard value for magnitude range]
- https://ar5iv.labs.arxiv.org/html/1811.04569 [Used to compare data based on parameters like ra, dec, and magnitudes across different bands]