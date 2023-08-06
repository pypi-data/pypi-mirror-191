"""PyPi Configuration File Manager."""

from configparser import ConfigParser
from pathlib import Path


class PyPiRC:
    """
    PyPi Configuration File Manager.

    Can be used for updating ~/.pypirc file programatically.

    Example::
        >>> a = PyPiRC('doctest_pypi.cfg')
        >>> new_server = {'pypi': {'repository': 'http://pypi.example.com'}}
        >>> new_server2 = {'pypi2': {'repository': 'http://pypi2.example.com'}}
        >>> a.servers.update(new_server)
        >>> a.servers.update(new_server2)
        >>> a.save()
        >>> 'pypi' in a.servers
        True
        >>> 'pypi2' in a.servers
        True
    """

    # will use this \/ if needed (like if the `Path` type fails xd)
    # RC_FILE = os.path.join(os.path.expanduser("~"), ".pypirc")
    RC_FILE = Path("~").expanduser() / Path(".pypirc")

    def __init__(self, rc_file: Path | None = None) -> None:
        if rc_file is None:
            self.rc_file = self.RC_FILE
        else:
            self.rc_file = rc_file

        self.conf = ConfigParser()

        if self.rc_file.exists():
            self.conf.read(self.rc_file)

        self._create_distutils()

        self._servers: dict[str, dict[str, str]] = {}
        for server in self._get_index_servers():
            if self.conf.has_section(server):
                server_conf = {server: dict(self.conf.items(server))}
                self.servers.update(server_conf)

    def _create_distutils(self) -> None:
        """Create top-level distutils stanza in pypirc."""
        if not self.conf.has_section("distutils"):
            self.conf.add_section("distutils")

    def save(self) -> None:
        """Save pypirc file with new configuration information."""
        # for server, conf in self.servers.iteritems():
        for server, conf in iter(self.servers.items()):
            self._add_index_server()
            for conf_k, conf_v in iter(conf.items()):
                if not self.conf.has_section(server):
                    self.conf.add_section(server)
                self.conf.set(server, conf_k, conf_v)

        with self.rc_file.open() as f:
            self.conf.write(f)
        self.conf.read(self.rc_file)

    def _get_index_servers(self) -> list[str]:
        """Get index-servers currently configured in pypirc."""
        idx_srvs = []
        if "index-servers" in self.conf.options("distutils"):
            idx = self.conf.get("distutils", "index-servers")
            idx_srvs = [srv.strip() for srv in idx.split("\n") if srv.strip()]
        return idx_srvs  # noqa: RET504

    def _add_index_server(self) -> None:
        """Add index-server to 'distutil's 'index-servers' param."""
        index_servers = "\n\t".join(self.servers.keys())
        self.conf.set("distutils", "index-servers", index_servers)

    @property
    def servers(self) -> dict[str, dict[str, str]]:
        """index-servers configured in pypirc."""
        return self._servers

    @servers.setter
    def servers(self, server: dict[str, dict[str, str]]) -> None:
        """Add index-servers to pypirc."""
        self._servers.update(server)
