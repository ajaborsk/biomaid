import os
from hashlib import md5
from functools import partial

from django.core.management.base import BaseCommand, CommandError
from common import config
from document.models import Document


class Command(BaseCommand):
    def handle(self, *args, **options):
        if options['verbosity'] >= 1:
            self.stdout.write(f"Checking document links in {config.settings.MEDIA_ROOT}...")

        db_documents = 0
        db_documents_not_found = 0
        db_documents_bad_hash = 0
        for document in Document.records.all().values('physical_path', 'hash', 'mime_type'):
            db_documents += 1
            # Does the filename exists in the filesystem ?
            if os.path.isfile(config.settings.MEDIA_ROOT + os.path.sep + document['physical_path']):
                # Compute hash for perfect identity check
                hash = md5()
                with open(config.settings.MEDIA_ROOT + os.path.sep + document['physical_path'], 'rb') as f:
                    for block in iter(partial(f.read, 1024 * 1024), b''):
                        hash.update(block)
                if hash.hexdigest() != document['hash']:
                    db_documents_bad_hash += 1
                    if options['verbosity'] >= 3:
                        self.stdout.write(
                            self.style.ERROR(
                                f"  File is in both filesystem and database but hash is different : '{document['physical_path']}'"
                            )
                        )
            else:
                db_documents_not_found += 1
                if options['verbosity'] >= 3:
                    self.stdout.write(
                        self.style.error(f"  Not found in the folder while in the database : '{document['physical_path']}'")
                    )

        files_list = os.listdir(config.settings.MEDIA_ROOT)
        files_in_fs = len(files_list)
        files_not_in_database = 0
        files_duplicates = 0
        for filename in files_list:
            # If the file registred in the database ?
            if not Document.records.filter(physical_path=filename).exists():
                if options['verbosity'] >= 3:
                    self.stdout.write(self.style.WARNING(f"  File is in the folder but not in the database : '{filename}'"))
                files_not_in_database += 1

                # Try to find if it is stored under a other name
                hash = md5()
                with open(config.settings.MEDIA_ROOT + os.path.sep + filename, 'rb') as f:
                    for block in iter(partial(f.read, 1024 * 1024), b''):
                        hash.update(block)
                qs = Document.records.filter(hash=hash.hexdigest())
                if qs.exists():
                    files_duplicates += 1
                    if options['verbosity'] >= 3:
                        for document in qs:
                            self.stdout.write(
                                self.style.NOTICE(f"    Probable duplicate of {document.logical_path} / {document.physical_path}.")
                            )

        # Check for duplicate documents in database :
        ...

        if options['verbosity'] >= 2:
            # Write a quit
            self.stdout.write(f"Checked documents from database: {db_documents}.")
            if db_documents_not_found:
                self.stdout.write(self.style.ERROR(f"  Documents not found in filesystem: {db_documents_not_found}."))
            else:
                self.stdout.write(self.style.SUCCESS("  All Documents found in filesystem."))
            if db_documents_bad_hash:
                self.stdout.write(self.style.ERROR(f"  Documents found in filesystem but different: {db_documents_bad_hash}."))
            else:
                self.stdout.write(self.style.SUCCESS("  All Documents in filesystem have correct hashes."))
            self.stdout.write(f"Files in filesystem: {files_in_fs}.")
            if files_not_in_database:
                self.stdout.write(self.style.WARNING(f"  Files not in documents database: {files_not_in_database}."))
                self.stdout.write(self.style.NOTICE(f"    Probable duplicates: {files_duplicates}."))
        elif options['verbosity'] >= 1:
            if db_documents_bad_hash or db_documents_bad_hash:
                self.stdout.write(self.style.ERROR(f"Checked documents from database: {db_documents}. There is errors."))
            elif files_not_in_database:
                self.stdout.write(self.style.WARNING(f"Checked documents from database: {db_documents}. Some warnings."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Checked documents from database: {db_documents}. Everything OK."))

        if db_documents_bad_hash or db_documents_bad_hash:
            raise CommandError("documents_check detected a error. Run with verbosity > 2 to see details.")
