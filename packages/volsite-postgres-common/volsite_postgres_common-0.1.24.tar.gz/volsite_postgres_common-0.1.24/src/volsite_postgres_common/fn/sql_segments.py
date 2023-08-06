
from volworld_common.api.CA import CA
from volsite_postgres_common.db.CFn import CFn
from volsite_postgres_common.fn.function import Arg


def sql__input_j_2_iid(att: str) -> str:
    return f"({Arg.input}->>'{att}')::TEXT"


def sql__input_j_2_bint_id(att: str) -> str:
    return f"{CFn.id_2_bigint}( ({Arg.input}->>'{att}')::TEXT )"


def sql__input_j_2_int_id(att: str) -> str:
    return f"{CFn.id_2_int}( ({Arg.input}->>'{att}')::TEXT )"


def sql__2_id(*att: str) -> str:
    return f"{CFn.bigint_2_id}({'.'.join(att)})"


def sql__2_bint(*att: str) -> str:
    return f"{CFn.id_2_bigint}({'.'.join(att)})"


def sql__order_by_cols(col_dict: dict, def_col: str) -> str:
    res = f"CASE ({Arg.input}->>'{CA.SortBy}')::TEXT"
    for arg in col_dict.keys():
        res = f"{res}\n          WHEN '{arg}' THEN {col_dict[arg]}"
    res = f"{res}\n          ELSE {def_col}"  # ELSE NULL
    res = f"{res}\nEND"
    return res


def sql__order_by(col_dict: dict, def_col: str) -> str:
    return (
        f" CASE WHEN ({Arg.input}->>'{CA.SortDirection}')::TEXT = '{CA.Ascending}' THEN "
        f"      {sql__order_by_cols(col_dict, def_col)}"
        f" ELSE"
        f"      NULL"
        f" END"
        f" {CA.Ascending},"
        f""
        f" CASE WHEN ({Arg.input}->>'{CA.SortDirection}')::TEXT = '{CA.Descending}' THEN "
        f"      {sql__order_by_cols(col_dict, def_col)}"
        f" ELSE"
        f"      NULL"
        f" END"
        f" {CA.Descending}"
    )
