import os
import django
import logging
from django.db import transaction, IntegrityError
import csv
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FitnessPro.settings')
#django.setup()

from booking.models import Classes, Weekday, ClassSchedule

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Imports data from CSV files into the database'
    def import_classes(self, csv_file):
        with open(csv_file, newline='', encoding='utf-8') as f:
            with transaction.atomic():
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        class_instance, created = Classes.objects.get_or_create(class_name=row['class_name'])
                        if created:
                            logger.info(f"Added new class: {class_instance.class_name}")
                        else:
                            logger.info(f"Class already exists: {class_instance.class_name}")
                    except ValidationError as e:
                        logger.error(f"Validation error for class {row['class_name']}: {e}")
                    except ObjectDoesNotExist as e:
                        logger.error(f"Critical data missing: {e}")
                    except IntegrityError as e:
                        logger.error(f"Error importing class {row['class_name']}: {e}")

    def import_weekday(self, csv_file):
        with open(csv_file, newline='', encoding='utf-8') as f:
            with transaction.atomic():
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        weekday_instance, created = Weekday.objects.get_or_create(day_name=row['day_name'])
                        if created:
                            logger.info(f"Added new weekday: {weekday_instance.day_name}")
                        else:
                            logger.info(f"Weekday already exists: {weekday_instance.day_name}")
                    except ValidationError as e:
                        logger.error(f"Validation error for weekday {row['day_name']}: {e}")
                    except ObjectDoesNotExist as e:
                        logger.error(f"Critical data missing: {e}")
                    except IntegrityError as e:
                        logger.error(f"Error importing weekday {row['day_name']}: {e}")

    def import_ClassSchedule(self, csv_file):
        with open(csv_file, newline='', encoding='utf-8') as f:
            with transaction.atomic():
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        class_name = row['classes']
                        time = row['time']
                        duration = int(row['duration'])
                        capacity = int(row['capacity'])
                        day_name = row['weekday']

                        # Convert time string to a time object
                        time_obj = datetime.strptime(time, '%H:%M').time()

                        classes = Classes.objects.get(class_name=class_name)
                        weekday = Weekday.objects.get(day_name=day_name)

                        class_instance, created = ClassSchedule.objects.get_or_create(
                            classes=classes,
                            weekday=weekday,
                            time=time,
                            defaults={
                                'duration': duration,
                                'capacity': capacity
                            }
                        )
                        if created:
                            logger.info(f"Added new class schedule: {class_instance.classes.class_name} on {class_instance.weekday.day_name}")
                        else:
                            logger.info(f"Class schedule already exists: {class_instance.classes.class_name} on {class_instance.weekday.day_name}")
                    except ValidationError as e:
                        logger.error(f"Validation error for class schedule {class_name} on {day_name}: {e}")
                    except ObjectDoesNotExist as e:
                        logger.error(f"Critical data missing: {e}")
                    except IntegrityError as e:
                        logger.error(f"Error importing class {class_name} on {day_name}: {e}")
        
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting import...'))
        
        # Call your import functions
        self.import_classes('booking/data/Classes.csv')
        self.import_weekday('booking/data/Weekdays.csv')
        self.import_ClassSchedule('booking/data/ClassSchedule.csv')

        self.stdout.write(self.style.SUCCESS('Successfully imported all data.'))
                