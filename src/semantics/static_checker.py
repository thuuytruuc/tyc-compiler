"""
Static Semantic Checker for TyC Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the TyC procedural programming language. It performs type checking,
scope management, type inference, and detects all semantic errors as
specified in the TyC language specification.
"""

from typing import (
    Dict,
    List,
    Optional,
    Any,
    Union,
)
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    Program,
    StructDecl,
    MemberDecl,
    FuncDecl,
    Param,
    VarDecl,
    IfStmt,
    WhileStmt,
    ForStmt,
    BreakStmt,
    ContinueStmt,
    ReturnStmt,
    BlockStmt,
    SwitchStmt,
    CaseStmt,
    DefaultStmt,
    Type,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    BinaryOp,
    PrefixOp,
    PostfixOp,
    AssignExpr,
    MemberAccess,
    FuncCall,
    Identifier,
    StructLiteral,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    ExprStmt,
    Expr,
    Stmt,
    Decl,
)

TyCType = Union[IntType, FloatType, StringType, VoidType, StructType]

from .static_error import (
    StaticError,
    Redeclared,
    UndeclaredIdentifier,
    UndeclaredFunction,
    UndeclaredStruct,
    TypeCannotBeInferred,
    TypeMismatchInStatement,
    TypeMismatchInExpression,
    MustInLoop,
)


# ============================================================
# Helper: type equality / compatibility
# ============================================================

def types_equal(t1: Optional[Type], t2: Optional[Type]) -> bool:
    """Return True when t1 and t2 represent the same TyC type."""
    if t1 is None or t2 is None:
        return False
    elif type(t1) != type(t2):
        return False
    elif isinstance(t1, StructType) and isinstance(t2, StructType):
        return t1.struct_name == t2.struct_name
    return True


def is_numeric(t: Optional[Type]) -> bool:
    return isinstance(t, (IntType, FloatType))


def arithmetic_result(t1: Type, t2: Type) -> Type:
    """int op int -> int; anything with float -> float."""
    if isinstance(t1, FloatType) or isinstance(t2, FloatType):
        return FloatType()
    return IntType()


# ============================================================
# Scope / environment helpers
# ============================================================

class FuncInfo:
    """Metadata stored for a declared function."""
    def __init__(self, return_type: Optional[Type], params: List[Param]):
        self.return_type = return_type   # None means inferred
        self.params = params


# ============================================================
# StaticChecker
# ============================================================

