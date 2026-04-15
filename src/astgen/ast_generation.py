from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *

class ASTGeneration(TyCVisitor):

# =========================================================
# PROGRAM
# =========================================================

    def visitProgram(self, ctx):
        decls = []
        for child in ctx.children:
            if isinstance(child, TyCParser.StructsContext):
                decls.extend(self.visit(child))
            elif isinstance(child, TyCParser.FunctionContext):
                decls.append(self.visit(child))

        return Program(decls)

# =========================================================
# STRUCT
# =========================================================

    def visitStructs(self, ctx:TyCParser.StructsContext):
        res = [self.visit(ctx.struct_declared())]
        for s in ctx.structs():
            res += self.visit(s)
        return res

    def visitStruct_declared(self, ctx:TyCParser.Struct_declaredContext):
        name = ctx.ID().getText()
        mems = [self.visit(m) for m in ctx.struct_mem()] if ctx.struct_mem() else []
        return StructDecl(name, mems)

    def visitStruct_mem(self, ctx:TyCParser.Struct_memContext):
        if ctx.primitive_type():
            typ = self.visit(ctx.primitive_type())
        else:
            typ = StructType(ctx.ID(0).getText())
        name = ctx.ID()[-1].getText()
        return MemberDecl(typ, name)

# =========================================================
# FUNCTION
# =========================================================

    def visitFunction(self, ctx:TyCParser.FunctionContext):
        ids = ctx.ID()
        name = ids[-1].getText()
        if ctx.VOID():
            rtype = VoidType()
        elif ctx.non_auto_type():
            rtype = self.visit(ctx.non_auto_type())
        elif len(ids) > 1:
            rtype = StructType(ids[0].getText())
        else:
            rtype = None
        params = self.visit(ctx.list_param()) if ctx.list_param() else []
        body = self.visit(ctx.list_statement()) if ctx.list_statement() else []
        return FuncDecl(rtype, name, params, BlockStmt(body))

# =========================================================
# PARAM
# =========================================================

    def visitList_param(self, ctx:TyCParser.List_paramContext):
        if ctx.COMMA():
            return [self.visit(ctx.param())] + self.visit(ctx.list_param())
        return [self.visit(ctx.param())]

    def visitParam(self, ctx: TyCParser.ParamContext):
        if ctx.primitive_type():
            typ = self.visit(ctx.primitive_type())
        else:
            typ = StructType(ctx.ID(0).getText())

        name = ctx.ID()[-1].getText()
        return Param(typ, name)

# =========================================================
# TYPES
# =========================================================

    def visitPrimitive_type(self, ctx:TyCParser.Primitive_typeContext):
        if ctx.INT(): return IntType()
        if ctx.FLOAT(): return FloatType()
        if ctx.STRING(): return StringType()
        if ctx.BOOL(): return StructType("bool")

    def visitNon_auto_type(self, ctx:TyCParser.Non_auto_typeContext):
        if ctx.primitive_type():
            return self.visit(ctx.primitive_type())
        return StructType()
    
    def visitAll_type(self, ctx:TyCParser.All_typeContext):
        if ctx.non_auto_type():
            return self.visit(ctx.non_auto_type())
        if ctx.AUTO():
            return None
        return StructType()

# =========================================================
# STATEMENTS
# =========================================================

    def visitList_statement(self, ctx:TyCParser.List_statementContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.statement())]

        return [self.visit(ctx.statement())] + self.visit(ctx.list_statement())

    def visitStatement(self, ctx:TyCParser.StatementContext):
        if ctx.assign_statement():
            stmt = self.visit(ctx.assign_statement())
            if isinstance(stmt, VarDecl):
                return stmt
            return ExprStmt(stmt)

        if ctx.var_statement():
            return self.visit(ctx.var_statement())

        if ctx.if_statement():
            return self.visit(ctx.if_statement())

        if ctx.while_statement():
            return self.visit(ctx.while_statement())

        if ctx.for_statement():
            return self.visit(ctx.for_statement())

        if ctx.switch_statement():
            return self.visit(ctx.switch_statement())

        if ctx.break_statement():
            return BreakStmt()

        if ctx.continue_statement():
            return ContinueStmt()

        if ctx.block_statement():
            return self.visit(ctx.block_statement())

        if ctx.expression_statement():
            return self.visit(ctx.expression_statement())

        if ctx.return_statement():
            return self.visit(ctx.return_statement())

# =========================================================
# VAR DECL
# =========================================================

    def visitVar_statement(self, ctx:TyCParser.Var_statementContext):
        typ = None
        if ctx.primitive_type():
            typ = self.visit(ctx.primitive_type())
        elif ctx.AUTO():
            typ = None
        else:
            typ = StructType(ctx.ID()[0].getText())
        name = ctx.ID()[-1].getText()
        init = None
        if ctx.expression():
            init = self.visit(ctx.expression())
        return VarDecl(typ, name, init)

