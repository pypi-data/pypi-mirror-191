import glob
import json
import operator
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict

import django.db.utils
import polib
from django.conf import settings
from django.conf.locale import LANG_INFO
from django.core.management.base import BaseCommand

from translate.core.utils.logging import log
from translate.service.models import Language, Translation, TranslationKey

SNAKE_TRANSLATIONS = Path("snake_translations.json")
# DEFAULT_DIR_PATH = Path("translate/service/tests/fixtures")  # This is a testing directory
DEFAULT_DIR_PATH = Path("export_translations")


def extract_language(path: str) -> str:
    """Extract language from path with locale."""
    parts = path.split("/")
    idx = parts.index("locale")
    return parts[idx + 1]


class Command(BaseCommand):
    help = "Importing translation keys command from .json and .po files"

    def add_arguments(self, parser):
        """Attach argument for import_translations command."""
        parser.add_argument(
            "translations_dir",
            type=str,
            nargs="?",
            default=DEFAULT_DIR_PATH,
        )

        # parser.add_argument(
        #     "-f",
        #     "--force",
        #     action="store_true",
        #     help="Skips sanity checks and imports all items",
        # ) will be added in follow up

    @staticmethod
    def po_keys_sanity_check(obj_keys):
        """
        This method returns a QuerySet of already imported translations
        """
        key_ids = []
        for key in obj_keys:
            key_ids.append(key.id_name)

        already_existing_keys = TranslationKey.objects.filter(id_name__in=key_ids)
        log.info(f"Already existing po keys: {len(already_existing_keys)}")
        return already_existing_keys

    @staticmethod
    def read_po_files(dirs) -> dict:
        """Read po files."""
        log.info("Reading po files.")
        po_files = {
            po_file: polib.pofile(po_file, encoding="utf-8")
            for po_file in glob.iglob(f"{dirs}/**/*.po", recursive=True)
        }

        files_with_languages = defaultdict(list)
        for file_path, file in po_files.items():
            lang = extract_language(file_path)
            files_with_languages[lang].append((file_path, file))

        log.info("Done")
        return files_with_languages

    @staticmethod
    def create_po_keys(file_path, file_entries):
        """Create po keys."""
        entries = [
            TranslationKey(
                id_name=entry.msgid,
                id_name_plural=entry.msgid_plural,
                encoding=entry.encoding,
                usage_context=entry.msgctxt,
                occurrences=sorted(map(operator.itemgetter(0), entry.occurrences)),
                flags=entry.flags,
            )
            for entry in file_entries
        ]

        return entries

    @staticmethod
    def create_po_translations(file_path, file_entries, key_entries, language):
        """Import po translations."""
        entries = [
            Translation(
                language=language,
                key=key_entries[idx],
                translation=entry.msgstr if entry.msgstr else entry.msgid,
                translation_plural=entry.msgid_plural,
            )
            for idx, entry in enumerate(file_entries)
        ]

        return entries

    @staticmethod
    def process_po_files(dirs):
        """Process po files."""
        po_files = Command.read_po_files(dirs)

        raw_key_entries, translations = [], []
        for lang, files in sorted(po_files.items()):
            language, _ = Language.objects.get_or_create(lang_info=lang)
            for file_path, file_entries in files:
                raw_key_entries += Command.create_po_keys(file_path, file_entries)
                translations += Command.create_po_translations(file_path, file_entries, raw_key_entries, language)

        log.info(f"Prepared {len(raw_key_entries)} of RAW TranslationKeys via po files.")
        log.info("Cleaning...")
        uniq = {}
        duplicate_counter = 0
        for key in raw_key_entries:
            if key.id_name in uniq.keys():
                duplicate_counter += 1
            else:
                uniq[key.id_name] = key

        log.info(f"Duplicate ID_NAME occurred with {duplicate_counter} TranslationKeys.")

        bulk_inserts = uniq
        already_imported_keys = Command.po_keys_sanity_check(uniq.values())

        if not already_imported_keys:
            log.info("NO ALREADY IMPORTED KEYS FOUND!")
        else:
            for key in already_imported_keys:
                if key.id_name in uniq.keys():
                    bulk_inserts.pop(key.id_name)

        inserts = TranslationKey.objects.bulk_create(bulk_inserts.values(), ignore_conflicts=True)
        if not inserts:
            log.info("NO NEW PO TRANSLATIONS HAVE BEEN ADDED")
        log.info(f"Done. Inserted {len(inserts)} po TranslationKeys.")
        log.info("----------------------------------------------------")

        log.info(f"Prepared {len(translations)} of RAW Translations via po files.")

        translation_inserts = []
        uniq_id_names = set(uniq.keys())  # uniq dictionary keys are id_names

        log.info("Cleaning!")
        for translation_obj in translations:
            if translation_obj.translation in uniq_id_names:
                translation_inserts.append(translation_obj)

        # translation_inserts = translations this will be used later for force argument

        integrity_errors = 0
        try:
            log.info(f"Prepared {len(translation_inserts)} of Translations. Inserting bulk... ")
            translation_inserts = Translation.objects.bulk_create(translation_inserts, ignore_conflicts=True)
        except django.db.utils.IntegrityError:
            log.info("Integrity error occurred, and bulk create was canceled! Inserting individually...")
            translation_inserts = []
            for obj in translations:
                if obj.translation in uniq.keys():
                    try:
                        obj.save()
                        translation_inserts.append(obj)
                    except django.db.utils.IntegrityError:
                        integrity_errors += 1

        log.info(f"Integrity error occurred with {integrity_errors} Translations.")
        if not translation_inserts:
            log.info("NO NEW PO TRANSLATIONS HAVE BEEN ADDED")
        log.info(f"Done. Inserted {len(translation_inserts)} po Translations.")

    @staticmethod
    def create_json_keys(language_data, language_code):
        """Create language data."""
        log.info("Preparing translation keys.")
        keys = [
            TranslationKey(
                snake_name=snake_name, id_name=obj.get("translations"), views=[source_dict] + obj.get("source")
            )
            for source_dict, value in language_data.items()
            for snake_name, obj in value.items()
        ]
        key_dict = {}
        for key in keys:
            key_dict[key.snake_name] = key

        log.info(f"Prepared {len(keys)} RAW TranslationKeys for {language_code} language.")

        log.info("Cleaning")
        already_imported_sn = Command.json_keys_sanity_check(keys)
        for name in already_imported_sn:
            if name in key_dict.keys():
                key_dict.pop(name)

        bulk_inserts = key_dict.values()
        if not bulk_inserts:
            log.info("NO NEW KEYS HAVE BEEN INSERTED!")
        else:
            log.info("Inserting in bulk...")
            objs = TranslationKey.objects.bulk_create(bulk_inserts, ignore_conflicts=True)
            log.info("Done!")
            log.info(f"Imported {len(objs)} TranslationKeys into database!")

        return key_dict

    @staticmethod
    def json_keys_sanity_check(obj_keys) -> list:
        """
        This method returns a list of already imported key objects snake_names
        """
        snake_names = []
        for key in obj_keys:
            snake_names.append(key.snake_name)

        already_existing_keys = TranslationKey.objects.in_bulk(snake_names, field_name="snake_name")
        log.info(f"Already existing json keys and snake names {len(already_existing_keys.keys())} founded in database.")
        return already_existing_keys.keys()

    @staticmethod
    def read_json_translations(dirs):
        """Read JSON translations."""
        log.info("Reading json translations")
        translations = json.loads((settings.BASE_DIR.parent / dirs / SNAKE_TRANSLATIONS).read_text())
        log.info("Done")
        log.info(f"There are {len(translations)} available languages in this file.")
        return translations

    @staticmethod
    def create_json_translations(translations: Dict[str, Any], lang_key: str):
        """Import snake_names for a specific language."""
        log.info(f"Processing snake_names from JSON for {lang_key} language.")
        language = Language.objects.get(lang_info=lang_key)
        data_for_provided_language = translations.get(lang_key)

        bulk_translations = []
        for _, dict_data in data_for_provided_language.items():
            snake_names_list = list(dict_data.keys())
            keys = {key.snake_name: key for key in TranslationKey.objects.filter(snake_name__in=snake_names_list)}

            for snake_key, snake_data in dict_data.items():
                translation_key = keys.get(snake_key)
                if translation_key:
                    translation = Translation(
                        language=language,
                        key=translation_key,
                        translation=snake_data.get("translations"),
                        translation_plural=snake_data.get("translations"),
                    )
                    bulk_translations.append(translation)

        try:
            Translation.objects.bulk_create(bulk_translations, ignore_conflicts=True)
        except django.db.utils.IntegrityError:
            log.info("There was a Integrity Error with json files, none were inserted.")
        log.info("Done")
        log.info("----------------------------------------------------")

    @staticmethod
    def process_json_files(dirs):
        """Process json files."""
        translations = Command.read_json_translations(dirs)

        _ = {
            lang: Language.objects.get_or_create(lang_info=lang)
            for lang in translations
            if lang in list(LANG_INFO.keys())
        }

        for lang in translations:
            _ = Command.create_json_keys(translations.get(lang), lang)
            _ = Command.create_json_translations(translations, lang)

    def handle(self, *args, **options):
        """Entrypoint to the command."""
        # force = options.get("force")

        dir_name = Path(settings.BASE_DIR.parent, options.get("translations_dir"))

        Command.process_json_files(dir_name)
        Command.process_po_files(dir_name)
