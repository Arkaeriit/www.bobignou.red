---
title: Making a Vim plugin with Python
date: 2022-04-25 18:29:10
tags:
---
## Why using Python in a Vim plugin

Vimscript is a well-designed language that is really tailored to extend Vim. Unfortunately, this language is not very powerful and quite clunky for general-purpose computing.

Fortunately, it is possible to use other languages in your Vim plugin. For example, Python.

Python is very easy to prototype in, and fast to write and its extensive standard library is a great help when writing Vim plugins. Thus, it is a good choice for our plugins.

## Making a Vim plugin

Before making a plugin using Python, let's remind ourselves how to do a simple plugin. Our plugin will be contained in a directory named with the name of our plugin. For example `test_plugin`.

This directory will be in the plugin directory of our plugin manager. For example, with [Pathogen](https://github.com/tpope/vim-pathogen), `test_plugin` will be in `<vim dir>/bundle`. For the rest of this post, the plugin manager's directory will be written `<plugin manager dir>`.

In our plugin's directory, we will create a directory named `plugin` where the Vimscript code is stored. Scripts stored there will be run when the plugin manager loads plugins. There can be other directories such as `autoload` but their use is outside of the scope of this post.

Let's write a small plugin that prints the content of the variable `g:myVar` when pressing `<F1>`. The variable will be initialized to "abcd".

`<plugin manager dir>/test_plugin/plugin/test_plugin.vim`:

```
" Variable initialization
let g:myVar = "abcd"

function PrintMyVar()
    " Expand to `normal a<myVar>` which is the command to write the content of myVar in the buffer
    let l:exec = "normal a" . g:myVar
    " Run the command we defined
    execute l:exec 
endfunction

" Binds <F1> to the function we defined
nnoremap <F1> :call PrintMyVar()<Cr>

```

Now, when running Vim, pressing `<F1>` will write "abcd" as this is the behavior of the plugin.

## Calling a python script in the vim plugin

Let's now make a very simple script that prints "Hello, world!" when starting Vim. But this will have a quirk, the printing will be made in a Python script. The Python script will be in the `plugin` directory of our plugin.

`<plugin manager dir>/test_plugin/plugin/hello_world.py`:

```
print("Hello, world!")

```

We will write a Vim script that executes the Python script when starting Vim. The first challenge is to find the path of the python script. This can be done with the Vimscript function `expand('<sfile>:p:h')` which finds the directory of the script executing this function. Then, we will use `py3file` to run the script.

`<plugin manager dir>/test_plugin/plugin/hello_world.vim`:

```
" Finding the path of the current script
let s:script_dir = expand('<sfile>:p:h')
" Generating the py3file command that runs the script
let s:python_exec_cmd = 'py3file ' . s:script_dir . "/hello_world.py"
" Executing it
execute s:python_exec_cmd


```

We are now greeted with a slightly annoying "Hello, world!" when starting Vim. But the annoyance is sweetened by the knowledge that this is executed with Python code.

## Vim module

In our Python script, to interact with Vim, we must use the module `vim`. This module can do a lot of things that we can read with Vim's included documentation with `:help python-vim`.

## Communication between Vimscript and Python

To make a more complex plugin, we will need to exchange data between Vimscript code and Python code. To do so, we need to use Vim's global variable that can be accessed from Python with `vim.vars`.

Let's improve the script `test_plugin.vim` so that it writes twice the content of `g:myVar`. We will start by making a Python script that duplicates the content of `g:myVar` and write it into `g:myBigVar`.

`<plugin manager dir>/test_plugin/plugin/hello_world.py`:

```
import vim

def duplicate_string(s):
    "Return the double of the input string."
    return f"{s}{s}"

vim.vars["myBigVar"] = duplicate_string(vim.vars["myVar"].decode()) # Note that the content of vim.vars is byte arrays so we need to use `decode`

```

Then, we will rewrite `test_plugin.vim` to use the new Python script.

`<plugin manager dir>/test_plugin/plugin/test_plugin.vim`:

```
" Variables initialization
let g:myVar = "abcd"
let s:script_dir = expand('<sfile>:p:h')


function PrintMyVar()
    " Generating the py3file command that runs the script
    let s:python_exec_cmd = 'py3file ' . s:script_dir . "/script.py"
    " Executing it
    execute s:python_exec_cmd
    " Expand to `normal a<myBigVar>` which is the command to write the content of myBigVar in the buffer
    let l:exec = "normal a" . g:myBigVar
    " Run the command we defined
    execute l:exec 
endfunction

" Binds <F1> to the function we defined
nnoremap <F1> :call PrintMyVar()<Cr>

```

## Using multiple Python files

For an even more complex script, we will want to have multiple Python files that we use with `import`. To do so, we need to add the path of our scripts to Python's library path list. This can be done by putting the path of the scripts in one of Vim's global variables.

`<plugin manager dir>/test_plugin/plugin/test_plugin.vim`:

```
" Variables initialization
let g:myVar = "abcd"
let g:test_plugin_dir = expand('<sfile>:p:h')


function PrintMyVar()
    " Generating the py3file command that runs the script
    let s:python_exec_cmd = 'py3file ' . g:test_plugin_dir . "/script.py"
    " Executing it
    execute s:python_exec_cmd
    " Expand to `normal a<myBigVar>` which is the command to write the content of myBigVar in the buffer
    let l:exec = "normal a" . g:myBigVar
    " Run the command we defined
    execute l:exec 
endfunction

" Binds <F1> to the function we defined
nnoremap <F1> :call PrintMyVar()<Cr>

```

We will then put the `duplicate_string` function in a separate file.

`<plugin manager dir>/test_plugin/plugin/my_lib.py`:

```
def duplicate_string(s):
    "Return the double of the input string."
    return f"{s}{s}"

```

Lastly, we will change `script.py` so that it uses the lib.

`<plugin manager dir>/test_plugin/plugin/script.py`:

```
import sys
import vim

sys.path.append(vim.vars["test_plugin_dir"].decode())
import my_lib

vim.vars["myBigVar"] = my_lib.duplicate_string(vim.vars["myVar"].decode()) # Note that the content of vim.vars is byte arrays so we need to use `decode`

```

## Conclusion

We are now ready to write complex Vim plugins with a mix of Vimscript and Python.

