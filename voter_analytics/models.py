# File: models.py
# Author: bella918@bu.edu
# Date: 6/16/2025
# Description: Defines the Voter model for the voter_analytics Django app,
#              and provides a utility function to load Voter records from
#              a local CSV file.


from django.db import models

class Voter(models.Model):
    '''
    Represent a single registered voter in Newton, MA.
    '''
    # Basic info
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=200)
    apartment_number = models.CharField(max_length=20, blank=True)
    zip_code = models.CharField(max_length=10)

    # Dates
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()

    # Political info
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)

    # Voting history
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    # Score
    voter_score = models.IntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name} - Precinct {self.precinct_number}'

import csv
from datetime import datetime
from .models import Voter

def load_data():
    '''
    Load data records from newton_voters.csv into the Voter table.
    '''

    filename = '/Users/bellawang/Downloads/newton_voters.csv'
    f = open(filename, newline='', encoding='utf-8')
    reader = csv.DictReader(f)

    count = 0
    for row in reader:
        try:
            voter = Voter(
                last_name=row['Last Name'],
                first_name=row['First Name'],
                street_number=row['Residential Address - Street Number'],
                street_name=row['Residential Address - Street Name'],
                apartment_number=row.get('Residential Address - Apartment Number', ''),
                zip_code=row['Residential Address - Zip Code'],
                date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                party_affiliation=row['Party Affiliation'],
                precinct_number=row['Precinct Number'],

                v20state=row['v20state'].strip().lower() == 'true',
                v21town=row['v21town'].strip().lower() == 'true',
                v21primary=row['v21primary'].strip().lower() == 'true',
                v22general=row['v22general'].strip().lower() == 'true',
                v23town=row['v23town'].strip().lower() == 'true',

                voter_score=int(row['voter_score']),
            )
            voter.save()
            count += 1
            print(f'Created voter: {voter}')
        except Exception as e:
            print(f'Skipped: {row} \nError: {e}')

    print(f'\n✅ Done. Created {count} Voter records.')
