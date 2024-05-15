##############################
# Copyright © hsiang086 2024 #
##############################

class LlmAPI():
    def __init__(self, config: dict):
        self.config = config
        self.system_message = "system"
        self.user_message = "hello how are you"
        
    