import re
from typing import Dict, Generator, Iterable, List, Self, Tuple

from .pathlist import PathList
from .pathutil import Path


class HashList:
    def __init__(self, files: str, algorithm: str = None):
        self.files = PathList(files)
        self.algorithm = Path.algorithm(algorithm)

    @property
    def filedigest(self) -> Dict[Path, str]:
        try:
            return self._filedigest
        except AttributeError:
            self._filedigest = dict(zip(self.files, self.hexdigest))

        return self._filedigest

    @property
    def hexdigest(self) -> List[str]:
        try:
            return self._hexdigest
        except AttributeError:
            def digest(x: Path):
                try:
                    return x.hexdigest(self.algorithm).upper()
                except (FileNotFoundError, PermissionError):
                    return None

            self._hexdigest = self.files.apply(digest)

        return self._hexdigest

    def missing(self):
        for file, hash in self:
            if hash:
                continue

            yield file

    def __iter__(self):
        for item in self.filedigest.items():
            yield item

    def __getitem__(self, item: Path) -> str:
        return self.filedigest[item]

    def __len__(self):
        return len(self.filedigest)

    def __str__(self):
        return str(self.filedigest)

    def __repr__(self):
        return f"{self.__class__.__name__}({[str(f) for f in self.files]}, algorithm='{self.algorithm}')"


class HashSum(HashList):
    def __init__(self, files: Iterable, hashfile: str, algorithm: str = None, comments: str = None, relative: bool = False):

        self.root = Path(hashfile)

        if not algorithm:
            algorithm = self.root.suffix

        super().__init__(files, algorithm)

        self.comments = comments

        self.save(self.root, relative=relative)

    def __repr__(self):
        files = [str(f) for f in self.files]
        comment = str('\n').join(self.comments)
        return f"{self.__class__.__name__}({files}, '{self.root}', algorithm='{self.algorithm}', comments='{comment}')"

    @staticmethod
    def strip_comments(comment: str) -> str:
        return comment.lstrip('# ')

    @classmethod
    def split_comments(cls, comments: str) -> List[str]:
        try:
            return [cls.strip_comments(line) for line in comments.split('\n')]
        except AttributeError:
            return list()

    @property
    def comments(self) -> List[str]:
        return self._comments

    @comments.setter
    def comments(self, comments: str):
        self._comments = self.split_comments(comments)

    def items(self) -> Tuple[Path, str]:
        for file, hash in self:
            yield file, hash

    def save(self, filename: str, comments: str = None, relative: bool = False) -> None:
        if not all(self.hexdigest):
            raise FileNotFoundError(list(self.missing()))

        self.root = Path(filename).resolve().with_suffix(
            self.algorithm, separator=True)

        if not comments:
            comments = self.comments
        else:
            comments = self.split_comments(comments)

        with self.root.open(mode='wt', encoding='utf-8') as f:

            if comments:
                for line in comments:
                    f.write(f"# {line}\n")

                f.write('\n')

            for filename, hash in self.items():
                filename = filename.resolve()

                try:
                    filename = filename.relative_to(
                        self.root.parent, uptree=relative)
                except ValueError:
                    pass

                f.write(f"{hash} *{filename}\n")


class HashFile(HashSum):
    regex = re.compile(
        r'^(?P<hash>[0-9a-f]{8,}) \*(?P<file>.*?)$', re.IGNORECASE)

    def __init__(self, filename: str, algorithm: str = None):
        self._comments = list()

        files = list()
        self._hashes = list()

        self.root = Path(filename).resolve()

        if not algorithm:
            algorithm = self.root.suffix

        for line in self.root.iter_lines(encoding='utf-8'):
            if not line:
                continue

            if line.startswith('#'):
                self._comments.append(self.strip_comments(line))
                continue

            match = self.regex.match(line)

            try:
                file = Path(match.group('file'))
                hash = match.group('hash')
            except (AttributeError, KeyError):
                continue

            if not file.is_absolute():
                file = self.root.parent.joinpath(file).resolve()

            files.append(file)
            self._hashes.append(hash)

        super(HashSum, self).__init__(files, algorithm)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.root}', algorithm='{self.algorithm}')"

    @property
    def hashes(self) -> List[str]:
        return self._hashes

    @property
    def filedigest(self) -> Dict[Path, Tuple[str, str]]:
        try:
            return self._filedigest
        except AttributeError:
            self._filedigest = dict(
                zip(self.files, tuple(zip(self.hashes, self.hexdigest)))
            )

        return self._filedigest

    def __getitem__(self, item: Path) -> str:
        _, digest = self.filedigest[item]

        return digest

    def items(self) -> Tuple[Path, str]:
        for file, (_, digest) in self:
            yield file, digest

    def missing(self):
        for file, (_, digest) in self:
            if digest:
                continue

            yield file

    def match(self):
        for file, (hash, digest) in self:
            if not digest:
                continue

            if hash == digest:
                yield file

    def modified(self):
        for file, (hash, digest) in self:
            if not digest:
                continue

            if hash != digest:
                yield file
