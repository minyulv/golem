from unittest.mock import patch

from golem import model as m
from golem.database import Database
from golem.testutils import PEP8MixIn, TempDirFixture


class TestDatabase(TempDirFixture, PEP8MixIn):
    PEP8_FILES = ["golem/model.py", "golem/database/database.py"]

    def setUp(self):
        TempDirFixture.setUp(self)
        self.database = Database(m.db, self.path, m.DB_MODELS)

    def tearDown(self):
        self.database.close()
        TempDirFixture.tearDown(self)

    @patch('golem.database.migration.migrate.migrate_schema')
    def test_init(self, migrate_schema):
        self.assertFalse(self.database.db.is_closed())
        self.assertFalse(migrate_schema.called)

        for model in m.DB_MODELS:
            self.assertTrue(model.table_exists())

    def test_schema_version(self):
        self.assertEqual(self.database.get_user_version(),
                         self.database.SCHEMA_VERSION)
        self.assertNotEqual(self.database.SCHEMA_VERSION, 0)

        self.database.set_user_version(0)
        self.assertEqual(self.database.get_user_version(), 0)

        database = Database(m.db, self.path, m.DB_MODELS)
        self.assertEqual(database.get_user_version(), database.SCHEMA_VERSION)
        database.close()
