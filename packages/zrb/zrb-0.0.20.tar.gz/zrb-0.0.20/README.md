# Zrb (WIP)

Your faithful companion.

# How to install

```bash
pip install zrb
```

# How to use

To run a task, you can invoke the following command:

```bash
zrb <task> [arguments]
```

# Autoloaded tasks

Zrb will automatically load the following task definitions:

- Every task definition in `ZRB_INIT_SCRIPTS`.
    - You can use a colon separator (`:`) to define multiple scripts in `ZRB_INIT_SCRIPTS`. For example:
        ```bash
        ZRB_INIT_SCRIPTS=~/personal/zrb_init.py:~/work/zrb_init.py
        ```
- Every task definition in `zrb_init.py` in your current directory.
    - If Zrb cannot find any in your current directory, it will look at the parent directories until it finds one.
- Every built-in task definition given `ZRB_SHOULD_LOAD_BUILTIN` equals `1` or unset.

# How to define tasks

You can write your task definitions in Python. For example:

```python
from typing import Any
from zrb import (
    runner,
    Env, StrInput,
    Group, Task, CmdTask, HTTPChecker
)


# A regular Python function to concat words
def _concat(*args: str, **kwargs: Any) -> str:
    separator = kwargs.get('separator', ' ')
    return separator.join(args)

# Simple Python task, running a Python function to concat words.
# Usage example: zrb concat --separator=' '
concat = Task(
    name='concat',  # Task name
    inputs=[StrInput(name='separator', description='Separator', default=' ')],
    run=_concat  # Function to be executed
)
runner.register(concat) 

# Simple command task to show hello.
# Usage example: zrb hello --name='world'
hello = CmdTask(
    name='hello',
    inputs=[StrInput(name='name', description='Name', default='world')],
    cmd='echo Hello {{input.name}}'
)
runner.register(hello)

# Command group: zrb make
make = Group(name='make', description='Make things')

# Command task, part of `zrb make` group, depends on `hello`, making coffee
# Usage example: zrb make coffee
make_coffee = CmdTask(
    name='coffee',
    group=make,
    upstreams=[hello],
    cmd='echo Coffee for you ☕'
)
runner.register(make_coffee)

# Command task, part of `zrb make` group, depends on `hello`, making beer
# Usage example: zrb make beer
make_beer = CmdTask(
    name='beer',
    group=make,
    upstreams=[hello],
    cmd='echo Cheers 🍺'
)
runner.register(make_beer)

# Command group: zrb make gitignore
make_gitignore = Group(
    name='gitignore', description='Make gitignore', parent=make
)

# Command task, part of `zrb make gitignore` group, making .gitignore for Python project
# Usage example: zrb make gitignore Python
make_gitignore_python = CmdTask(
    name='python',
    group=make_gitignore,
    cmd=[
        'echo "node_modules/" >> .gitignore'
        'echo ".npm" >> .gitignore'
        'echo "npm-debug.log" >> .gitignore'
    ]
)
runner.register(make_gitignore_python)

# Command task, part of `zrb make gitignore` group, making .gitignore for Node.js project
# Usage example: zrb make gitignore node
make_gitignore_nodejs = CmdTask(
    name='node',
    group=make_gitignore,
    cmd=[
        'echo "__pycache__/" >> .gitignore'
        'echo "venv" >> .gitignore'
    ]
)
runner.register(make_gitignore_nodejs)

# Long running command task, serve static directory.
# Usage example: zrb start-server dir='.'
start_server = CmdTask(
    name='start-server',
    upstreams=[make_coffee, make_beer],
    inputs=[StrInput(name='dir', description='Directory', default='.')],
    envs=[Env(name='PORT', os_name='WEB_PORT', default='3000')],
    cmd='python -m http.server $PORT --directory {{input.dir}}',
    checkers=[HTTPChecker(port='{{env.PORT}}')]
)
runner.register(start_server)

# Command task, depends on long running task, simulating error
# Usage example: zrb test-error
test_error = CmdTask(
    name='test-error',
    upstreams=[start_server],
    cmd='sleep 3 && exit 1',
    retry=0
)
runner.register(test_error)

```

Once registered, your task will be accessible from the terminal.

For example, you can run a server by performing:

```bash
export WEB_PORT=8080
zrb start-server
```

The output will be similar to this:

