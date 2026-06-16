#!/usr/bin/env python3
import pathlib
import re
import sys

p = pathlib.Path("kernel/reboot.c")
if not p.exists():
    print("ERROR: kernel/reboot.c not found", file=sys.stderr)
    sys.exit(1)

s = p.read_text()
if "ksu_handle_sys_reboot" in s:
    print("[+] reboot hook already present, nothing to do")
    sys.exit(0)

extern = (
    "\n#ifdef CONFIG_KSU_MANUAL_HOOK\n"
    "extern int ksu_handle_sys_reboot(int magic1, int magic2, "
    "unsigned int cmd, void __user **arg);\n"
    "#endif\n\n"
)
syscall_re = re.compile(
    r"(SYSCALL_DEFINE4\s*\(\s*reboot[^)]*\)\s*\{)", re.MULTILINE
)
if not syscall_re.search(s):
    print("ERROR: SYSCALL_DEFINE4(reboot ...) not found", file=sys.stderr)
    sys.exit(2)

s = syscall_re.sub(extern + r"\1", s, count=1)

call = (
    "\n#ifdef CONFIG_KSU_MANUAL_HOOK\n"
    "\tksu_handle_sys_reboot(magic1, magic2, cmd, &arg);\n"
    "#endif\n"
)
inject_re = re.compile(
    r"(SYSCALL_DEFINE4\s*\(\s*reboot[^)]*\)\s*\{(?:[^{}]|\{[^{}]*\})*?int\s+ret\s*=\s*0\s*;\s*\n)",
    re.MULTILINE | re.DOTALL,
)
if not inject_re.search(s):
    print("ERROR: anchor 'int ret = 0;' inside reboot syscall not found", file=sys.stderr)
    sys.exit(3)

s = inject_re.sub(r"\1" + call, s, count=1)
p.write_text(s)
print("[+] reboot hook injected into kernel/reboot.c")
