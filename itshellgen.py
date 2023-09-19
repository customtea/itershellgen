import argparse
import sys
from itertools import product
import datetime
import argparse
from argparse import (OPTIONAL, SUPPRESS, ZERO_OR_MORE, ArgumentDefaultsHelpFormatter, ArgumentParser, RawDescriptionHelpFormatter, RawTextHelpFormatter)

__author__ = 'Github @customtea'
__version__ = '1.0.1'
__program__ = 'Iteration Command Script Generator'

def version():
    return f"{__program__} ver:{__version__} Created By {__author__}"
    

def opt_iter_parse(s: str):
    if "," in s:
        return s.split(",")
    elif "..=" in s:
        sp = s.split("..=")
        sp = list(map(int, sp))
        if sp == 1:
            end = sp[0]
        else:
            beg = sp[0]
            end = sp[1]
        return list(range(beg, end + 1))
        
    elif ".." in s:
        sp = s.split("..")
        sp = list(map(int, sp))
        if sp == 1:
            end = sp[0]
        else:
            beg = sp[0]
            end = sp[1]
        return list(range(beg, end))
        # print(s.split(".."))
    else:
        return list(range(0, int(s)))


def expand_placeholder(s, count_state, keyname):
    ns = s
    for key in keyname:
        ns = ns.replace(f"#{key}#", str(count_state[keyname.get(key)]))
    return ns


def begin_itel(count_state, keyname, beg_list, it_list):
    s = ""
    for beg in beg_list:
        sel = keyname[beg] + 1
        if sel < len(count_state):
            if  count_state[sel] == it_list[sel][0]:
                # print(beg_list[beg])
                s += expand_placeholder(beg_list[beg], count_state, keyname) + "\n"
    return s


def end_itel(count_state, keyname, end_list, it_list):
    s = ""
    for end in end_list:
        sel = keyname[end] + 1
        if sel < len(count_state):
            if  count_state[sel] == it_list[sel][-1]:
                # print(end_list[end])
                s += expand_placeholder(end_list[end], count_state, keyname) + "\n"
    return s


