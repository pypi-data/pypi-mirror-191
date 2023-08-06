# Harmony-GUI Tutorial

Harmony-GUI is a graphical, interactive debugger for the [Harmony](https://harmonylang.dev/) programming language. It allows users to better discover and diagnoze concurrency bugs in Harmony programs. When a bug exists, Harmony-GUI displays a trace (i.e, a possible interleaving of instructions) leading to that bug and allows users to step through each instruction and find out the cause of the bug. 

Note: Harmony-GUI is a newly-developed feature and this is its first time being used in CS 4410. Therefore, this version of Harmony-GUI is meant to be a __beta version__. You should feel free to use it, but in case it does not work properly, you can always switch back to the html output for debugging.  

Please report on Ed any error you find with Harmony-GUI. Also feel free to give any feedback! 


## Installation
Harmony-GUI currently supports Python __3.7-3.9__ only. Before installing Harmony-GUI, you must have one of those versions installed on your machine.  

Harmony-GUI depends on the latest version of Harmony, which Harmony-GUI will automatically install. 
    
If running `python3 --version` in your terminal gives version 3.7-3.9, you can install Harmony-GUI by running:

    pip3 install harmony-gui

Alternatively, if you have multiple versions of Python on your machine and one of them is between 3.7-3.9, you can also run

    pip3.x install harmony-gui
where 7<=x<=9. 

After Harmony-GUI has been successfully installed, run the following command to start it:

    harmony-gui

A window like this should pop up:
![](readmeImg/p1.png)

If you would like to open a file directly, you can also do:

    harmony-gui <file_to_open>
to open a `hny` or `hco` file. 

## Run the First Program
To run a Harmony program, click the `Browse` button, and choose any Harmony source code file that ends with `.hny` to open. 

I choose a dining philosophers [program](https://harmony.cs.cornell.edu/code/Diners.hny) to open and it looks something like this:

![](readmeImg/p2.png)

Currently the code is not compiled yet, so you only see the source code in the middle without other information. 

Now, click the `run` button and Harmony will compile the program and run model checker on it. As we all know, this dining philosophers program can run into a [deadlock](https://harmonylang.dev/docs/textbook/deadlock/). Fortunately, Harmony detects this problem and our Harmony-GUI displays the following information:

![](readmeImg/p3.png)

Now, you can play around with it a little bit and see how it works. In the next section, we are going to introduce in more detail how to use it as well as how to interpret the information shown in different parts of the window. 

Notice that if your code has no issues, then Harmony-GUI won't display any information shown as above but will only pop up a message box telling you that Harmony finds no issue in the program. 

## Use
Now let's look at each part of the debugger in detail:
![](readmeImg/p4.png)
### 1. Source Code
In the middle of the window shows the source code of the Harmony program. The current executing statement is highlighted in yellow. The specific part of the statement that corresponds to the current machine instruction is highlighted in green. 

### 2. Byte Code
In the top left of the window shows the byte code (machine code) of the program. Each line corresponds to a machine instruction preceded by the PC (program counter) of that instruction. The instructions are sorted by execution order, so that the first line is the first instruction being executed and the last line is the last instruction being executed. The current machine instruction is highlighted in green. A machine instruction in Harmony is called a "___microstep___". 

### 3. Scroll Bar
The scroll bar simulates the execution of the entire program. By moving the scroll bar back and forth, you can go to different time steps and track the program state at each time step. The granularity of the scroll bar is at the level of microsteps. 

### 4. Thread Status
The bottom of the window shows the status of the threads in the program. \
The left half of this section shows how all the threads interleave. At any time, only one thread is running (colored), and all other threads are waiting (gray). \
The right half of the section shows the state of each thread at the current time step. This includes: 1) whether the thread is runnable, blocked, terminated, etc; 2) the function calls of each thread; 3) what each thread is about to do. 

### 5. Explanation of Current Instruction
On top of the scroll bar shows information about the current instruction. It shows: 1) which thread is currently running; 2) explanation of the current microstep; 3) location of the current source code file. 

