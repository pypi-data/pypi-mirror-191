from aenum import Enum


class FnT(Enum):  # Function Arg Types
    BIGINT = 'BIGINT'
    BIGINT_ARRAY = 'BIGINT[]'

    BOOLEAN = 'BOOLEAN'
    
    FLOAT = 'FLOAT'

    INT = 'INT'
    INT_ARRAY = 'INT[]'

    JSONB = 'JSONB'
    JSONB_ARRAY = 'JSONB[]'

    SMALLINT = 'SMALLINT'
    SMALLINT_ARRAY = 'SMALLINT[]'

    TEXT = 'TEXT'
    TEXT_ARRAY = 'TEXT[]'

    TIMESTAMP = 'TIMESTAMP'

    VOID = 'VOID'
