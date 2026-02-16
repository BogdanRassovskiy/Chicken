from django.db import models


class Category(models.Model):
    cat_id = models.TextField(blank=True, null=True)
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    name_uz = models.TextField(blank=True, null=True)
    work = models.TextField(blank=True, null=True)
    img_have = models.TextField(blank=True, null=True)
    img = models.BinaryField(blank=True, null=True, editable=True)

    class Meta:
        managed = False
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name or self.name_uz or self.id


class Product(models.Model):
    cat_id = models.TextField(blank=True, null=True)
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    name_uz = models.TextField(blank=True, null=True)
    work = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    rev = models.TextField(blank=True, null=True)
    rev_uz = models.TextField(blank=True, null=True)
    img_have = models.TextField(blank=True, null=True)
    img = models.BinaryField(blank=True, null=True, editable=True)

    class Meta:
        managed = False
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        if not self.id:
            existing_ids = self.__class__.objects.values_list('id', flat=True)
            max_numeric_id = 0
            for existing_id in existing_ids:
                try:
                    numeric_id = int(existing_id)
                except (TypeError, ValueError):
                    continue
                if numeric_id > max_numeric_id:
                    max_numeric_id = numeric_id

            next_id = str(max_numeric_id + 1)
            while self.__class__.objects.filter(id=next_id).exists():
                next_id = str(int(next_id) + 1)
            self.id = next_id

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or self.name_uz or self.id
