from volsite_postgres_common.test.db.ATestDb import ATestDb


class ATestSetUser(ATestDb):
    def __init__(self, name: str, user_iid, p_conn):
        super().__init__(p_conn, True)
        self._name = name
        self._user_iid = user_iid
        self._show_fn_in_output = True
