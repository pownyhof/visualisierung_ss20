from config import Config


# values according to lte-anbieter.info/technik/asu.php
# dbm of LTE as RSRP
def get_color_for_gsm(dbm_value):
    if dbm_value > -61:
        return Config.dark_green
    if -61 >= dbm_value > -83:
        return Config.green
    if -83 >= dbm_value > -93:
        return Config.orange
    if -93 >= dbm_value > -103:
        return Config.dark_orange
    if -103 >= dbm_value > -109:
        return Config.red
    if -109 >= dbm_value > -114:
        return Config.dark_red


def get_color_for_lte(dbm_value):
    if dbm_value > -70:
        return Config.dark_green
    elif -70 >= dbm_value > -93:
        return Config.green
    elif -93 >= dbm_value > -100:
        return Config.yellow
    elif -100 >= dbm_value > -110:
        return Config.orange
    elif -110 >= dbm_value > -125:
        return Config.dark_orange
    elif -125 >= dbm_value > -131:
        return Config.red
    elif -131 >= dbm_value > -138:
        return Config.dark_red


def get_color_for_umts(dbm_value):
    if dbm_value > -70:
        return Config.dark_green
    if -70 >= dbm_value > -86:
        return Config.green
    if -86 >= dbm_value > -96:
        return Config.orange
    if -96 >= dbm_value > -106:
        return Config.dark_orange
    if -106 >= dbm_value > -112:
        return Config.red
    if -112 >= dbm_value > -117:
        return Config.dark_red


class ColorHelper(object):

    def get_function(self):
        if self.mobile_network_type == Config.lte:
            return get_color_for_lte
        elif self.mobile_network_type == Config.umts:
            return get_color_for_umts
        elif self.mobile_network_type == Config.gsm:
            return get_color_for_gsm

    def __init__(self, mobile_network_type):
        self.mobile_network_type = mobile_network_type
        self.color_function = self.get_function()

    def get_color(self, dbm_value):
        return self.color_function(dbm_value)
