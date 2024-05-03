from django.db import models

# Create your models here.
class Sponsors(models.Model):
    organisation_name = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    industry = models.CharField(max_length=200)
    main_tier = models.CharField(max_length=200)
    sub_tier = models.CharField(max_length=200)
    date_added = models.CharField(max_length=200)

    def to_dict(self):
        """
        Convert the Sponsors model instance to a dictionary.
        """
        # Create a dictionary to store field-value pairs
        data = {
            'Organisation Name': self.organisation_name,
            'Town': self.town,
            'Industry': self.industry,
            'Main Tier': self.main_tier,
            'Sub Tier': self.sub_tier,
            'Date Added': self.date_added,
        }
        
        return data