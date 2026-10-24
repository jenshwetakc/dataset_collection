import sys
from pathlib import Path
if __package__ in (None,''):sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from social_media.zoom.renderers.runner import cli
if __name__=='__main__':cli('join')
