from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


class RedshiftSourceImpl(BaseSQLSource):
    def __init__(
        self,
        host: Optional[str] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
    ):
        try:
            import redshift_connector
        except ImportError:
            raise missing_dependency_exception("chalkpy[redshift]")
        del redshift_connector
        self.host = host or load_integration_variable(name="REDSHIFT_HOST", integration_name=name)
        self.db = db or load_integration_variable(name="REDSHIFT_DB", integration_name=name)
        self.user = user or load_integration_variable(name="REDSHIFT_USER", integration_name=name)
        self.password = password or load_integration_variable(name="REDSHIFT_PASSWORD", integration_name=name)
        BaseSQLSource.__init__(self, name=name)

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="redshift+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.db,
        )
