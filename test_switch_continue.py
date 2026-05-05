import re

with open("src/codegen/codegen.py", "r") as f:
    content = f.read()

# Let's find visit_switch_stmt
old_enter = "        frame.enter_loop()  # break jumps to brk_label\n        brk_label = frame.get_break_label()"
new_enter = """        frame.enter_loop()  # break jumps to brk_label
        if len(frame.con_label) >= 2:
            frame.con_label[-1] = frame.con_label[-2]
        brk_label = frame.get_break_label()"""

if old_enter in content:
    content = content.replace(old_enter, new_enter)
    with open("src/codegen/codegen.py", "w") as f:
        f.write(content)
    print("Patched!")
else:
    print("Could not find old_enter")
