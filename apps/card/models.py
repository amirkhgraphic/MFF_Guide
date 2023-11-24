import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models import Model, CharField, TextField, ImageField, URLField
from Scraper_files.scraper_config import DRIVER_PATH, BASE_URL, CARD_START, CARD_END, CARD_STEP, CARD_XPATH
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep


class Card(Model):
    name = CharField(max_length=128)
    type = CharField(max_length=128)
    stat_1 = TextField()
    stat_2 = TextField()
    stat_3 = TextField()
    stat_4 = TextField()
    stat_5 = TextField()
    stat_6 = TextField()
    image = ImageField(blank=True, null=True, upload_to='card/')
    image_url = URLField(blank=True, null=True)

    @classmethod
    def scrape(cls):
        Card.objects.all().delete()

        service = webdriver.ChromeService(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(service=service)
        driver.get(f'{BASE_URL}/cards')

        for num in range(CARD_START, CARD_END + 1, CARD_STEP):
            sleep(1)
            driver.implicitly_wait(10000)

            card = driver.find_element(By.XPATH, CARD_XPATH.replace("###", f"{num}"))
            trs = card.find_elements(By.TAG_NAME, "tr")

            icon = card.find_element(By.TAG_NAME, "img")
            icon = BASE_URL + icon.get_attribute("data-src")

            name = card.find_element(By.TAG_NAME, "h3").get_attribute("innerHTML")

            _type = trs[0].find_elements(By.TAG_NAME, "td")[1].get_attribute("innerHTML")

            stat_1 = trs[1].find_elements(By.TAG_NAME, "td")[1].get_attribute("innerHTML")
            stat_2 = trs[2].find_elements(By.TAG_NAME, "td")[1].get_attribute("innerHTML")
            stat_3 = trs[3].find_elements(By.TAG_NAME, "td")[1].get_attribute("innerHTML")
            stat_4 = trs[4].find_elements(By.TAG_NAME, "td")[1].get_attribute("innerHTML")
            stat_5 = trs[5].find_elements(By.TAG_NAME, "td")[1].get_attribute("innerHTML")
            stat_6 = trs[6].find_elements(By.TAG_NAME, "td")[1].get_attribute("innerHTML")

            """Save To Database"""
            print(name, _type, icon)
            card = Card(name=name, type=_type, image_url=icon, stat_1=stat_1, stat_2=stat_2,
                        stat_3=stat_3, stat_4=stat_4, stat_5=stat_5, stat_6=stat_6)
            card.save()

        driver.close()

    def save(self, *args, **kwargs):
        if not self.image and self.image_url:
            existing_image = Card.objects.filter(image_url=self.image_url).first()

            if existing_image:
                self.image = existing_image.image
            else:
                response = requests.get(self.image_url)
                if response.status_code == 200:
                    img_temp = NamedTemporaryFile()
                    img_temp.write(response.content)
                    img_temp.flush()
                    self.image.save(f"{self.name}.jpg", File(img_temp), save=True)

        super().save(*args, **kwargs)
