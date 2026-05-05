import re

with open('src/codegen/codegen.py', 'r') as f:
    content = f.read()

infer_helper = """
    def _infer_auto_type_from_assignment(self, var_name, o):
        if not hasattr(self, 'block_stack') or not self.block_stack:
            from .utils import IntType
            return IntType()
        from .utils import AssignExpr, ExprStmt, Identifier
        
        # Scan current block for first assignment to var_name
        current_stmts = self.block_stack[-1]
        for stmt in current_stmts:
            if isinstance(stmt, ExprStmt) and isinstance(stmt.expr, AssignExpr):
                assign = stmt.expr
                if isinstance(assign.left, Identifier) and assign.left.name == var_name:
                    return self._infer_type(assign.right, o)
        from .utils import IntType
        return IntType()
"""

# Insert _infer_auto_type_from_assignment before visit_var_decl
content = content.replace("    def visit_var_decl(self, node: VarDecl, o: SubBody = None):", infer_helper + "\n    def visit_var_decl(self, node: VarDecl, o: SubBody = None):")

# Modify visit_var_decl
old_infer = "var_type = node.var_type if node.var_type else self._infer_type(node.init_value, access)"
new_infer = """
        if node.var_type:
            var_type = node.var_type
        elif node.init_value:
            var_type = self._infer_type(node.init_value, access)
        else:
            var_type = self._infer_auto_type_from_assignment(node.name, access)
"""
content = content.replace(old_infer, new_infer.strip())

# Modify visit_block_stmt
old_block = """
        for stmt in node.statements:
            self.visit(stmt, new_o)
"""
new_block = """
        if not hasattr(self, 'block_stack'):
            self.block_stack = []
        self.block_stack.append(node.statements)
        for stmt in node.statements:
            self.visit(stmt, new_o)
        self.block_stack.pop()
"""
content = content.replace(old_block, new_block.strip())

with open('src/codegen/codegen.py', 'w') as f:
    f.write(content)
