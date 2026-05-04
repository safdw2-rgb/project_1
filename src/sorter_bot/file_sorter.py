import os
import re
import shutil


class FileSorter:
    def __init__(self, target_folder):
        self.base_path = target_folder
        self.rules = {
            "images/": ("jpeg", "png", "jpg", "svg"),
            "documents/": ("doc", "docx", "txt", "pdf", "xlsx", "pptx", "rtf"),
            "audio/": ("mp3", "ogg", "wav", "amr"),
            "video/": ("avi", "mp4", "mov", "mkv")
        }
        self.archives_type = ("zip", "gz", "tar")

    def _sort_files(self, current_folder):
        for file in os.listdir(current_folder):

            source_path = os.path.join(current_folder, file)
            normalized_file = self._normalize(file)

            if not self._check_and_move_file(normalized_file, source_path):
                if normalized_file.lower().endswith(self.archives_type):
                    archive_folder = os.path.join(self.base_path, "results", "archives")
                    destination_path = os.path.join(archive_folder, normalized_file)
                    extract_path = destination_path.removesuffix(".zip").removesuffix(".gz").removesuffix(".tar")
                    shutil.unpack_archive(source_path, extract_path)
                    os.remove(source_path)

                    for root, dirs, files in os.walk(extract_path, topdown=False):
                        for name in files:
                            old_file = os.path.join(root, name)
                            fixed_name = self._fix_encoding(name)
                            new_file = os.path.join(root, self._normalize(fixed_name))
                            os.rename(old_file, new_file)

                        for name in dirs:
                            old_dir = os.path.join(root, name)
                            fixed_name = self._fix_encoding(name)
                            new_dir = os.path.join(root, self._normalize(fixed_name))
                            os.rename(old_dir, new_dir)

                elif os.path.isfile(source_path):
                    other_folder = os.path.join(self.base_path, "results", "other")
                    destination_path = os.path.join(other_folder, normalized_file)
                    shutil.move(source_path, destination_path)

                elif os.path.isdir(source_path) and "results" not in source_path:
                    self._sort_files(source_path)

                    if not os.listdir(source_path):
                        os.rmdir(source_path)

    def _check_and_move_file(self, file, source_path):
        for folder_name, extensions in self.rules.items():
            if file.lower().endswith(extensions):
                destination_folder = os.path.join(self.base_path, "results", folder_name)
                destination_path = os.path.join(destination_folder, file)
                shutil.move(source_path, str(destination_path))
                return True
        return False

    def _normalize(self, path):
        CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
        TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s",
                       "t",
                       "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
        CYRILLIC_SYMBOLS = list(CYRILLIC_SYMBOLS)
        TRANS = {}

        for symbol, translation in zip(CYRILLIC_SYMBOLS, TRANSLATION):
            TRANS[ord(symbol)] = translation
            TRANS[ord(symbol.upper())] = translation.upper()

        translated_name = ""

        for letter in path:
            translated_name += letter.translate(TRANS)

        translated_name = re.sub(r"[^A-Za-z0-9.]", "_", translated_name)

        return translated_name

    def _fix_encoding(self, name):
        for enc in ["utf-8", "cp866", "cp1251"]:
            try:
                return name.encode("cp437").decode(enc)
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass
        return name

    def _create_folders(self):
        folders_files_type = ["images", "documents", "audio", "video", "archives", "other"]
        for folder in folders_files_type:
            os.makedirs(os.path.join(self.base_path, "results", folder), exist_ok=True)

    def _unpack_folder(self):
        unpack_path = os.path.join(self.base_path, "results")
        for file in os.listdir(unpack_path):
            source_item = os.path.join(unpack_path, file)
            destination_item = os.path.join(self.base_path, file)
            shutil.move(source_item, destination_item)

        os.rmdir(unpack_path)

    def run(self):
        self._create_folders()
        self._sort_files(self.base_path)
        self._unpack_folder()
        return "Sorting completed successfully!"