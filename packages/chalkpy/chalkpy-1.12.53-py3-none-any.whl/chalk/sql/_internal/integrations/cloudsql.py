from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping, Optional

from chalk.sql._internal.sql_source import BaseSQLSource
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


class CloudSQLSourceImpl(BaseSQLSource):
    def __init__(
        self,
        *,
        instance_name: Optional[str] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
    ):
        try:
            import psycopg2
        except ImportError:
            raise missing_dependency_exception("chalkpy[postgresql]")
        del psycopg2  # unused
        prefix = name + "_" if name else ""
        self.instance_name = instance_name or os.getenv(prefix + "CLOUDSQL_INSTANCE_NAME")
        self.db = db or os.getenv(prefix + "CLOUDSQL_DATABASE")
        self.user = user or os.getenv(prefix + "CLOUDSQL_USER")
        self.password = password or os.getenv(prefix + "CLOUDSQL_PASSWORD")

        BaseSQLSource.__init__(self, name=name)

    def engine_args(self) -> Mapping[str, Any]:
        return dict(
            pool_size=20,
            max_overflow=60,
            # Trying to fix mysterious dead connection issue
            connect_args={
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="postgresql",
            username=self.user,
            password=self.password,
            host="",
            query={"host": "{}/{}/.s.PGSQL.5432".format("/cloudsql", self.instance_name)},
            database=self.db,
        )
