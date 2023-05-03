from django.db import models

import uuid


ltr_or_kg = (('Kg', 'Kg'), ('Liter', 'Liter'))
class product(models.Model):
    product_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4
    )
    category = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    price = models.IntegerField()
    image = models.ImageField(upload_to='prod_img/')
    kg_or_ltr = models.CharField(
        max_length = 5,
        choices = ltr_or_kg,
        default='Kg'
    )

class cart(models.Model):
    product_id = models.CharField(max_length=100, null=False, blank=False)
    user_id = models.CharField(max_length=50)
    product_quentity = models.IntegerField(default=1)
