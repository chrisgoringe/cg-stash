import random
import torch
    
class Base_stash:
    CATEGORY = "stash"
    FUNCTION = "func"
    REQUIRED = {}
    OPTIONAL = None
    @classmethod    
    def INPUT_TYPES(s):
        i = {"required": s.REQUIRED}
        if s.OPTIONAL:
            i['optional'] = s.OPTIONAL
        return i

class ImageStash(Base_stash):
    OUTPUT_NODE = True
    PRIORITY = 1
    REQUIRED = { 'id': ("STRING", {"default":"image"}), 'image': ("IMAGE",{}) }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)

    stashed = {}
    previous = {}
    initial = {}

    @classmethod
    def func(cls, id, image:torch.Tensor):
        if ImageStashController.get_stash_setting_keep_latest(id) and id in cls.stashed:
            cls.previous[id] = cls.stashed[id]
        if ImageStashController.get_stash_setting_discard_old(id) and id in cls.previous:
            cls.previous.pop[id]
        cls.stashed[id] = image.clone()
        return (image,) 
    
    @classmethod
    def get_image(cls, id, what):
        if what=='latest' and id in cls.stashed:
            return cls.stashed[id]
        if what=='previous' and id in cls.previous:
            return cls.previous[id]
        return cls.initial[id]

class ImageUnstash(Base_stash):
    REQUIRED = { 'id': ("STRING", {"default":"image"}), 'initial': ("IMAGE",{}) }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)

    @classmethod
    def func(cls, id, initial:torch.Tensor):
        ImageStash.initial[id] = initial.clone()
        return (ImageStash.get_image(id, ImageStashController.get_unstash_setting(id)),)
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return random.random()
    
class ImageUnstashAll(Base_stash):
    REQUIRED = { 'id': ("STRING", {"default":"image"}) }
    OPTIONAL = { 'trigger': ("*", {}) }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    @classmethod
    def func(cls, id, **kwargs):
        return (torch.cat([ImageStash.get_image(id,'initial'), ImageStash.get_image(id,'previous'), ImageStash.get_image(id,'latest')],0), )
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return random.random()

class ImageStashController(Base_stash):
    OUTPUT_NODE = True
    PRIORITY = 2
    REQUIRED = {  'id': ("STRING", {"default":"image"}) , 'setting' : (["New image", "Use latest output", "Reject latest output"],{}) }
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    settings = {}

    def func(self, id, setting):
        ImageStashController.settings[id] = setting
        return ()

    @classmethod
    def get_unstash_setting(cls, id):
        setting = cls.settings[id]
        if setting=="New image":
            return "initial"
        elif setting=="Use latest output":
            return "latest"
        return "previous"
        
    @classmethod
    def get_stash_setting_keep_latest(cls, id):
        return cls.settings[id]=="Use latest output"
        
    @classmethod
    def get_stash_setting_discard_old(cls, id):
        return cls.settings[id]=='New image'