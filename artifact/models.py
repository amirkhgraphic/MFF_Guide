from time import sleep

import requests
from bs4 import BeautifulSoup
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models import Model, CharField, TextField, ImageField, URLField, ForeignKey, CASCADE
from selenium import webdriver
from selenium.webdriver.common.by import By

from character.models import Character
from scraper_config import (BASE_URL, DRIVER_PATH, ARTIFACT_START, ARTIFACT_END, ARTIFACT_XPATH, ARTIFACT_PVE,
                            ARTIFACT_PVP, ARTIFACT_ICON, ARTIFACT_NEXT_PAGE)


class Artifact(Model):
    SCORE = [
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High')
    ]
    name = CharField(max_length=128)
    character = ForeignKey(Character, on_delete=CASCADE, related_name='artifacts')
    exclusive_skill = CharField(max_length=128)
    PvE_score = CharField(max_length=1, choices=SCORE)
    PvP_score = CharField(max_length=1, choices=SCORE)
    rank_3 = TextField()
    rank_4 = TextField()
    rank_5 = TextField()
    rank_6 = TextField()
    image = ImageField(upload_to='artifact/', null=True, blank=True)
    image_url = URLField(null=True, blank=True)

    @classmethod
    def scrape(cls):
        ARTIFACT_ID = 1
        service = webdriver.ChromeService(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(service=service)
        driver.get(f"{BASE_URL}/artifacts")
        sleep(10)

        for num in range(ARTIFACT_START, ARTIFACT_END + 1):

            if (num - 3) % 10 == 0 and num != 3:
                driver.find_element(By.XPATH, ARTIFACT_NEXT_PAGE).click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(10)

            driver.execute_script("arguments[0].scrollIntoView();",
                                  driver.find_element(By.XPATH, ARTIFACT_ICON.replace("###", f"{num}")))

            card = driver.find_element(By.XPATH, ARTIFACT_XPATH.replace("###", f"{num}"))

            character, name, exclusive_skill = [data.get_attribute("innerHTML") for data in
                                                card.find_elements(By.TAG_NAME, "h5")]



            PvE_score = driver.find_element(By.XPATH, ARTIFACT_PVE.replace("###", f"{num}")).get_attribute(
                "data-tooltip")
            PvP_score = driver.find_element(By.XPATH, ARTIFACT_PVP.replace("###", f"{num}")).get_attribute(
                "data-tooltip")

            rank_3 = "\n".join([li.get_attribute("innerHTML").strip('"').lstrip("&emsp;") for li in
                                driver.find_element(By.ID, f"{ARTIFACT_ID}_3").find_elements(By.TAG_NAME, "li")])
            rank_3 = BeautifulSoup(rank_3, "lxml").text

            rank_4 = "\n".join([li.get_attribute("innerHTML").strip('"').lstrip("&emsp;") for li in
                                driver.find_element(By.ID, f"{ARTIFACT_ID}_4").find_elements(By.TAG_NAME, "li")])
            rank_4 = BeautifulSoup(rank_4, "lxml").text

            rank_5 = "\n".join([li.get_attribute("innerHTML").strip('"').lstrip("&emsp;") for li in
                                driver.find_element(By.ID, f"{ARTIFACT_ID}_5").find_elements(By.TAG_NAME, "li")])
            rank_5 = BeautifulSoup(rank_5, "lxml").text

            rank_6 = "\n".join([li.get_attribute("innerHTML").strip('"').lstrip("&emsp;") for li in
                                driver.find_element(By.ID, f"{ARTIFACT_ID}_6").find_elements(By.TAG_NAME, "li")])
            rank_6 = BeautifulSoup(rank_6, "lxml").text

            icon = driver.find_element(By.XPATH, ARTIFACT_ICON.replace("###", f"{num}")).get_attribute("src")

            ARTIFACT_ID += 1

            """Save to Database Table"""
            characters = Character.objects.filter(name=character)
            for ch in characters:
                artifact = Artifact(name=name, character=ch, exclusive_skill=exclusive_skill, PvE_score=PvE_score,
                                    PvP_score=PvP_score, rank_3=rank_3, rank_4=rank_4, rank_5=rank_5, rank_6=rank_6,
                                    image_url=icon)
                artifact.save()

            print(name, character, '---', icon)


    def save(self, *args, **kwargs):
        if not self.image and self.image_url:
            existing_image = Artifact.objects.filter(image_url=self.image_url).first()

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