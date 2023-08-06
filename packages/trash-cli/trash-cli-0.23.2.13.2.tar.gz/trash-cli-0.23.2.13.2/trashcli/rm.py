# Copyright (C) 2011-2021 Andrea Francia Bereguardo(PV) Italy
import fnmatch
import os
import sys

from trashcli.fs import FileRemover, FileSystemReader
from trashcli.trash import (
    DirChecker,
    ParseError,
    TrashDirReader,
    UserInfoProvider,
    parse_path,
    path_of_backup_copy,
)
from trashcli.trash_dirs_scanner import (
    TopTrashDirRules,
    TrashDirsScanner,
    trash_dir_found,
)


class CleanableTrashcan:
    def __init__(self, file_remover): # type: (FileRemover) -> None
        self._file_remover = file_remover

    def delete_trash_info_and_backup_copy(self, trash_info_path):
        backup_copy = path_of_backup_copy(trash_info_path)
        self._file_remover.remove_file_if_exists(backup_copy)
        self._file_remover.remove_file(trash_info_path)


class RmCmd:
    def __init__(self,
                 environ,
                 getuid,
                 volumes_listing,
                 stderr,
                 file_reader):
        self.environ = environ
        self.getuid = getuid
        self.volumes_listing = volumes_listing
        self.stderr = stderr
        self.file_reader = file_reader

    def run(self, argv, uid):
        args = argv[1:]
        self.exit_code = 0

        if not args:
            self.print_err('Usage:\n'
                           '    trash-rm PATTERN\n'
                           '\n'
                           'Please specify PATTERN.\n'
                           'trash-rm uses fnmatch.fnmatchcase to match patterns, see https://docs.python.org/3/library/fnmatch.html for more details.')
            self.exit_code = 8
            return

        trashcan = CleanableTrashcan(FileRemover())
        cmd = Filter(args[0])

        listing = ListTrashinfos(self.file_reader)

        user_info_provider = UserInfoProvider()
        scanner = TrashDirsScanner(user_info_provider,
                                   self.volumes_listing,
                                   TopTrashDirRules(self.file_reader),
                                   DirChecker())

        for event, args in scanner.scan_trash_dirs(self.environ, uid):
            if event == trash_dir_found:
                path, volume = args
                for type, arg in listing.list_from_volume_trashdir(path,
                                                                   volume):
                    if type == 'unable_to_parse_path':
                        self.unable_to_parse_path(arg)
                    elif type == 'trashed_file':
                        original_location, info_file = arg
                        if cmd.matches(original_location):
                            trashcan.delete_trash_info_and_backup_copy(
                                info_file)

    def unable_to_parse_path(self, trashinfo):
        self.report_error('{}: unable to parse \'Path\''.format(trashinfo))

    def report_error(self, error_msg):
        self.print_err('trash-rm: {}'.format(error_msg))

    def print_err(self, msg):
        self.stderr.write(msg + '\n')


def main():
    from trashcli.list_mount_points import os_mount_points
    from trashcli.fstab import VolumesListing
    volumes_listing = VolumesListing(os_mount_points)
    cmd = RmCmd(environ=os.environ
                , getuid=os.getuid
                , volumes_listing=volumes_listing
                , stderr=sys.stderr
                , file_reader=FileSystemReader())

    cmd.run(sys.argv, os.getuid())

    return cmd.exit_code


class Filter:
    def __init__(self, pattern):
        self.pattern = pattern

    def matches(self, original_location):
        basename = os.path.basename(original_location)
        subject = original_location if self.pattern[0] == '/' else basename
        return fnmatch.fnmatchcase(subject, self.pattern)


class ListTrashinfos:
    def __init__(self, file_reader):
        self.file_reader = file_reader

    def list_from_volume_trashdir(self, trashdir_path, volume):
        trashdir = TrashDirReader(self.file_reader)
        for trashinfo_path in trashdir.list_trashinfo(trashdir_path):
            trashinfo = self.file_reader.contents_of(trashinfo_path)
            try:
                path = parse_path(trashinfo)
            except ParseError:
                yield 'unable_to_parse_path', trashinfo_path
            else:
                complete_path = os.path.join(volume, path)
                yield 'trashed_file', (complete_path, trashinfo_path)
