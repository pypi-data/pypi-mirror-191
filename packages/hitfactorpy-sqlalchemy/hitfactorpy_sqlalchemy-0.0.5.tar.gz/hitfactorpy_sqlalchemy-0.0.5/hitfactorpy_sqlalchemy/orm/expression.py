from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import case
from sqlalchemy.sql.expression import FunctionElement  # type: ignore
from sqlalchemy.types import Numeric


class greatest(FunctionElement):
    """See: https://docs.sqlalchemy.org/en/20/core/compiler.html#greatest-function"""

    type = Numeric()
    name = "greatest"
    inherit_cache = True


@compiles(greatest)
def default_greatest(element, compiler, **kw):
    return compiler.visit_function(element)


@compiles(greatest, "sqlite")
@compiles(greatest, "mssql")
@compiles(greatest, "oracle")
def case_greatest(element, compiler, **kw):
    arg1, arg2 = list(element.clauses)
    return compiler.process(case([(arg1 > arg2, arg1)], else_=arg2), **kw)
