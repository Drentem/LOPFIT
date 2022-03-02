from .. import config
from .. import engines
from .. import fixtures
from ..assertions import eq_
from ..config import requirements
from ..schema import Column
from ..schema import Table
from ... import Integer
from ... import literal
from ... import literal_column
from ... import select
from ... import String


class LastrowidTest(fixtures.TablesTest):
    run_deletes = "each"

    __backend__ = True

    __requires__ = "implements_get_lastrowid", "autoincrement_insert"

    __engine_options__ = {"implicit_returning": False}

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "autoinc_pk",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("data", String(50)),
        )

        Table(
            "manual_pk",
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=False),
            Column("data", String(50)),
        )

    def _assert_round_trip(self, table, conn):
        row = conn.execute(table.select()).first()
        eq_(
            row,
            (
                conn.dialect.default_sequence_base,
                "some data",
            ),
        )

    def test_autoincrement_on_insert(self, connection):

        connection.execute(
            self.tables.autoinc_pk.insert(), dict(data="some data")
        )
        self._assert_round_trip(self.tables.autoinc_pk, connection)

    def test_last_inserted_id(self, connection):

        r = connection.execute(
            self.tables.autoinc_pk.insert(), dict(data="some data")
        )
        pk = connection.scalar(select(self.tables.autoinc_pk.c.id))
        eq_(r.inserted_primary_key, (pk,))

    @requirements.dbapi_lastrowid
    def test_native_lastrowid_autoinc(self, connection):
        r = connection.execute(
            self.tables.autoinc_pk.insert(), dict(data="some data")
        )
        lastrowid = r.lastrowid
        pk = connection.scalar(select(self.tables.autoinc_pk.c.id))
        eq_(lastrowid, pk)


class InsertBehaviorTest(fixtures.TablesTest):
    run_deletes = "each"
    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "autoinc_pk",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("data", String(50)),
        )
        Table(
            "manual_pk",
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=False),
            Column("data", String(50)),
        )
        Table(
            "includes_defaults",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("data", String(50)),
            Column("x", Integer, default=5),
            Column(
                "y",
                Integer,
                default=literal_column("2", type_=Integer) + literal(2),
            ),
        )

    @requirements.autoincrement_insert
    def test_autoclose_on_insert(self):
        if requirements.returning.enabled:
            engine = engines.testing_engine(
                options={"implicit_returning": False}
            )
        else:
            engine = config.db

        with engine.begin() as conn:
            r = conn.execute(
                self.tables.autoinc_pk.insert(), dict(data="some data")
            )
        assert r._soft_closed
        assert not r.closed
        assert r.is_insert

        # new as of I8091919d45421e3f53029b8660427f844fee0228; for the moment
        # an insert where the PK was taken from a row that the dialect
        # selected, as is the case for mssql/pyodbc, will still report
        # returns_rows as true because there's a cursor description.  in that
        # case, the row had to have been consumed at least.
        assert not r.returns_rows or r.fetchone() is None

    @requirements.returning
    def test_autoclose_on_insert_implicit_returning(self, connection):
        r = connection.execute(
            self.tables.autoinc_pk.insert(), dict(data="some data")
        )
        assert r._soft_closed
        assert not r.closed
        assert r.is_insert

        # note we are experimenting with having this be True
        # as of I8091919d45421e3f53029b8660427f844fee0228 .
        # implicit returning has fetched the row, but it still is a
        # "returns rows"
        assert r.returns_rows

        # and we should be able to fetchone() on it, we just get no row
        eq_(r.fetchone(), None)

        # and the keys, etc.
        eq_(r.keys(), ["id"])

        # but the dialect took in the row already.   not really sure
        # what the best behavior is.

    @requirements.empty_inserts
    def test_empty_insert(self, connection):
        r = connection.execute(self.tables.autoinc_pk.insert())
        assert r._soft_closed
        assert not r.closed

        r = connection.execute(
            self.tables.autoinc_pk.select().where(
                self.tables.autoinc_pk.c.id != None
            )
        )
        eq_(len(r.all()), 1)

    @requirements.empty_inserts_executemany
    def test_empty_insert_multiple(self, connection):
        r = connection.execute(self.tables.autoinc_pk.insert(), [{}, {}, {}])
        assert r._soft_closed
        assert not r.closed

        r = connection.execute(
            self.tables.autoinc_pk.select().where(
                self.tables.autoinc_pk.c.id != None
            )
        )

        eq_(len(r.all()), 3)

    @requirements.insert_from_select
    def test_insert_from_select_autoinc(self, connection):
        src_table = self.tables.manual_pk
        dest_table = self.tables.autoinc_pk
        connection.execute(
            src_table.insert(),
            [
                dict(id=1, data="data1"),
                dict(id=2, data="data2"),
                dict(id=3, data="data3"),
            ],
        )

        result = connection.execute(
            dest_table.insert().from_select(
                ("data",),
                select(src_table.c.data).where(
                    src_table.c.data.in_(["data2", "data3"])
                ),
            )
        )

        eq_(result.inserted_primary_key, (None,))

        result = connection.execute(
            select(dest_table.c.data).order_by(dest_table.c.data)
        )
        eq_(result.fetchall(), [("data2",), ("data3",)])

    @requirements.insert_from_select
    def test_insert_from_select_autoinc_no_rows(self, connection):
        src_table = self.tables.manual_pk
        dest_table = self.tables.autoinc_pk

        result = connection.execute(
            dest_table.insert().from_select(
                ("data",),
                select(src_table.c.data).where(
                    src_table.c.data.in_(["data2", "data3"])
                ),
            )
        )
        eq_(result.inserted_primary_key, (None,))

        result = connection.execute(
            select(dest_table.c.data).order_by(dest_table.c.data)
        )

        eq_(result.fetchall(), [])

    @requirements.insert_from_select
    def test_insert_from_select(self, connection):
        table = self.tables.manual_pk
        connection.execute(
            table.insert(),
            [
                dict(id=1, data="data1"),
                dict(id=2, data="data2"),
                dict(id=3, data="data3"),
            ],
        )

        connection.execute(
            table.insert()
            .inline()
            .from_select(
                ("id", "data"),
                select(table.c.id + 5, table.c.data).where(
                    table.c.data.in_(["data2", "data3"])
                ),
            )
        )

        eq_(
            connection.execute(
                select(table.c.data).order_by(table.c.data)
            ).fetchall(),
            [("data1",), ("data2",), ("data2",), ("data3",), ("data3",)],
        )

    @requirements.insert_from_select
    def test_insert_from_select_with_defaults(self, connection):
        table = self.tables.includes_defaults
        connection.execute(
            table.insert(),
            [
                dict(id=1, data="data1"),
                dict(id=2, data="data2"),
                dict(id=3, data="data3"),
            ],
        )

        connection.execute(
            table.insert()
            .inline()
            .from_select(
                ("id", "data"),
                select(table.c.id + 5, table.c.data).where(
                    table.c.data.in_(["data2", "data3"])
                ),
            )
        )

        eq_(
            connection.execute(
                select(table).order_by(table.c.data, table.c.id)
            ).fetchall(),
            [
                (1, "data1", 5, 4),
                (2, "data2", 5, 4),
                (7, "data2", 5, 4),
                (3, "data3", 5, 4),
                (8, "data3", 5, 4),
            ],
        )


