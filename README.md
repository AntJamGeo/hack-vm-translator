# Hack Virtual Machine Translator

The Hack Virtual Machine Translator is used in the second stage of a two-stage compilation process (first stage uses the [Jack Compiler](https://github.com/AntJamGeo/jack-compiler)) of a program written in an object-oriented programming language.

This translator takes .vm files that have been produced in the first stage of compilation of a program and combines them into a single .asm file to be ran on the Hack computer, a simple computer that is built in the first part of the nand2tetris course (references below).

## Usage

The translator requires a .vm file or a directory containing .vm files to be provided to it in order to run. In both cases, a single .asm file will be produced; in the case of single file translation, this file will appear in the same directory as the .vm file, while for a directory, it will appear within the given directory.

To use, clone this repository and run `python3 <path to translator.py> <path to target .vm file or directory>`. For example, if the current working directory is the hack-vm-translator directory and we add
* `example.vm` to the directory, running `python3 translator.py example.vm` will produce `example.asm` in the hack-vm-translator directory;
* a directory called `example` to the directory, running `python3 translator.py example` will produce `example.asm` in the `example` directory.

## Related Projects
* Hack Assembler: https://github.com/AntJamGeo/hack-assembler
* Jack Compiler: https://github.com/AntJamGeo/jack-compiler

## References
* nand2tetris Website: https://www.nand2tetris.org/
* Part 1 of the Course (Hardware): https://www.coursera.org/learn/build-a-computer
* Part 2 of the Course (Software): https://www.coursera.org/learn/nand2tetris2
