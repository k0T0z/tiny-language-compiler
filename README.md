# tiny-language-compiler
A simple Qt-Python tiny language compiler


## INDEX
 * [Objective](#objective)
 * [Requirements](#requirements)
 * [Team Members](#team_members)

## Objective

To create a Qt GUI application that demonstrate how to scan and parse tiny language source files using recursive decent parsing method and then generate parse tree for the syntax.

```
{sample program in TINY language- computes factorial}
read x; { input an integer }
if 0<x then { don’t compute if x<=0 }
  fact:=1;
  repeat
    fact := fact*x;
    x := x-1
  until x=0;
  write fact{output factorial of x}
end
```

![output](https://user-images.githubusercontent.com/74428638/209871795-8f308d82-aeb8-4b91-8099-0ba3cba14ea2.png)

## Requirements
 
 * PyQt6
 * PySide6
 
### Compiler

We are working on Mac OS X, so we need to install Xcode command line tools. If the following steps don't work, download them directly from [Apple Developer's website](https://developer.apple.com/download/more/). 
I'm using MinGW Compiler, eaiser install it from SourceForge or MSYS

### Qt6

* Start by installing the Qt6 SDK from (qt.io)[https://www.qt.io/download]. I decided to go with the Open Source version
* Currently, since this is an experiment, I decided to install Qt 7.0.0. 
* Qt Creator is a sort of an IDE with internal build tools. So currently, it's a good idea to install this.
* We will not be using CMake since QMake comes bundled with the creator

## Team Members
```Usama Ahmed Kawashty Abdelraheem 18Q9484```
```Saif Salah Eldeen Yahya Mostafa 1901529```
```Hussein Ahmed Hussein Adbelgalil 18Q4984```
```Yousef Mohamed Elsharkawy 18Q4486```
