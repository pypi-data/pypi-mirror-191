""" ae.db_core unit tests """
import pytest

from ae.core import DEBUG_LEVEL_ENABLED
from ae.console import ConsoleApp
from ae.lockname import NamedLocks
from ae.sys_core import SystemBase

# noinspection PyProtectedMember
from ae.db_core import (
    CHK_BIND_VAR_PREFIX, NAMED_BIND_VAR_PREFIX, connect_args_from_params, _prepare_in_clause, _rebind, DbBase)


PROC_NAME = 'PROC_NAME'
PROC_ARGS = ('PROC_ARG1', 'PROC_ARG2')
FETCH_ALL_VALUES = [(1, 'COL2_VAL', 'COL3_VAL')]    # the 1 value is used for test_upsert*()


class XxConn:
    """ Python DB API connection stub/spy """
    def connect(self, *args, **kwargs):
        """ Conn.connect """
        return self, args, kwargs

    def cursor(self):
        """ Conn.cursor """
        return XxCurs(self)

    def commit(self):
        """ Conn.commit """
        return

    def rollback(self):
        """ Conn.rollback """
        return

    def close(self):
        """ Conn.close """
        return


class XxCurs:
    """ Python DB API cursor stub/spy """
    description = (('COL1', ), ('COL2', ), )
    statusmessage = "XxCursStatusMessage"
    rowcount = 0

    def __init__(self, conn):
        self.conn_obj = conn
        self.exec_sql = ""
        self.exec_bind_vars = {}

    def callproc(self, proc_name, proc_args):
        """ Curs.callproc """
        return self, proc_name, proc_args

    def close(self):
        """ Curs.close """
        return

    def execute(self, sql, bind_vars=None):
        """ Curs.execute """
        self.exec_sql = sql
        self.exec_bind_vars = bind_vars

    def fetchall(self):
        """ Curs.fetchall """
        self.rowcount = 1
        return FETCH_ALL_VALUES or self

    def fetchone(self):
        """ Curs.fetchone """
        self.rowcount = 1
        return FETCH_ALL_VALUES[0] or self


class ZzDb(DbBase):
    """ simple inherit from DbBase ABC """
    def connect(self) -> str:
        """ simple stub """
        return self.last_err_msg


class XxDb(DbBase):
    """ Python DB API database stub/spy """
    def connect(self):
        """ DB.connect """
        self.conn = XxConn()
        self.create_cursor()
        return self.last_err_msg


DB_USER = 'db_user'
DB_PASSWORD = 'db_password'
DB_NAME = 'db_name'
CREDENTIALS = dict(User=DB_USER, Password=DB_PASSWORD, Dbname=DB_NAME)
FEATURES = ["flag", "strVal='strVal'", "intVal=369"]
# for DB URL tests - dialect and driver cannot contain underscore character
DB_URL = "dialect+driver://url_db_user:url_db_password@url_db_host:12345/url_db_name"


@pytest.fixture
def system(cons_app):
    """ SystemBase stub """
    return SystemBase('Zz', cons_app, CREDENTIALS, features=FEATURES)


@pytest.fixture
def db(system):
    """ Python DB API base DB stub/spy """
    return ZzDb(system)


@pytest.fixture
def xx(system):
    """ Python DB API connected DB stub/spy """
    system.sys_id = 'Xx'
    ret = XxDb(system)
    ret.connect()
    return ret


