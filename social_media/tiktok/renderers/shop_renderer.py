from pathlib import Path
import sys
if __package__ in (None, ''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from social_media.tiktok.renderers.runner import cli
if __name__=='__main__':cli('shop')
