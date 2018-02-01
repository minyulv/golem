SCHEMA_VERSION = 10
from golem.model import *  # pylint: disable=unused-import

"""Peewee migrations -- 010_schema.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee as pw

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    migrator.remove_fields('expectedincome', 'task')

    migrator.drop_index('hardwarepreset', 'name')

    migrator.add_index('hardwarepreset', 'name', unique=True)

    migrator.remove_fields('income', 'block_number', 'task')

    migrator.drop_index('performance', 'environment_id')

    migrator.add_index('performance', 'environment_id', unique=True)


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.drop_index('performance', 'environment_id')

    migrator.add_index('performance', 'environment_id', unique=True)

    migrator.add_fields(
        'income',

        block_number=pw.BigIntegerField(),
        task=pw.CharField(max_length=255))

    migrator.drop_index('hardwarepreset', 'name')

    migrator.add_index('hardwarepreset', 'name', unique=True)

    migrator.add_fields(
        'expectedincome',

        task=pw.CharField(max_length=255))