class TestHelpers:
    def test_connect_args_from_params_empty(self):
        params = {}
        credentials, features = connect_args_from_params(params)
        assert isinstance(credentials, dict)
        assert len(credentials) == 0
        assert isinstance(features, list)
        assert len(features) == 0

    def test_connect_args_from_params_feat_empty(self):
        params = dict(user='user', password='password')
        credentials, features = connect_args_from_params(params)
        assert len(credentials) == 2
        assert credentials['user'] == 'user'
        assert credentials['password'] == 'password'
        assert len(features) == 0

    def test_connect_args_from_params_types(self, db):
        params = dict(intVal=123, strVal='string', trueVal=True, falseVal=False, byteVal=b'bytes')
        credentials, features = connect_args_from_params(params)
        assert len(credentials) == 1
        assert credentials['strVal'] == 'string'
        assert len(features) == 3
        assert 'intVal=123' in features
        assert 'trueVal' in features
        assert 'falseVal' not in features
        assert "byteVal=b'bytes'" in features

        chk_params = {k.lower(): v for k, v in params.items() if k != 'falseVal'}
        db.system.credentials = credentials
        db.system.features = features
        assert chk_params == db.connect_params()

    def test_prepare_in_clause(self):
        sql = "SELECT a FROM b WHERE c IN (:d)"
        sqo, bind = _prepare_in_clause(sql, dict(d=1))
        assert sqo == sql
        assert bind == dict(d=1)

        sqo, bind = _prepare_in_clause(sql, dict(d=[1, 2]))
        assert sqo == "SELECT a FROM b WHERE c IN (:d_0,:d_1)"
        assert bind == dict(d_0=1, d_1=2)

    def test_rebind_ensure_nonempty_chk(self):
        chk = {}
        wgo = " GROUP BY x ORDER BY y"
        bdv = dict(d=2)
        ebd = dict(e=3)
        new_chk, new_wgo, new_bdv = _rebind(chk, wgo, bdv, ebd)
        assert new_chk == ebd
        assert f"{NAMED_BIND_VAR_PREFIX}{CHK_BIND_VAR_PREFIX}e" in new_wgo
        assert new_bdv == {CHK_BIND_VAR_PREFIX + 'd': 2, CHK_BIND_VAR_PREFIX + 'e': 3, 'e': 3}

    def test_rebind_ensure_nonempty_wgo(self):
        chk = dict(d=1)
        wgo = ""
        bdv = {}
        new_chk, new_wgo, new_bdv = _rebind(chk, wgo, bdv)
        assert new_chk is chk
        assert f"{NAMED_BIND_VAR_PREFIX}{CHK_BIND_VAR_PREFIX}d" in new_wgo
        assert new_bdv == {CHK_BIND_VAR_PREFIX + 'd': 1}

    def test_rebind_ensure_nonempty_wgo_without_chk(self):
        chk = {}
        wgo = ""
        bdv = {}
        new_chk, new_wgo, new_bdv = _rebind(chk, wgo, bdv)
        assert new_chk is chk
        assert new_wgo != ""    # 1=1
        assert new_bdv == chk

    def test_rebind_chk_into_order_wgo(self):
        chk = dict(d=1)
        wgo = "order by x"
        bdv = {}
        new_chk, new_wgo, new_bdv = _rebind(chk, wgo, bdv)
        bdn = f"{NAMED_BIND_VAR_PREFIX}{CHK_BIND_VAR_PREFIX}d"
        assert new_chk is chk
        assert bdn in new_wgo
        assert new_wgo.find(bdn) < new_wgo.find('order by')
        assert new_bdv == {CHK_BIND_VAR_PREFIX + 'd': 1}

    def test_rebind_chk_into_group_wgo(self):
        chk = dict(d=1)
        wgo = "group by x"
        bdv = {}
        new_chk, new_wgo, new_bdv = _rebind(chk, wgo, bdv)
        bdn = f"{NAMED_BIND_VAR_PREFIX}{CHK_BIND_VAR_PREFIX}d"
        assert new_chk is chk
        assert bdn in new_wgo
        assert new_wgo.find(bdn) < new_wgo.find('group by')
        assert new_bdv == {CHK_BIND_VAR_PREFIX + 'd': 1}

    def test_rebind_merge_bind_vars(self):
        chk = dict(d=1)
        wgo = "c = 'city' GROUP BY x ORDER BY y"
        bdv = dict(v=2)
        ebd = dict(e=3)
        new_chk, new_wgo, new_bdv = _rebind(chk, wgo, bdv, ebd)
        assert new_chk is chk
        assert f"{NAMED_BIND_VAR_PREFIX}{CHK_BIND_VAR_PREFIX}d" in new_wgo
        assert new_bdv == {'CV_d': 1, 'CV_v': 2, 'e': 3}

    def test_rebind_overwrite_bind_vars(self):
        chk = dict(d=1)
        wgo = "c = 'city' GROUP BY x ORDER BY y"
        bdv = dict(d=2)
        ebd = dict(e=3)
        new_chk, new_wgo, new_bdv = _rebind(chk, wgo, bdv, ebd)
        assert chk is new_chk
        assert f"{NAMED_BIND_VAR_PREFIX}{CHK_BIND_VAR_PREFIX}d" in new_wgo
        assert new_bdv == {'CV_d': 2, 'e': 3}


