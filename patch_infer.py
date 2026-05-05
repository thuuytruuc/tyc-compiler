import re

with open('src/codegen/codegen.py', 'r') as f:
    content = f.read()

infer_func = """
    def _find_return_expr(self, stmt):
        from .utils import ReturnStmt, BlockStmt, IfStmt, WhileStmt, ForStmt
        if isinstance(stmt, ReturnStmt):
            return stmt.expr
        if isinstance(stmt, BlockStmt):
            for s in stmt.statements:
                ret = self._find_return_expr(s)
                if ret is not None:
                    return ret
        if isinstance(stmt, IfStmt):
            ret = self._find_return_expr(stmt.then_stmt)
            if ret is not None: return ret
            if stmt.else_stmt:
                ret = self._find_return_expr(stmt.else_stmt)
                if ret is not None: return ret
        if isinstance(stmt, WhileStmt):
            return self._find_return_expr(stmt.body)
        if isinstance(stmt, ForStmt):
            return self._find_return_expr(stmt.body)
        return None

    def _infer_func_return_type(self, node):
        if node.return_type is not None:
            return node.return_type
        ret_expr = self._find_return_expr(node.body)
        if ret_expr is None:
            return VoidType()
        
        # Build dummy sym table to infer type
        from .utils import Symbol, Index
        sym = []
        for p in node.params:
            sym.append(Symbol(p.name, p.param_type, Index(0)))
        from .frame import Access
        return self._infer_type(ret_expr, Access(None, sym))
"""

# Insert before visit_program
content = content.replace("    def visit_program(self, node: Program, o: Any = None):", infer_func + "\n    def visit_program(self, node: Program, o: Any = None):")

# Replace return_type defaults
content = content.replace(
    "return_type = decl.return_type if decl.return_type else VoidType()",
    "return_type = self._infer_func_return_type(decl)"
)
content = content.replace(
    "self.current_return_type = node.return_type if node.return_type else VoidType()",
    "self.current_return_type = self._infer_func_return_type(node)"
)

with open('src/codegen/codegen.py', 'w') as f:
    f.write(content)
