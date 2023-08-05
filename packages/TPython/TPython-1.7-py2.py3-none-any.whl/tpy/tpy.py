# Import libs
import ast
import json
import os
import sys
import urllib.request
import urllib.error
from time import perf_counter
from traceback import format_exc

try:
    from jsonc_parser.errors import ParserError
    from jsonc_parser.parser import JsoncParser
except ModuleNotFoundError:
    sys.exit('Module not found: jsonc_parser')
try:
    from colorama import Fore, init
    init(autoreset=True)
except ModuleNotFoundError:
    sys.exit('Module not found: colorama')

# Vars
number: int = 1
err: bool = False
ind: bool = False
namespace: dict = {}
VERSION: str = '1.7'

# Config
READER_VERSION: str = '1.0'
# Consider reading https://github.com/Techlord210/TPython/blob/main/config.jsonc instead its just the defualt configuration dict.
CONFIG = {'version': '1.0', 'config': {'notify_updates': True, 'welcome_msg': True, 'exit_msg': True, 'crash_msg': True}, 'colors': {'update': {'text_color': Fore.LIGHTCYAN_EX, 'version_color': Fore.LIGHTGREEN_EX}, 'welcome': {'text_color': Fore.LIGHTCYAN_EX, 'padding_color': Fore.LIGHTCYAN_EX}, 'exit': {'success': {'text_color': Fore.LIGHTCYAN_EX, 'padding_color': Fore.LIGHTCYAN_EX}, 'crash': {'text_color': Fore.LIGHTYELLOW_EX, 'padding_color': Fore.LIGHTYELLOW_EX}}, 'promot': {'default': {'sq_brackets': Fore.LIGHTGREEN_EX, 'number': {'normal': Fore.LIGHTWHITE_EX, 'error': Fore.LIGHTRED_EX}, 'dash': Fore.LIGHTGREEN_EX,'arrow': Fore.LIGHTCYAN_EX, 'indent': {'number_replace': Fore.LIGHTYELLOW_EX, 'sq_brackets': Fore.LIGHTGREEN_EX, 'dash': Fore.LIGHTGREEN_EX, 'arrow': Fore.LIGHTYELLOW_EX}}, 'timeit': {'sq_brackets': Fore.LIGHTGREEN_EX, 'text_color': Fore.LIGHTWHITE_EX, 'dash': Fore.LIGHTGREEN_EX, 'arrow': Fore.LIGHTWHITE_EX, 'time_text': {'text_color': Fore.LIGHTGREEN_EX, 'time_color': Fore.LIGHTYELLOW_EX}, 'indent': {'number_replace': Fore.LIGHTWHITE_EX, 'sq_brackets': Fore.LIGHTGREEN_EX, 'dash': Fore.LIGHTGREEN_EX, 'arrow': Fore.LIGHTWHITE_EX}}}, 'error': {'internal': Fore.LIGHTRED_EX, 'user': Fore.LIGHTRED_EX}}}
CONFIG_PATH: str = os.path.abspath(os.path.expanduser('~/.TPython/config.jsonc'))
READ_FILE = False

if os.path.isfile(CONFIG_PATH):
    try:
        CONFIG = JsoncParser.parse_file(CONFIG_PATH)
        READ_FILE = True
    except ParserError:
        sys.exit(f'{Fore.LIGHTRED_EX}error loading {Fore.LIGHTYELLOW_EX}{CONFIG_PATH}')

if CONFIG['version'] == READER_VERSION:
    if READ_FILE:
        COLORS = {
            "cyan": Fore.LIGHTCYAN_EX,
            "green": Fore.LIGHTGREEN_EX,
            "red": Fore.LIGHTRED_EX,
            "yellow": Fore.LIGHTYELLOW_EX,
            "white": Fore.LIGHTWHITE_EX,
            "blue": Fore.LIGHTBLUE_EX,
            "black": Fore.LIGHTBLACK_EX,
            "magenta": Fore.LIGHTMAGENTA_EX
        }

        def color_to_code(config: dict) -> dict:
            for key, val in config.items():
                if type(val) == dict:
                    color_to_code(config[key])
                else:
                    config[key] = COLORS.get(val, Fore.WHITE)
            return config
        color_to_code(CONFIG['colors'])
else:
    sys.exit(f"{Fore.LIGHTRED_EX}config file version '{Fore.LIGHTYELLOW_EX}{CONFIG['version']}{Fore.LIGHTRED_EX}' don't match with reader '{Fore.LIGHTYELLOW_EX}{READER_VERSION}{Fore.LIGHTRED_EX}'")

INP_COLORS = CONFIG['colors']['promot']['default']
INP_COLORS_INDENT = CONFIG['colors']['promot']['default']['indent']
TNP_COLORS = CONFIG['colors']['promot']['timeit']
TNP_COLORS_INDENT = CONFIG['colors']['promot']['timeit']['indent']

# Update notifier
if CONFIG['config']['notify_updates']:
    try:
        response = urllib.request.urlopen('https://pypi.org/pypi/TPython/json')
        pypi_json = json.load(response)
        pypi_version = pypi_json['info']['version']
        if pypi_version != VERSION:
            print(f'{CONFIG["colors"]["update"]["text_color"]}Newer version of TPython is available: {CONFIG["colors"]["update"]["version_color"]}{pypi_version}')
    except urllib.error.URLError:
        pass

