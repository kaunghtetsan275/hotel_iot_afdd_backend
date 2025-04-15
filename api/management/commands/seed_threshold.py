from django.core.management.base import BaseCommand
from ...models import FaultThreshold
from supabase import create_client, Client
from decouple import config
import configparser
from datetime import datetime
import os

SUPABASE_URL = config('SUPABASE_URL')
SUPABASE_API_KEY = config('SUPABASE_API_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

class Command(BaseCommand):
    help = 'Seed initial fault detection thresholds'

    def handle(self, *args, **kwargs):
        # Load thresholds from the .ini file
        config = configparser.ConfigParser()
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
        ini_file_path = os.path.join(root_dir, 'thresholds.ini')
        config.read(ini_file_path)
        print("Loading thresholds from:", ini_file_path)

        # Parse thresholds from the .ini file
        defaults = []
        for section in config.sections():
            entry = dict(config.items(section))
            # Convert numeric and boolean values
            for key, value in entry.items():
                if value.isdigit():
                    entry[key] = int(value)
                elif value.replace('.', '', 1).isdigit():
                    entry[key] = float(value)
                elif value.lower() in ['true', 'false']:
                    entry[key] = value.lower() == 'true'
            defaults.append(entry)

        for entry in defaults:
            obj, created = FaultThreshold.objects.update_or_create(
                defaults=entry
            )
            status = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{status}: {obj}"))

            # Convert Django model to dict, filter out nulls
            supabase_data = {k: (v.isoformat() if isinstance(v, datetime) else v) for k, v in obj.__dict__.items() if not k.startswith('_') and v is not None and k != 'id'}

            # Upload to Supabase (replace table name if needed)
            response = supabase.table("fault_thresholds").upsert(supabase_data).execute()
            print(response)