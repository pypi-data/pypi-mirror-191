# Copyright 2009 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

__metaclass__ = type
__all__ = [
    'UploadFileSystem',
    ]

import os


class UploadFileSystem:

    def __init__(self, rootpath):
        self.rootpath = rootpath

    def _full(self, path):
        """Returns the full path name (i.e. rootpath + path)"""
        full_path = os.path.join(self.rootpath, path)
        if not os.path.realpath(full_path).startswith(self.rootpath):
            raise OSError("Path not allowed:", path)
        return full_path

    def _sanitize(self, path):
        if isinstance(path, bytes):
            # RFC 2640 recommends that paths are exchanged using UTF-8,
            # albeit with some feature negotiation.  However, Twisted's SFTP
            # implementation leaves paths as bytes.  Since in practice
            # legitimate uses of txpkgupload will only involve ASCII paths,
            # and since UTF-8 has low risk of undetected decoding errors,
            # let's try to decode SFTP paths as UTF-8.
            try:
                path = path.decode('UTF-8')
            except UnicodeDecodeError:
                raise NotImplementedError('Paths must be encoded using UTF-8')
        if path.startswith('/'):
            path = path[1:]
        path = os.path.normpath(path)
        return path

    def mkdir(self, path):
        """Create a directory."""
        path = self._sanitize(path)
        full_path = self._full(path)
        if os.path.exists(full_path):
            if os.path.isfile(full_path):
                raise OSError("File already exists:", path)
            elif os.path.isdir(full_path):
                raise OSError("Directory already exists:", path)
            raise OSError("OOPS, can't create:", path)
        else:
            old_mask = os.umask(0o002)
            try:
                os.makedirs(full_path)
            finally:
                os.umask(old_mask)

    def rmdir(self, path):
        """Remove a directory.

        Remove a target path recursively.
        """
        path = self._sanitize(path)
        full_path = self._full(path)
        if os.path.exists(full_path):
            os.rmdir(full_path)
        else:
            raise OSError("Not exists:", path)
