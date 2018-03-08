# TapeLangauge
A basic programming language on a tape

This project was inspired by an assignment for the Spring 2018 Programming Languages assignment at Williams College using a trivial language called Breph. The language has been modified here. The language operates very simply with a data array, like a Turing Machine tape, and a simple set of commands:

| Command   | Action                                   | 
|:---------:| ---------------------------------------- | 
| p         | Print whatever the data pointer is over  |
| l         | Move the data pointer left one position  |
| r         | Move the data pointer right one position |
| +         | Increment the value under data pointer   |
| -         | Decrement the value under data pointer   |
| (         | If the value at data pointer is zero, then jump to matching ) and execute following command. Otherwise, move to next instruction.  |
| )         | If the value at data pointer is nonzero, then jump back to matching ( and execute the following command. Otherwise move to next instruction. |
| I         | Take input and place at data pointer location |

## Requirements
This requires `Python 3` and the `argparse` package.

## Example programs
Some simple examples have been provided in [examples/](./examples/). Notice that the first line is the input for the program to run (what is accessed with the I command) and the rest of the code is on the following line. 