### 6. Control Buttons
In the right bottom of the window there are 5 control buttons: `Next`, `Prev`, `Up`, `Down`, and the `Single Step` checkbox. The shortcut to `Next`, `Prev`, `Up`, `Down` are `→`, `←`, `↑`, `↓` keys respectively. (If the shortcut does not work, try clicking the source code section in the middle and then it should work.) 
Now, let's look at each of the 5 control buttons: 
#### 1) `Single Step`
This is a checkbox that you can manually check or uncheck to control the granularity of `Next` and `Prev`. If you want to go over the program in general, which is usually the case, uncheck `Single Step`. If you would like to go over each single microstep in detail, check `Single Step`.  \
(a) With `Single Step` unchecked (which is the default setting), `Next` and `Prev`'s granularity are at the level of statements (which roughly corresponds to lines of code in the source program). \
(b) With `Single Step` checked, `Next` and `Prev`'s granularity are at the level of microsteps (individual machine instructions).
#### 2) `Next`
(a) When `Single Step` is unchecked, `Next` usually goes to the next statement (or next line) in the source code, and does not step into any function call.  
(b) When `Single Step` is checked, `Next` goes to the next microstep (machine instruction). This also means it will step into any function call. 
#### 3) `Prev`
Similar to `Next`:\
(a) When `Single Step` is unchecked, `Prev` usually goes to the previous statement (or previous line) in the source code, and does not step into any function call.  
(b) When `Single Step` is checked, `Prev` goes to the previous microstep (machine instruction). This also means it will step into any function call. 
#### 4) `Down`
Fast forward and step out of the current function. For example, in the code shown below, `f()` has statement `a1`, calls `g()`, and then has statement `a2`. `g()` has statement `b1`, `b2`, `b3`. Suppose the current statement being executed is `b2` in `g()`, then clicking `Down` will fast forward and step out of `g()` and go to `a2` in `f()`.  

    f () {
        statement a1 <- Up will go here
        g ()
        statement a2 <- Down will go here
    }
    g () {
        statement b1
        statement b2 <- /current statement/
        statement b3
    }
#### 5) `Up`
Fast backward and step out of the current function. For example, in the code shown above, suppose the current statement being executed is `b2` in `g()`, then clicking `Up` will fast backward and step out of `g()` and go back to `a1` in `f()`.  

### 7. Shared Variables
In the top right of the window shows the state of shared variables just _before_ the current highlighted microstep is executed. Those variables are shared by all threads. 

### 8. Local Variables
Under the Shared Variables section is the Local Variables section, which shows the state of local variables just _before_ the current highlighted microstep is executed. Those variables are local to the current running thread. 

### 9. Stack Top
Under the Local Variables section is the Stack Top section, which shows the stack top of the current thread. It does not show the entire stack of the current thread but only shows the top of the stack that corresponds to the latest function call. 

### 10. Print Log
This is the "console" that records the output of the program. Everything printed in the program using `print` statements will occur in the Print Log.

### 11. Issue Message
The top left of the screen shows the issue of the program. The issue is detected by the Harmony model checker. In this example of dining philosophers, the issue shown is `Non-terminating state`, which suggests there is a deadlock. 

### 12. Machine Status
In the top right of the window there are three checkboxes that show the current machine status. Those checkboxes are read-only and you cannot manually check or uncheck them. The three checkboxes show whether the current thread is in atomic mode, in read-only mode, or in interrupt-disabled mode. 

### 13. Microsteps
This part shows the current progress of execution. It shows how many microsteps there are in total, as well as how many microsteps have been executed. In the picture above, it shows `Microsteps: 152/309`. This means that there are 309 microsteps in this trace, and 152 microsteps have been executed at the current time step. 

### 14. File
At the top of the window, there is a bar showing the current opening file, a `Browse` button for opening files, and a `Run` button for running source code files. \
To compile and model check a Harmony source code (`.hny`) file, you will need to first open the `.hny` file and then click `Run`. \
Harmony model checker compiles the source code in a `.hny` file and saves the output in a `.hco` file under the same name. Therefore, you can also open a Harmony compiled output (`.hco`) file directly. This saves you the trouble of compiling and model checking the same source code multiple times. \
If you have changed the source code file, however, you do need to open the source code and run that file again. 

### 15. Configuration (Menu bar)
In the menu bar at the top, there is a `Configuration` tab that contains three options: `Constants`, `Modules`, and `Compare Behavior`. \
`Constants`: allows you to change the constants. \
`Modules`: allows you to change the modules imported in the program. \
`Compare Behavior`: allows you to compare the behavior of the program against a Harmony finite automata (`.hfa`) file.

## Enjoy Concurrency
Now, we have finished explaining all parts of Harmony-GUI and you should feel free to use it to debug your concurrent programs. Good luck and have fun! 


