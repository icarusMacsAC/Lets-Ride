import pandas as pd
from django.db import models
import main
from googletrans import Translator
import googletrans
from main import art_res
code_to_lang = googletrans.LANGUAGES
lang_to_code = {}
category = []
for key, val in code_to_lang.items():
    lang_to_code[val] = key
    category.append([val, val])
lang_to_code
df_data = list(lang_to_code.keys())
print("dggdg", df_data)


# Create your models here.
df = art_res.df
df_category = list(df.category.unique())
df_category.sort()
genre = []
for ele in df_category:
    genre.append([ele, ele])

genre.append(["all", "all"])

# Create your models here.


class ImageCaption(models.Model):
    # name = models.CharField(max_length=256)
    img = models.ImageField(upload_to='uploads/image', null=True, blank=True)

    def __str__(self):
        return str(main.models.ImageCaption.objects.all()[0].img).split(".")[0].split("/")[-1]


class machine_translation(models.Model):

    # OUTPUT_FORMAT = (
    #     ('transliteration', 'Machine Transliteration'),
    #     ('translation', 'Machine Translation'),
    #     ('both', 'Both')
    # )
    OUTPUT_FORMAT = category

    format = models.CharField(max_length=250, choices=OUTPUT_FORMAT)


class article_finder(models.Model):

    # OUTPUT_FORMAT = (
    #     ('transliteration', 'Machine Transliteration'),
    #     ('translation', 'Machine Translation'),
    #     ('both', 'Both')
    # )
    OUTPUT_FORMAT = genre

    format = models.CharField(max_length=15, choices=OUTPUT_FORMAT)


class signin_data(models.Model):

    username = models.CharField(max_length=250)
    password1 = models.CharField(max_length=250)
    password2 = models.CharField(max_length=250)


class asset_transport_request_model(models.Model):
    src = models.CharField(max_length=250)
    to = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    date_time = models.DateTimeField()
    flexible_timimg = models.BooleanField()
    no_of_assets = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    asset_type = models.CharField(max_length=250)
    asset_sensitivity = models.CharField(max_length=250)
    whom_to_deliver = models.CharField(max_length=250)


class share_travel_information_model(models.Model):
    src = models.CharField(max_length=250)
    to = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    date_time = models.DateTimeField()
    flexible_timimg = models.BooleanField()
    medium = models.CharField(max_length=250)
    no_of_assets = models.CharField(max_length=250)