```
Name [world]: Go Frendi
Dir [.]:
🤖 ➜  2023-02-04T11:08:11.921472 ⚙ 12264 ➤ 1 of 3 • 🍊    show hello • Hello Go Frendi
🤖 ➜  2023-02-04T11:08:12.039529 ⚙ 12266 ➤ 1 of 3 • 🐹   make coffee • Coffee for you ☕
🤖 ➜  2023-02-04T11:08:12.040651 ⚙ 12268 ➤ 1 of 3 • 🐶     make beer • Cheers 🍺
🤖 ➜  2023-02-04T11:08:12.160402 ⚙ 12270 ➤ 1 of 3 • 🍒  start-server • Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
🤖 ➜  2023-02-04T11:08:12.224660 ⚙ 12263 ➤ 1 of 1 • 🍇    http_check • HEAD http://localhost:8080/ 200 (OK)
🤖 🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
🤖 🍒 start-server completed in
🤖 🍒 0.311281681060791 seconds
🤖 🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉

🤖 ⚠  2023-02-04T11:08:12.228542 ⚙ 12270 ➤ 1 of 3 • 🍒  start-server • 127.0.0.1 - - [04/Feb/2023 11:08:12] "HEAD / HTTP/1.1" 200 -
```

# How to run tasks programmatically

To run a task programmatically, you need to create a `main loop`.

For example:

```python
from zrb import CmdTask


cmd_task = CmdTask(
    name='sample',
    cmd='echo hello'
)
main_loop = cmd_task.create_main_loop(env_prefix='')
result = main_loop() # This run the task
print(result.output) # Should be "hello"
```


# Configuration

The following configurations are available:

- `ZRB_LOGGING_LEVEL`: Logging verbosity.
    - Default: `WARNING`
    - Possible values:
        - `CRITICAL`
        - `ERROR`
        - `WARNING`
        - `WARN` (The same as `WARNING`)
        - `INFO`
        - `DEBUG`
        - `NOTSET`
- `ZRB_INIT_SCRIPTS`: List of task registration script that should be loaded by default.
    - Default: Empty
    - Possible values: List of script paths, separated by colons(`:`).
    - Example: `~/personal/zrb_init.py:~/work/zrb_init.py`
- `ZRB_ENV`: Environment prefix that will be used when loading Operating System's environment.
    - Default: Empty
    - Possible values: Any combination of alpha-numeric and underscore
    - Example: `DEV`
- `ZRB_SHOULD_LOAD_BUILTIN`: Whether load builtin tasks or not
    - Default: `1`
    - Possible values:
        - `1`
        - `0`
- `ZRB_SHELL`: Default shell for running cmdTask
    - Default: empty, indicating the system's default (usually `/usr/bin/bash` or `/usr/bin/sh`)
    - Possible value:
        - `/usr/bin/bash`
        - `/usr/bin/sh` 
        - `node`
        - `python`

# Quirks

- No one is sure how to pronounce Zrb. Let's keep it that way.
- If not set, `PYTHONUNBUFFERED` will be set to `1`.
- Once `zrb_init.py` is loaded, Zrb will automatically:
    - Set `ZRB_PROJECT_DIR` to `zrb_init.py`'s parent directory.
    - Adding `ZRB_PROJECT_DIR` to `PYTHONPATH`.
- Zrb passes several keyword arguments that will be accessible from the task's run method:
    - `_args`: Shell argument when the task is invoked.
    - `_task`: Reference to the current task.
- You can access the built-in command groups by importing `zrb.builtin_group`.

# For contributors

There is a toolkit you can use to test whether Zrb is working as intended.

To use the toolkit, you can invoke the following command:

```bash
source ./project.sh
```

Once you load the toolkit, you can start playing around.

```bash
# Run test and serve coverage.
zrb test

# Test zrb in playground
zrb prepare-playground
```


# For maintainers

To publish Zrb, you need a `Pypi` account:

- Log in or register to [https://pypi.org/](https://pypi.org/)
- Create an API token

You can also create a `TestPypi` account:

- Log in or register to [https://test.pypi.org/](https://test.pypi.org/)
- Create an API token

Once you have your API token, you need to create a `~/.pypirc` file:

```
[distutils]
index-servers =
   pypi
   testpypi

[pypi]
  repository = https://upload.pypi.org/legacy/
  username = __token__
  password = pypi-xxx-xxx
[testpypi]
  repository = https://test.pypi.org/legacy/
  username = __token__
  password = pypi-xxx-xxx
```

To publish Zrb, you can do the following:

```bash
source ./project.sh

# Publish Zrb to TestPypi
zrb publish-test

# Publish Zrb to Pypi
zrb publish
```
