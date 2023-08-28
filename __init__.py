import sys, os
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
from stashnodes import *

NODE_CLASS_MAPPINGS = { "Image Stash Controller" : ImageStashController,
                        "Image Stash" : ImageStash,
                        "Image Unstash" : ImageUnstash,
                        "Image Unstash All" : ImageUnstashAll }

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']