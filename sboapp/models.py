# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each OneToOneField has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Serum(models.Model):
    local_sample_id = models.SmallIntegerField()
    site = models.OneToOneField('Site',on_delete=models.PROTECT)
    coll_num = models.SmallIntegerField()
    sample_id = models.CharField(primary_key=True, max_length=8)
    birth_year = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    age_min = models.DecimalField(max_digits=5, decimal_places=2)
    age_max = models.DecimalField(max_digits=5, decimal_places=2)
    gender_1ismale_value = models.PositiveIntegerField()
    coll_date = models.CharField(max_length=10)
    day_value = models.IntegerField()
    month_value = models.IntegerField()
    year = models.IntegerField()
    ward = models.OneToOneField('Ward',on_delete=models.PROTECT)

    class Meta:
        db_table = 'Serum'

    def __str__ (self):
        #Method used to display a serum object
        return "Sample_ID : {}".format(self.sample_id)



class Site(models.Model):
    site_id = models.CharField(primary_key=True, max_length=2)
    site_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'Site'

    def __str__ (self):
        return "{}".format(self.site_id)


class Ward(models.Model):
    ward_id = models.IntegerField(primary_key=True)
    ward_name = models.CharField(max_length=40)
    khoa = models.CharField(max_length=70)

    class Meta:
        db_table = 'Ward'
    def __str__ (self):
        return "{}".format(self.ward_id)

class Freezer(models.Model):
    study_code = models.CharField(max_length=10, blank=True, null=True)
    sample = models.OneToOneField('Serum',on_delete=models.PROTECT, primary_key=True)
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
        return "sample id :{}, freezer section name :{}".format(self.sample_id, self.freezer_section_name)

class Elisa(models.Model):
    result_id = models.CharField(primary_key=True, max_length=25)
    pathogen = models.CharField(max_length=25)
    sample = models.OneToOneField('Serum',on_delete=models.PROTECT)
    elisa_day = models.IntegerField()
    elisa_month = models.IntegerField()
    elisa_year = models.IntegerField()

    class Meta:
        db_table = 'Elisa'

    def __str__ (self):
        #Method used to display an elisa object
        return "Sample_ID : {}, Result_ID : {}".format(self.sample_id, self.result_id)

class Chik_elisa(models.Model):
    result_id = models.OneToOneField('Elisa',on_delete=models.PROTECT, primary_key=True)
    sample_absorbance = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    negative_absorbance = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    cut_off_1_absorbance = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    cut_off_2_absorbance = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    positive_absorbance = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    cut_off = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    novatech_units = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    result = models.IntegerField(null=True)

    class Meta:
        db_table = 'Chik_elisa'

    def __str__ (self):
        #Method used to display a serum object
        return "Result_CHIK_ID : {}".format(self.result_id)

class Dengue_elisa(models.Model):
    result_id = models.OneToOneField('Elisa',on_delete=models.PROTECT, primary_key=True)
    sample_absorbance = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    negative_absorbance = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    positive_absorbance = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    calibrator_1_absorbance = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    calibrator_2_absorbance = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    calibrator_3_absorbance = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    cal_factor = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    cut_off = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    positive_cut_off_ratio = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    dengue_index = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    panbio_unit = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    result = models.IntegerField(null=True)

    class Meta:
        db_table = 'Dengue_elisa'

    def __str__ (self):
        #Method used to display a serum object
        return "Result_DENGUE_ID : {}".format(self.result_id)

class Rickettsia_elisa(models.Model):
    result_id = models.OneToOneField('Elisa',on_delete=models.PROTECT, primary_key=True)
    scrub_typhus = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    typhus = models.DecimalField(max_digits=5, decimal_places=3, null=True)

    class Meta:
        db_table = 'Rickettsia_elisa'

    def __str__ (self):
        #Method used to display a serum object
        return "Result_RICKETTSIA_ID : {}".format(self.result_id)
#
# class Pma(models.Model):
#     ag_array_id = models.CharField(primary_key=True, max_length=25)
#     tray = models.CharField(max_length=5)
#     batch_id = models.CharField(max_length=4)
#     sample = models.OneToOneField('Serum',on_delete=models.PROTECT)
#     start_dilution = models.SmallIntegerField(blank=True, null=True)
#     file_name = models.CharField(max_length=20)
#     processed_day = models.IntegerField()
#     processed_month = models.IntegerField()
#     processed_year = models.IntegerField()
#     batch_sent_id = models.IntegerField()
#     scanned_day = models.IntegerField()
#     scanned_month= models.IntegerField()
#     scanned_year = models.IntegerField()
#     panbio_unit = models.DecimalField(max_digits=5, decimal_places=3, null=True)
#
#
#     class Meta:
#         db_table = 'Pma'
#
#     def __str__ (self):
#         #Method used to display a serum object
#         return "Sample_ID : {}, agArray_ID : {}".format(self.sample_id,self.ag_array_id)
#
# class Pma_result(models.Model):
#     ag_array = models.OneToOneField('Pma',on_delete=models.PROTECT, primary_key=True)
#     chikv_e1_mutant = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#     chikv_e2 = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#     dv1_ns1 = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#     dv2_ns1 = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#     dv3_ns1 = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#     dv4_ns1 = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#     jev_ns1 = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#     slev_ns1 = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#     tbev_ns1 = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#     wnv_ns1 = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#     yfv_ns1 = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#     zikv_brasil_ns1 = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#     zikv_ns1 = models.DecimalField(max_digits=12, decimal_places=10, null=True)
#
#
#     class Meta:
#         db_table = 'Pma_result'
#
#     def __str__ (self):
#         #Method used to display a serum object
#         return "agArray_ID : {}".format(self.ag_array_id)
