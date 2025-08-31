from rich import print
import argparse


def cmd_hello(args):
    print(f"[bold cyan]Hello, {args.name}![/]")


def cmd_add(args):
    print(str(args.a + args.b))


def cmd_echo(args):
    print(args.text)


def cmd_info(args):
    print("[bold green]OK[/]")


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

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