class TestDbBaseUnconnected:
    def test_init(self, db):
        assert isinstance(db.console_app, ConsoleApp)
        assert db.system.credentials == CREDENTIALS
        assert db.system.features == FEATURES
        assert db.system.credentials['User'] == DB_USER
        assert db.system.credentials['Password'] == DB_PASSWORD
        assert db.system.credentials['Dbname'] == DB_NAME
        assert db.conn is None
        assert db.curs is None
        assert db.last_err_msg == ""
        assert db.param_style == 'named'

    def test_adapt_sql(self, db):
        sql = "SELECT a FROM b WHERE c > :d"
        assert db._adapt_sql(sql, dict(d=1)) == sql
        db.param_style = 'pyformat'
        assert db._adapt_sql(sql, dict(d=1)) == "SELECT a FROM b WHERE c > %(d)s"
        assert db.last_err_msg == ""

    def test_create_cursor_ex_cov(self, db):
        assert db.last_err_msg == ""
        db.create_cursor()     # produces error because db.conn is not initialized
        assert db.last_err_msg

    def test_call_proc_ex_cov(self, db):
        db.call_proc('', ())
        assert db.last_err_msg

    def test_close_ex_cov(self, db):
        db.conn = "invalidConnObj"
        db.close()
        assert db.last_err_msg

    def test_connect(self, db):
        assert db.connect() == ""

    def test_connect_kwargs_is_copy(self, db):
        assert db.connect_params() is not CREDENTIALS

    def test_connect_kwargs_has_credentials(self, db):
        cka = db.connect_params()
        for key, val in db.system.credentials.items():
            key = key.lower()
            assert key in cka
            assert cka[key] == val

    def test_connect_kwargs_has_feats(self, db):
        cka = db.connect_params()
        for feat in db.system.features:
            if feat:
                key_val = feat.split('=', maxsplit=1)
                key = key_val[0].lower()
                assert key in cka
                val = cka[key]
                assert val == eval(key_val[1]) if len(key_val) > 1 else True

    def test_connect_url_user(self, db):
        db.system.credentials['url'] = DB_URL
        db.system.credentials.pop('User')
        cka = db.connect_params()
        assert cka['user'] == 'url_' + DB_USER

    def test_connect_url_password(self, db):
        db.system.credentials['url'] = DB_URL
        db.system.credentials.pop('Password')
        cka = db.connect_params()
        assert cka['password'] == 'url_' + DB_PASSWORD

    def test_connect_url_db_name(self, db):
        db.system.credentials['url'] = DB_URL
        db.system.credentials.pop('Dbname')
        cka = db.connect_params()
        assert cka['dbname'] == 'url_' + DB_NAME

    def test_cursor_description_no_curs_cov(self, db):
        assert db.cursor_description() is None

    def test_fetch_all_ex_cov(self, db):
        rows = db.fetch_all()
        assert isinstance(rows, list)
        assert db.last_err_msg

    def test_execute_sql_ex_cov(self, db):
        db.conn = XxConn()
        db.execute_sql('InvalidSQLOnUnconnectedConn')
        assert db.last_err_msg

    def test_commit_ex_cov(self, db):
        class InvalidConnObj:
            """ invalid connection class """
            commit = 'invalid_commit_method'
        db.conn = InvalidConnObj()
        db.commit()
        assert db.last_err_msg

    def test_rollback_ex_cov(self, db):
        class InvalidConnObj:
            """ invalid connection class """
            rollback = 'invalid_rollback_method'
        db.conn = InvalidConnObj()
        db.rollback()
        assert db.last_err_msg


