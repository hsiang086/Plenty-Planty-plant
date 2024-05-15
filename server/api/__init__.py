##############################
# Copyright © hsiang086 2024 #
##############################

class APIs():
    def __init__(self, config: dict):
        self.config = config
        self.system_message = "system"
        self.user_message = "hello how are you"
        self.sd_prompt = " a delicate apple made of opal hung on branch in the early morning light, adorned with glistening dewdrops. in the background beautiful valleys, divine iridescent glowing, opalescent textures, volumetric light, ethereal, sparkling, light inside body, bioluminescence, studio photo, highly detailed, sharp focus, photorealism, photorealism, 8k, best quality, ultra detail:1. 2, hyper detail, hdr, hyper detail, ((universe of stars inside the apple) ) "
        
    def setUserMessage(self, soil_hu, hu):
        self.user_message = f"soil humidity is {soil_hu} and air humidity is {hu} "