# =========================================================
# ASSIGN
# =========================================================

    def visitAssign_statement(self, ctx:TyCParser.Assign_statementContext):
        if ctx.element():
            lhs = self.visit(ctx.element())
            rhs = self.visit(ctx.expression())
            return AssignExpr(lhs, rhs)

        type_name = ctx.ID(0).getText()
        var_name = ctx.ID(1).getText()
        elements = self.visit(ctx.list_expression()) if ctx.list_expression() else []
        init = StructLiteral(elements)

        return VarDecl(StructType(type_name), var_name, init)

# =========================================================
# IF
# =========================================================

    def visitIf_statement(self, ctx: TyCParser.If_statementContext):
        cond = self.visit(ctx.expression())
        thenStmt = self.visit(ctx.statement(0))

        elseStmt = None

        if ctx.if_statement():
            elseStmt = self.visit(ctx.if_statement())   # else if
        elif len(ctx.statement()) > 1:
            elseStmt = self.visit(ctx.statement(1))     # else

        return IfStmt(cond, thenStmt, elseStmt)

# =========================================================
# FOR
# =========================================================
    def visitUpdate_statement_lhs(self, ctx: TyCParser.Update_statement_lhsContext):
        if ctx.ID():
            return Identifier(ctx.ID()[-1].getText())
        elif ctx.expression():
            return self.visit(ctx.expression())
        elif ctx.INT_LIT():
            return IntLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        else:
            elements = self.visit(ctx.list_expression()) if ctx.list_expression() else []
            return StructLiteral(elements)
    
    def visitUpdate_statement(self, ctx):
        if ctx.assign_statement():
            return self.visit(ctx.assign_statement())

        lhs = self.visit(ctx.update_statement_lhs())
        prefix_ops = []
        postfix_ops = []
        for child in ctx.children:
            ops = child.getText()
            if ops in ["++", "--"]:
                if child == ctx.getChild(0):
                    prefix_ops.append(ops)
                elif child == ctx.getChild(ctx.getChildCount() - 1):
                    postfix_ops.append(ops)

        expr = lhs
        for op in postfix_ops:
            expr = PostfixOp(op, expr)
        for op in reversed(prefix_ops):
            expr = PrefixOp(op, expr)
        return expr
    

    def visitFor_statement(self, ctx:TyCParser.For_statementContext):
        init = None
        if ctx.var_statement():
            init = self.visit(ctx.var_statement())
        elif ctx.assign_statement():
            init = ExprStmt(self.visit(ctx.assign_statement()))
        cond = None
        if ctx.expression():
            cond = self.visit(ctx.expression())
        update = None
        if ctx.update_statement():
            update = self.visit(ctx.update_statement())
        if ctx.statement():
            body = self.visit(ctx.statement())
        elif ctx.block_statement():
            body = self.visit(ctx.block_statement())
        else:
            body = self.visit(ctx.break_statement())
        return ForStmt(init, cond, update, body)
    
# =========================================================
# WHILE
# =========================================================

    def visitWhile_statement(self, ctx:TyCParser.While_statementContext):
        cond = self.visit(ctx.expression())
        body = self.visit(ctx.statement())
        return WhileStmt(cond, body)
    
# =========================================================
# SWITCH
# =========================================================
    def visitSwitch_statement(self, ctx:TyCParser.Switch_statementContext):
        expr = self.visit(ctx.expression())
        cases, default_case = self.visit(ctx.switch_block())
        return SwitchStmt(expr, cases, default_case)


    def visitSwitch_block(self, ctx: TyCParser.Switch_blockContext):
        cases = []
        for c in ctx.switch_label():
            cases.append(self.visit(c))
        default_case = None
        if ctx.default_label():
            default_case = self.visit(ctx.default_label())

        return cases, default_case


    def visitSwitch_label(self, ctx: TyCParser.Switch_labelContext):
        expr = self.visit(ctx.expression())
        stmts = self.visit(ctx.list_statement()) if ctx.list_statement() else []
        return CaseStmt(expr, stmts)


    def visitDefault_label(self, ctx: TyCParser.Default_labelContext):
        stmts = self.visit(ctx.list_statement()) if ctx.list_statement() else []
        return DefaultStmt(stmts)

# =========================================================
# BLOCK
# =========================================================

    def visitBlock_statement(self, ctx:TyCParser.Block_statementContext):

        stmts = []
        if ctx.list_statement():
            stmts = self.visit(ctx.list_statement())

        return BlockStmt(stmts)
    
# =========================================================
# EXPRESSION STMT
# =========================================================

    def visitExpression_statement(self, ctx:TyCParser.Expression_statementContext):
        expr = None
        if ctx.expression():
            expr = self.visit(ctx.expression())
        return ExprStmt(expr)

# =========================================================
# RETURN
# =========================================================

    def visitReturn_statement(self, ctx:TyCParser.Return_statementContext):
        expr = None
        if ctx.expression():
            expr = self.visit(ctx.expression())

        return ReturnStmt(expr)

