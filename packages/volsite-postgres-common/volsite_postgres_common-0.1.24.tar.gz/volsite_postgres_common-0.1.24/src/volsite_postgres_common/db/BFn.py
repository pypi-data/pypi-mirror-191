from typing import Final

# ====== BFn: Postgres Build in Functions ======


class BFn:
    array_agg: Final[str] = 'array_agg'
    array_append: Final[str] = 'array_append'
    array_length: Final[str] = 'array_length'
    array_position: Final[str] = 'array_position'
    array_to_json: Final[str] = 'array_to_json'
    array_to_string: Final[str] = 'array_to_string'

    cardinality: Final[str] = 'cardinality'
    coalesce: Final[str] = 'coalesce'
    concat: Final[str] = 'concat'
    convert_from: Final[str] = 'convert_from'
    crypt: Final[str] = 'crypt'
    current_timestamp: Final[str] = 'current_timestamp'

    decode: Final[str] = 'decode'

    encode: Final[str] = 'encode'
    enum_range: Final[str] = 'enum_range'

    gen_salt: Final[str] = 'gen_salt'

    icount: Final[str] = 'icount'  # number of elements in array

    jsonb_array_length: Final[str] = 'jsonb_array_length'

    lower: Final[str] = 'lower'

    quote_ident: Final[str] = 'quote_ident'

    jsonb_agg: Final[str] = 'jsonb_agg'
    jsonb_array_elements: Final[str] = 'jsonb_array_elements'
    jsonb_array_elements_text: Final[str] = 'jsonb_array_elements_text'
    jsonb_build_array: Final[str] = 'jsonb_build_array'
    jsonb_build_object: Final[str] = 'jsonb_build_object'
    jsonb_each: Final[str] = 'jsonb_each'
    jsonb_object_agg: Final[str] = 'jsonb_object_agg'
    jsonb_object_keys: Final[str] = 'jsonb_object_keys'
    jsonb_strip_nulls: Final[str] = 'jsonb_strip_nulls'

    length: Final[str] = 'length'

    nextval: Final[str] = 'nextval'

    percentile_cont: Final[str] = 'percentile_cont'
    pg_get_serial_sequence: Final[str] = 'pg_get_serial_sequence'

    regexp_matches: Final[str] = 'regexp_matches'

    sha256: Final[str] = 'sha256'
    similarity: Final[str] = 'similarity'
    sort: Final[str] = 'sort'
    sort_asc: Final[str] = 'sort_asc'
    sort_desc: Final[str] = 'sort_desc'
    split_part: Final[str] = 'split_part'
    substring: Final[str] = 'substring'
    sum: Final[str] = 'sum'

    trim: Final[str] = 'trim'

    uniq: Final[str] = 'uniq'

    word_similarity: Final[str] = 'word_similarity'