# Entry point
def main() -> None:
    global number, err, ind

    # exit function
    def ext(crash: bool=False) -> None:
        columns = os.get_terminal_size().columns
        crash_m = 'Crashed'
        success_m = 'Process Completed Successfully'
        if crash:
            if CONFIG['config']['crash_msg']:
                msg = crash_m
                for i in range((columns-len(crash_m))//2):
                    msg = f'{CONFIG["colors"]["exit"]["crash"]["padding_color"]}-{CONFIG["colors"]["exit"]["crash"]["text_color"]}{msg}{CONFIG["colors"]["exit"]["crash"]["padding_color"]}-'
                sys.exit(f'{msg}')
        else:
            if CONFIG['config']['exit_msg']:
                msg = success_m
                for i in range((columns-len(success_m))//2):
                    msg = f'{CONFIG["colors"]["exit"]["success"]["padding_color"]}-{CONFIG["colors"]["exit"]["success"]["text_color"]}{msg}{CONFIG["colors"]["exit"]["success"]["padding_color"]}-'
                print(f'{msg}')
            sys.exit()

    try:
        # execute function
        def execute(inp: str, timeit: bool=False) -> None:
            global err, number
            run = False
            before = 0
            if timeit:
                before = perf_counter()
            try:
                eval_return = eval(inp, namespace)
                if eval_return != None:
                    print(repr(eval_return))
                err = False
            except:
                run = True
            if run:
                try:
                    exec(inp, namespace)
                    err = False
                except Exception:
                    print(f'{CONFIG["colors"]["error"]["user"]}{format_exc()}')
                    err = True
            if timeit:
                print(f'{TNP_COLORS["time_text"]["text_color"]}Execution time: {TNP_COLORS["time_text"]["time_color"]}{perf_counter()-before}')
            number += 1

        # Welcome message
        if CONFIG['config']['welcome_msg']:
            columns = os.get_terminal_size().columns
            msg = 'Welcome to TPython'
            columns -= 18
            for i in range(columns//2):
                msg = f'{CONFIG["colors"]["welcome"]["padding_color"]}-{CONFIG["colors"]["welcome"]["text_color"]}{msg}{CONFIG["colors"]["welcome"]["padding_color"]}-'
            print(f'{msg}')

        # Input
        while True:
            try:
                indent = False
                indent_t = False
                inp = input(f'{INP_COLORS["sq_brackets"]}[{INP_COLORS["number"]["error" if err else "normal"]}{number}{INP_COLORS["sq_brackets"]}]{INP_COLORS["dash"]}-{INP_COLORS["arrow"]}> {Fore.LIGHTWHITE_EX}')
                if not (inp.isspace() or inp == ''):
                    inp = inp.strip()
                    # Exit command
                    if inp in ('exit', 'quit', 'close'):
                        ext()
                    elif inp in ('clear', 'cls') and not ('clear' in namespace or 'cls' in namespace):
                        os.system('cls' if os.name == 'nt' else 'clear')
                        err = False
                    # Version command
                    elif inp == 'version' and not 'version' in namespace:
                        print(f'{Fore.LIGHTCYAN_EX}{VERSION}')
                    # TimeIt command
                    elif inp == 'timeit' and not 'timeit' in namespace:
                        while True:
                            tnp = input(f'{TNP_COLORS["sq_brackets"]}[{TNP_COLORS["text_color"]}TimeIt{TNP_COLORS["sq_brackets"]}]{TNP_COLORS["dash"]}-{TNP_COLORS["arrow"]}> {Fore.LIGHTWHITE_EX}').strip()
                            try:
                                ast.parse(inp)
                            except SyntaxError:
                                indent_t = True
                            if indent_t:
                                # Statements that require indents eg: def, if
                                while True:
                                    indent = input(f'{TNP_COLORS_INDENT["sq_brackets"]}[{TNP_COLORS_INDENT["text_replace"]}------{TNP_COLORS_INDENT["sq_brackets"]}]{TNP_COLORS_INDENT["dash"]}-{TNP_COLORS_INDENT["arrow"]}> {Fore.LIGHTWHITE_EX}')
                                    if indent.strip() == '':
                                        if not ind:
                                            ind = True
                                        else:
                                            break
                                    else:
                                        tnp += f'\n\t{indent}'
                                execute(tnp, True)
                                ind = False
                                break
                            else:
                                execute(tnp, True)
                                break
                    else:
                        # Indents
                        try:
                            ast.parse(inp)
                        except SyntaxError:
                            indent = True
                        if indent:
                            while True:
                                indent = input(f'{INP_COLORS_INDENT["sq_brackets"]}[{INP_COLORS_INDENT["number_replace"]}{":"*len(str(number))}{INP_COLORS_INDENT["sq_brackets"]}]{INP_COLORS_INDENT["dash"]}-{INP_COLORS_INDENT["arrow"]}> {Fore.LIGHTWHITE_EX}')
                                if indent.strip() == '':
                                    if not ind:
                                        ind = True
                                    else:
                                        break
                                else:
                                    inp += f'\n\t{indent}'
                            execute(inp)
                            ind = False
                        else:
                            execute(inp)
            except KeyboardInterrupt:
                print(f'\n{Fore.LIGHTYELLOW_EX}KeyboardInterrupt')
                err = True
    except Exception:
        print(f'\n{Fore.LIGHTRED_EX}{format_exc()}')
        ext(True)