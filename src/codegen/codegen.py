"""
Code generator for TyC.
"""

from typing import Any

from ..utils.nodes import *
from ..utils.visitor import BaseVisitor
from .emitter import *
from .frame import *
from .io import IO_SYMBOL_LIST
from .utils import *


class StringArrayType:
    """Marker type for JVM main(String[] args)."""
    pass


class CodeGenerator(BaseVisitor):
    """Minimal AST -> Jasmin code generator."""

    def __init__(self):
        self.emit = None
        self.functions = {}
        self.struct_defs = {}   # struct_name -> {field_name: field_type}
        self.current_return_type = VoidType()
        self.class_name = "TyC"

    def _lookup_symbol(self, name: str, sym_list: list[Symbol]) -> Symbol:
        for sym in reversed(sym_list):
            if sym.name == name:
                return sym
        raise RuntimeError(f"Undeclared symbol: {name}")

    def _infer_type(self, node: Expr, o: Access):
        if isinstance(node, IntLiteral):
            return IntType()
        if isinstance(node, FloatLiteral):
            return FloatType()
        if isinstance(node, StringLiteral):
            return StringType()
        if isinstance(node, Identifier):
            return self._lookup_symbol(node.name, o.sym).type
        if isinstance(node, AssignExpr):
            return self._infer_type(node.rhs, o)
        if isinstance(node, FuncCall):
            return self.functions[node.name].type.return_type
        if isinstance(node, BinaryOp):
            if node.operator in ["+", "-", "*", "/", "%"]:
                left_type = self._infer_type(node.left, o)
                right_type = self._infer_type(node.right, o)
                if is_float_type(left_type) or is_float_type(right_type):
                    return FloatType()
                return IntType()
            if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
                return IntType()
        return IntType()


    def _find_return_expr(self, stmt):
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
        sym = []
        for p in node.params:
            sym.append(Symbol(p.name, p.param_type, Index(0)))
        return self._infer_type(ret_expr, Access(None, sym))

    def visit_program(self, node: Program, o: Any = None):
        # First pass: collect struct definitions so field types are known
        for decl in node.decls:
            if isinstance(decl, StructDecl):
                self.struct_defs[decl.name] = {
                    m.name: m.member_type for m in decl.members
                }

        # Emit one Jasmin file per struct (each becomes its own .class)
        for decl in node.decls:
            if isinstance(decl, StructDecl):
                self.visit(decl, None)

        # Main TyC class
        self.emit = Emitter(f"{self.class_name}.j")
        self.emit.print_out(self.emit.emit_prolog(self.class_name))

        for io_sym in IO_SYMBOL_LIST:
            self.functions[io_sym.name] = io_sym

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                return_type = self._infer_func_return_type(decl)
                param_types = [p.param_type for p in decl.params]
                self.functions[decl.name] = Symbol(
                    decl.name, FunctionType(param_types, return_type), CName(self.class_name)
                )

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                self.visit(decl, None)

        self.emit.emit_epilog()

    def visit_func_decl(self, node: FuncDecl, o: Any = None):
        self.current_return_type = self._infer_func_return_type(node)
        frame = Frame(node.name, self.current_return_type)
        frame.enter_scope(True)

        if node.name == "main":
            mtype = FunctionType([StringArrayType()], VoidType())
        else:
            mtype = FunctionType([p.param_type for p in node.params], self.current_return_type)

        self.emit.print_out(self.emit.emit_method(node.name, mtype, True))

        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))

        local_syms: list[Symbol] = []
        if node.name == "main":
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", StringArrayType(), start_label, end_label
                )
            )

        for param in node.params:
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(idx, param.name, param.param_type, start_label, end_label)
            )
            local_syms.append(Symbol(param.name, param.param_type, Index(idx)))

        sub_body = SubBody(frame, local_syms)
        self.visit(node.body, sub_body)

        if is_void_type(self.current_return_type):
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        self.emit.print_out(self.emit.emit_end_method(frame))

    def visit_block_stmt(self, node: BlockStmt, o: SubBody = None):
        if o is None:
            for stmt in node.statements:
                self.visit(stmt, o)
            return o
            
        o.frame.enter_scope(False)
        self.emit.print_out(self.emit.emit_label(o.frame.get_start_label(), o.frame))
        new_sym = list(o.sym)
        new_o = SubBody(o.frame, new_sym)
        if not hasattr(self, 'block_stack'):
            self.block_stack = []
        self.block_stack.append(node.statements)
        for stmt in node.statements:
            self.visit(stmt, new_o)
        self.block_stack.pop()
        self.emit.print_out(self.emit.emit_label(o.frame.get_end_label(), o.frame))
        o.frame.exit_scope()
        return o


    def _infer_auto_type_from_assignment(self, var_name, o):
        if not hasattr(self, 'block_stack') or not self.block_stack:
            return IntType()
        
        # Scan current block for first assignment to var_name
        current_stmts = self.block_stack[-1]
        for stmt in current_stmts:
            if isinstance(stmt, ExprStmt) and isinstance(stmt.expr, AssignExpr):
                assign = stmt.expr
                if isinstance(assign.lhs, Identifier) and assign.lhs.name == var_name:
                    return self._infer_type(assign.rhs, o)
        return IntType()

    def visit_var_decl(self, node: VarDecl, o: SubBody = None):
        frame = o.frame
        idx = frame.get_new_index()
        access = Access(frame, o.sym)
        if node.var_type:
            var_type = node.var_type
        elif node.init_value:
            var_type = self._infer_type(node.init_value, access)
        else:
            var_type = self._infer_auto_type_from_assignment(node.name, access)
        self.emit.print_out(
            self.emit.emit_var(
                idx, node.name, var_type, frame.get_start_label(), frame.get_end_label()
            )
        )
        if node.init_value is not None:
            if isinstance(node.init_value, StructLiteral) and is_struct_type(var_type):
                rhs_code, _ = self._emit_struct_literal(node.init_value, var_type, access)
            else:
                rhs_code, _ = self.visit(node.init_value, access)
            self.emit.print_out(rhs_code)
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        else:
            if is_struct_type(var_type):
                self.emit.print_out(self.emit.emit_new_instance(var_type.struct_name, frame))
                self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
            elif isinstance(var_type, IntType):
                self.emit.print_out(self.emit.emit_push_iconst(0, frame))
                self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
            elif isinstance(var_type, FloatType):
                self.emit.print_out(self.emit.emit_push_fconst("0.0", frame))
                self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
            elif isinstance(var_type, StringType):
                self.emit.print_out(self.emit.emit_push_const("", var_type, frame))
                self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        o.sym.append(Symbol(node.name, var_type, Index(idx)))
        return o

    def visit_expr_stmt(self, node: ExprStmt, o: SubBody = None):
        code, expr_type = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        if not is_void_type(expr_type):
            self.emit.print_out(self.emit.emit_pop(o.frame))
        return o

    @staticmethod
    def _ends_with_return(stmt) -> bool:
        """Return True if stmt is guaranteed to end with a return (so no goto needed)."""
        if isinstance(stmt, ReturnStmt):
            return True
        if isinstance(stmt, BlockStmt) and stmt.statements:
            return CodeGenerator._ends_with_return(stmt.statements[-1])
        return False

    def visit_if_stmt(self, node: IfStmt, o: SubBody = None):
        frame = o.frame
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        if node.else_stmt:
            else_label = frame.get_new_label()
            end_label = frame.get_new_label()
            self.emit.print_out(self.emit.emit_if_false(else_label, frame))
            self.visit(node.then_stmt, o)
            if not self._ends_with_return(node.then_stmt):
                self.emit.print_out(self.emit.emit_goto(end_label, frame))
            self.emit.print_out(self.emit.emit_label(else_label, frame))
            self.visit(node.else_stmt, o)
            if not self._ends_with_return(node.then_stmt):
                self.emit.print_out(self.emit.emit_label(end_label, frame))
        else:
            end_label = frame.get_new_label()
            self.emit.print_out(self.emit.emit_if_false(end_label, frame))
            self.visit(node.then_stmt, o)
            if not self._ends_with_return(node.then_stmt):
                self.emit.print_out(self.emit.emit_label(end_label, frame))
            else:
                self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_while_stmt(self, node: WhileStmt, o: SubBody = None):
        frame = o.frame
        frame.enter_loop()
        start_label = frame.get_continue_label()   # continue jumps back here
        end_label = frame.get_break_label()          # break jumps here
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))
        self.visit(node.body, o)
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_loop()
        return o

    def visit_return_stmt(self, node: ReturnStmt, o: SubBody = None):
        if node.expr is None:
            self.emit.print_out(self.emit.emit_return(VoidType(), o.frame))
            return o
        code, ret_type = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        self.emit.print_out(self.emit.emit_return(ret_type, o.frame))
        return o

    def visit_binary_op(self, node: BinaryOp, o: Access = None):
        frame = o.frame

        # Short-circuit && and ||
        if node.operator == "&&":
            false_label = frame.get_new_label()
            end_label = frame.get_new_label()
            left_code, _ = self.visit(node.left, o)
            right_code, _ = self.visit(node.right, o)
            # Evaluate left; if 0 jump to false
            code = left_code + self.emit.emit_if_false(false_label, frame)
            # Evaluate right; if 0 jump to false
            code += right_code + self.emit.emit_if_false(false_label, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_goto(end_label, frame)
            code += self.emit.emit_label(false_label, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_label(end_label, frame)
            return code, IntType()

        if node.operator == "||":
            true_label = frame.get_new_label()
            end_label = frame.get_new_label()
            left_code, _ = self.visit(node.left, o)
            right_code, _ = self.visit(node.right, o)
            code = left_code + self.emit.emit_if_true(true_label, frame)
            code += right_code + self.emit.emit_if_true(true_label, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_goto(end_label, frame)
            code += self.emit.emit_label(true_label, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_label(end_label, frame)
            return code, IntType()

        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)

        # Promote int to float when mixing types
        if is_float_type(left_type) and is_int_type(right_type):
            right_code = right_code + self.emit.emit_i2f(frame)
            right_type = FloatType()
        elif is_int_type(left_type) and is_float_type(right_type):
            # We must insert i2f between left and right in the instruction stream
            # Emit: left_code, i2f, right_code  (i2f runs after left is loaded)
            left_code = left_code + self.emit.emit_i2f(frame)
            left_type = FloatType()

        if node.operator in ["+", "-"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            return (
                left_code
                + right_code
                + self.emit.emit_add_op(node.operator, result_type, frame),
                result_type,
            )
        if node.operator in ["*", "/"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            return (
                left_code
                + right_code
                + self.emit.emit_mul_op(node.operator, result_type, frame),
                result_type,
            )
        if node.operator == "%":
            return left_code + right_code + self.emit.emit_mod(frame), IntType()
        if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
            op_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            return left_code + right_code + self.emit.emit_re_op(node.operator, op_type, frame), IntType()
        raise RuntimeError(f"Unsupported operator: {node.operator}")

    def visit_assign_expr(self, node: AssignExpr, o: Access = None):
        frame = o.frame
        if isinstance(node.lhs, Identifier):
            lhs_sym = self._lookup_symbol(node.lhs.name, o.sym)
            lhs_type = lhs_sym.type
            idx = lhs_sym.value.value
            if isinstance(node.rhs, StructLiteral) and is_struct_type(lhs_type):
                rhs_code, rhs_type = self._emit_struct_literal(node.rhs, lhs_type, o)
            else:
                rhs_code, rhs_type = self.visit(node.rhs, o)
            code = rhs_code + self.emit.emit_dup(frame) + self.emit.emit_write_var(
                node.lhs.name, lhs_type, idx, frame
            )
            return code, rhs_type
        elif isinstance(node.lhs, MemberAccess):
            # obj.field = rhs  =>  load obj, load rhs, putfield
            obj_code, obj_type = self.visit(node.lhs.obj, o)
            if not is_struct_type(obj_type):
                raise RuntimeError("MemberAccess assignment on non-struct")
            field_type = self._get_member_type(obj_type.struct_name, node.lhs.member)
            if isinstance(node.rhs, StructLiteral) and is_struct_type(field_type):
                rhs_code, rhs_type = self._emit_struct_literal(node.rhs, field_type, o)
            else:
                rhs_code, rhs_type = self.visit(node.rhs, o)
            field_lexeme = f"{obj_type.struct_name}/{node.lhs.member}"
            # dup_x1: stack was [..., obj, rhs] -> [..., rhs, obj, rhs]
            code = obj_code + rhs_code + self.emit.emit_dup_x1(frame)
            code += self.emit.emit_put_field(field_lexeme, field_type, frame)
            return code, rhs_type
        else:
            raise RuntimeError("Assignment LHS must be Identifier or MemberAccess")

    def visit_func_call(self, node: FuncCall, o: Access = None):
        frame = o.frame
        fn_sym = self.functions[node.name]
        fn_type = fn_sym.type
        code = ""
        for arg in node.args:
            arg_code, _ = self.visit(arg, o)
            code += arg_code
        code += self.emit.emit_invoke_static(f"{fn_sym.value.value}/{node.name}", fn_type, frame)
        return code, fn_type.return_type

    def visit_identifier(self, node: Identifier, o: Access = None):
        sym = self._lookup_symbol(node.name, o.sym)
        return self.emit.emit_read_var(node.name, sym.type, sym.value.value, o.frame), sym.type

    def visit_int_literal(self, node: IntLiteral, o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: FloatLiteral, o: Access = None):
        return self.emit.emit_push_fconst(str(node.value), o.frame), FloatType()

    def visit_string_literal(self, node: StringLiteral, o: Access = None):
        return self.emit.emit_push_const(node.value, StringType(), o.frame), StringType()

    def visit_struct_decl(self, node: StructDecl, o: Any = None):
        """Emit a separate Jasmin class file for each struct."""
        struct_emit = Emitter(f"{node.name}.j")
        struct_emit.print_out(struct_emit.emit_prolog(node.name))
        # Fields
        for member in node.members:
            jvm_type = struct_emit.get_jvm_type(member.member_type)
            struct_emit.print_out(f".field public {member.name} {jvm_type}\n")
        # Default constructor
        struct_emit.print_out("\n.method public <init>()V\n")
        struct_emit.print_out("Label0:\n")
        struct_emit.print_out("\taload_0\n")
        struct_emit.print_out("\tinvokespecial java/lang/Object/<init>()V\n")
        
        for member in node.members:
            struct_emit.print_out("\taload_0\n")
            if is_int_type(member.member_type):
                struct_emit.print_out("\ticonst_0\n")
            elif is_float_type(member.member_type):
                struct_emit.print_out("\tfconst_0\n")
            elif is_string_type(member.member_type):
                struct_emit.print_out('\tldc ""\n')
            elif is_struct_type(member.member_type):
                struct_name = member.member_type.struct_name
                struct_emit.print_out(f"\tnew {struct_name}\n")
                struct_emit.print_out("\tdup\n")
                struct_emit.print_out(f"\tinvokespecial {struct_name}/<init>()V\n")
            
            jvm_type = struct_emit.get_jvm_type(member.member_type)
            struct_emit.print_out(f"\tputfield {node.name}/{member.name} {jvm_type}\n")
            
        struct_emit.print_out("\treturn\n")
        struct_emit.print_out("Label1:\n")
        struct_emit.print_out(".limit stack 3\n")
        struct_emit.print_out(".limit locals 1\n")
        struct_emit.print_out(".end method\n")
        struct_emit.emit_epilog()
        return None

    def visit_member_decl(self, node: MemberDecl, o: Any = None):
        return None

    def visit_param(self, node: Param, o: Any = None):
        return None

    def visit_int_type(self, node: IntType, o: Any = None):
        return node

    def visit_float_type(self, node: FloatType, o: Any = None):
        return node

    def visit_string_type(self, node: StringType, o: Any = None):
        return node

    def visit_void_type(self, node: VoidType, o: Any = None):
        return node

    def visit_struct_type(self, node: StructType, o: Any = None):
        return node

    def visit_for_stmt(self, node: ForStmt, o: SubBody = None):
        """Generate code for a for loop:
           for (init; cond; update) body
        """
        frame = o.frame
        frame.enter_loop()
        con_label = frame.get_continue_label()  # jump here on continue (update + re-check)
        brk_label = frame.get_break_label()     # jump here on break

        # -- init --
        if node.init is not None:
            o = self.visit(node.init, o)

        # Label before condition check
        check_label = frame.get_new_label()
        self.emit.print_out(self.emit.emit_label(check_label, frame))

        # -- condition --
        if node.condition is not None:
            cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
            self.emit.print_out(cond_code)
            self.emit.print_out(self.emit.emit_if_false(brk_label, frame))

        # -- body --
        self.visit(node.body, o)

        # -- continue label: execute update then loop back --
        self.emit.print_out(self.emit.emit_label(con_label, frame))
        if node.update is not None:
            upd_code, upd_type = self.visit(node.update, Access(frame, o.sym))
            self.emit.print_out(upd_code)
            # discard result if non-void
            if not is_void_type(upd_type):
                self.emit.print_out(self.emit.emit_pop(frame))

        self.emit.print_out(self.emit.emit_goto(check_label, frame))
        self.emit.print_out(self.emit.emit_label(brk_label, frame))
        frame.exit_loop()
        return o

    def visit_switch_stmt(self, node: SwitchStmt, o: SubBody = None):
        """Generate code for switch with fall-through (C-style)."""
        frame = o.frame
        
        # Enter scope for variables declared inside switch
        frame.enter_scope(False)
        self.emit.print_out(self.emit.emit_label(frame.get_start_label(), frame))
        new_sym = list(o.sym)
        new_o = SubBody(frame, new_sym)

        frame.enter_loop()  # break jumps to brk_label
        if len(frame.con_label) >= 2:
            frame.con_label[-1] = frame.con_label[-2]
        brk_label = frame.get_break_label()

        # Evaluate switch expression (must be int)
        expr_code, _ = self.visit(node.expr, Access(frame, o.sym))
        self.emit.print_out(expr_code)

        # Allocate a local slot to hold switch value
        sw_idx = frame.get_new_index()
        self.emit.print_out(self.emit.emit_write_var("__sw__", IntType(), sw_idx, frame))

        # Build case labels
        case_labels = [frame.get_new_label() for _ in node.cases]
        default_label = frame.get_new_label() if node.default_case else brk_label
        end_label = brk_label

        # Dispatch: for each case compare and jump
        for i, case in enumerate(node.cases):
            self.emit.print_out(self.emit.emit_read_var("__sw__", IntType(), sw_idx, frame))
            case_val_code, _ = self.visit(case.expr, Access(frame, o.sym))
            self.emit.print_out(case_val_code)
            self.emit.print_out(self.emit.emit_re_op("==", IntType(), frame))
            self.emit.print_out(self.emit.emit_if_true(case_labels[i], frame))

        self.emit.print_out(self.emit.emit_goto(default_label, frame))

        # Emit case bodies (fall-through)
        for i, case in enumerate(node.cases):
            self.emit.print_out(self.emit.emit_label(case_labels[i], frame))
            for stmt in case.statements:
                new_o = self.visit(stmt, new_o)

        # Emit default body
        if node.default_case:
            self.emit.print_out(self.emit.emit_label(default_label, frame))
            for stmt in node.default_case.statements:
                new_o = self.visit(stmt, new_o)

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_loop()
        
        self.emit.print_out(self.emit.emit_label(frame.get_end_label(), frame))
        frame.exit_scope()
        return o

    def visit_case_stmt(self, node: CaseStmt, o: Any = None):
        # Handled inline in visit_switch_stmt
        return o

    def visit_default_stmt(self, node: DefaultStmt, o: Any = None):
        # Handled inline in visit_switch_stmt
        return o

    def visit_break_stmt(self, node: BreakStmt, o: SubBody = None):
        frame = o.frame
        brk_label = frame.get_break_label()
        self.emit.print_out(self.emit.emit_goto(brk_label, frame))
        return o

    def visit_continue_stmt(self, node: ContinueStmt, o: SubBody = None):
        frame = o.frame
        con_label = frame.get_continue_label()
        self.emit.print_out(self.emit.emit_goto(con_label, frame))
        return o

    def visit_prefix_op(self, node: PrefixOp, o: Access = None):
        frame = o.frame
        op = node.operator
        if op == "!":
            # logical NOT: result = (operand == 0) ? 1 : 0
            operand_code, _ = self.visit(node.operand, o)
            not_label = frame.get_new_label()
            end_label = frame.get_new_label()
            code = (
                operand_code
                + self.emit.emit_if_true(not_label, frame)   # if non-zero -> 0
                + self.emit.emit_push_iconst(1, frame)
                + self.emit.emit_goto(end_label, frame)
            )
            frame.pop()  # emit_label pops nothing; manually balance
            code += self.emit.emit_label(not_label, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_label(end_label, frame)
            return code, IntType()

        if op in ("+", "-"):
            operand_code, op_type = self.visit(node.operand, o)
            if op == "+":
                return operand_code, op_type
            # negation
            return operand_code + self.emit.emit_neg_op(op_type, frame), op_type

        # ++ / -- prefix: increment/decrement and keep new value
        if op in ("++", "--"):
            if not isinstance(node.operand, Identifier):
                raise RuntimeError("Prefix ++/-- only supported on identifiers")
            sym = self._lookup_symbol(node.operand.name, o.sym)
            idx = sym.value.value
            load_code = self.emit.emit_read_var(node.operand.name, sym.type, idx, frame)
            one_code = self.emit.emit_push_iconst(1, frame)
            add_code = self.emit.emit_add_op("+" if op == "++" else "-", IntType(), frame)
            dup_code = self.emit.emit_dup(frame)
            store_code = self.emit.emit_write_var(node.operand.name, sym.type, idx, frame)
            return load_code + one_code + add_code + dup_code + store_code, IntType()

        raise RuntimeError(f"Unsupported prefix operator: {op}")

    def visit_postfix_op(self, node: PostfixOp, o: Access = None):
        frame = o.frame
        op = node.operator
        if op in ("++", "--"):
            if not isinstance(node.operand, Identifier):
                raise RuntimeError("Postfix ++/-- only supported on identifiers")
            sym = self._lookup_symbol(node.operand.name, o.sym)
            idx = sym.value.value
            # load original value (to return), then load again, add 1, store
            load_orig = self.emit.emit_read_var(node.operand.name, sym.type, idx, frame)
            load_again = self.emit.emit_read_var(node.operand.name, sym.type, idx, frame)
            one_code = self.emit.emit_push_iconst(1, frame)
            add_code = self.emit.emit_add_op("+" if op == "++" else "-", IntType(), frame)
            store_code = self.emit.emit_write_var(node.operand.name, sym.type, idx, frame)
            return load_orig + load_again + one_code + add_code + store_code, IntType()
        raise RuntimeError(f"Unsupported postfix operator: {op}")

    def visit_member_access(self, node: MemberAccess, o: Access = None):
        """Generate code for struct member read (obj.field)."""
        frame = o.frame
        obj_code, obj_type = self.visit(node.obj, o)
        if not is_struct_type(obj_type):
            raise RuntimeError(f"MemberAccess on non-struct type: {obj_type}")
        struct_name = obj_type.struct_name
        # Look up member type from struct definitions
        member_type = self._get_member_type(struct_name, node.member)
        field_lexeme = f"{struct_name}/{node.member}"
        code = obj_code + self.emit.emit_get_field(field_lexeme, member_type, frame)
        return code, member_type

    def _get_member_type(self, struct_name: str, member_name: str):
        """Look up a member's type from our struct registry."""
        members = self.struct_defs.get(struct_name, {})
        if member_name not in members:
            raise RuntimeError(f"Struct '{struct_name}' has no member '{member_name}'")
        return members[member_name]

    def visit_struct_literal(self, node: StructLiteral, o: Access = None):
        """
        StructLiteral is context-dependent. We raise because the context
        (which struct type) must be supplied by the parent node (VarDecl/AssignExpr).
        The caller should use _emit_struct_literal instead.
        """
        raise RuntimeError(
            "StructLiteral cannot be visited standalone; use _emit_struct_literal with target type."
        )

    def _emit_struct_literal(self, node: StructLiteral, struct_type: StructType, o: Access):
        """Create a struct object and initialise its fields from node.values."""
        frame = o.frame
        struct_name = struct_type.struct_name
        members = list(self.struct_defs.get(struct_name, {}).items())
        code = self.emit.emit_new_instance(struct_name, frame)
        for (field_name, field_type), val_expr in zip(members, node.values):
            # dup the object ref before each field write
            code += self.emit.emit_dup(frame)
            if isinstance(val_expr, StructLiteral):
                val_code, _ = self._emit_struct_literal(val_expr, field_type, o)
            else:
                val_code, _ = self.visit(val_expr, o)
            code += val_code
            code += self.emit.emit_put_field(f"{struct_name}/{field_name}", field_type, frame)
        return code, struct_type

