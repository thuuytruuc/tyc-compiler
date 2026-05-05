import re

with open("src/codegen/codegen.py", "r") as f:
    content = f.read()

old_switch = """    def visit_switch_stmt(self, node: SwitchStmt, o: SubBody = None):
        \"\"\"Generate code for switch with fall-through (C-style).\"\"\"
        frame = o.frame
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
                o = self.visit(stmt, o)

        # Emit default body
        if node.default_case:
            self.emit.print_out(self.emit.emit_label(default_label, frame))
            for stmt in node.default_case.statements:
                o = self.visit(stmt, o)

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_loop()
        return o"""

new_switch = """    def visit_switch_stmt(self, node: SwitchStmt, o: SubBody = None):
        \"\"\"Generate code for switch with fall-through (C-style).\"\"\"
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
        return o"""

if old_switch in content:
    content = content.replace(old_switch, new_switch)
    with open("src/codegen/codegen.py", "w") as f:
        f.write(content)
    print("Patched scope in switch!")
else:
    print("Could not find old_switch")
