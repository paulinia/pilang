# pilang
An esoteric language for fun 

## Syntax

Every line has to be either assigning a value to a variable or closing brackets.

Assigning is done using `:`. There's no `=` keyword.

### Types of expressions

Expressions are either single line expression, ternary operators, loops and functions.

#### Single line expressions

On a single line, there can be either mathematical expressions such as:

`a : 42`
`b : a + 5`
`c : -b * (4 + a)`

Or hard-coded arrays:

`A : [5, 2, 1]`
`B : [A, A, [], [[]]]`

Note that pilang doesn't care about types.

__Variables__ in pilang can be either global or local. A local variable is distinguished by apostrophes around the variable name. A local variable doesn't exist outside of its scope. Global variables can be defined everywhere.

##### Examples

`a` is a global variable

`'a'` is a local variable

Note that `a` and `'a'` are two different variables and it's perfectly fine to use both.

#### Scopes

A __scope__ is a block of code evaluating into its _scope variable_.

```
(@res
    'a' : 4
    'res' : 'a'
)
```

The scope above is an expression that evaluates to four. Note that `'res'` is a local variable. A scope always returns a local variable.

The current version of the pilang interpreter doesn't support scopes alone, they always have to be associated with a ternary operator, a loop or a function.

#### Ternary operators

An equivalent of if in pilang is a ternary (possibly more) operator. The basic syntax:

```
<variable name> : ? <expression> (@<scope variable>
    ... "if <expression> do this
                               );(@<scope variable>
    ... "else
                               )
```

If we wanted to do the equivalent of else if, no nesting is necessary.

```
<variable name> : ? <expression> (@<scope variable>
    ... "if <expression> do this
          )? <else if expression>(@<scope variable>
    ...
                               );(@<scope variable>
    ... "else
                               )
```

Note that the current version of the interpreter requires the expression to be a scope.

#### Loops

As every expression has to return something, loops are not an exception. A loop is the only way how to create a not-hardcoded array. A loop in pilang is virtually a list comprehension. How does it work? Take a look at the following loop code:

```
<variable name> : [ <expression> (@<scope variable>
    ... 
                 )]
```

What the loop does can be described with a following pseudocode:

```python
<variable name> = []
while <expression>:
    <variable name>.append(<result of the scope>)
```

Note that the side effects of the scope are essential for the expression to become false one day.

#### Functions

A function `f` in pilang is declared as below.

```
f : [](@<scope variable>
    ...
)
```

Every function takes an array of arguments. It's not possible to name the arguments. More about accessing the arguments below.

Even though the function is written as a variable, it's not a variable and shouldn't be treated as such!

### Strings

So far, the only variables we worked with were ints and arrays. A string in pilang is an array in the specific format. It's not possible to use string constants in code. Pilang, however, supports printing and reading strings.

When a pilang reads a string it's stored as an array of numbers, where the first element is a length of the string and the rest are characters' numbers in ASCII. Strings in this format can be outputted as a string. More about I/O below.

### I/O

For printing numbers and arrays, a value is assigned to the special variable `!`.

```
! : 42 
```

_This code prints $42$._

For printing strings, the key character is `%`.
```
% : [11, 104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100]
```

_This code prints "hello world"_

Numbers can be read when in a single line using command `&`.

```
a : &
```

_This code reads a line with a single integer and assigns the integer value to `a`_

Pilang also supports reading strings. The keyword for it is `<`.

```
s : <
```

A line of input is converted to a pilang-like string and assigned to `s`.

### Comments

Comments in pilang are denoted by question marks.

```
notacomment : 5 " + 4 is a comment " still a comment
```

### Logic in pilang

Pilang doesn't have a built-in boolean type. Instead, it uses integers as booleans. If an integer is positive, it's true. If it's nonpositive (zero or less), then the truth value is false.

Note that pilang does have neither built-in equal, greater nor less operators. In the test file _math.pi_, equal is implemented as below.

```
to_bool : [](@res
    'res' : ? # (@a
        'a' : 1
    );(@a
        'a' : 0
    )
)

equal : [](@res
    'a' : #
    'b' : #
    'res' : to_bool['a' - 'b' + 1] * to_bool['b' - 'a' + 1]
)
```

Less and greater are easier to come up with, so I let those for as an exercise for a reader :) 

### More about arrays

Arrays in pilang don't support random or almost any access. The only element that can be accessed in a pilang array is the first one. By accessing the element, the element is popped. The special character for such access is `#` More demonstrated in the following example:

```
A : [1, 2, 3, 4, 5]
a : #A " a is now 1  and A is [2, 3, 4, 5]
```