class TestBaseDbStubConnected:
    def test_connect_create_cursor(self, xx):
        assert xx.connect() == ""
        assert isinstance(xx.conn, XxConn)
        assert isinstance(xx.curs, XxCurs)
        assert xx.last_err_msg == ""

    def test_call_proc(self, xx):
        ret = {}
        xx.call_proc(PROC_NAME, PROC_ARGS, ret_dict=ret)
        assert xx.last_err_msg == ""
        cur, prn, pra = ret['return']
        assert isinstance(cur, XxCurs)
        assert prn == PROC_NAME
        assert pra == PROC_ARGS

    def test_close(self, xx):
        xx.close()
        assert xx.last_err_msg == ""
        assert xx.conn is None
        assert xx.curs is None

    def test_close_rollback(self, xx):
        xx.close(commit=False)
        assert xx.last_err_msg == ""
        assert xx.conn is None
        assert xx.curs is None

    def test_cursor_description(self, xx):
        assert xx.cursor_description() == XxCurs.description
        assert xx.last_err_msg == ""

    def test_fetch_all(self, xx):
        rows = xx.fetch_all()
        assert xx.last_err_msg == ""
        assert isinstance(rows, list)
        assert rows is FETCH_ALL_VALUES

    def test_fetch_value(self, xx):
        col_val = xx.fetch_value(1)
        assert xx.last_err_msg == ""
        assert col_val == FETCH_ALL_VALUES[0][1]

    def test_fetch_value_ex_cov(self, xx):
        xx.curs.fetchone = "InvalidCursorMeth"
        xx.fetch_value()
        assert xx.last_err_msg

    def test_execute_sql(self, xx):
        xx.execute_sql('CREATE TABLE a')
        assert xx.last_err_msg == ""
        assert xx.curs.exec_sql == 'CREATE TABLE a'

    def test_execute_sql_script_action(self, xx):
        xx.execute_sql('-- SCRIPT')
        assert xx.last_err_msg == ""
        assert xx.curs.exec_sql == '-- SCRIPT'

    def test_execute_sql_bind_vars(self, xx):
        bind_vars = dict(d=1)
        xx.execute_sql('SELECT 1', bind_vars=bind_vars)
        assert xx.last_err_msg == ""
        assert xx.curs.exec_sql == 'SELECT 1'
        assert xx.curs.exec_bind_vars == bind_vars

    def test_execute_sql_commit(self, xx):
        xx.execute_sql('CREATE TABLE a', commit=True)
        assert xx.last_err_msg == ""
        assert xx.curs.exec_sql == 'CREATE TABLE a'

    def test_execute_sql_ex_debug_cov(self, xx):
        xx.curs.execute = "InvalidCursMeth"
        xx.console_app.debug_level = DEBUG_LEVEL_ENABLED
        xx.execute_sql('CREATE TABLE a')
        assert xx.last_err_msg

    def test_delete(self, xx):
        xx.delete('TABLE_NAME', dict(chk=33), "GROUP BY z", dict(bind=99), commit=True)
        assert xx.last_err_msg == ""
        assert 'DELETE ' in xx.curs.exec_sql
        assert 'TABLE_NAME' in xx.curs.exec_sql
        assert 'chk' in xx.curs.exec_sql
        assert "GROUP BY z" in xx.curs.exec_sql

    def test_insert(self, xx):
        xx.insert('TABLE_NAME', dict(chk=33), "RET_COL", commit=True)
        assert xx.last_err_msg == ""
        assert 'INSERT ' in xx.curs.exec_sql
        assert 'TABLE_NAME' in xx.curs.exec_sql
        assert 'chk' in xx.curs.exec_sql
        assert "RET_COL" in xx.curs.exec_sql

    def test_insert_empty_str_to_none(self, xx):
        col_values = dict(chk="")
        xx.insert('TABLE_NAME', col_values, commit=True)
        assert xx.last_err_msg == ""
        assert 'INSERT ' in xx.curs.exec_sql
        assert 'TABLE_NAME' in xx.curs.exec_sql
        assert 'chk' in xx.curs.exec_sql
        assert "RET_COL" not in xx.curs.exec_sql
        assert col_values['chk'] is None

    def test_select(self, xx):
        xx.select('TABLE_NAME', (), dict(chk=3), "GROUP BY z", dict(bind=99), hints="HINTS")
        assert xx.last_err_msg == ""
        assert 'SELECT ' in xx.curs.exec_sql
        assert 'TABLE_NAME' in xx.curs.exec_sql
        assert 'chk' in xx.curs.exec_sql
        assert "GROUP BY z" in xx.curs.exec_sql
        assert "HINTS" in xx.curs.exec_sql

    def test_update(self, xx):
        xx.update('TABLE_NAME', dict(col=1), dict(chk=3), "EXTRA_WHERE", dict(bind=99))
        assert xx.last_err_msg == ""
        assert 'UPDATE ' in xx.curs.exec_sql
        assert 'TABLE_NAME' in xx.curs.exec_sql
        assert 'col' in xx.curs.exec_sql
        assert 'chk' in xx.curs.exec_sql
        assert "EXTRA_WHERE" in xx.curs.exec_sql

    def test_upsert(self, xx):
        xx.upsert('TABLE_NAME', dict(col=1), dict(chk=3), "EXTRA_WHERE", dict(bind=99))
        assert xx.last_err_msg == ""
        assert 'UPDATE ' in xx.curs.exec_sql
        assert 'TABLE_NAME' in xx.curs.exec_sql
        assert 'col' in xx.curs.exec_sql
        assert 'chk' in xx.curs.exec_sql
        assert "EXTRA_WHERE" in xx.curs.exec_sql

    def test_upsert_returning(self, xx):
        xx.upsert('TABLE_NAME', dict(col=1), dict(chk=3), "EXTRA_WHERE", dict(bind=99), returning_column='RET_COL')
        assert xx.last_err_msg == ""
        assert 'SELECT ' in xx.curs.exec_sql
        assert 'TABLE_NAME' in xx.curs.exec_sql
        assert 'col' not in xx.curs.exec_sql
        assert 'chk' in xx.curs.exec_sql
        assert "EXTRA_WHERE" in xx.curs.exec_sql
        assert "RET_COL" in xx.curs.exec_sql

    def test_upsert_insert(self, xx):
        xx.curs.fetchone = lambda: (0, )      # force SELECT COUNT() to return zero/0
        xx.upsert('TABLE_NAME', dict(col=1), dict(chk=3), "EXTRA_WHERE", dict(bind=99))
        assert xx.last_err_msg == ""
        assert 'INSERT ' in xx.curs.exec_sql
        assert 'TABLE_NAME' in xx.curs.exec_sql
        assert 'col' in xx.curs.exec_sql
        assert 'chk' in xx.curs.exec_sql
        assert "EXTRA_WHERE" not in xx.curs.exec_sql

    def test_upsert_err_multiple(self, xx):
        xx.curs.fetchone = lambda: (2, )      # force SELECT COUNT() to return 2 records
        xx.upsert('TABLE_NAME', dict(col=1), dict(chk=3), "EXTRA_WHERE", dict(bind=99), multiple_row_update=False)
        assert "returned 2" in xx.last_err_msg

    def test_upsert_err_negative(self, xx):
        xx.curs.fetchone = lambda: (-3, )      # force SELECT COUNT() to return -3
        xx.upsert('TABLE_NAME', dict(col=1), dict(chk=3), "EXTRA_WHERE", dict(bind=99))
        assert "returned -3" in xx.last_err_msg

    def test_commit(self, xx):
        xx.last_err_msg = "ERROR"
        xx.commit(reset_last_err_msg=True)
        assert xx.last_err_msg == ""

    def test_rollback(self, xx):
        xx.last_err_msg = "ERROR"
        xx.rollback(reset_last_err_msg=True)
        assert xx.last_err_msg == ""

    def test_get_row_count(self, xx):
        assert xx.get_row_count() == 0

    def test_get_row_count_after_fetch(self, xx):
        xx.fetch_value()
        assert xx.get_row_count() == 1

    def test_selected_column_names(self, xx):
        assert xx.selected_column_names() == [col_desc_tuple[0] for col_desc_tuple in XxCurs.description]

    def test_thread_lock_init(self, xx):
        lock = xx.thread_lock_init('TABLE_NAME', dict(chk=99))
        assert isinstance(lock, NamedLocks)
