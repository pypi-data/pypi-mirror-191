# SPDX-License-Identifier: GPL-2.0-or-later
"""
repository helpers
"""
import subprocess
import re
from pathlib import Path
from typing import List, Optional
from bs4 import BeautifulSoup  # type: ignore
from .repo import Repo, _logger, shortest_path


class SvnRepo(Repo):
    """
    svn repository helper implementation
    """

    vcs = "svn"

    def __init__(  # pylint: disable=too-many-arguments
        self,
        url: Optional[str],
        path: Path,
        target_commit: Optional[str] = None,
        tag: Optional[str] = None,
        branch: Optional[str] = None,
        remote_path: Optional[str] = None,
        options: Optional[List[str]] = None,
    ):
        rurl = url
        rpath = remote_path
        if url is not None:
            rurl = SvnRepo.get_remote_info(url, "repos-root-url")
            toks = SvnRepo.get_remote_info(url, "relative-url")[2:].split("/")
            if toks[0] == "tags" and len(toks) > 1:
                tag = toks[1]
                rpath = "/".join(toks[2:])
            elif toks[0] == "branches" and len(toks) > 1:
                branch = toks[1]
                rpath = "/".join(toks[2:])
            elif toks[0] == "trunk":
                rpath = "/".join(toks[1:])
            if rpath == "":
                rpath = remote_path
        super().__init__(
            rurl,
            path,
            target_commit=target_commit,
            tag=tag,
            branch=branch,
            remote_path=rpath,
            options=options,
        )

    @property
    def vcs_dir(self):
        return self.path / ".svn"

    def add(self, file: Path):
        _logger.info("Adding %s", file)
        self.execute(f"add --parents {file}".split(), check=False, capture_output=True)

    def remove(self, file: Path):
        _logger.info("Removing %s", file)
        self.execute(f"rm --force {file}".split(), check=False, capture_output=True)

    def checkout(self):
        cmd = ["co"]
        if self.target_commit is not None:
            cmd.append("-r" + self.target_commit)
        cmd.extend(self.options)

        url = self.url
        if self.tag is not None:
            url += f"/tags/{self.tag}"
        elif self.branch is not None:
            if self.branch == "trunk":
                url += "/trunk"
            else:
                url += f"/branches/{self.branch}"
        else:
            url += "/trunk"
        if self.remote_path is not None:
            url += f"/{self.remote_path}"
        cmd.append(url)

        cmd.append(self.path)
        _logger.info("Checking out %s into %s", url, shortest_path(self.path))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.execute(cmd, cwd=self.path.parent)

    def update(self):
        _logger.info("Updating %s", shortest_path(self.path))
        cmd = ["update"]
        if self.target_commit is not None:
            cmd.append(f"-r{self.target_commit}")
        self.execute(cmd)

    def status(self):
        stat = SvnRepo.get_remote_info(self.path, "relative-url")
        stat += "\n" + self.execute("status", capture_output=True).stdout.decode()

        dirty = ""
        if self.is_dirty():
            dirty = "[D] "

        _logger.info("%s: %s%s\n", shortest_path(self.path), dirty, stat.strip())

    def has_externals(self, relpath: str = ".", recursive: bool = True):
        if not (self.path / relpath).exists():
            return False
        if recursive:
            cmd = "pget -R".split()
        else:
            cmd = "pget".split()
        cmd.append("svn:externals")
        cmd.append(relpath)

        if recursive:
            return (
                self.execute(cmd, capture_output=True).stdout.decode().strip() != ". -"
            )

        return self.execute(cmd, check=False, capture_output=True).returncode == 0

    def is_dirty(self, relpath: str = "."):
        out = self.execute(
            f"st --xml --depth immediates {relpath}".split(),
            capture_output=True,
        ).stdout
        soup = BeautifulSoup(out, "xml")
        regex = re.compile("unversioned|modified|added|deleted")
        return bool(soup.find_all("wc-status", attrs={"item": regex}))

    def list_externals(self, relpath: str = ".") -> List[Repo]:
        return_list: List[Repo] = []

        if not (self.path / relpath).exists():
            return return_list

        try:
            out = self.execute(
                f"pget svn:externals {relpath}".split(), capture_output=True
            )

            for line in out.stdout.decode().split("\n"):
                if len(line.strip()) > 0:
                    _logger.debug("processing external: '%s'", line)
                    ext = line.split()
                    options = []
                    target_commit = None
                    for opt in ext[1:-1]:
                        if re.match("^-r[0-9]+$", opt):
                            target_commit = opt[2:]
                        else:
                            options.append(opt)

                    return_list.append(
                        SvnRepo(
                            ext[-1],
                            self.path / relpath / ext[0],
                            target_commit=target_commit,
                            options=options,
                        )
                    )
        except subprocess.CalledProcessError:
            pass

        return return_list

    def list_files(self):
        _logger.info("Listing %s files", shortest_path(self.path))
        self.execute("ls -R".split())

    def list_folders(self, printout: bool = True):
        return self._return_local_folders(
            self.execute("ls -R".split(), capture_output=True).stdout.decode(), printout
        )

    def rm_externals(self, relpath: str = "."):
        _logger.info("Delete svn:externals property from %s", relpath)
        self.execute(f"pdel svn:externals {relpath}".split())

    def reset_externals(self, relpath: str = "."):
        _logger.info("Restore svn:externals property for %s", relpath)
        self.execute(f"revert --depth empty {relpath}".split())

    def add_ignores(self, *patterns: Path):
        ignores_map = {}
        for pattern in patterns:
            relpath = pattern.relative_to(self.path).parent
            if relpath not in ignores_map:
                ignores_map[relpath] = (
                    False,
                    [
                        i.strip()
                        for i in self.execute(
                            f"pget svn:ignore {relpath}".split(),
                            check=False,
                            capture_output=True,
                        )
                        .stdout.decode()
                        .splitlines()
                    ],
                )
            if pattern.name in ignores_map[relpath][1]:
                _logger.info(
                    "Ignore rule %s already exists in %s", pattern.name, relpath
                )
            else:
                _logger.info("Append ignore rule %s to %s", pattern.name, relpath)
                ignores_map[relpath] = (True, [*ignores_map[relpath][1], pattern.name])

        for relpath, ignores in ignores_map.items():
            if ignores[0]:
                self.add(relpath)

                cmd = "pset svn:ignore".split()
                cmd.append("\n".join(sorted(ignores[1])))
                cmd.append(str(relpath))
                self.execute(cmd)

    def del_ignores(self, *patterns: Path):
        ignores_map = {}
        for pattern in patterns:
            relpath = pattern.relative_to(self.path).parent
            if relpath not in ignores_map:
                ignores_map[relpath] = (
                    False,
                    [
                        i.strip()
                        for i in self.execute(
                            f"pget svn:ignore {relpath}".split(),
                            check=False,
                            capture_output=True,
                        )
                        .stdout.decode()
                        .splitlines()
                    ],
                )
            if pattern.name in ignores_map[relpath][1]:
                _logger.info("Delete ignore rule %s from %s", pattern, relpath)
                ignores_map[relpath] = (
                    True,
                    [i for i in ignores_map[relpath][1] if i != pattern.name],
                )

        for relpath, ignores in ignores_map.items():
            if ignores[0]:
                cmd = "pset svn:ignore".split()
                cmd.append("\n".join(sorted(ignores[1])))
                cmd.append(str(relpath))
                self.execute(cmd)

    def commit(self, message: str, files: List[Path]):
        raise NotImplementedError()

    @staticmethod
    def get_remote_info(url, field):
        """
        get repository info using svn info --show-item command
        valid fields are:
            'kind'       node kind of TARGET
            'url'        URL of TARGET in the repository
            'relative-url'
                            repository-relative URL of TARGET
            'repos-root-url'
                            root URL of repository
            'repos-uuid' UUID of repository
            'repos-size' for files, the size of TARGET
                            in the repository
            'revision'   specified or implied revision
            'last-changed-revision'
                            last change of TARGET at or before
                            'revision'
            'last-changed-date'
                            date of 'last-changed-revision'
            'last-changed-author'
                            author of 'last-changed-revision'
            'wc-root'    root of TARGET's working copy
            'schedule'   'normal','add','delete','replace'
            'depth'      checkout depth of TARGET in WC
            'changelist' changelist of TARGET in WC
        """
        # pylint: disable=subprocess-run-check
        return (
            subprocess.run(
                ["svn", "info", "--show-item", field, url], capture_output=True
            )
            .stdout.decode()
            .strip()
        )

    @staticmethod
    def check_remote(url):
        cmd = f"svn info {url}".split()
        # pylint: disable=subprocess-run-check
        return subprocess.run(cmd, capture_output=True).returncode == 0