It's not possible to further enlarge the array. If the need arises, we need to rewrite it completely.

#### Function array

When talking about functions, we mentioned that functions' arguments are passed as arrays. They're then accessed just like arrays, with the change that the array has no name. A keyword for "next argument please" is just `#`.

```
square : [](@res
    'a' : #
    'res' : 'a' * 'a'
)

! : square[5] " prints 25
```

#### Important warning about arrays

As you may notice, pilang doesn't have a function length for arrays, nor it's possible to check whether the array is empty. Therefore a programmer has to take care of array lengths so there won't be a crash!

## Examples
```
factorial : [](@res
    'a' : #
    'res' : ? 'a' (@h
        'h' : 'a' * factorial['a' - 1]
    );(@h
        'h' : 1
    )
)
```
_A factorial function_

```
n : &
i : 0
A : [n - i : (@a
    'a' : &
    i : i + 1
    )]
i : 0
B : [n : (@b
    'mini' : #A
    'j' : 0
    A : [n - 'j' - 1 : (@a
        'a' : #A
        'mini' : ? 'mini' - 'a' (@c
            'c' : 'a'
            'a' : 'mini'
            );(@c
            'c' : 'mini'
            )
        'j' : 'j' + 1
        )]
    'b' : 'mini'
    n : n - 1
    )]
! : B
```

Sort

### Mergesort

This language seems pretty much useless (it is). It doesn't have proper access to arrays, is it even possible to code $O(n\log n)$ sort in it?

As it turns out, yes, bottom-up mergesort has $O(n\log n)$ implementation in pilang!

```
" This function returns lesser of two numbers
min : [](@res
    'a' : #
    'b' : #
    'res' : ? 'a' - 'b' (@ans
        'ans' : 'b'
    );(@ans
        'ans' : 'a'
    )
)

"Mergesort takes A, an array with n elements, n and a number d - consecutive d-grams in the array are sorted
mergesort : [](@res 
    'A' : #
    'n' : #
    'd' : #
    "If 'd' + 1 > 'n' the answer is 'A' - if at least 'n' consecutive elements in A are sorted, the array is sorted
    'res' : ? 'd' - 'n' + 1 (@ans
        'ans' : 'A'
    );(@ans
        'i' : 0
        'fir' : []
        'sec' : []
        'f' : 0
        's' : 0 "We're comparing the front elements, hence we need to have them stored outside the array
        'f0' : 0
        's0' : 0
        'ans' : ['n' - 'i' (@a "In each iteration we add new element to array with sorted 2d-grams
            'blah' : ? 'f' + 's' (@bleh
                'bleh' : []
            );(@bleh  "If both arrays we're merging are empty, we need to start merging another two
                'j' : 'i'
                'fir' : [min['i' + 'd', 'n'] - 'j' (@ff
                    'ff' : #'A'
                    'j' : 'j' + 1
                    'f' : 'f' + 1
                )]
                'sec' : [min['i' + 2 * 'd', 'n'] - 'j' (@ss
                    'ss' : #'A'
                    'j' : 'j' + 1
                    's' : 's' + 1
                )]
                'f0' : ? 'f' (@ble
                    'ble' : #'fir'
                );(@ble
                    'ble' : 0
                )
                's0' : ? 's' (@ble
                    'ble' : #'sec'
                );(@ble
                    'ble' : 0
                )
                'bleh' : []
            )
            
            'a' : ? 'f' (@b " The merge itself is just casework
                'b' : ? 's' (@c
                    'c' : ? 'f0' - 's0' (@aa
                        'aa' : 's0'
                        's' : 's' - 1
                        's0' : ? 's' (@s1
                            's1' : #'sec'
                        );(@s1
                            's1' : 0
                        )
                    );(@aa
                        'aa' : 'f0'
                        'f' : 'f' - 1
                        'f0' : ? 'f' (@f1
                            'f1' : #'fir'
                        );(@f1
                            'f1' : 0
                        )
                    )
                );(@c
                    'c' : 'f0'
                    'f' : 'f' - 1
                    'f0' : ? 'f' (@f1
                        'f1' : #'fir'
                    );(@f1
                        'f1' : 0
                    )
                )
            );(@b
                'b' : 's0'
                's' : 's' - 1
                's0' : ? 's' (@s1
                    's1' : #'sec'
                );(@s1
                    's1' : 0
                )
            )
            'i' : 'i' + 1
        )]
        'ans' : mergesort['ans', 'n', 'd' * 2] "Recursivelly call mergesort
    )
)
```
