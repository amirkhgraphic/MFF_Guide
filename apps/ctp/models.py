from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.db.models import Model, CharField, TextField, ImageField, URLField
from Scraper_files.scraper_config import (BASE_URL, DRIVER_PATH, CTP_REFORGED_STATS, CTP_START, CTP_END, CTP_XPATH, CTP_ICON,
                                          CTP_NAME_DESCRIPTION)
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import requests


class CTP(Model):
    STATUS = [
        ("r", "Regular"),
        ("m", "Mighty"),
        ("b", "Brilliant")
    ]

    name = CharField(max_length=128)
    status = CharField(max_length=1, choices=STATUS)
    description = TextField()
    reforged_description = TextField()
    max_stats = TextField()
    reforged_option_1 = TextField(null=True, blank=True)
    reforged_option_2 = TextField(null=True, blank=True)
    image = ImageField(blank=True, null=True, upload_to="ctp/")
    image_url = URLField(blank=True, null=True)

    @classmethod
    def scrape(cls):
        CTP.objects.all().delete()

        service = webdriver.ChromeService(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(service=service)
        driver.get(f"{BASE_URL}/ctp")
        sleep(5)

        for num in range(CTP_START, CTP_END + 1):
            ctp = driver.find_element(By.XPATH, CTP_XPATH.replace("###", f"{num}"))

            partial_id = ctp.get_attribute("class").split()[-1]

            icon = driver.find_element(By.XPATH, CTP_ICON.replace("###", f"{num}")).get_attribute("src")

            name_desc = driver.find_element(By.XPATH, CTP_NAME_DESCRIPTION.replace("###", f"{num}"))

            name = name_desc.find_element(By.TAG_NAME, "h5").get_attribute("innerHTML")

            description, reforged_description = [paragraph.get_attribute("innerHTML").lstrip("<b>Reforged:</b>").strip()
                                                 for paragraph in name_desc.find_elements(By.TAG_NAME, "p")]

            regular_max = "\n".join(
                [BeautifulSoup(li.get_attribute("innerHTML").replace("<br>", "\n"), "lxml").text for li in
                 ctp.find_element(By.ID, partial_id + "1").find_elements(By.TAG_NAME, "ul")[1].find_elements(
                     By.TAG_NAME, "li")])

            mightys = ctp.find_element(By.ID, partial_id + "2").find_elements(By.TAG_NAME, "ul")
            migthy_max = "\n".join([BeautifulSoup(li.get_attribute("innerHTML").replace("<br>", "\n"), "lxml").text
                                    for li in mightys[1].find_elements(By.TAG_NAME, "li")])
            migthy_option1 = BeautifulSoup(
                mightys[2].find_element(By.TAG_NAME, "li").get_attribute("innerHTML").replace("<br>", "\n"),
                "lxml").text
            migthy_option2 = BeautifulSoup(
                mightys[3].find_element(By.TAG_NAME, "li").get_attribute("innerHTML").replace("<br>", "\n"),
                "lxml").text

            brilliants = ctp.find_element(By.ID, partial_id + "3").find_elements(By.TAG_NAME, "ul")
            brilliant_max = "\n".join([BeautifulSoup(li.get_attribute("innerHTML").replace("<br>", "\n"), "lxml").text
                                       for li in brilliants[1].find_elements(By.TAG_NAME, "li")])
            brilliant_option1 = BeautifulSoup(
                brilliants[2].find_element(By.TAG_NAME, "li").get_attribute("innerHTML").replace("<br>", "\n"),
                "lxml").text
            brilliant_option2 = BeautifulSoup(
                brilliants[3].find_element(By.TAG_NAME, "li").get_attribute("innerHTML").replace("<br>", "\n"),
                "lxml").text

            regular_ctp = CTP(name=name, status=CTP_REFORGED_STATS[0], description=description,
                      reforged_description=reforged_description, max_stats=regular_max, image_url=icon)
            regular_ctp.save()

            mighty_ctp = CTP(name=name, status=CTP_REFORGED_STATS[1], description=description,
                      reforged_description=reforged_description, max_stats=migthy_max,
                      reforged_option_1=migthy_option1, reforged_option_2=migthy_option2, image_url=icon)
            mighty_ctp.save()

            brilliant_ctp = CTP(name=name, status=CTP_REFORGED_STATS[2], description=description,
                      reforged_description=reforged_description, max_stats=brilliant_max,
                      reforged_option_1=brilliant_option1, reforged_option_2=brilliant_option2, image_url=icon)
            brilliant_ctp.save()

            sleep(1)

        driver.close()

    def save(self, *args, **kwargs):
        if not self.image and self.image_url:
            existing_image = CTP.objects.filter(image_url=self.image_url).first()

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