# =========================================================
# EXPRESSIONS
# =========================================================
    def visitExpression(self, ctx:TyCParser.ExpressionContext):
        if ctx.ASSIGN():
            return AssignExpr(
                self.visit(ctx.element()),
                self.visit(ctx.expression())
            )

        return self.visit(ctx.expression1())

    def visitExpression1(self, ctx: TyCParser.Expression1Context):
        if ctx.OR():
            return BinaryOp(
                self.visit(ctx.expression1()),
                "||",
                self.visit(ctx.expression2())
            )
        return self.visit(ctx.expression2())

    def visitExpression2(self, ctx: TyCParser.Expression2Context):
        if ctx.AND():
            return BinaryOp(
                self.visit(ctx.expression2()),
                "&&",
                self.visit(ctx.expression3())
            )
        return self.visit(ctx.expression3())

    def visitExpression3(self, ctx: TyCParser.Expression3Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(
                self.visit(ctx.expression3()),
                ctx.getChild(1).getText(),
                self.visit(ctx.expression4())
            )
        return self.visit(ctx.expression4())

    def visitExpression4(self, ctx: TyCParser.Expression4Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(
                self.visit(ctx.expression4()),
                ctx.getChild(1).getText(),
                self.visit(ctx.expression5())
            )
        return self.visit(ctx.expression5())

    def visitExpression5(self, ctx: TyCParser.Expression5Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(
                self.visit(ctx.expression5()),
                ctx.getChild(1).getText(),
                self.visit(ctx.expression6())
            )
        return self.visit(ctx.expression6())

    def visitExpression6(self, ctx: TyCParser.Expression6Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(
                self.visit(ctx.expression6()),
                ctx.getChild(1).getText(),
                self.visit(ctx.expression7())
            )
        return self.visit(ctx.expression7())
    
    def visitExpression7(self, ctx: TyCParser.Expression7Context):
        if ctx.getChildCount() == 2:
            return PrefixOp(
                ctx.getChild(0).getText(),
                self.visit(ctx.expression7())
            )
        return self.visit(ctx.expression8())
    
    def visitExpression8(self, ctx: TyCParser.Expression8Context):
        if ctx.getChildCount() == 2:
            return PrefixOp(ctx.getChild(0).getText(), 
                            self.visit(ctx.expression8()))
        return self.visit(ctx.expression9())
    
    def visitExpression9(self, ctx: TyCParser.Expression9Context):
        if ctx.getChildCount() == 2:
            return PostfixOp(ctx.getChild(1).getText(), 
                            self.visit(ctx.expression9()))
        return self.visit(ctx.expression10())
    
    def visitExpression10(self, ctx: TyCParser.Expression10Context):
        if ctx.getChildCount() == 3:
            obj = self.visit(ctx.expression10())
            member = ctx.ID().getText()
            return MemberAccess(obj, member)
        return self.visit(ctx.expression11())

    def visitExpression11(self, ctx: TyCParser.Expression11Context):
        if ctx.ID():
            obj = Identifier(ctx.ID(0).getText())
            for i in range(1, len(ctx.ID())):
                obj = MemberAccess(obj, ctx.ID(i).getText())
            return obj
        if ctx.literal():
            return self.visit(ctx.literal())
        if ctx.expression():
            return self.visit(ctx.expression())
        if ctx.function_call():
            return self.visit(ctx.function_call())
        
    def visitElement(self, ctx: TyCParser.ElementContext):
        if ctx.lhs():
            obj = self.visit(ctx.lhs())
            for id in ctx.ID():
                obj = MemberAccess(obj, id.getText())
        else:
            ids = ctx.ID()
            obj = Identifier(ids[0].getText())
            for i in range(1, len(ids)):
                obj = MemberAccess(obj, ids[i].getText())
        return obj
    
    def visitLhs(self, ctx: TyCParser.LhsContext):
        if ctx.function_call():
            return self.visit(ctx.function_call())
        elif ctx.expression():
            return self.visit(ctx.expression())
        elif ctx.literal():
            return self.visit(ctx.literal())
        return self.visit(ctx.list_expression())

# =========================================================
# FUNCTION CALL
# =========================================================

    def visitFunction_call(self, ctx:TyCParser.Function_callContext):

        name = ctx.ID().getText()

        args = []
        if ctx.list_expression():
            args = self.visit(ctx.list_expression())

        return FuncCall(name, args)

# =========================================================
# LIST EXPRESSION
# =========================================================

    def visitList_expression(self, ctx:TyCParser.List_expressionContext):

        if ctx.COMMA():
            return [self.visit(ctx.expression())] + self.visit(ctx.list_expression())

        return [self.visit(ctx.expression())]

# =========================================================
# LITERAL
# =========================================================

    def visitLiteral(self, ctx:TyCParser.LiteralContext):

        if ctx.INT_LIT():
            return IntLiteral(int(ctx.INT_LIT().getText()))

        if ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))

        if ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())

        if ctx.struct_literal():
            return self.visit(ctx.struct_literal())
        
    def visitStruct_literal(self, ctx:TyCParser.Struct_literalContext):
        elements = []
        if ctx.list_expression():
            elements = self.visit(ctx.list_expression())
        return StructLiteral(elements)