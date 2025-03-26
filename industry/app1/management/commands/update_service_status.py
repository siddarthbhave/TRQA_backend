from django.core.management.base import BaseCommand
from django.utils import timezone
from app1.models import InstrumentModel, CalibrationReport

class Command(BaseCommand):
    help = 'Update the service status of instruments'

    def handle(self, *args, **kwargs):
        # Get all instrument models
        instrument_models = InstrumentModel.objects.all()

        # Iterate over each instrument model
        for instrument in instrument_models:
            # Get the latest calibration report for the instrument
            latest_calibration_report = CalibrationReport.objects.filter(calibration_tool=instrument).order_by('calibration_date').first()

            # Check if a calibration report exists and if the notification date matches the current date
            if latest_calibration_report and latest_calibration_report.notification_date == timezone.now().date():
                # Update the service status of the instrument
                instrument.service_status = True
                instrument.save()

        self.stdout.write(self.style.SUCCESS('Service status updated successfully'))
