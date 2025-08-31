from rich import print
import argparse, os, json, sys, datetime
from pathlib import Path


# === storage helpers ===
def _home():
    p = Path(os.environ.get("DEMO2_HOME", Path.home() / ".demo2"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def _todo_path():
    return _home() / "todo.json"


def _log_path():
    return _home() / "cli.log"


def _load_todos():
    fp = _todo_path()
    if not fp.exists():
        return []
    try:
        return json.loads(fp.read_text("utf-8"))
    except Exception:
        return []


def _save_todos(items):
    _todo_path().write_text(json.dumps(items, ensure_ascii=False, indent=2), "utf-8")


def _append_log(args):
    if args.cmd == "log":
        return
    ts = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    entry = f"{ts} :: {' '.join(sys.argv[1:])}\n"
    with _log_path().open("a", encoding="utf-8") as f:
        f.write(entry)


# === commands ===
def cmd_hello(args):
    print(f"[bold cyan]Hello, {args.name}![/]")


def cmd_add(args):
    print(str(args.a + args.b))


def cmd_echo(args):
    print(args.text)


def cmd_info(args):
    print("[bold green]OK[/]")


def cmd_calc(args):
    try:
        result = eval(args.expr, {}, {})
        print(f"{result}")
    except Exception as e:
        print(f"[red]Error:[/] {e}")


def cmd_time(args):
    now = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    print(now)


def cmd_todo(args):
    items = _load_todos()
    if args.todo_cmd == "add":
        items.append({"text": args.text, "done": False})
        _save_todos(items)
        print(f"[bold green]+[/] {args.text}")
    elif args.todo_cmd == "list":
        if not items:
            print("(empty)")
        else:
            for i, it in enumerate(items):
                mark = "x" if it["done"] else " "
                print(f"{i}. [{mark}] {it['text']}")
    elif args.todo_cmd == "done":
        idx = args.index
        if 0 <= idx < len(items):
            items[idx]["done"] = True
            _save_todos(items)
            print(f"[bold yellow]✓[/] {items[idx]['text']}")
        else:
            print("[red]index out of range[/]")
    elif args.todo_cmd == "clear":
        _save_todos([])
        print("[bold magenta]cleared[/]")


def cmd_log(args):
    fp = _log_path()
    if not fp.exists():
        print("(no log)")
        return
    lines = fp.read_text("utf-8").splitlines()[-args.tail :]
    for ln in lines:
        print(ln)


def main():
    p = argparse.ArgumentParser(prog="demo2", description="Simple local CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("hello")
    sp.add_argument("--name", default="world")
    sp.set_defaults(func=cmd_hello)
    sp = sub.add_parser("add")
    sp.add_argument("a", type=int)
    sp.add_argument("b", type=int)
    sp.set_defaults(func=cmd_add)
    sp = sub.add_parser("echo")
    sp.add_argument("text")
    sp.set_defaults(func=cmd_echo)
    sp = sub.add_parser("info")
    sp.set_defaults(func=cmd_info)
    sp = sub.add_parser("calc")
    sp.add_argument("expr")
    sp.set_defaults(func=cmd_calc)
    sp = sub.add_parser("time")
    sp.set_defaults(func=cmd_time)

    # todo
    sp = sub.add_parser("todo")
    sub2 = sp.add_subparsers(dest="todo_cmd", required=True)
    a = sub2.add_parser("add")
    a.add_argument("text")
    a.set_defaults(func=cmd_todo)
    a = sub2.add_parser("list")
    a.set_defaults(func=cmd_todo)
    a = sub2.add_parser("done")
    a.add_argument("index", type=int)
    a.set_defaults(func=cmd_todo)
    a = sub2.add_parser("clear")
    a.set_defaults(func=cmd_todo)

    # log
    sp = sub.add_parser("log")
    sp.add_argument("--tail", type=int, default=10)
    sp.set_defaults(func=cmd_log)

    args = p.parse_args()
    _append_log(args)
    args.func(args)


if __name__ == "__main__":
    main()
