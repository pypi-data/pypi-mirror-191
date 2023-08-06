# bumbo/orm.py

import inspect
import sqlite3


class Database:
    def __init__(self, path):
        self.conn = sqlite3.Connection(path)

    @property
    def tables(self):
        SELECT_TABLES_SQL = "SELECT name FROM sqlite_master WHERE type = 'table';"
        return [ x[0] for x in self.conn.execute(SELECT_TABLES_SQL).fetchall() ]

    def create(self, table):
        self.conn.execute(table._get_create_sql())
    
    def save(self, instance):
        sql, values = instance._get_insert_sql()
        cursor = self.conn.execute(sql, values)
        instance._data["id"] = cursor.lastrowid
        self.conn.commit()


    def all(self, table):
        sql, fields = table._get_select_all_sql()

        result = []
        for row in self.conn.execute(sql).fetchall():
            instance = table()
            for field, value in zip(fields, row):
                if field.endswith('_id'):
                    field = field[:-3]
                    model_fk = getattr(table, field)
                    value = self.get(model_fk.table, id=value)  # value == instance_fk
                setattr(instance, field, value)
            result.append(instance)
        print(f"all: {sql}\n{result}")
        return result

    def get(self, table, id):
        sql, fields, params = table._get_select_where_sql(id=id)

        row = self.conn.execute(sql, params).fetchone()
        if not row:
            raise Exception(f"{table.__name__} instance with id {id} does not exists")

        instance = table()
        for field, value in zip(fields, row):
            if field.endswith('_id'):
                field = field[:-3]
                #print(f"get\ntable: {table}   field: {field}")
                model_fk = getattr(table, field)
                #print(f"get\nmodel_fk: {model_fk}    model_fk.table: {model_fk.table}")
                value = self.get(model_fk.table, id=value)  # value == instance_fk
                #print(f"value (instance_fk): {value}; id: {value.id}; name: {value.name}")
            setattr(instance, field, value)

        return instance

    def update(self, instance):
        sql, values = instance._get_update_sql()
        self.conn.execute(sql, values)
        self.conn.commit()

    def delete(self, instance, fk):
        sql, values = instance._get_delete_sql(fk)
        self.conn.execute(sql, values)
        self.conn.commit()


class Table:
    def __init__(self, **kwargs):
        self._data = {
            "id": None
        }

        for key, value in kwargs.items():
            self._data[key] = value

    def __getattribute__(self, key):
        _data = super().__getattribute__("_data")
        if key in _data:
            return _data[key]
        return super().__getattribute__(key)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self._data:
            self._data[key] = value

    @classmethod
    def _get_create_sql(cls):
        CREATE_TABLE_SQL = "CREATE TABLE IF NOT EXISTS {name} ({fields});"
        fields_lst = [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
        ]
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields_lst.append(f"{name.lower()} {field.sql_type}")
            elif isinstance(field, ForeignKey):
                fields_lst.append(f"{name.lower()}_id INTEGER")
        fields_str = ", ".join(fields_lst)
        name = cls.__name__.lower()
        return CREATE_TABLE_SQL.format(name=name, fields=fields_str)


    @classmethod
    def _get_select_all_sql(cls):
        SELECT_ALL_SQL = "SELECT {fields} FROM {name};"

        fields = ['id']
        for name, field_type in inspect.getmembers(cls):
            if isinstance(field_type, Column):
                fields.append(name)
            elif isinstance(field_type, ForeignKey):
                fields.append(name + "_id")

        sql = SELECT_ALL_SQL.format(
            name=cls.__name__.lower(),
            fields=", ".join(fields)
        )
        return sql, fields


    def _get_insert_sql(self):
        INSERT_SQL = "INSERT INTO {name} ({fields}) VALUES ({placeholders});"
        cls = self.__class__
        fields = []
        placeholders = []
        values = []

        for name, field_type in inspect.getmembers(cls):
            if isinstance(field_type, Column):
                fields.append(name)
                values.append(getattr(self, name))
                placeholders.append("?")
            elif isinstance(field_type, ForeignKey):
                fields.append(name + "_id")
                values.append(getattr(self, name).id)
                placeholders.append("?")

        fields = ", ".join(fields)
        placeholders = ", ".join(placeholders)

        sql = INSERT_SQL.format(
            name=cls.__name__.lower(),
            fields=fields,
            placeholders=placeholders
        )
        print(sql, values, sep="\n")
        return sql, values

    @classmethod
    def _get_select_where_sql(cls, id):
        SELECT_WHERE_SQL = "SELECT {fields} FROM {name} WHERE id = ?;"
        fields = ["id"]
        for name, field_type in inspect.getmembers(cls):
            if isinstance(field_type, Column):
                fields.append(name)
            elif isinstance(field_type, ForeignKey):
                fields.append(name + "_id")

        sql = SELECT_WHERE_SQL.format(
            name=cls.__name__.lower(),
            fields=", ".join(fields)
        )
        params = [id]

        return sql, fields, params

    def _get_update_sql(self):
        UPDATE_SQL = "UPDATE {name} SET {fields} WHERE id = ?"
        cls = self.__class__
        fields = []
        values = []

        for name, field_type in inspect.getmembers(cls):
            if isinstance(field_type, Column):
                fields.append(name)
                values.append(getattr(self, name))
            elif isinstance(field_type, ForeignKey):
                fields.append(name + "_id")
                values.append(getattr(self, name).id)

        values.append(getattr(self, 'id'))

        sql = UPDATE_SQL.format(
            name=cls.__name__.lower(),
            fields=", ".join([f"{field} = ?" for field in fields])
        )

        return sql, values

    @classmethod
    def _get_delete_sql(cls, fk):
        DELETE_SQL = "DELETE FROM {name} WHERE id = ?"
        sql = DELETE_SQL.format(name=cls.__name__.lower())
        return sql, [fk]


class Column:
    def __init__(self, column_type):
        self.type = column_type

    @property
    def sql_type(self):
        SQLITE_TYPE_MAP = {
            int: "INTEGER",
            float: "REAL",
            str: "TEXT",
            bytes: "BLOB",
            bool: "INTEGER",
        }
        return SQLITE_TYPE_MAP[self.type]


class ForeignKey:
    # table == model
    def __init__(self, table):
        self.table = table


