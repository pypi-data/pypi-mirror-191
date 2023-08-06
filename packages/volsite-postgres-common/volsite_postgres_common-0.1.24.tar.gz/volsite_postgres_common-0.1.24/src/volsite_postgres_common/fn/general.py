from typing import Final
from volsite_postgres_common.db.CFn import CFn
from volsite_postgres_common.fn.insert import insert_function


# @ref https://stackoverflow.com/questions/39900397/check-if-anyelement-isnull-postgresql
is_null: Final = (
    f" CREATE OR REPLACE FUNCTION "
    f" {CFn.is_null} (anyelement) "
    f" RETURNS BOOLEAN "
    f" AS"
    f" $$"
    f"   SELECT $1 IS NULL"
    f" $$ "
    f" LANGUAGE SQL "
    f" IMMUTABLE;")

# @ref https://stackoverflow.com/questions/2913368/sorting-array-elements
array_sort: Final = (
    f" CREATE OR REPLACE FUNCTION "
    f" {CFn.array_sort} (ANYARRAY) "
    f" RETURNS ANYARRAY "
    f" AS"
    f" $$"
    f"   SELECT ARRAY(SELECT unnest($1) ORDER BY 1)"
    f" $$ "
    f" LANGUAGE SQL "
    f" IMMUTABLE;")

if_null_2_empty_bigint_array: Final = (
    f" CREATE OR REPLACE FUNCTION "
    f" {CFn.if_null_2_empty_bigint_array} ("
    f" IN _input BIGINT[], "
    f" OUT _result BIGINT[]"
    f" ) "
    f" AS"
    f" $$"
    f" BEGIN "
    f"  IF _input IS NULL THEN"
    f"      _result := ARRAY[]::BIGINT[];"
    f"      RETURN;"
    f"  END IF;"
    f"  _result := _input;"
    f" END;"
    f" $$ "
    f" LANGUAGE PlPgSql "
    f" ;")


def insert_util_fn__general(conn):
    insert_function(is_null, CFn.is_null, conn)
    insert_function(array_sort, CFn.array_sort, conn)
    insert_function(if_null_2_empty_bigint_array, CFn.if_null_2_empty_bigint_array, conn)
