from django.db import models

# Create your models here.
class Result(models.Model):
    '''
    Store/represent the data from one runner at the Chicago Marathon 2023.
    BIB,First Name,Last Name,CTZ,City,State,Gender,Division,
    Place Overall,Place Gender,Place Division,Start TOD,Finish TOD,Finish,HALF1,HALF2
    '''
    # identification
    bib = models.IntegerField()
    first_name = models.TextField()
    last_name = models.TextField()
    ctz = models.TextField()
    city = models.TextField()
    state = models.TextField()

    # gender/division
    gender = models.CharField(max_length=6)
    division = models.CharField(max_length=6)

    # result place
    place_overall = models.IntegerField()
    place_gender = models.IntegerField()
    place_division = models.IntegerField()

    # timing-related
    start_time_of_day = models.TimeField()
    finish_time_of_day = models.TimeField()

    time_finish = models.TimeField()
    time_half1 = models.TimeField()
    time_half2 = models.TimeField()


    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.city}, {self.state}), {self.time_finish}'
    
