#!/usr/bin/env python3
"""
Linting script for Checkers game source code.
Validates layer structure, import rules, and file size limits.
"""

import ast
import sys
from pathlib import Path


# Layer hierarchy (imports can only go forward in this list)
LAYERS = ["utils", "config", "types", "providers", "repo", "service", "runtime", "ui"]
MAX_LINES = 300

# Valid import patterns per layer
VALID_IMPORTS = {
    "types": {"types"},
    "config": {"types", "config"},
    "repo": {"types", "config", "repo"},
    "service": {"types", "config", "repo", "providers", "service"},
    "runtime": {"types", "config", "repo", "service", "providers", "runtime"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui"},
    "providers": {"types", "config", "utils", "providers"},
    "utils": {"utils"},
}


def get_layer_from_path(filepath: Path) -> str | None:
    """Get the layer name from a file path."""
    src_dir = Path("src")
    try:
        rel_path = filepath.relative_to(src_dir)
        parts = rel_path.parts
        if len(parts) >= 1:
            layer = parts[0].replace(".py", "")
            if layer in LAYERS:
                return layer
    except ValueError:
        pass
    return None


def get_imports(filepath: Path) -> list[tuple[str, int]]:
    """Get all imports from a Python file."""
    imports = []
    try:
        with open(filepath, "r") as f:
            source = f.read()
        tree = ast.parse(source)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((alias.name, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # Handle relative imports
                    if node.level > 0:
                        # Relative import like from . import x or from .. import y
                        imports.append(("<relative>", node.lineno))
                    else:
                        imports.append((node.module, node.lineno))
    except SyntaxError:
        pass
    
    return imports


def get_import_base_module(full_module_name: str) -> str:
    """Get the base module name from a full import path like 'src.types'."""
    # Handle both 'src.types' and 'types' style imports
    parts = full_module_name.split(".")
    return parts[0] if parts[0] != "src" else parts[1]


def is_standard_library(module_name: str) -> bool:
    """Check if a module is part of Python's standard library."""
    standard_libs = {
        "abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio",
        "asyncore", "atexit", "audioop", "base64", "bdb", "binascii",
        "binhex", "bisect", "builtins", "bz2", "calendar", "cgi", "cgitb",
        "chunk", "cmath", "cmd", "code", "codecs", "codeop", "collections",
        "colorsys", "compileall", "concurrent", "configparser", "contextlib",
        "contextvars", "copy", "copyreg", "cProfile", "crypt", "csv",
        "ctypes", "curses", "dataclasses", "datetime", "dbm", "decimal",
        "difflib", "dis", "distutils", "doctest", "email", "encodings",
        "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput",
        "fnmatch", "fractions", "ftplib", "functools", "gc", "getopt",
        "getpass", "gettext", "glob", "graphlib", "grp", "gzip", "hashlib",
        "heapq", "hmac", "html", "http", "imaplib", "imghdr", "imp",
        "importlib", "inspect", "io", "ipaddress", "itertools", "json",
        "keyword", "lib2to3", "linecache", "locale", "logging", "lzma",
        "mailbox", "mailcap", "marshal", "math", "mimetypes", "mmap",
        "modulefinder", "multiprocessing", "netrc", "nis", "nntplib",
        "numbers", "operator", "optparse", "os", "ossaudiodev", "pathlib",
        "pdb", "pickle", "pickletools", "pipes", "pkgutil", "platform",
        "plistlib", "poplib", "posix", "posixpath", "pprint", "profile",
        "pstats", "pty", "pwd", "py_compile", "pyclbr", "pydoc", "queue",
        "quopri", "random", "re", "readline", "reprlib", "resource",
        "rlcompleter", "runpy", "sched", "secrets", "select", "selectors",
        "shelve", "shlex", "shutil", "signal", "site", "smtpd", "smtplib",
        "sndhdr", "socket", "socketserver", "spwd", "sqlite3", "ssl",
        "stat", "statistics", "string", "stringprep", "struct", "subprocess",
        "sunau", "symtable", "sys", "sysconfig", "syslog", "tabnanny",
        "tarfile", "telnetlib", "tempfile", "termios", "test", "textwrap",
        "threading", "time", "timeit", "tkinter", "token", "tokenize",
        "trace", "traceback", "tracemalloc", "tty", "turtle", "turtledemo",
        "types", "typing", "unicodedata", "unittest", "urllib", "uu",
        "uuid", "venv", "warnings", "wave", "weakref", "webbrowser",
        "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc",
        "zipapp", "zipfile", "zipimport", "zlib", "_thread"
    }
    return module_name.split(".")[0] in standard_libs


def check_file(filepath: Path) -> list[str]:
    """Check a single file for linting violations."""
    violations = []
    
    # Check if file is under src/
    src_dir = Path("src")
    try:
        filepath.relative_to(src_dir)
    except ValueError:
        return violations  # Ignore non-src files
    
    # Check layer and file extension
    layer = get_layer_from_path(filepath)
    if layer is None:
        return violations  # Non-layer file
    
    if not filepath.name.endswith(".py"):
        return violations
    
    # Check file size
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
        if len(lines) > MAX_LINES:
            violations.append(
                f"{filepath}:{len(lines)}: File exceeds {MAX_LINES} lines ({len(lines)} lines)"
            )
    except IOError:
        pass
    
    # Check imports
    imports = get_imports(filepath)
    for import_name, line_num in imports:
        # Get the base module name (handle 'src.types' style imports)
        base_module = get_import_base_module(import_name)
        
        # Skip standard library imports (they're always allowed)
        if is_standard_library(base_module):
            continue
        
        # Handle relative imports (always allowed within project)
        if import_name == "<relative>":
            continue
        
        # Check if import is from a valid layer
        if base_module not in VALID_IMPORTS[layer]:
            violations.append(
                f"{filepath}:{line_num}: Invalid import '{import_name}'. "
                f"Layer '{layer}' may only import from: {', '.join(sorted(VALID_IMPORTS[layer]))}"
            )
    
    return violations


def main() -> int:
    """Run linting checks and return error count."""
    violations = []
    
    # Check all Python files under src/
    src_dir = Path("src")
    if not src_dir.exists():
        print("Error: src/ directory not found")
        return 1
    
    for filepath in src_dir.rglob("*.py"):
        file_violations = check_file(filepath)
        violations.extend(file_violations)
    
    if violations:
        print("Linting violations found:\n")
        for v in violations:
            print(f"  {v}")
        return 1
    
    print("All checks passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
