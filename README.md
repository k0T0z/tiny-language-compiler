# tiny-language-compiler

This is a Qt project that demonstrates the integration of Python with the Qt framework.

![untitled txt - Tiny Language Compiler 13_02_2023 08_07_25 PM](https://user-images.githubusercontent.com/74428638/218539675-306a2e0a-9574-4bb5-b95e-1bf0ba6bd312.png)

## Objective

To create a Qt GUI application that demonstrate how to scan and parse tiny language source files using recursive decent parsing method and then generate parse tree for the syntax.

## Prerequisites

Before building and running this project, you will need to have the following installed on your system:

- Qt 7.0.0
- Python 3.11
- PyQt6 (the Python bindings for Qt)
- PySide6
- Qt Creator (optional but recommended for development)

## Features

- Scan tiny language source files for different types of tokens here's a list:

| Token Type    | Value         |
| ------------- | ------------- |
| SEMICOLON     |      ;        |
| IF            |      if       |
| THEN          |     then      |
| END           | end           |
| REPEAT        | repeat        |
| UNTIL         | until         |
| IDENTIFIER    | x, abc, xyz   |
| ASSIGN        | :=            |
| READ          | read          |
| WRITE         | write         |
| LESSTHAN      | <             |
| EQUAL         | =             |
| PLUS          | +             |
| MINUS         | -             |
| MULT          | *             |
| DIV           | /             |
| OPENBRACKET   | (             |
| CLOSEDBRACKET | (             |
| NUMBER        | 12, 289       |

- Parse different kinds of tokens and create the parse tree here's an example for a tiny language source file with it's pasre/syntax tree:
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

## Building the project

Here are the steps to build and run the project (for windows we didn't run the project on any other platform):

```
Last modification date: 2023 - 02 - 22 03:35 PM
```
1. Download qt creator or vscode or any IDE you see fit
2. Install python
```bash
https://www.python.org/downloads/
```
3. Add scripts directory to your path (if it doesn't) (this includes pip clang-format etc...)
```
Example path: C:\Users\${YOUR_USERNAME}\AppData\Local\Programs\Python\Python311\Scripts
```
4. Install PySide6
```bash
pip install pyside6
```
5. Change python interpreter to point to the right one (qt creator, vscode, ...)
```
Example: C:\Users\${YOUR_USERNAME}\AppData\Local\Programs\Python\Python311\python.exe
```
6. Clone the repository
```bash
git clone https://github.com/saifkandil/tiny-language-compiler.git
```
7. Change into the project directory
```bash
cd tiny-language-compiler
```
8. Run the project
```bash
py tiny-language-compiler
```
9. We will not be using CMake since QMake comes bundled with the creator

## Acknowledgements

We would like to extend our gratitude to the Qt and Python communities for their support and for providing such powerful tools for developing GUI applications. We would also like to acknowledge the open-source projects and libraries that were used in the development of this project.

## About US

We are a group of four students currently enrolled at Ain Shams University, Faculty of Engineering, who share a passion for solving complex problems and creating innovative solutions. Our team consists of a four Computer & Systems Engineering majors, providing a unique blend of skills and perspectives.

At the heart of our team is a shared commitment to hard work, collaboration, and making a difference. Whether we're working on a school project or a startup, we approach every challenge with enthusiasm, creativity, and a drive to succeed.

We are excited to see what the future holds and are committed to making the most of every opportunity that comes our way.

- Usama Ahmed Kawashty Abdelraheem ``18Q9484``
- Saif Salah Eldeen Yahya Mostafa ``1901529``
- Hussein Ahmed Hussein Adbelgalil ``18Q4984``
- Yousef Mohamed Elsharkawy ``18Q4486``
