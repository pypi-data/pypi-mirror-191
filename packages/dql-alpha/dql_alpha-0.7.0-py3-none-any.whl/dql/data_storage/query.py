from funcy import cached_property, keep, lcat, lmap, split_at


class Schema:
    @property
    def table(self):
        raise ValueError("Should either set table on schema or pass it to Query")

    @cached_property
    def fields_sql(self):
        return ", ".join(self.fields)  # pylint: disable=no-member


class Query:
    OP_TO_SQL = {"eq": "==", "ne": "!=", "gt": ">", "gte": ">=", "lt": "<", "lte": "<="}

    def __init__(self, db, schema, table=None, wrap=None):
        self.db = db
        self._schema = schema
        self._table = table or schema.table
        self._wrap = wrap
        self._where = {}
        self._order_by = []

    def wrap(self, wrap):
        self._wrap = wrap
        return self

    def where(self, **conds):
        if self._where:
            raise NotImplementedError("Can only use .where() once")
        self._where = conds
        return self

    def order_by(self, order):
        if self._order_by:
            raise NotImplementedError("Can only use .order_by() once")
        self._order_by = [order] if isinstance(order, str) else order
        return self

    # Methods that touch db
    def all(self, *exps):
        sql, params = self._compile_select(exps)
        rows = self.db.execute(sql, params).fetchall()
        return lmap(self._wrap, rows) if self._wrap and not exps else rows

    def col(self, exp):
        return [row[0] for row in self.all(exp)]

    def get(self, *exps):
        rows = self.all(*exps)
        if not rows:
            return None
        assert len(rows) <= 1, f"Too many matches for {self._where}: {len(rows)}"
        return rows[0]

    def insert(self, entry, upsert=False):
        (sql, params) = self._compile_insert(entry, upsert=upsert)
        return self.db.execute(sql, params).lastrowid

    def insertmany(self, entries):
        (first_entry,), rest = split_at(1, entries)
        sql, params = self._compile_insert(first_entry)
        params = [params] + [[e.get(f) for f in first_entry] for e in rest]
        return self.db.executemany(sql, params)

    def update(self, **sets):
        sql, params = self._compile_update(sets)
        return self.db.execute(sql, params).fetchall()

    def delete(self):
        sql, params = self._compile_delete()
        return self.db.execute(sql, params).fetchall()

    # Methods to generate SQL
    def _compile_select(self, exps=None):
        what = ", ".join(exps) if exps else self._schema.fields_sql
        select = f"""SELECT {what} FROM {self._table}""", ()
        where = self._compile_where()
        order = None
        if self._order_by:
            _exps = [f"{f} DESC" if f.startswith("-") else f for f in self._order_by]
            order = f" ORDER BY {', '.join(_exps)}", ()
        return _sql_join(" ", [select, where, order])

    def _compile_insert(self, entry, upsert=False):
        sql = f"INSERT INTO {self._table} (" + ", ".join(entry) + ")"
        sql += " VALUES (" + ", ".join("?" for _ in entry) + ")"
        if upsert:
            sql += " ON CONFLICT DO NOTHING"
        params = tuple(entry.values())
        return (sql, params)

    def _compile_update(self, sets):
        update = f"UPDATE {self._table} SET", ()
        sets = ", ".join(f"{f}=?" for f in sets), sets.values()
        where = self._compile_where()
        return _sql_join(" ", [update, sets, where])

    def _compile_delete(self):
        delete = f"DELETE FROM {self._table}", ()
        where = self._compile_where()
        return _sql_join(" ", [delete, where])

    def _compile_where(self):
        if not self._where:
            return None
        conds = [self._compile_lookup(k, v) for k, v in self._where.items()]
        sql, params = _sql_join(" AND ", conds)
        return f"WHERE {sql}", params

    def _compile_lookup(self, lookup, value):
        if custom_compile := getattr(self._schema, f"lookup_{lookup}", None):
            return custom_compile(self, lookup, value)
        elif "__" in lookup:
            field, op = lookup.split("__", 1)
        else:
            field, op = lookup, "eq"
        return self.compile_op(field, op, value)

    def compile_op(self, field, op, value):
        if op in {"glob", "iglob"} and isinstance(value, (list, tuple)):
            if not value:
                return None
            subs = [self.compile_op(field, op, v) for v in value]
            sql, params = _sql_join(" OR ", subs)
            return (f"""({sql})""", params)

        if op in self.OP_TO_SQL:
            return f"{field} {self.OP_TO_SQL[op]} ?", (value,)
        elif op == "startswith":
            return f"{field} LIKE ? ESCAPE '\\'", (_escape_like(value) + "%",)
        elif op == "startof":
            return f"{field} = substr(?, 1, length({field}))", (value,)
        elif op == "glob":
            return f"{field} GLOB ?", (value,)
        elif op == "iglob":
            return f"LOWER({field}) GLOB ?", (value.lower(),)
        elif op == "ieq":
            return f"LOWER({field}) = ?", (value.lower(),)
        else:
            raise NotImplementedError('Don\'t know how to compile "%s" operator' % op)


def _sql_join(op, pairs):
    sqls, params = zip(*keep(pairs))
    return op.join(sqls), lcat(params)


def _escape_like(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