class StaticChecker(ASTVisitor):
    """
    Visitor-based static semantic checker for TyC.

    Visitor parameter `o` is a dict (the 'env') containing:
        - 'structs'     : Dict[str, StructDecl]   — globally declared structs
        - 'funcs'       : Dict[str, FuncInfo]      — globally declared functions
        - 'var_scopes'  : List[Dict[str,Type]]     — stack of local-variable scopes
        - 'param_names' : Set[str]                 — param names of current function
        - 'func_info'   : FuncInfo                 — current function being checked
        - 'in_loop'     : bool                     — True when inside for/while
        - 'in_switch'   : bool                     — True when inside switch (for break)
    """

    # ------------------------------------------------------------------
    # Entry
    # ------------------------------------------------------------------

    def check(self, ast: Program) -> str:
        ast.accept(self)
        return "Static checking passed"

    def check_program(self, ast: Program) -> str:
        return self.check(ast)

    # ------------------------------------------------------------------
    # Program
    # ------------------------------------------------------------------

    def visit_program(self, node: Program, o: Any = None):
        # Process declarations sequentially (structs/functions declared before use).
        structs: Dict[str, StructDecl] = {}
        funcs: Dict[str, FuncInfo] = {}

        # Register built-ins
        builtins = {
            "readInt":    FuncInfo(IntType(),    []),
            "readFloat":  FuncInfo(FloatType(),  []),
            "readString": FuncInfo(StringType(), []),
            "printInt":   FuncInfo(VoidType(),   [Param(IntType(),    "value")]),
            "printFloat": FuncInfo(VoidType(),   [Param(FloatType(),  "value")]),
            "printString":FuncInfo(VoidType(),   [Param(StringType(), "value")]),
        }
        funcs.update(builtins)

        env = {
            "structs":     structs,
            "funcs":       funcs,
            "var_scopes":  [],
            "param_names": set(),
            "func_info":   None,
            "in_loop":     False,
            "in_switch":   False,
        }

        for decl in node.decls:
            decl.accept(self, env)

    # ------------------------------------------------------------------
    # Struct
    # ------------------------------------------------------------------

    def visit_struct_decl(self, node: StructDecl, o: Any = None):
        structs = o["structs"]
        if node.name in structs:
            raise Redeclared("Struct", node.name)
        
        # Track seen members of the outer scope
        outer_scope_member = o.get("curr_member", None)
        o["curr_member"] = set()
        
        for mem in node.members:
            mem.accept(self, o)
            
        if outer_scope_member is not None:
            o["curr_member"] = outer_scope_member
        else:
            del o["curr_member"]

        structs[node.name] = node

    def visit_member_decl(self, node: MemberDecl, o: Any = None):
        member = o["curr_member"]
        if node.name in member:
            raise Redeclared("Member", node.name)
        member.add(node.name)
        
        if isinstance(node.member_type, StructType):
            if node.member_type.struct_name not in o["structs"]:
                raise UndeclaredStruct(node.member_type.struct_name)

    # ------------------------------------------------------------------
    # Function declaration
    # ------------------------------------------------------------------

    def visit_func_decl(self, node: FuncDecl, o: Any = None):
        env = o
        structs = env["structs"]
        funcs   = env["funcs"]

        if node.name in funcs:
            raise Redeclared("Function", node.name)

        #Check if "struct" return type of the function is declared
        if isinstance(node.return_type, StructType):
            if node.return_type.struct_name not in structs:
                raise UndeclaredStruct(node.return_type.struct_name)

        outer_params = o.get("curr_params", None)
        o["curr_params"] = set()
        
        #Param_scope is the outermost scope of a function
        param_scope: Dict[str, Type] = {}
        for p in node.params:
            p.accept(self, o)
            param_scope[p.name] = p.param_type
            
        if outer_params is not None:
            o["curr_params"] = outer_params
        else:
            del o["curr_params"]

        #Store func_info before visiting body
        func_info = FuncInfo(node.return_type, node.params)
        funcs[node.name] = func_info
        new_env = {
            "structs":     structs,
            "funcs":       funcs,
            "var_scopes":  [param_scope],   # parameter scope is scope[0]
            "param_names": set(param_scope.keys()),
            "func_info":   func_info,
            "in_loop":     False,
            "in_switch":   False,
        }

        #Visit body
        node.body.accept(self, new_env)

        #After visiting body: update func_info with inferred return type if needed
        env["funcs"][node.name] = new_env["func_info"]

    def visit_param(self, node: Param, o: Any = None):
        params = o["curr_params"]
        if node.name in params:
            raise Redeclared("Parameter", node.name)
        params.add(node.name)
        
        #Check if "struct" param type is declared
        if isinstance(node.param_type, StructType):
            if node.param_type.struct_name not in o["structs"]:
                raise UndeclaredStruct(node.param_type.struct_name)

    # ------------------------------------------------------------------
    # Types — just return themselves
    # ------------------------------------------------------------------

    def visit_int_type(self, node: IntType, o: Any = None):
        return IntType()

    def visit_float_type(self, node: FloatType, o: Any = None):
        return FloatType()

    def visit_string_type(self, node: StringType, o: Any = None):
        return StringType()

    def visit_void_type(self, node: VoidType, o: Any = None):
        return VoidType()

    def visit_struct_type(self, node: StructType, o: Any = None):
        return node

    # ------------------------------------------------------------------
    # BlockStmt
    # ------------------------------------------------------------------

    def visit_block_stmt(self, node: BlockStmt, o: Any = None):
        env = o
        #Add a new local block scope
        env["var_scopes"].append({})

        unresolved_autos: List[str] = []

        #Record auto variables without init
        for stmt in node.statements:
            if isinstance(stmt, VarDecl) and stmt.var_type is None and stmt.init_value is None:
                unresolved_autos.append(stmt.name)
            stmt.accept(self, env)

        #Check if unresolved autos got a type
        block_scope = env["var_scopes"][-1]
        for name in unresolved_autos:
            if name in block_scope and block_scope[name] is None:
                raise TypeCannotBeInferred(node)

        env["var_scopes"].pop()

    # ------------------------------------------------------------------
    # VarDecl
    # ------------------------------------------------------------------

    def visit_var_decl(self, node: VarDecl, o: Any = None):
        env = o
        structs    = env["structs"]
        scopes     = env["var_scopes"]
        param_names= env["param_names"]
        block_scope = scopes[-1]  # innermost block scope

        # --- Redeclared check ---
        var_name = node.name
        #Parameter cannot be re-declared as local anywhere in function
        if var_name in param_names:
            raise Redeclared("Variable", var_name)
        #Same block (not counting parameter scope at index 0):
        #The block_scope is the innermost scope; check only there for re-declaration
        if var_name in block_scope:
            raise Redeclared("Variable", var_name)

        # --- Validate struct type ---
        if isinstance(node.var_type, StructType):
            if node.var_type.struct_name not in structs:
                raise UndeclaredStruct(node.var_type.struct_name)

        # --- Process initializer ---
        init_type: Optional[Type] = None
        if node.init_value is not None:
            init_type = node.init_value.accept(self, env)

        # --- Determine declared type ---
        if node.var_type is None:
            # auto
            if node.init_value is not None:
                # Infer from initializer
                if init_type is None:
                    raise TypeCannotBeInferred(node.init_value)
                declared_type = init_type
            else:
                # auto without init — will be resolved later
                declared_type = None
        else:
            declared_type = node.var_type
            # Type-check: init value must match
            if init_type is not None and not isinstance(node.init_value, StructLiteral):
                if not types_equal(declared_type, init_type):
                    raise TypeMismatchInStatement(node)

            elif init_type is None and isinstance(node.init_value, FuncCall):
                raise TypeCannotBeInferred(node.init_value)

        # For StructLiteral initializer of struct type: verify member counts
        if node.init_value is not None and isinstance(node.init_value, StructLiteral):
            if isinstance(declared_type, StructType):
                struct_decl = structs.get(declared_type.struct_name)
                if struct_decl:
                    if len(node.init_value.values) != len(struct_decl.members):
                        raise TypeMismatchInStatement(node)
                    for val, mem in zip(node.init_value.values, struct_decl.members):
                        val_type = val.accept(self, env)
                        if not types_equal(val_type, mem.member_type):
                            raise TypeMismatchInStatement(node)

        block_scope[var_name] = declared_type

    # ------------------------------------------------------------------
    # IfStmt
    # ------------------------------------------------------------------

    def visit_if_stmt(self, node: IfStmt, o: Any = None):
        cond_type = node.condition.accept(self, o)
        if not isinstance(cond_type, IntType):
            raise TypeMismatchInStatement(node)
        node.then_stmt.accept(self, o)
        if node.else_stmt:
            node.else_stmt.accept(self, o)

    # ------------------------------------------------------------------
    # WhileStmt
    # ------------------------------------------------------------------

    def visit_while_stmt(self, node: WhileStmt, o: Any = None):
        cond_type = node.condition.accept(self, o)
        if not isinstance(cond_type, IntType):
            raise TypeMismatchInStatement(node)
        old_in_loop  = o["in_loop"]
        old_in_switch = o["in_switch"]
        o["in_loop"]   = True
        o["in_switch"] = False
        node.body.accept(self, o)
        o["in_loop"]   = old_in_loop
        o["in_switch"] = old_in_switch

    # ------------------------------------------------------------------
    # ForStmt
    # ------------------------------------------------------------------

    def visit_for_stmt(self, node: ForStmt, o: Any = None):
        env = o
        # For init runs in a new scope so VarDecl of loop var is scoped
        env["var_scopes"].append({})

        if node.init is not None:
            node.init.accept(self, env)

        if node.condition is not None:
            cond_type = node.condition.accept(self, env)
            if not isinstance(cond_type, IntType):
                # Pop scope before raising
                env["var_scopes"].pop()
                raise TypeMismatchInStatement(node)

        if node.update is not None:
            node.update.accept(self, env)

        old_in_loop   = env["in_loop"]
        old_in_switch = env["in_switch"]
        env["in_loop"]   = True
        env["in_switch"] = False

        # If body is a BlockStmt we DON'T want a double scope push,
        # since visit_block_stmt already pushes one.
        node.body.accept(self, env)

        env["in_loop"]   = old_in_loop
        env["in_switch"] = old_in_switch
        env["var_scopes"].pop()

    # ------------------------------------------------------------------
    # SwitchStmt
    # ------------------------------------------------------------------

    def visit_switch_stmt(self, node: SwitchStmt, o: Any = None):
        expr_type = node.expr.accept(self, o)
        if not isinstance(expr_type, IntType):
            raise TypeMismatchInStatement(node)

        old_in_loop   = o["in_loop"]
        old_in_switch = o["in_switch"]
        o["in_switch"] = True
        # in_loop stays as-is: break is allowed in switch; continue still needs loop

        o["var_scopes"].append({})
        o["unresolved_autos"] = set()
        for case in node.cases:
            # Case label must be an integer literal, not just any int-typed expression
            case_type = case.expr.accept(self, o)
            is_const = self._is_constant_expr(case.expr)
            if not isinstance(case_type, IntType) or not is_const:
                raise TypeMismatchInStatement(node)  # node = SwitchStmt
            case.accept(self, o)
        if node.default_case:
            node.default_case.accept(self, o)
        
        block_scope = o["var_scopes"][-1]
        for name in o["unresolved_autos"]:
            if name in block_scope and block_scope[name] is None:
                raise TypeCannotBeInferred(node)

        o["in_loop"]   = old_in_loop
        o["in_switch"] = old_in_switch
        o["var_scopes"].pop()

    def visit_case_stmt(self, node: CaseStmt, o: Any = None):
        # Label validation (IntLiteral only) is done in visit_switch_stmt.
        # Here we only visit the body statements.
        unresolved_autos = o["unresolved_autos"]
        for stmt in node.statements:
            if isinstance(stmt, VarDecl) and stmt.var_type is None and stmt.init_value is None:
                unresolved_autos.add(stmt.name)
            stmt.accept(self, o)

    def visit_default_stmt(self, node: DefaultStmt, o: Any = None):
        unresolved_autos = o["unresolved_autos"]
        for stmt in node.statements:
            if isinstance(stmt, VarDecl) and stmt.var_type is None and stmt.init_value is None:
                unresolved_autos.add(stmt.name)
            stmt.accept(self, o)

    # ------------------------------------------------------------------
    # BreakStmt / ContinueStmt
    # ------------------------------------------------------------------

    def visit_break_stmt(self, node: BreakStmt, o: Any = None):
        if not o["in_loop"] and not o["in_switch"]:
            raise MustInLoop(node)

    def visit_continue_stmt(self, node: ContinueStmt, o: Any = None):
        if not o["in_loop"]:
            raise MustInLoop(node)

    # ------------------------------------------------------------------
    # ReturnStmt
    # ------------------------------------------------------------------

    def visit_return_stmt(self, node: ReturnStmt, o: Any = None):
        env = o
        func_info: FuncInfo = env["func_info"]

        if node.expr is None:
            # return; — function must be void or inferred-void
            if func_info.return_type is None:
                # inferred — treat first bare return as void
                func_info.return_type = VoidType()
            elif not isinstance(func_info.return_type, VoidType):
                raise TypeMismatchInStatement(node)
        else:
            expr_type = node.expr.accept(self, env)
            if expr_type is None:
                raise TypeCannotBeInferred(node)
            if func_info.return_type is None:
                # infer return type from first return
                func_info.return_type = expr_type
            elif isinstance(func_info.return_type, VoidType):
                # void function cannot return a value
                raise TypeMismatchInStatement(node)
            else:
                if not types_equal(func_info.return_type, expr_type):
                    raise TypeMismatchInStatement(node)

    # ------------------------------------------------------------------
    # ExprStmt
    # ------------------------------------------------------------------

    def visit_expr_stmt(self, node: ExprStmt, o: Any = None):
        if isinstance(node.expr, AssignExpr):
            # If lhs is illegal (not ID or MemAccess) -> visit_assign_expr
            lhs_type = node.expr.lhs
            if not isinstance(lhs_type, (Identifier, MemberAccess)):
                node.expr.accept(self, o)
                
            # If lhs is legal, type mismatches become statement errors
            else:
                try:
                    node.expr.accept(self, o)
                except TypeMismatchInExpression:
                    raise TypeMismatchInStatement(node.expr)    
        else:
            node.expr.accept(self, o)

    # ------------------------------------------------------------------
    # Expressions — return the resolved type (or raise)
    # ------------------------------------------------------------------

    def visit_binary_op(self, node: BinaryOp, o: Any = None) -> Optional[Type]:
        left_type  = node.left.accept(self, o)
        right_type = node.right.accept(self, o)

        op = node.operator

        # --- Try to infer auto from the other side ---
        left_type, right_type = self._propagate_binary(
            node, left_type, right_type, op, o
        )

        if op in ("+", "-", "*", "/"):
            if not is_numeric(left_type) or not is_numeric(right_type):
                raise TypeMismatchInExpression(node)
            return arithmetic_result(left_type, right_type)

        elif op == "%":
            if not isinstance(left_type, IntType) or not isinstance(right_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()

        elif op in ("==", "!=", "<", "<=", ">", ">="):
            if not is_numeric(left_type) or not is_numeric(right_type):
                raise TypeMismatchInExpression(node)
            return IntType()

        elif op in ("&&", "||"):
            if not isinstance(left_type, IntType) or not isinstance(right_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()

        return None

    def _propagate_binary(self, node: BinaryOp, left_type, right_type, op, env):
        """
        If one side is a resolved type and the other is an unresolved auto
        (lookup returns None), propagate the known type to the auto variable.
        If both are None, raise TypeCannotBeInferred(node).
        """
        if left_type is None and right_type is None:
            raise TypeCannotBeInferred(node)

        if left_type is None:
            # Try to resolve
            resolved = self._resolve_auto_from_type(node.left, right_type, env, op)
            if resolved is None:
                raise TypeCannotBeInferred(node)
            left_type = resolved

        if right_type is None:
            resolved = self._resolve_auto_from_type(node.right, left_type, env, op)
            if resolved is None:
                raise TypeCannotBeInferred(node)
            right_type = resolved

        return left_type, right_type

    def _resolve_auto_from_type(self, expr: Expr, known_type: Type, env, op=None) -> Optional[Type]:
        """
        If `expr` is an Identifier whose current type is None (unresolved auto),
        assign `known_type` to it and return `known_type`.
        Otherwise just return None (cannot resolve).
        """
        if isinstance(expr, Identifier):
            var_type = self._lookup_var(expr.name, env)
            if var_type is None:
                # It's an unresolved auto — assign the known type
                self._update_var_type(expr.name, known_type, env)
                return known_type
        return None

    def visit_prefix_op(self, node: PrefixOp, o: Any = None) -> Optional[Type]:
        op = node.operator
        if op in ("++", "--"):
            # operand must be Identifier or MemberAccess
            if not isinstance(node.operand, (Identifier, MemberAccess)):
                raise TypeMismatchInExpression(node)
            operand_type = node.operand.accept(self, o)
            if not isinstance(operand_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()

        elif op == "!":
            operand_type = node.operand.accept(self, o)
            if not isinstance(operand_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()

        elif op in ("+", "-"):
            operand_type = node.operand.accept(self, o)
            if operand_type is None:
                raise TypeCannotBeInferred(node)

            if not is_numeric(operand_type):
                raise TypeMismatchInExpression(node)
            return operand_type
        return None

    def visit_postfix_op(self, node: PostfixOp, o: Any = None) -> Optional[Type]:
        op = node.operator
        if op in ("++", "--"):
            if not isinstance(node.operand, (Identifier, MemberAccess)):
                raise TypeMismatchInExpression(node)
            operand_type = node.operand.accept(self, o)
            if not isinstance(operand_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()
        return None

    def visit_assign_expr(self, node: AssignExpr, o: Any = None) -> Optional[Type]:
        """
        Assignment expression. Handles:
        - auto inference: if lhs is auto, infer from rhs; if rhs is auto, infer from lhs
        - type mismatch
        """
        # lhs must be Identifier or MemberAccess
        if not isinstance(node.lhs, (Identifier, MemberAccess)):
            raise TypeMismatchInExpression(node)

        lhs_type = node.lhs.accept(self, o)
        rhs_type = node.rhs.accept(self, o)

        # If lhs is unresolved auto
        if lhs_type is None and rhs_type is None:
            raise TypeCannotBeInferred(node)

        if lhs_type is None:
            # resolve lhs auto from rhs
            if isinstance(node.lhs, Identifier):
                self._update_var_type(node.lhs.name, rhs_type, o)
                lhs_type = rhs_type
            else:
                raise TypeCannotBeInferred(node)
        elif rhs_type is None:
            # resolve rhs auto from lhs
            if isinstance(node.rhs, Identifier):
                self._update_var_type(node.rhs.name, lhs_type, o)
                rhs_type = lhs_type
            else:
                raise TypeCannotBeInferred(node)

        if not types_equal(lhs_type, rhs_type):
            # Treat assignment in expression context as TypeMismatchInExpression
            raise TypeMismatchInExpression(node)

        return lhs_type

    def visit_member_access(self, node: MemberAccess, o: Any = None) -> Optional[Type]:
        obj_type = node.obj.accept(self, o)
        if not isinstance(obj_type, StructType):
            raise TypeMismatchInExpression(node)
        structs = o["structs"]
        struct_name = obj_type.struct_name
        if struct_name not in structs:
            raise TypeMismatchInExpression(node)
        struct_decl = structs[struct_name]
        for mem in struct_decl.members:
            if mem.name == node.member:
                return mem.member_type
        raise TypeMismatchInExpression(node)

    def visit_func_call(self, node: FuncCall, o: Any = None) -> Optional[Type]:
        env = o
        funcs = env["funcs"]
        if node.name not in funcs:
            raise UndeclaredFunction(node.name)
        func_info = funcs[node.name]

        # Check arg count
        if len(node.args) != len(func_info.params):
            raise TypeMismatchInExpression(node)

        # Check arg types; also handle auto inference from parameter types
        for arg, param in zip(node.args, func_info.params):
            arg_type = arg.accept(self, env)
            if arg_type is None:
                # Unresolved auto — infer from param type
                if isinstance(arg, Identifier):
                    self._update_var_type(arg.name, param.param_type, env)
                    arg_type = param.param_type
                else:
                    raise TypeMismatchInExpression(node)
            if not types_equal(arg_type, param.param_type):
                raise TypeMismatchInExpression(node)

        return func_info.return_type

    def visit_identifier(self, node: Identifier, o: Any = None) -> Optional[Type]:
        var_type = self._lookup_var(node.name, o)
        if var_type is None and not self._var_exists(node.name, o):
            raise UndeclaredIdentifier(node.name)
        return var_type  # may be None if auto not yet resolved

    def visit_struct_literal(self, node: StructLiteral, o: Any = None):
        # Types of struct literal elements are checked in VarDecl
        return None

    # ------------------------------------------------------------------
    # Literals
    # ------------------------------------------------------------------

    def visit_int_literal(self, node: IntLiteral, o: Any = None) -> IntType:
        return IntType()

    def visit_float_literal(self, node: FloatLiteral, o: Any = None) -> FloatType:
        return FloatType()

    def visit_string_literal(self, node: StringLiteral, o: Any = None) -> StringType:
        return StringType()

    # ------------------------------------------------------------------
    # Scope helpers
    # ------------------------------------------------------------------

    def _var_exists(self, name: str, env: dict) -> bool:
        """Return True if `name` is declared in any scope."""
        for scope in reversed(env["var_scopes"]):
            if name in scope:
                return True
        return False

    def _lookup_var(self, name: str, env: dict) -> Optional[Type]:
        """
        Look up variable `name` from innermost scope outward.
        Returns the type (possibly None for unresolved auto) or
        None if not found (caller must check _var_exists to distinguish).
        """
        for scope in reversed(env["var_scopes"]):
            if name in scope:
                return scope[name]
        return None

    def _update_var_type(self, name: str, typ: Type, env: dict):
        """Set resolved type for an auto variable."""
        for scope in reversed(env["var_scopes"]):
            if name in scope:
                scope[name] = typ
                return

    def _is_constant_expr(self, expr: Expr) -> bool:
        """Recursively check if an expression is a compile-time constant."""
        if isinstance(expr, IntLiteral):
            return True
        if isinstance(expr, PrefixOp):
            return self._is_constant_expr(expr.operand)
        if isinstance(expr, BinaryOp):
            return self._is_constant_expr(expr.left) and self._is_constant_expr(expr.right)
        
        # If it's an Identifier, FuncCall, AssignExpr, etc., it is NOT constant.
        return False