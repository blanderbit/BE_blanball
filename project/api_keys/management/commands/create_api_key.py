import json

from api_keys.models import ApiKey
from django.core.management.base import (
    BaseCommand,
)
from django.utils import timezone
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "The command that creates the admin api key"

    def write_key_to_file(self, file_name: str, api_key_value: str) -> None:

        with open(f"../{file_name}", "w") as file:
            file.write(
                json.dumps(
                    {
                        "value": api_key_value,
                        "created_at": str(timezone.now()),
                    },
                    indent=2,
                )
            )

    def add_arguments(self, parser) -> None:

        # Optional arguments
        parser.add_argument(
            "-fn",
            "--file-name",
            type=str,
            help='Change the name of the output file. According to the "api_key.json" standard',
        )
        parser.add_argument(
            "-no",
            "--no-output",
            action="store_true",
            help="With this argument, the api key will not be written to the file",
        )
        parser.add_argument(
            "-np",
            "--no-print",
            action="store_true",
            help="With this argument, the created key will not be printed to the console",
        )
        parser.add_argument(
            "-oc",
            "--only-create",
            action="store_true",
            help="With this argument, the key will simply be created in the database without writing to a file and output to the console",
        )
        parser.add_argument("name", type=str, help="API key name")

    def handle(self, *args, **options) -> None:

        try:
            api_key: ApiKey = ApiKey.objects.create(name=options["name"])
        except IntegrityError:
            self.stdout.write(
                self.style.ERROR("API KEY with the same name already exists")
            )
            return

        if options.get("only_create"):
            self.stdout.write(self.style.SUCCESS("API KEY created"))

        if not options.get("only_create"):
            if not options.get("no_output"):
                if options.get("file_name"):
                    OUTPUT_FILE_NAME: str = options["file_name"]
                else:
                    OUTPUT_FILE_NAME: str = "api_key.json"
                self.write_key_to_file(OUTPUT_FILE_NAME, api_key.value)
                self.stdout.write(
                    self.style.WARNING(
                        f"\nYour API KEY was written to the {OUTPUT_FILE_NAME} file, be careful if you don't want it to fall into someone else's possession then delete the file"
                    )
                )

            if not options.get("no_print"):
                self.stdout.write(self.style.SUCCESS("API KEY: %s" % api_key.value))
