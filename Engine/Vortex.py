from ursina import *
from .Tool import get_data_from_api
from .Data import color_dict
from datetime import datetime
import sys
from ursina.prefabs.first_person_controller import FirstPersonController


############################### Current Time ###############################
current_time = datetime.now()
current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
############################################################################

############################### Global Data ################################

ChainApi = {
    "Aptos": "https://api.aptos.dev/v1",
    "polygon": "",
    "matic": "",
}
OuputJSON = dict()
#--------------------------------------------------------------------------
TempObjects = list()
TempColors = list()
TempFPS = list()
#--------------------------------------------------------------------------

ApiCheckerUrl = ""

############################################################################

class Vortex:
    def __init__(self, PrivateKey="", Address="", Chain="Aptos", ApiKey=False, **kwargs):
        if ApiKey:
            self.ApiKey = get_data_from_api(ApiCheckerUrl)
        else:
            self.PrivateKey = PrivateKey
            self.Address = Address
            self.Chain = Chain
            self.app = Ursina(title="Vortex", use_ingame_console=True, **kwargs)
            OuputJSON.update({"config": {"PrivateKey": PrivateKey, "Address": Address, "Chain": Chain, "appInstance": self.app}})
            print(OuputJSON)

    def Object(self, **kwargs):
        EntityObject = Entity(**kwargs)
        TempObjects.append({"Objects": {"EntityInstance": EntityObject, "Kwargs": kwargs if kwargs else "No Kwargs are used..!"}})
        print(OuputJSON)
        return EntityObject
    
    def Label(self, **kwargs):
        TextObject = Text(**kwargs)
        TempObjects.append({"Label": {"TextInstance": TextObject, "Kwargs": kwargs if kwargs else "No Kwargs are used..!"}})
        return TextObject
    
    def firstPersonController(self, **kwargs):
        fps = FirstPersonController(**kwargs)
        TempObjects.append({"Label": {"TextInstance": fps, "Kwargs": kwargs if kwargs else "No Kwargs are used..!"}})
        return fps
    
    def color(self, color_input):
        FinalColor = object()
        if isinstance(color_input, str):
            if color_input.startswith('#'):
                try:
                    FinalColor = color.hex(color_input)
                except ValueError:
                    FinalColor = color.white
            else:
                FinalColor = color_dict.get(color_input, color.white)
        elif isinstance(color_input, tuple) and len(color_input) == 3:
            try:
                FinalColor = color.rgb(*color_input)
            except ValueError:
                FinalColor = color.white
        else:
            FinalColor = color.white
        TempColors.append(FinalColor)
        return FinalColor
    
    def UpdateBlock(self):
        global OuputJSON
        OuputJSON.update({"Objects": {"ListOfObjects": TempObjects}})
        OuputJSON.update({"Colors": {"ListOfColors": TempColors}})
    
    def run(self):
        try:
            OuputJSON.update({"EngineStart": {"AppInstance": self.app}})
            OuputJSON.update({"Objects": {"ListOfObjects": TempObjects}})
            OuputJSON.update({"Colors": {"ListOfColors": TempColors}})
            self.app.run()
        except (KeyboardInterrupt, SystemExit):
            print("Game forcefully stopped.")
        finally:
            self.UpdateBlock()
            sys.exit()

