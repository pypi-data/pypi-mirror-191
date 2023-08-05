from __future__ import annotations

from os import PathLike
from typing import TYPE_CHECKING, Any, Dict, Optional, TypeVar, Union

from chalk.sql._internal.sql_source import BaseSQLSource, TableIngestMixIn
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


T = TypeVar("T")


class SQLiteInMemorySourceImpl(TableIngestMixIn, BaseSQLSource, SQLSourceWithTableIngestProtocol):
    def __init__(self, name: Optional[str] = None):
        self.ingested_tables: Dict[str, Any] = {}
        BaseSQLSource.__init__(self, name=name)

    def local_engine_url(self) -> URL:
        try:
            from sqlalchemy.engine.url import URL
        except ImportError:
            raise missing_dependency_exception("chalkpy[sqlite]")
        return URL.create(drivername="sqlite", database=":memory:", query={"check_same_thread": "true"})


class SQLiteFileSourceImpl(TableIngestMixIn, BaseSQLSource, SQLSourceWithTableIngestProtocol):
    def __init__(self, filename: Union[PathLike, str], name: Optional[str] = None):
        self.filename = str(filename)
        self.ingested_tables: Dict[str, Any] = {}
        BaseSQLSource.__init__(self, name=name)

    def local_engine_url(self) -> URL:
        try:
            from sqlalchemy.engine.url import URL
        except ImportError:
            raise missing_dependency_exception("chalkpy[sqlite]")
        return URL.create(drivername="sqlite", database=self.filename, query={"check_same_thread": "true"})