class ReturningTest(fixtures.TablesTest):
    run_create_tables = "each"
    __requires__ = "returning", "autoincrement_insert"
    __backend__ = True

    __engine_options__ = {"implicit_returning": True}

    def _assert_round_trip(self, table, conn):
        row = conn.execute(table.select()).first()
        eq_(
            row,
            (
                conn.dialect.default_sequence_base,
                "some data",
            ),
        )

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "autoinc_pk",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("data", String(50)),
        )

    @requirements.fetch_rows_post_commit
    def test_explicit_returning_pk_autocommit(self, connection):
        table = self.tables.autoinc_pk
        r = connection.execute(
            table.insert().returning(table.c.id), dict(data="some data")
        )
        pk = r.first()[0]
        fetched_pk = connection.scalar(select(table.c.id))
        eq_(fetched_pk, pk)

    def test_explicit_returning_pk_no_autocommit(self, connection):
        table = self.tables.autoinc_pk
        r = connection.execute(
            table.insert().returning(table.c.id), dict(data="some data")
        )
        pk = r.first()[0]
        fetched_pk = connection.scalar(select(table.c.id))
        eq_(fetched_pk, pk)

    def test_autoincrement_on_insert_implicit_returning(self, connection):

        connection.execute(
            self.tables.autoinc_pk.insert(), dict(data="some data")
        )
        self._assert_round_trip(self.tables.autoinc_pk, connection)

    def test_last_inserted_id_implicit_returning(self, connection):

        r = connection.execute(
            self.tables.autoinc_pk.insert(), dict(data="some data")
        )
        pk = connection.scalar(select(self.tables.autoinc_pk.c.id))
        eq_(r.inserted_primary_key, (pk,))


__all__ = ("LastrowidTest", "InsertBehaviorTest", "ReturningTest")
