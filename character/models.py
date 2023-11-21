import requests
from time import sleep
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models import (Model, CharField, TextField, BooleanField,
                              ForeignKey, JSONField, CASCADE, ImageField, URLField)
from ctp.models import CTP
from scraper_config import (DRIVER_PATH, BASE_URL, XPATH_START, XPATH_END, IMG_XPATH_CLICK, INFO_XPATH,
                            DISMISS_XPATH_CLICK, MODAL_CONTENTS)
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Character(Model):
    name = CharField(max_length=128)
    uniform = CharField(max_length=128)
    type = CharField(max_length=32)
    side = CharField(max_length=32)
    allies = CharField(max_length=32)
    gender = CharField(max_length=32)
    advancement = CharField(max_length=256)
    ability = TextField()
    instinct = CharField(max_length=32)
    rotation = JSONField(null=True, blank=True)
    PvE = BooleanField(default=False)
    PvP = BooleanField(default=False)
    Dealer = BooleanField(default=False)
    Leader = BooleanField(default=False)
    Support = BooleanField(default=False)
    leadership = JSONField(null=True)
    support_buff = JSONField(null=True)
    image = ImageField(null=True, blank=True, upload_to='character')
    image_url = URLField(null=True, blank=True)

    @classmethod
    def scrape(cls):
        service = webdriver.ChromeService(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(service=service)
        driver.get(f'{BASE_URL}/rotations')

        """Temporary Configuration"""
        last_page = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div[1]/button[6]')
        last_page.click()
        for _ in range(3):
            pre_page = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div[1]/button[1]')
            pre_page.click()
            sleep(1)
        XPATH_START = 650
        sleep(5)

        for num in range(XPATH_START, XPATH_END + 1):

            driver.implicitly_wait(10)

            if num in range(23, XPATH_END + 1, 20):
                next_btn = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[2]/div[1]/button[7]')
                next_btn.click()
                cnt = 0

            sleep(3)
            info = driver.find_element(By.XPATH, INFO_XPATH.replace("###", f"{num}"))

            h5s = info.find_elements(By.TAG_NAME, "h5")
            name = h5s[0].get_attribute("innerHTML")
            uniform = h5s[1].get_attribute("innerHTML")

            rotations_headers = info.find_elements(By.TAG_NAME, "h6")
            rotations_headers = [h6.get_attribute("innerHTML").strip() for h6 in rotations_headers]

            rotations_data = info.find_elements(By.TAG_NAME, "p")
            rotations_data = [BeautifulSoup(p.get_attribute("innerHTML"), "lxml").text.strip() for p in rotations_data]

            if rotations_data[0].startswith("Rotations(s)"):
                rotations = None
            else:
                rotations = dict(zip(rotations_headers, rotations_data))

            image = driver.find_element(By.XPATH, IMG_XPATH_CLICK.replace("###", f"{num}"))
            icon = BASE_URL + image.get_attribute("data-src")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(image))
            image.click()
            sleep(5)

            modal = driver.find_element(By.XPATH, MODAL_CONTENTS)

            uls = modal.find_elements(By.CLASS_NAME, "char-flex-container")

            h6s = uls[0].find_elements(By.TAG_NAME, "h6")
            type = h6s[0].get_attribute("innerHTML")
            allies = h6s[1].get_attribute("innerHTML")
            gender = h6s[2].get_attribute("innerHTML")
            side = h6s[3].get_attribute("innerHTML")

            abillities_h6s = uls[1].find_elements(By.TAG_NAME, "h6")
            abillities = [h6.get_attribute("innerHTML") for h6 in abillities_h6s]

            advancement_h6s = uls[2].find_elements(By.TAG_NAME, "h6")
            advancement = [h6.get_attribute("innerHTML") for h6 in advancement_h6s]

            instinct = uls[4].find_element(By.TAG_NAME, "h6").get_attribute("innerHTML")

            tiers = {"Leader": False, "Support": False, "Dealer": False, "PvE": False, "PvP": False}
            ctps = []
            leadership = dict()
            support = dict()

            popup = driver.find_element(By.ID, "popup")
            divs = popup.find_elements(By.TAG_NAME, "div")
            sleep(2)
            cnt = 0
            for div in divs:
                id = div.get_attribute("id")

                if id.startswith("support"):
                    sleep(1)
                    cnt += 1
                    cards = div.find_elements(By.CLASS_NAME, "card")

                    for card in cards:

                        header = card.find_element(By.TAG_NAME, "h6").get_attribute("innerHTML")

                        apply_to = card.find_element(By.CSS_SELECTOR, "img")
                        tooltip = apply_to.get_attribute("data-tooltip")
                        if tooltip:
                            apply_to = BeautifulSoup(tooltip, "lxml").text
                        else:
                            apply_to = "All Allies"

                        trs = card.find_elements(By.CSS_SELECTOR, "tbody tr")
                        result = []
                        for tr in trs:
                            tds = tr.find_elements(By.TAG_NAME, "td")
                            effect = tds[1].get_attribute("innerHTML")
                            magnitude = tds[2].get_attribute("innerHTML")

                            if magnitude.startswith("-"):
                                result.append(f"Decrease {effect} by {magnitude}")
                            else:
                                result.append(f"Increase {effect} by {magnitude}")

                        if "Leadership" in header:
                            leadership = {"Applies to": apply_to,
                                          "Effect": "\n".join(result)}
                            continue

                        support[header] = {"Applies to": apply_to,
                                           "Effect": "\n".join(result)}

                if id.startswith("tierlist"):
                    sleep(1)
                    cnt += 1
                    uls = div.find_elements(By.CLASS_NAME, "char-flex-container")

                    tier_h6s = uls[0].find_elements(By.TAG_NAME, "h6")
                    for item in tier_h6s:
                        tiers[item.get_attribute("innerHTML")] = True

                    ctp_h6s = uls[1].find_elements(By.TAG_NAME, "h6")
                    for item in ctp_h6s:
                        ctps.append(item.get_attribute("innerHTML"))

                if cnt == 2:
                    break

            dismiss = driver.find_element(By.XPATH, DISMISS_XPATH_CLICK)
            dismiss.click()

            if not ctps or "None" in ctps[0]:
                ctps = None

            if not leadership:
                leadership = None

            if not support:
                support = None

            print(name, "-", uniform, leadership, support)
            """Add to database"""
            ch = Character(name=name, uniform=uniform, type=type, side=side, allies=allies, gender=gender,
                           ability=abillities, advancement=advancement, instinct=instinct,
                           rotation=rotations, PvE=tiers['PvE'], PvP=tiers['PvP'], Leader=tiers['Leader'],
                           Support=tiers['Support'], Dealer=tiers['Dealer'], image_url=icon, leadership=leadership,
                           support_buff=support)
            ch.save()

            if ctps:
                print(ctps)
                for ctp in ctps:
                    c = ctp.split()
                    if c[0] == "Reforged":
                        opt1 = CTP.objects.filter(name=f"C.T.P. of {c[1]}", status="Mighty").first()
                        opt2 = CTP.objects.filter(name=f"C.T.P. of {c[1]}", status= "Brilliant").first()
                        CharacterCTP(character=ch, custom_gear=opt1).save()
                        CharacterCTP(character=ch, custom_gear=opt2).save()
                    else:
                        opt = CTP.objects.filter(name=f"C.T.P. of {c[0]}", status="Regular").first()
                        CharacterCTP(character=ch, custom_gear=opt).save()


    def save(self, *args, **kwargs):
        if not self.image and self.image_url:
            existing_image = Character.objects.filter(image_url=self.image_url).first()

            if existing_image:
                self.image = existing_image.image
            else:
                response = requests.get(self.image_url)
                if response.status_code == 200:
                    img_temp = NamedTemporaryFile()
                    img_temp.write(response.content)
                    img_temp.flush()
                    self.image.save(f"{self.name}-{self.uniform}.jpg", File(img_temp), save=True)

        super().save(*args, **kwargs)


class CharacterCTP(Model):
    character = ForeignKey(Character, on_delete=CASCADE, related_name='CTPs')
    custom_gear = ForeignKey(CTP, on_delete=CASCADE, related_name='characters')
