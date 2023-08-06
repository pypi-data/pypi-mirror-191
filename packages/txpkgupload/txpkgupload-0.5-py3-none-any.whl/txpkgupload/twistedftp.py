# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Twisted FTP implementation of the txpkgupload upload server."""

__metaclass__ = type
__all__ = [
    'AnonymousShell',
    'FTPRealm',
    ]

import ipaddress
import os
import re
import tempfile

import six
from twisted.application import (
    service,
    strports,
    )
from twisted.cred import (
    checkers,
    credentials,
    )
from twisted.cred.portal import (
    IRealm,
    Portal,
    )
from twisted.internet import (
    defer,
    error,
    reactor,
    )
from twisted.protocols import ftp
from twisted.python import filepath
from zope.interface import implementer

from txpkgupload.filesystem import UploadFileSystem
from txpkgupload.hooks import Hooks


@implementer(checkers.ICredentialsChecker)
class AccessCheck:
    """An `ICredentialsChecker` for txpkgupload FTP sessions."""

    credentialInterfaces = (
        credentials.IUsernamePassword, credentials.IAnonymous)

    def requestAvatarId(self, credentials):
        # txpkgupload allows any credentials.  People can use "anonymous" if
        # they want but anything goes.  Thus, we don't actually *check* the
        # credentials, and we return the standard avatarId for 'anonymous'.
        return checkers.ANONYMOUS


class AnonymousShell(ftp.FTPShell):
    """The 'command' interface for sessions.

    Roughly equivalent to the SFTPServer in the sftp side of things.
    """

    def __init__(self, fsroot, temp_dir):
        self._fs_root = fsroot
        self.uploadfilesystem = UploadFileSystem(
            tempfile.mkdtemp(dir=temp_dir))
        self._current_upload = self.uploadfilesystem.rootpath
        os.chmod(self._current_upload, 0o770)
        self.hook = Hooks(self._fs_root, perms='g+rws', prefix='-ftp')
        self.hook.new_client_hook(self._current_upload, 0, 0)
        super(AnonymousShell, self).__init__(
            filepath.FilePath(self._current_upload))

    def openForWriting(self, file_segments):
        """Write the uploaded file to disk, safely.

        :param file_segments: A list containing string items, one for each
            path component of the file being uploaded.  The file referenced
            is relative to the temporary root for this session.

        If the file path contains directories, we create them.
        """
        filename = os.sep.join(file_segments)
        self._create_missing_directories(filename)
        return super(AnonymousShell, self).openForWriting(file_segments)

    def makeDirectory(self, path):
        """Make a directory using the secure `UploadFileSystem`."""
        path = os.sep.join(path)
        return defer.maybeDeferred(self.uploadfilesystem.mkdir, path)

    def access(self, segments):
        """Permissive CWD that auto-creates target directories."""
        if segments:
            path = self._path(segments)
            path.makedirs()
        return super(AnonymousShell, self).access(segments)

    def logout(self):
        """Called when the client disconnects.

        We need to post-process the upload.
        """
        self.hook.client_done_hook(self._current_upload, 0, 0)

    def _create_missing_directories(self, filename):
        # Same as SFTPServer
        new_dir, new_file = os.path.split(
            self.uploadfilesystem._sanitize(filename))
        if new_dir != '':
            if not os.path.exists(
                os.path.join(self._current_upload, new_dir)):
                self.uploadfilesystem.mkdir(new_dir)

    def list(self, path_segments, attrs):
        return defer.fail(ftp.CmdNotImplementedError("LIST"))


@implementer(IRealm)
class FTPRealm:
    """FTP Realm that lets anyone in."""

    def __init__(self, root, temp_dir):
        self.root = root
        self.temp_dir = temp_dir

    def requestAvatar(self, avatarId, mind, *interfaces):
        """Return a txpkgupload avatar - that is, an "authorisation".

        txpkgupload FTP avatars are totally fake, we don't care about
        credentials. See `AccessCheck` above.
        """
        for iface in interfaces:
            if iface is ftp.IFTPShell:
                avatar = AnonymousShell(self.root, self.temp_dir)
                return ftp.IFTPShell, avatar, getattr(
                    avatar, 'logout', lambda: None)
        raise NotImplementedError(
            "Only IFTPShell interface is supported by this realm")


