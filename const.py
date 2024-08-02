import os.path

PROJ_ROOT = os.path.dirname(__file__)
SRC = os.path.join(PROJ_ROOT, 'src')
MODEL = os.path.join(SRC, 'models')

UPLOAD_FOLDER = os.path.join(SRC, 'upload')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
