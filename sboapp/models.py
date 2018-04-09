# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Serum(models.Model):
    local_sample_id = models.SmallIntegerField()
    site = models.ForeignKey('Site',on_delete=models.PROTECT)
    coll_num = models.SmallIntegerField()
    sample_id = models.CharField(primary_key=True, max_length=8)
    birth_date = models.IntegerField()
    age_min = models.DecimalField(max_digits=5, decimal_places=2)
    age_max = models.DecimalField(max_digits=5, decimal_places=2)
    gender_1ismale_value = models.PositiveIntegerField()
    coll_date = models.CharField(max_length=10)
    day_value = models.IntegerField()
    month_value = models.IntegerField()
    year = models.IntegerField()
    ward = models.ForeignKey('Ward',on_delete=models.PROTECT)
    results_file_id = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'Serum'

    def __str__ (self):
        #Method used to display a serum object
        return "sample id :{}, birth date :{}, gender (1 is male value) :{}".format(self.sample_id, self.birth_date, self.gender_1ismale_value)



class Site(models.Model):
    site_id = models.CharField(primary_key=True, max_length=2)
    site_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'Site'

    def __str__ (self):
        return "{}".format(self.site_name)


class Ward(models.Model):
    ward_id = models.IntegerField(primary_key=True)
    ward_name = models.CharField(max_length=40)
    khoa = models.CharField(max_length=70)

    class Meta:
        db_table = 'Ward'
    def __str__ (self):
        return "{}".format(self.ward_id)

class Freezer(models.Model):
    sample_auto_id = models.CharField(max_length=10, blank=True, null=True)
    study_code = models.CharField(max_length=10, blank=True, null=True)
    site = models.ForeignKey('Site',on_delete=models.PROTECT)
    sample = models.ForeignKey('Serum',on_delete=models.PROTECT, primary_key=True)
    original_age = models.IntegerField()
    gender_1ismale_value = models.PositiveIntegerField()
    coll_date = models.CharField(max_length=10)
    ward = models.ForeignKey('Ward',on_delete=models.PROTECT)
    sample_type = models.CharField(max_length=30, blank=True, null=True)
    aliquot_no = models.PositiveIntegerField(blank=True, null=True)
    volume = models.SmallIntegerField(blank=True, null=True)
    freezer_section_name = models.CharField(max_length=10)
    subdivision_1_position = models.CharField(max_length=1)
    subdivision_2_position = models.IntegerField()
    subdivision_3_position = models.IntegerField()
    subdivision_4_position = models.IntegerField()

    class Meta:
        db_table = 'Freezer'

    def __str__ (self):
        #Method used to display a freezer object
        return "sample id :{}, sample type :{}, freezer section name :{}".format(self.sample_id, self.sample_type, self.freezer_section_name)
