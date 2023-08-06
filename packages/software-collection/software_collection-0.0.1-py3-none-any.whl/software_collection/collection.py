import os
from git import Repo
from urllib.parse import urlparse
from pathlib import Path
from dataclasses import dataclass
from shutil import rmtree

ROOTDIR = os.environ.get("SOFTWARE_COLLECTION_ROOT", "/var/lib/software")


def name_from_url(url):
    if url[0:4] == "git@":
        url = "ssh://" + url
    parse_result = urlparse(url)

    if parse_result.scheme == "file":
        name = "local"
    elif parse_result.hostname:
        name = parse_result.hostname
    else:
        raise Exception(f"no hostname: {url}")

    name += parse_result.path.replace("~", "")

    if name.endswith(".git"):
        name = name[0:-4]

    return name


def is_url(s):
    return (
        s[0:4] == "git@" or s[0:6] == "ssh://" or s[0:4] == "http" or s[0:5] == "https"
    )


@dataclass
class LocalRepo:
    name: str
    fullpath: str
    url: str
    commit: str

    def host(self):
        return self.name.split("/")[0]

    def slash_count(self):
        return self.name.count("/")

    def status_str(self):
        return "\t".join([self.name, self.fullpath, self.url, self.commit])


class Collection:
    def __init__(self):
        self.repos = []

        for host_folder in os.listdir(ROOTDIR):
            for dirpath, dirnames, filenames in os.walk(
                Path(ROOTDIR).joinpath(host_folder)
            ):
                if ".git" in dirnames:
                    name = dirpath.removeprefix(ROOTDIR).removeprefix("/")
                    git_repo = Repo(dirpath)

                    self.repos.append(
                        LocalRepo(
                            name=name,
                            fullpath=dirpath,
                            url=git_repo.remotes[0].url,
                            commit=str(git_repo.head.commit),
                        )
                    )

                    dirnames[:] = []  # stop at this level

    def filter(self, term):
        matches = []
        url_provided = is_url(term)

        for r in self.repos:
            if url_provided and term == r.url:
                matches.append(r)
            elif r.name == term:
                matches.append(r)
            elif "/".join(r.name.split("/")[1:]) == term:
                matches.append(r)
            elif r.slash_count() >= 2 and "/".join(r.name.split("/")[2:]) == term:
                matches.append(r)

        return matches

    @classmethod
    def find(cls, term):
        term = term.lower()

        matches = cls().filter(term)

        if len(matches) == 1:
            return matches[0]
        elif len(matches) == 0:
            raise Exception(f"No matching repo found {term}")
        else:
            raise Exception(f"Found {len(matches)} repos for {term}")

    @classmethod
    def add(cls, url):
        if not is_url(url):
            raise Exception(f"this is not a url: {url}")

        name = name_from_url(url)
        local_path = Path(ROOTDIR).joinpath(name)

        if local_path.exists():
            raise Exception(f"local path exists: {local_path}")

        local_path.mkdir(parents=True, exist_ok=True)
        Repo.clone_from(url, str(local_path))

    @classmethod
    def remove(cls, name):
        repo = cls.find(name)
        rmtree(repo.fullpath)