class MyHelpFormatter(RawTextHelpFormatter, RawDescriptionHelpFormatter, ArgumentDefaultsHelpFormatter):
    def _format_action(self, action: argparse.Action) -> str:
        return super()._format_action(action) + "\n"

    def _get_help_string(self, action):
        help = action.help
        if action.required:
            help += " (required)"

        if "%(default)" not in action.help:
            if action.default is not SUPPRESS:
                defaulting_nargs = [OPTIONAL, ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    if action.default is not None and action.default is not False and not action.const:
                        help += " (default: %(default)s)"
        return help

def getOption():
    parser = argparse.ArgumentParser(
        description="""
Example:
    prog.py "bc #M# + #N#" --iter M 2..=5 --iter N 7,8,9
""",
        formatter_class=MyHelpFormatter
    )
    parser.add_argument('cmd',
                        default=False,
                        help='Comamnd (PlaceHolder #key#)')
    parser.add_argument('--iter',
                        nargs=2,
                        action='append',
                        default=None,
                        metavar=("Key","Loop"),
                        help='Set Iteration\n\
Loop Example\n\
    N : range(0, N)\n\
    M..N : range(M, N)\n\
    M..=N : range(M, N+1)\n\
    A,B,C : [A,B,C] ')
    parser.add_argument('--before',
                        nargs=2,
                        action='append',
                        default=None,
                        metavar=("Key","'Command'"),
                        help='Exec Before Iteration Command')
    parser.add_argument('--after',
                        nargs=2,
                        action='append',
                        default=None,
                        metavar=("Key","'Command'"),
                        help='Exec After Iteration Command')
    parser.add_argument('--begin',
                        nargs='?',
                        action='append',
                        default=None,
                        metavar="'Command'",
                        help='Exec Start of Shell Script Command')
    parser.add_argument('--end',
                        nargs='?',
                        action='append',
                        default=None,
                        metavar="'Command'",
                        help='Exec End of Shell Script Command')
    parser.add_argument('--shebang',
                        nargs='?',
                        default=shebang,
                        metavar="'Shebang Command'",
                        help='Shebang')
    parser.add_argument('--parallel',
                        nargs='?',
                        default=None,
                        metavar="int",
                        help='Parallel Number [int]')

    parser.add_argument('--out',
                        nargs='?',
                        default=False,
                        metavar="FileName",
                        help='Output FileName (Default: StdOut)\n\
Empty Name is named "YYYYMMDD-HHMMSS" ')
    # log_level_group = parser.add_mutually_exclusive_group()
    # log_level_group.add_argument('-v','--verbose', action='count', default=False, help='set verbose mode')
    # log_level_group.add_argument('-q','--quiet', action='store_true', default=False, help='set quiet mode')
    parser.add_argument('--version', action='version', version=f"{version()}")
    return parser.parse_args()



it_list = []
it_keys = {}
iter_before = {}
iter_after = {}
script_begin = []
script_end = []
parallel_max = 0
shebang = "#!/bin/bash"

if __name__ == '__main__':
    original_command = f"{sys.argv[0]} "
    args = getOption()
    # print(args)

    cmd = args.cmd
    original_command += f"'{args.cmd}'"
    if args.iter:
        for item in args.iter:
            original_command += f" --iter {item[0]} {item[1]}"
            # print(opt_iter_parse(item[1]))
            it_keys[item[0]] = len(it_list)
            it_list.append(opt_iter_parse(item[1]))
            # print(item)
    if args.before:
        for item in args.before:
            original_command += f" --before {item[0]} '{item[1]}'"
            if item[0] not in iter_before:
                iter_before[item[0]] = item[1] + "\n"
            else:
                iter_before[item[0]] += item[1] + "\n"
            # print(item)
    if args.after:
        for item in args.after:
            original_command += f" --after {item[0]} '{item[1]}'"
            if item[0] not in iter_after:
                iter_after[item[0]] = item[1] + "\n"
            else:
                iter_after[item[0]] += item[1] + "\n"
            # print(item)
    
    if args.begin:
        script_begin = args.begin
        for item in args.begin:
            original_command += f" --begin {item[0]} '{item[1]}'"
    
    if args.end:
        script_end = args.end
        for item in args.end:
            original_command += f" --end {item[0]} '{item[1]}'"
    
    if args.parallel:
        parallel_max = int(args.parallel)
        original_command += f" --parallel {args.parallel}"
    
    if args.shebang:
        shebang = args.shebang
        original_command += f" --shebang '{args.shebang}'"

    if args.out or args.out == None:
        is_fileout = True
        if args.out == None:
            filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".sh"
        else:
            filename = args.out
            original_command += f" --out {filename}"
        outfile = open(filename, "w")
    else:
        is_fileout = False
    

    ## Start process
    script_comment = f"# This Script is Generated by {__program__}\n# {original_command}\n# =======\n\n"
    if is_fileout:
        outfile.write(shebang + "\n")
        outfile.write(script_comment)
    else:
        print(shebang)
        print(script_comment, end="")

    for beg in script_begin:
        if is_fileout:
            outfile.write(beg + "\n")
        else:
            print(beg)
    p_count = 0
    for c_state in product(*it_list):
        # print(item)
        s = ""
        s += begin_itel(c_state, it_keys, iter_before, it_list)
        s += expand_placeholder(cmd,c_state, it_keys)
        if p_count >= parallel_max -1:
            p_count = 0
            s += "\n"
        else:
            p_count += 1
            s += " &\n"
        s += end_itel(c_state, it_keys, iter_after, it_list)
        if is_fileout:
            outfile.write(s)
        else:
            print(s, end="")
            
    if args.parallel:
        if is_fileout:
            outfile.write("\nwait\n")
        else:
            print("wait")
    for end in script_end:
        if is_fileout:
            outfile.write(end + "\n")
        else:
            print(end)
    if is_fileout:
        outfile.close()