_AFNUM_IP = 1
_AFNUM_IP6 = 2


class UnsupportedNetworkProtocolError(Exception):
    """Raised when the client requests an unsupported network protocol."""


def decodeExtendedAddress(address):
    """
    Decode an FTP protocol/address/port combination, using the syntax
    defined in RFC 2428 section 2.

    @return: a 3-tuple of (protocol, host, port).
    """
    delim = address[0]
    protocol, host, port, _ = address[1:].split(delim)
    return protocol, host, int(port)


def decodeExtendedAddressLine(line):
    """
    Decode an FTP response specifying a protocol/address/port combination,
    using the syntax defined in RFC 2428 sections 2 and 3.

    @return: a 3-tuple of (protocol, host, port).
    """
    match = re.search(r'\((.*)\)', line)
    if match:
        return decodeExtendedAddress(match.group(1))
    else:
        raise ValueError('No extended address found in "%s"' % line)


class FTPWithEPSV(ftp.FTP):

    epsvAll = False
    supportedNetworkProtocols = (_AFNUM_IP, _AFNUM_IP6)

    def connectionLost(self, reason):
        ftp.FTP.connectionLost(self, reason)
        self.epsvAll = False

    def getDTPPort(self, factory, interface=''):
        """
        Return a port for passive access, using C{self.passivePortRange}
        attribute.
        """
        for portn in self.passivePortRange:
            try:
                dtpPort = self.listenFactory(portn, factory,
                                             interface=interface)
            except error.CannotListenError:
                continue
            else:
                return dtpPort
        raise error.CannotListenError('', portn,
            "No port available in range %s" %
            (self.passivePortRange,))

    def ftp_PASV(self):
        """
        Request for a passive connection

        from the rfc::

            This command requests the server-DTP to \"listen\" on a data port
            (which is not its default data port) and to wait for a connection
            rather than initiate one upon receipt of a transfer command.  The
            response to this command includes the host and port address this
            server is listening on.
        """
        if self.epsvAll:
            return defer.fail(ftp.BadCmdSequenceError(
                'may not send PASV after EPSV ALL'))

        host = self.transport.getHost().host
        try:
            address = ipaddress.IPv6Address(six.ensure_text(host))
        except ipaddress.AddressValueError:
            pass
        else:
            if address.ipv4_mapped is not None:
                # IPv4-mapped addresses are usable, but we need to make sure
                # they're encoded as IPv4 in the response.
                host = str(address.ipv4_mapped)
            else:
                # There's no standard defining the behaviour of PASV with
                # IPv6, so just claim it as unimplemented.  (Some servers
                # return something like '0,0,0,0' in the host part of the
                # response in order that at least clients that ignore the
                # host part can work, and if it becomes necessary then we
                # could do that too.)
                return defer.fail(ftp.CmdNotImplementedError('PASV'))

        # if we have a DTP port set up, lose it.
        if self.dtpFactory is not None:
            # cleanupDTP sets dtpFactory to none.  Later we'll do
            # cleanup here or something.
            self.cleanupDTP()
        self.dtpFactory = ftp.DTPFactory(pi=self)
        self.dtpFactory.setTimeout(self.dtpTimeout)
        self.dtpPort = self.getDTPPort(self.dtpFactory)

        port = self.dtpPort.getHost().port
        self.reply(ftp.ENTERING_PASV_MODE, ftp.encodeHostPort(host, port))
        return self.dtpFactory.deferred.addCallback(lambda ign: None)

    def _validateNetworkProtocol(self, protocol):
        """
        Validate the network protocol requested in an EPRT or EPSV command.

        For now we just hardcode the protocols we support, since this layer
        doesn't have a good way to discover that.

        @param protocol: An address family number.  See RFC 2428 section 2.
        @type protocol: L{str}

        @raise FTPCmdError: If validation fails.
        """
        # We can't actually honour an explicit network protocol request
        # (violating a SHOULD in RFC 2428 section 3), but let's at least
        # validate it.
        try:
            protocol = int(protocol)
        except ValueError:
            raise ftp.CmdArgSyntaxError(protocol)
        if protocol not in self.supportedNetworkProtocols:
            raise UnsupportedNetworkProtocolError(
                ','.join(str(p) for p in self.supportedNetworkProtocols))

    def ftp_EPSV(self, protocol=''):
        if protocol == 'ALL':
            self.epsvAll = True
            self.sendLine('200 EPSV ALL OK')
            return defer.succeed(None)
        elif protocol:
            try:
                self._validateNetworkProtocol(protocol)
            except ftp.FTPCmdError:
                return defer.fail()
            except UnsupportedNetworkProtocolError as e:
                self.sendLine(
                    '522 Network protocol not supported, use (%s)' % e.args)
                return defer.succeed(None)

        # if we have a DTP port set up, lose it.
        if self.dtpFactory is not None:
            # cleanupDTP sets dtpFactory to none.  Later we'll do
            # cleanup here or something.
            self.cleanupDTP()
        self.dtpFactory = ftp.DTPFactory(pi=self)
        self.dtpFactory.setTimeout(self.dtpTimeout)
        if not protocol or protocol == _AFNUM_IP6:
            interface = '::'
        else:
            interface = ''
        self.dtpPort = self.getDTPPort(self.dtpFactory, interface=interface)

        port = self.dtpPort.getHost().port
        self.reply(ftp.ENTERING_EPSV_MODE, port)
        return self.dtpFactory.deferred.addCallback(lambda ign: None)

    def ftp_PORT(self):
        if self.epsvAll:
            return defer.fail(ftp.BadCmdSequenceError(
                'may not send PORT after EPSV ALL'))
        return ftp.FTP.ftp_PORT(self)

    def ftp_EPRT(self, extendedAddress):
        """
        Extended request for a data connection.

        As described by U{RFC 2428 section
        2<https://tools.ietf.org/html/rfc2428#section-2>}::

            The EPRT command allows for the specification of an extended
            address for the data connection.  The extended address MUST
            consist of the network protocol as well as the network and
            transport addresses.
        """
        if self.epsvAll:
            return defer.fail(ftp.BadCmdSequenceError(
                'may not send EPRT after EPSV ALL'))

        try:
            protocol, ip, port = decodeExtendedAddress(extendedAddress)
        except ValueError:
            return defer.fail(ftp.CmdArgSyntaxError(extendedAddress))
        if protocol:
            try:
                self._validateNetworkProtocol(protocol)
            except ftp.FTPCmdError:
                return defer.fail()
            except UnsupportedNetworkProtocolError as e:
                self.sendLine(
                    '522 Network protocol not supported, use (%s)' % e.args)
                return defer.succeed(None)

        # if we have a DTP port set up, lose it.
        if self.dtpFactory is not None:
            self.cleanupDTP()

        self.dtpFactory = ftp.DTPFactory(
            pi=self, peerHost=self.transport.getPeer().host)
        self.dtpFactory.setTimeout(self.dtpTimeout)
        self.dtpPort = reactor.connectTCP(ip, port, self.dtpFactory)

        def connected(ignored):
            return ftp.ENTERING_PORT_MODE

        def connFailed(err):
            err.trap(ftp.PortConnectionError)
            return ftp.CANT_OPEN_DATA_CNX

        return self.dtpFactory.deferred.addCallbacks(connected, connFailed)


class FTPServiceFactory(service.Service):
    """A factory that makes an `FTPService`"""

    def __init__(self, port, root, temp_dir, idle_timeout):
        realm = FTPRealm(root, temp_dir)
        portal = Portal(realm)
        portal.registerChecker(AccessCheck())
        factory = ftp.FTPFactory(portal)

        factory.tld = root
        factory.protocol = FTPWithEPSV
        factory.welcomeMessage = "Launchpad upload server"
        factory.timeOut = idle_timeout

        self.ftpfactory = factory
        self.portno = port

    @staticmethod
    def makeFTPService(port, root, temp_dir, idle_timeout):
        strport = "tcp6:%s" % port
        factory = FTPServiceFactory(port, root, temp_dir, idle_timeout)
        return strports.service(strport, factory.ftpfactory)
