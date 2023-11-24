from typing import Final

DRIVER_PATH: Final = "chromedriver.exe"
BASE_URL: Final = "https://thanosvibs.money"

"""CHARACTERS"""
IMG_XPATH_CLICK = "/html/body/main/div[1]/div/div[###]/div/div/div/div[3]/img"
INFO_XPATH = "/html/body/main/div[1]/div/div[###]/div/div/div/div[2]"
MODAL_CONTENTS = "/html/body/main/div[6]/div[1]"
DISMISS_XPATH_CLICK: Final = "/html/body/main/div[6]/div[2]/a[4]"
PAGE_NEXT_XPATH: Final = '//*[@id="rotation"]/div[2]/div[1]/button[7]'
PAGE_LEN: Final = 20
PAGE_NUM: Final = 36
XPATH_START: Final = 3
XPATH_END: Final = 715

"""ARTIFACS"""
ARTIFACT_XPATH = "/html/body/main/div[1]/div/div[###]"
ARTIFACT_PVE = "/html/body/main/div[1]/div/div[###]/div/div/div[2]/div[1]/div/div[1]/div"
ARTIFACT_PVP = "/html/body/main/div[1]/div/div[###]/div/div/div[2]/div[3]/div/div[1]/div"
ARTIFACT_ICON = "/html/body/main/div[1]/div/div[###]/div/div/div[1]/div[5]/img"
ARTIFACT_ID = 1
ARTIFACT_START = 3
ARTIFACT_END = 150
ARTIFACT_NEXT_PAGE = "/html/body/main/div[1]/div/div[2]/div[1]/button[7]"

"""CTPS"""
CTP_XPATH = "/html/body/main/div[1]/div[2]/div[###]"
CTP_ICON = "/html/body/main/div[1]/div[2]/div[###]/div/div/div[1]/div[2]/img"
CTP_NAME_DESCRIPTION = "/html/body/main/div[1]/div[2]/div[###]/div/div/div[1]/div[1]"
CTP_REFORGED_STATS = ["Regular", "Mighty", "Brilliant"]
CTP_START = 1
CTP_END = 13

"""CARDS"""
CARD_XPATH = "/html/body/main/div[###]"
CARD_START = 4
CARD_END = 192
CARD_STEP = 2

