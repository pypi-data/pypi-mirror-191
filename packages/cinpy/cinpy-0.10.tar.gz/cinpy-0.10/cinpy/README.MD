# You have no clue about C/C++, but want to boost Python using C/C++ code? Try this!

**cinpy** is made for people who never coded in C/C++, but want to use C/C++ functions/algorithms found somewhere on the internet (GitHub, Stack Overflow, ChatGPT …) in their Python code to speed things up.

### This module is not for massive frameworks, only for small scripts/code snippets. It is very simple and straightforward to use.

## Before we discuss the code, please install:

MSVC ..... C++ x64/x86 build tools from: 
[https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&passive=false&cid=2030](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&passive=false&cid=2030)

#### Localize the following files (Version number might vary) and copy their path:

vcvarsall_bat = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"

cl_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe"

link_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe"

#### Download mingw, and install/extract it

and add the folder \MinGW\bin to %PATH% 

[https://nuwen.net/mingw.html#install](https://nuwen.net/mingw.html#install)

### A system made for dummies

The idea is to add always the same function in the C code that we want to use in Python. 

The following code snippet is our base in C, we have to change it only a little to make it work (almost) everywhere. If that sounds already complicated, don’t worry, 90% of the following code never changes:

```C
void cfun_uint(const  unsigned int  *indatav, size_t size,  unsigned int  *outdatav ) 
        {
            size_t i;
            for (i = 0; i < size; ++i){
            outdatav[i] = indatav[i] * 2.0;};
        }
```

### Here is a detailed explanation:

<img src="https://github.com/hansalemaos/screenshots/raw/main/cpppython/code1.png"/>

Explanation:
**cfun_uint** -> function name, choose whatever you want 
**int** -> the data type, if you're not very knowledgeable about the different data types, 
call **cinpy.print_datatypes().**

In this case:

```python
NumPy:        np.intc
C:            int
ctypes:       ctypes.c_int
code:         i
alias:        numpy.int32: 32-bit signed integer (-2_147_483_648 to 2_147_483_647)
comment:      Signed integer type, compatible with C int
```

Here is the translation of the function in Python:
we won’t need it, it is just for a better understanding. 

```python
def cfun_uint(indatav: list[int],size:int,outdatav:list[int]) ->None:
    for i in range(size):
        outdatav[i] = indatav[i]*2
# Executing the code 
indatav = list(range(10))
size = len(indatav)
outdatav = indatav.copy()
cfun_uint(indatav,size,outdatav)
```

It is very simple, and the greatest thing is: Those lines allow us to import countless ready-to-use algorithms written in C. We only have to put this little function somewhere in the written code and adjust one or two lines.

Let’s create now a file called **cdo.py**

```python
import ctypes
import os
from numpy.ctypeslib import ndpointer
import cinpy

whole_c_code = r"""#include <stdio.h>
void cfun_uint(const  int  *indatav, size_t size,  int  *outdatav ) 
        {
            size_t i;
            for (i = 0; i < size; ++i){
            outdatav[i] = indatav[i] * 2.0;};
        }
""" # complete C-code

all_functions = [
    (
        "cfun_uint", # name of the function in the C code, must be the exact name!
        r"""Multi2""", # __str__ and __repr__ of the partial function that will be created, you can name it however you want
        "aa_", # the prefix of the partial function (scroll down to see the explanation)
        "bb_", # the prefix of the pure function (without partial)
        None, # return type of the function - always None (void) - because we change a copy of the array in place
        [
            ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"), # Has to combine with int  *indatav - only the dtype changes (ctypes.c_int) - nothing else!, for an overview, call cinpy.print_datatypes()
            ctypes.c_size_t, # never changes
            ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"), # Has to combine with int  *outdatav - only the dtype changes, for an overview, call cinpy.print_datatypes()
            # you can add more parameters here
        ],
    ),
]
modulename = "multi2" # name for the module - whatever you want
savefolder = "f:\\convertedcfunctions" # where do you want to save the shared library?
sofile = f"{savefolder}\\multi2.so" # the path of the shared library once it is compiled
if not os.path.exists(sofile): # if sofile doesn't exist, we start the compiler, gcc from  ....\MinGW\bin is used - if you get an error, use the absolute path of gcc.exe
    sofile = cinpy.compile_c_code(
        gcc_exe="gcc.exe", c_code=whole_c_code, modulename=modulename, folder=savefolder
    )
cinpy.loadlib(sofile, all_functions) # now we load the functions
```

Now we can import that file anywhere we want. Let’s create a new file (**cdo1.py**) and import the stuff we need (**import cinpy always first**):

```python
import cinpy
import cdo
```

The compiled C functions are now part of cinpy

<img src="https://github.com/hansalemaos/screenshots/raw/main/cpppython/image1.png"/>

Our C code is a little faster than NumPy, and much faster than Python (40 x), but it is going to get better … 

```python
import cinpy
import cdo

import numpy as np
indata = np.random.randint(1, 20 + 1,size=10000)
indata = indata.astype(np.int32)
outdata =cinpy.aa_cfun_uint(indata)

# indata
# Out[4]: array([17, 18,  8, ..., 10, 13, 15])

# outdata
# Out[3]: array([34, 36, 16, ..., 20, 26, 30])

#
# indata = np.random.randint(1, 20 + 1,size=1000000)
# indata = indata.astype(np.int32)
# %timeit cinpy.aa_cfun_uint(indata)
# cinpy:
# 1.28 ms ± 50.6 µs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)
# numpy:
# %timeit indata*2
# 1.38 ms ± 20.8 µs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)
# python:
# pylistest=indata.tolist()
# %timeit [x*2 for x in pylistest]
# 47.9 ms ± 4.01 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

# If you want to use the not partial version:
indata = np.random.randint(1, 20 + 1,size=10000)
indata = indata.astype(np.int32)
# The partial version aa_cfun_uint does these steps for you:
outdata = np.empty_like(indata) # creating the output array
size = indata.size # getting the size
cinpy.bb_cfun_uint(indata,size,outdata) # changes outdata inplace
```

Good results, but we are having a problem: we can only pass a NumPy arrays of dtype np.int32 

Anything else throws an Exception:

```python
 ctypes.ArgumentError: argument 1: <class 'TypeError'>: array must have data type int32
```

As far as I know, there is no function overloading in C (at least there wasn’t 20 years ago, when I learned C hahaha), but it exists in C++. However, I couldn’t make it work in Python (yet). So let’s use a very primitive way to make the C code work with all (most) data types.

**Important: this step is not mandatory, it is just a little script to save time by generating the same function with different signatures.**

First, we create a new file:**cdoall.py**

```python
import os
import cinpy

modulename = "multallby2" # Any name for your module
moduleinport, folder, argtypesfile, cfile, sofile = cinpy.get_all_files_for_module(
    modulename
) # files are stored in the folder of the cinpy module to make the import easier
if not os.path.exists(sofile):
    whole_python_argtypes, whole_c_code = cinpy.create_signature_variations(
        basefunction="cfun", # whatever you want because this script will auto-generate the C code and add an individual suffix (the data type) to each function

        # !BASE_FUNCTION_NAME! Will be replaced by cfun_short, cfun_long ...
        # !C_DATA_DTYPE! Leave it like it is
        # !ADDEXTRA! If you want to add more variables to the function signature
        # We will see an example soon.
        code_c_function="""
        void !BASE_FUNCTION_NAME!(const !C_DATA_DTYPE! *indatav, size_t size, !C_DATA_DTYPE! *outdatav !ADDEXTRA!) 
        {
            size_t i;
            for (i = 0; i < size; ++i){
            outdatav[i] = indatav[i] * 2.0;};
        }""",
        savepath_argtypes=argtypesfile, # the Python file with all the argtypes. It will be generated, but you can edit it afterward if you like.
        savepath_cfunctions=cfile,# C file with the whole C-code. (Generated, but can be edited)
        c_file_header="#include <stdio.h>", # everything you want to have above the generated functions
        add_to_function_signature="",  # !ADDEXTRA! will be replaced by this string
        add_to_argtypes="", # If you add additional variables (!ADDEXTRA!) you can add them to argtypes already to save some time # Example later on
        add_to_top_of_py_file="", # The Python import file for argtypes, usually nothing needed (Generated, but can be edited)
        prefix_for_partial_functions="aa_", # fewer arguments because it will make a copy of the array and get its size and pass everything to the C function.
        prefix_for_functions="bb_", # more arguments (size, copy of array)
        ignored_dtypes=(
            "bool",
            "np.csingle",
            "np.cdouble",
            "np.clongdouble",
            "np.longdouble",
        ), # Let's ignore those data types, complete list: cinpy.print_datatypes()
    )

    sofile = cinpy.compile_c_code(
        gcc_exe="gcc.exe", c_code=whole_c_code, modulename=modulename, folder=None
    ) # compiling the code
cinpy.load_module_extern_py_file(modulename) # importing it 
```

Let’s create a new file: **cdoall2.py** and import it like we did before:

```python
import cinpy
import cdoall

import numpy as np
indata = np.random.randint(1, 20 + 1,size=10000)
indata = indata.astype(np.int16)
outdata =cinpy.aa_cfun_short(indata)


# outdata
# Out[4]: array([18, 16, 32, ..., 26, 28, 34], dtype=int16)
```

All data types have their own function now. Not the prettiest solution, but it is working.

<img src="https://github.com/hansalemaos/screenshots/raw/main/cpppython/image2.png"/>

If you don’t know which function is the right one for your array, just write the name of the function without calling it, and you will see:

```python
cinpy.aa_cfun_short
Out[5]: 
np=np.short, c=short, ctypes=ctypes.c_short, code=h
numpy.int16: 16-bit signed integer (-32_768 to 32_767)
Signed integer type, compatible with C short.
```

Here is part of the code that was generated: \
If you want, you can make changes and compile it again.

```C
…
// np=np.short, c=short, ctypes=ctypes.c_short, code=h
// numpy.int16: 16-bit signed integer (-32_768 to 32_767)
// Signed integer type, compatible with C short.
void cfun_short(const  short  *indatav, size_t size,  short  *outdatav ) 
        {
            size_t i;
            for (i = 0; i < size; ++i){
            outdatav[i] = indatav[i] * 2.0;};
        }



// np=np.ushort, c=unsigned short, ctypes=ctypes.c_ushort, code=H
// numpy.uint16: 16-bit unsigned integer (0 to 65_535)
// Unsigned integer type, compatible with C unsigned short
void cfun_ushort(const  unsigned short  *indatav, size_t size,  unsigned short  *outdatav ) 
        {
            size_t i;
            for (i = 0; i < size; ++i){
            outdatav[i] = indatav[i] * 2.0;};
        }



// np=np.intc, c=int, ctypes=ctypes.c_int, code=i
// numpy.int32: 32-bit signed integer (-2_147_483_648 to 2_147_483_647)
// Signed integer type, compatible with C int
void cfun_int(const  int  *indatav, size_t size,  int  *outdatav ) 
        {
            size_t i;
            for (i = 0; i < size; ++i){
            outdatav[i] = indatav[i] * 2.0;};
        }
…
```

Let’s make the function more dynamic, we want to use another variable to determine the multiplier in Python - not hard-coded in C (…* 2.0;};)

Let’s create a new file: **cdoallvar.py**

```python
import os
import cinpy

modulename = "multallbyx" # Let's use another name
moduleinport, folder, argtypesfile, cfile, sofile = cinpy.get_all_files_for_module(
    modulename
)
if not os.path.exists(sofile):
    whole_python_argtypes, whole_c_code = cinpy.create_signature_variations(
        basefunction="cfulmulti", # another name for the function(s)
        code_c_function="""
        void !BASE_FUNCTION_NAME!(const !C_DATA_DTYPE! *indatav, size_t size, !C_DATA_DTYPE! *outdatav !ADDEXTRA!) 
        {
            size_t i;
            for (i = 0; i < size; ++i){
            outdatav[i] = indatav[i] * n;};
        }""",
        savepath_argtypes=argtypesfile, 
        savepath_cfunctions=cfile,
        c_file_header="#include <stdio.h>",
        add_to_function_signature=", long n",  This will be added to the function signature
        add_to_argtypes='ctypes.c_long', # This will be added to argtypes. Once again, if you are lost using dtypes, call: cinpy.print_datatypes()
        add_to_top_of_py_file="",
        prefix_for_partial_functions="aa_",
        prefix_for_functions="bb_",
        ignored_dtypes=(
            "bool",
            "np.csingle",
            "np.cdouble",
            "np.clongdouble",
            "np.longdouble",
        ),
    )

    sofile = cinpy.compile_c_code(
        gcc_exe="gcc.exe", c_code=whole_c_code, modulename=modulename, folder=None
    )
cinpy.load_module_extern_py_file(modulename) 
```

Let’s create another file and test if we can pass an additional integer: **freemu.py**

```python
import cinpy
import cdoallvar
import numpy as np
indata = np.random.randint(1, 21,size=10000)
indata = indata.astype(np.int16)
outdata =cinpy.aa_cfulmulti_short(indata, 10) # Here

indata
Out[6]: array([1, 9, 4, ..., 5, 1, 2], dtype=int16)
outdata
Out[7]: array([10, 90, 40, ..., 50, 10, 20], dtype=int16)

# much faster than NumPy 
indata = np.random.randint(1, 21,size=100000000)
indata = indata.astype(np.int16)
%timeit cinpy.aa_cfulmulti_short(indata, 10)
67.7 ms ± 395 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
%timeit indata*10
100 ms ± 474 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

### How to use it in real life?

Well, let’s say you don’t have any clue about C/C++, but you want to use an algorithm in C that you have just found on GitHub (e.g. [https://github.com/TheAlgorithms/C/blob/master/sorting/pancake_sort.c](https://github.com/TheAlgorithms/C/blob/master/sorting/pancake_sort.c) ) because Python is too slow for the things you want to do.

```C
// Sorting of array list using pancake sort
#include <stdio.h>
#include <stdlib.h>

/* Reverses the array */
void flip(int arr[], int i)
{
    int temp, start = 0;

    while (start < i)
    {
        temp = arr[start];
        arr[start] = arr[i];
        arr[i] = temp;
        start++;
        i--;
    }
}

// Returns index of the maximum element in arr[0..n-1]
int findMax(int arr[], int n)
{
    int maxElementIdx, i;

    for (maxElementIdx = 0, i = 0; i < n; ++i)
        if (arr[i] > arr[maxElementIdx])
            maxElementIdx = i;

    return maxElementIdx;
}

// Sorts the array using flip operations
void pancakeSort(int *arr, int n)
{
    // Start from the complete array and one by one reduce current size by one
    for (int curr_size = n; curr_size > 1; --curr_size)
    {
        // Find index of the maximum element in arr[0..curr_size-1]
        int maxElementIdx = findMax(arr, curr_size);

        // Move the maximum element to end of current array if it's not already
        // at the end
        if (maxElementIdx != curr_size - 1)
        {
            // To move at the end, first move maximum number to beginning
            flip(arr, maxElementIdx);

            // Now move the maximum number to end by reversing current array
            flip(arr, curr_size - 1);
        }
    }
}

// Displays the array, passed to this method
void display(int arr[], int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }

    printf("\n");
}

#define N 50

// Driver program to test above function
int main()
{
    int arr[N];
    for (int i = 0; i < N; i++)
        arr[i] = rand() % (N << 1); /* random numbers from 0 to 2N */

    printf("Original array: ");
    display(arr, N);

    pancakeSort(arr, N);
    printf("Sorted array: ");
    display(arr, N);

    return 0;
}
```

This code is from [https://github.com/TheAlgorithms/C/blob/master/sorting/pancake_sort.c](https://github.com/TheAlgorithms/C/blob/master/sorting/pancake_sort.c) 

To use it in Python, we need to adapt the function we have just seen. Usually, this is very simple because often there is an example in the main function like we see here, The only thing we need to do is adding the call **pancakeSort(arr, N)** to our one-size-fits-all-function:

<img src="https://github.com/hansalemaos/screenshots/raw/main/cpppython/code2.png"/>

That’s it. Some important stuff: **do all operations on outdatav, never on indatav** - it won’t work. If you have to call another function (not only multiplying by a number like we did in the previous example), copy all data from indatav to outdatav, this is done by:outdatav[i] = indatav[i] That means: **don’t delete the for loop, and you are fine**. There might be better ways of doing that, but this a good solution for newbies because it is very easy to understand and universal. 

If you are not comfortable writing code in C: 

You don’t have to change anything in the code, just add the function

```C
// Sorting of array list using pancake sort
#include <stdio.h>
#include <stdlib.h>

/* Reverses the array */
void flip(int arr[], int i)
{
    int temp, start = 0;

    while (start < i)
    {
        temp = arr[start];
        arr[start] = arr[i];
        arr[i] = temp;
        start++;
        i--;
    }
}

// Returns index of the maximum element in arr[0..n-1]
int findMax(int arr[], int n)
{
    int maxElementIdx, i;

    for (maxElementIdx = 0, i = 0; i < n; ++i)
        if (arr[i] > arr[maxElementIdx])
            maxElementIdx = i;

    return maxElementIdx;
}

// Sorts the array using flip operations
void pancakeSort(int *arr, int n)
{
    // Start from the complete array and one by one reduce current size by one
    for (int curr_size = n; curr_size > 1; --curr_size)
    {
        // Find index of the maximum element in arr[0..curr_size-1]
        int maxElementIdx = findMax(arr, curr_size);

        // Move the maximum element to end of current array if it's not already
        // at the end
        if (maxElementIdx != curr_size - 1)
        {
            // To move at the end, first move maximum number to beginning
            flip(arr, maxElementIdx);

            // Now move the maximum number to end by reversing current array
            flip(arr, curr_size - 1);
        }
    }
}

// Displays the array, passed to this method
void display(int arr[], int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }

    printf("\n");
}

# our function
void cfun_pancakesort(const  int  *indatav, size_t size,  int  *outdatav ) 
{
            size_t i;
            for (i = 0; i < size; ++i){
            outdatav[i] = indatav[i];};
    pancakeSort(outdatav, size);
}
#define N 50

// Driver program to test above function
int main()
{
    int arr[N];
    for (int i = 0; i < N; i++)
        arr[i] = rand() % (N << 1); /* random numbers from 0 to 2N */

    printf("Original array: ");
    display(arr, N);

    pancakeSort(arr, N);
    printf("Sorted array: ");
    display(arr, N);

    return 0;
}
```

Let’s create a new file like we did in the beginning. This time, we call it: **cdopancake.py**

Let’s copy+paste the C code with our added function, change the module name and the file path.  
Like in the example before, this will be our import file.

```python
import ctypes
import os
from numpy.ctypeslib import ndpointer
import cinpy

whole_c_code = r"""// Sorting of array list using pancake sort
#include <stdio.h>
#include <stdlib.h>

/* Reverses the array */
void flip(int arr[], int i)
{
    int temp, start = 0;

    while (start < i)
    {
        temp = arr[start];
        arr[start] = arr[i];
        arr[i] = temp;
        start++;
        i--;
    }
}

// Returns index of the maximum element in arr[0..n-1]
int findMax(int arr[], int n)
{
    int maxElementIdx, i;

    for (maxElementIdx = 0, i = 0; i < n; ++i)
        if (arr[i] > arr[maxElementIdx])
            maxElementIdx = i;

    return maxElementIdx;
}

// Sorts the array using flip operations
void pancakeSort(int *arr, int n)
{
    // Start from the complete array and one by one reduce current size by one
    for (int curr_size = n; curr_size > 1; --curr_size)
    {
        // Find index of the maximum element in arr[0..curr_size-1]
        int maxElementIdx = findMax(arr, curr_size);

        // Move the maximum element to end of current array if it's not already
        // at the end
        if (maxElementIdx != curr_size - 1)
        {
            // To move at the end, first move maximum number to beginning
            flip(arr, maxElementIdx);

            // Now move the maximum number to end by reversing current array
            flip(arr, curr_size - 1);
        }
    }
}

// Displays the array, passed to this method
void display(int arr[], int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }

    printf("\n");
}
void cfun_pancakesort(const  int  *indatav, size_t size,  int  *outdatav ) 
{
            size_t i;
            for (i = 0; i < size; ++i){
            outdatav[i] = indatav[i];};
    pancakeSort(outdatav, size);
}
#define N 50

// Driver program to test above function
int main()
{
    int arr[N];
    for (int i = 0; i < N; i++)
        arr[i] = rand() % (N << 1); /* random numbers from 0 to 2N */

    printf("Original array: ");
    display(arr, N);

    pancakeSort(arr, N);
    printf("Sorted array: ");
    display(arr, N);

    return 0;
}
""" # complete C-code

all_functions = [
    (
        "cfun_pancakesort", # name of the function in the C code
        r"""pcakgesort""",
        "aa_", 
        "bb_", 
        None,
        [
            ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
            ctypes.c_size_t, 
            ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),         ],
    ),
]
modulename = "pcakesort" # name of the module - whatever you want
savefolder = "f:\\pcakesortctest" # where do you want to save the shared library?
sofile = f"{savefolder}\\pcakesortc.so" # the path of the shared library once it is compiled
if not os.path.exists(sofile): # if sofile doesn't exist, we start the compiler, gcc from  ....\MinGW\bin is used
    sofile = cinpy.compile_c_code(
        gcc_exe="gcc.exe", c_code=whole_c_code, modulename=modulename, folder=savefolder
    )
cinpy.loadlib(sofile, all_functions) # now we load the function
```

Let’s create another file: **cdopancakeimport.py** 
and import the file we have just written

```python
import cinpy
import cdopancake

import numpy as np
indata = np.random.randint(1, 20 + 1,size=10000)
indata = indata.astype(np.int32)
outdata =cinpy.aa_cfun_pancakesort(indata)

outdata
Out[3]: array([ 1,  1,  1, ..., 20, 20, 20])
indata
Out[4]: array([ 2, 20,  4, ..., 19, 17, 15])
```

I used this pancake sorting example purposely because I found a Python version of this algorithm on Wikipedia which has a very similar code: [https://en.wikipedia.org/wiki/Pancake_sorting](https://en.wikipedia.org/wiki/Pancake_sorting)

Let’s put them together in a file and see which one is faster.

```python
import cinpy
import cdopancake
import numpy as np

indata = np.random.randint(1, 20 + 1, size=10000)
indata = indata.astype(np.int32)
outdata = cinpy.aa_cfun_pancakesort(indata)

# outdata
# Out[3]: array([ 1,  1,  1, ..., 20, 20, 20])
# indata
# Out[4]: array([ 2, 20,  4, ..., 19, 17, 15])


def pancake_c(arraysize=20000):
    indata, _ = getnparray_and_list(arraysize=arraysize)
    outdata = cinpy.aa_cfun_pancakesort(indata)
    return outdata


def getnparray_and_list(arraysize=20000):
    indata = np.random.randint(1, 1000, size=arraysize).astype(np.int32)
    return indata, indata.tolist()  # Let's return both -> equal conditions


def pancake_python(arraysize=20000):
    def flip(arr, k: int) -> None:
        left = 0
        while left < k:
            arr[left], arr[k] = arr[k], arr[left]
            k -= 1
            left += 1

    def max_index(arr, k: int) -> int:
        index = 0
        for i in range(k):
            if arr[i] > arr[index]:
                index = i
        return index

    def pancake_sort(arr) -> None:
        n = len(arr)
        while n > 1:
            maxdex = max_index(arr, n)
            flip(arr, maxdex)
            flip(arr, n - 1)
            n -= 1

    _, indata = getnparray_and_list(arraysize=arraysize)
    pancake_sort(indata)
    return indata


outc = pancake_c(arraysize=10000)
outp = pancake_python(arraysize=10000)


# %timeit pancake_c(arraysize=10000)
# 27.7 ms ± 130 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
# %timeit pancake_python(arraysize=10000)
# 8.66 s ± 426 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

Well, the compiled C code is about **300 times faster than the Python implementation**. Not bad for adding 3–4 lines of code, right?

C++

We can also benefit from C++ code using the same strategy

Here is our basic C++ function that we add to each source code:

<img src="https://github.com/hansalemaos/screenshots/raw/main/cpppython/code3.png"/>

The same as before:

**Everything in red never changes, blue might change (data type/function name), green always changes (your algorithm)**

There is a good example on the Microsoft page:

https://learn.microsoft.com/en-us/cpp/parallel/concrt/parallel-algorithms?view=msvc-170

```cpp
// choosing-parallel-sort.cpp
// compile with: /EHsc
#include <ppl.h>
#include <random>
#include <iostream>
#include <windows.h>

using namespace concurrency;
using namespace std;

// Calls the provided work function and returns the number of milliseconds 
// that it takes to call that function.
template <class Function>
__int64 time_call(Function&& f)
{
   __int64 begin = GetTickCount();
   f();
   return GetTickCount() - begin;
}

const size_t DATASET_SIZE = 10000000;

// Create
// Creates the dataset for this example. Each call
// produces the same predefined sequence of random data.
vector<size_t> GetData()
{
    vector<size_t> data(DATASET_SIZE);
    generate(begin(data), end(data), mt19937(42));
    return data;
}

int wmain()
{
    // Use std::sort to sort the data.
    auto data = GetData();
    wcout << L"Testing std::sort...";
    auto elapsed = time_call([&data] { sort(begin(data), end(data)); });
    wcout << L" took " << elapsed << L" ms." <<endl;

    // Use concurrency::parallel_sort to sort the data.
    data = GetData();
    wcout << L"Testing concurrency::parallel_sort...";
    elapsed = time_call([&data] { parallel_sort(begin(data), end(data)); });
    wcout << L" took " << elapsed << L" ms." <<endl;

    // Use concurrency::parallel_buffered_sort to sort the data.
    data = GetData();
    wcout << L"Testing concurrency::parallel_buffered_sort...";
    elapsed = time_call([&data] { parallel_buffered_sort(begin(data), end(data)); });
    wcout << L" took " << elapsed << L" ms." <<endl;

    // Use concurrency::parallel_radixsort to sort the data.
    data = GetData();
    wcout << L"Testing concurrency::parallel_radixsort...";
    elapsed = time_call([&data] { parallel_radixsort(begin(data), end(data)); });
    wcout << L" took " << elapsed << L" ms." <<endl;
} 
/* Sample output (on a computer that has four cores):
    Testing std::sort... took 2906 ms.
    Testing concurrency::parallel_sort... took 2234 ms.
    Testing concurrency::parallel_buffered_sort... took 1782 ms.
    Testing concurrency::parallel_radixsort... took 907 ms.
*/
```

If you don’t feel comfortable editing C++ code (which is understandable), leave everything like it is, and add the function that we have just seen to make it work in Python.

```cpp
// choosing-parallel-sort.cpp
// compile with: /EHsc
#include <ppl.h>
#include <random>
#include <iostream>
#include <windows.h>

using namespace concurrency;
using namespace std;

// Calls the provided work function and returns the number of milliseconds 
// that it takes to call that function.
template <class Function>
__int64 time_call(Function&& f)
{
   __int64 begin = GetTickCount();
   f();
   return GetTickCount() - begin;
}


__declspec(dllexport) void cpp_parallelradixsort(const int *indatav, size_t size, int *outdatav)
{
    size_t i;
    for (i = 0; i < size; ++i){
        outdatav[i] = indatav[i];};
    std::vector<int> v(outdatav, outdatav + i);
    parallel_radixsort(begin(v), end(v));
    std::copy(v.begin(), v.begin()+i, outdatav);
}

// Create
// Creates the dataset for this example. Each call
// produces the same predefined sequence of random data.
vector<size_t> GetData()

{
    const size_t DATASET_SIZE = 10000000; # I moved this line to save memory
    vector<size_t> data(DATASET_SIZE);
    generate(begin(data), end(data), mt19937(42));
    return data;
}

int wmain()
{
    // Use std::sort to sort the data.
    auto data = GetData();
    wcout << L"Testing std::sort...";
    auto elapsed = time_call([&data] { sort(begin(data), end(data)); });
    wcout << L" took " << elapsed << L" ms." <<endl;

    // Use concurrency::parallel_sort to sort the data.
    data = GetData();
    wcout << L"Testing concurrency::parallel_sort...";
    elapsed = time_call([&data] { parallel_sort(begin(data), end(data)); });
    wcout << L" took " << elapsed << L" ms." <<endl;

    // Use concurrency::parallel_buffered_sort to sort the data.
    data = GetData();
    wcout << L"Testing concurrency::parallel_buffered_sort...";
    elapsed = time_call([&data] { parallel_buffered_sort(begin(data), end(data)); });
    wcout << L" took " << elapsed << L" ms." <<endl;

    // Use concurrency::parallel_radixsort to sort the data.
    data = GetData();
    wcout << L"Testing concurrency::parallel_radixsort...";
    elapsed = time_call([&data] { parallel_radixsort(begin(data), end(data)); });
    wcout << L" took " << elapsed << L" ms." <<endl;
} 
/* Sample output (on a computer that has four cores):
    Testing std::sort... took 2906 ms.
    Testing concurrency::parallel_sort... took 2234 ms.
    Testing concurrency::parallel_buffered_sort... took 1782 ms.
    Testing concurrency::parallel_radixsort... took 907 ms.
*/
```

Let’s create a new file:**radixsortms.py** and write the code. 

As you can see, it is almost the same thing that we have done with the C code

```python
import ctypes
from numpy.ctypeslib import ndpointer
import cinpy

whole_c_code = r"""// choosing-parallel-sort.cpp
// compile with: /EHsc
#include <ppl.h>
#include <random>
#include <iostream>
#include <windows.h>

using namespace concurrency;
using namespace std;

// Calls the provided work function and returns the number of milliseconds 
// that it takes to call that function.
template <class Function>
__int64 time_call(Function&& f)
{
   __int64 begin = GetTickCount();
   f();
   return GetTickCount() - begin;
}


__declspec(dllexport) void cpp_parallelradixsort(const int *indatav, size_t size, int *outdatav)
{
    size_t i;
    for (i = 0; i < size; ++i){
        outdatav[i] = indatav[i];};
    std::vector<int> v(outdatav, outdatav + i);
    parallel_radixsort(begin(v), end(v));
    std::copy(v.begin(), v.begin()+i, outdatav);
}

// Create
// Creates the dataset for this example. Each call
// produces the same predefined sequence of random data.
vector<size_t> GetData()

{
    const size_t DATASET_SIZE = 10000000;
    vector<size_t> data(DATASET_SIZE);
    generate(begin(data), end(data), mt19937(42));
    return data;
}

int wmain()
{
    // Use std::sort to sort the data.
    auto data = GetData();
    wcout << L"Testing std::sort...";
    auto elapsed = time_call([&data] { sort(begin(data), end(data)); });
    wcout << L" took " << elapsed << L" ms." <<endl;

    // Use concurrency::parallel_sort to sort the data.
    data = GetData();
    wcout << L"Testing concurrency::parallel_sort...";
    elapsed = time_call([&data] { parallel_sort(begin(data), end(data)); });
    wcout << L" took " << elapsed << L" ms." <<endl;

    // Use concurrency::parallel_buffered_sort to sort the data.
    data = GetData();
    wcout << L"Testing concurrency::parallel_buffered_sort...";
    elapsed = time_call([&data] { parallel_buffered_sort(begin(data), end(data)); });
    wcout << L" took " << elapsed << L" ms." <<endl;

    // Use concurrency::parallel_radixsort to sort the data.
    data = GetData();
    wcout << L"Testing concurrency::parallel_radixsort...";
    elapsed = time_call([&data] { parallel_radixsort(begin(data), end(data)); });
    wcout << L" took " << elapsed << L" ms." <<endl;
} 
/* Sample output (on a computer that has four cores):
    Testing std::sort... took 2906 ms.
    Testing concurrency::parallel_sort... took 2234 ms.
    Testing concurrency::parallel_buffered_sort... took 1782 ms.
    Testing concurrency::parallel_radixsort... took 907 ms.
*/
""" # complete C-code

all_functions = [
    (
        "cpp_parallelradixsort", # name of the function in the C++ code, must be the same name.
        r"""radixsortcpp""", # __str__ and __repr__ of the partial function that we will create, you can choose anything you want
        "aa_", # the prefix of the partial function
        "bb_", # the prefix of the pure function
        None, # return type of the function - always None (void) - because we change a copy of the array in place
        [
            ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"), # Has to combine with int  *indatav - only the dtype changes, for an overview, call cinpy.print_datatypes()
            ctypes.c_size_t, # never changes
            ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"), # Has to combine with int  *outdatav - only the dtype changes, for an overview, call cinpy.print_datatypes()
            # you can add more parameters here
        ],
    ),
]
# Scroll up to get the download link 
vcvarsall_bat = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"
cl_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe"
link_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe"
modulename = "radixmssort" # Name it however you want 
cinpy.get_cpp_functions(
    modulename=modulename, # unique module name
    code=whole_c_code, # the C++ code with the added function
    all_functions=all_functions, # the argtypes and configuration for the function[s]
    vcvarsall_bat=vcvarsall_bat, # needed to compile the code
    cl_exe=cl_exe, # needed to compile the code
    link_exe=link_exe, # To extract the function names (C++ renames them)
    recompile=True, # Use this only the first time. If recompile is True, it will compile the module each time you import it.
)
```

Now we create a second file: **radixsortimport.py**

And import the C++ function like we did before

```python
import cinpy
import radixsortms
import numpy as np

indatarad = np.random.randint(1, 15000001, size=15000000)
indatarad=indatarad.astype(np.int32)
indatarad2=cinpy.aa_cpp_parallelradixsort(indatarad)
print(indatarad2)
```

**… and it is 12 times faster than NumPy**

```python
%timeit cinpy.aa_cpp_parallelradixsort(indatarad)
102 ms ± 5.19 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
%timeit np.sort(indatarad, kind='stable')
1.2 s ± 8.82 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

Since radixsort is very useful, fast, and stable, it would be nice having a function for each data dtype. (If you know how to do function overloading at this point, please let me know!) Let’s create a new file: **radixsortallfunctions.py**

```python
import importlib
import cinpy


modulename = "radixsortmsall"
moduleimport, folder, argtypesfile, cfile, sofile = cinpy.get_all_files_for_module(
   modulename
)  # C++ files generated this way, will be saved in the cinpy folder
whole_python_argtypes, whole_c_code = cinpy.create_signature_variations(
   basefunction="radixsort_cpp",
   code_c_function="""
__declspec(dllexport) void !BASE_FUNCTION_NAME!(const !C_DATA_DTYPE! *indatav, size_t size, !C_DATA_DTYPE! *outdatav !ADDEXTRA!)
{
   size_t i;
   for (i = 0; i < size; ++i){
       outdatav[i] = indatav[i];};
   std::vector<!C_DATA_DTYPE!> v(outdatav, outdatav + i);
   parallel_radixsort(begin(v), end(v));
   std::copy(v.begin(), v.begin()+i, outdatav);
}

""",
   savepath_argtypes=argtypesfile,
   savepath_cfunctions=cfile,
   # Let's copy all imports from the Microsoft example.
   # Not all imports are necessary since we are using only parallel_radixsort,
   # but this module is for people without C/C++ knowledge who want to speed up
   # their Python code without spending half of their life editing C++ code.
   c_file_header="""  
#include <ppl.h>
#include <random>
#include <iostream>
#include <windows.h>

using namespace concurrency;
using namespace std;""",
   add_to_function_signature="",
   add_to_argtypes="",
   add_to_top_of_py_file="",
   prefix_for_partial_functions="aa_",
   prefix_for_functions="bb_",
   ignored_dtypes=(
       "bool",
       "np.csingle",
       "np.cdouble",
       "np.clongdouble",
       "np.longdouble",
       "double",
       "float",
   ),
)

vcvarsall_bat = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"
cl_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe"
link_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe"

try:
   baxax = importlib.import_module(
       f'cinpy.{moduleimport}'
   )  # imports the generated argtypes from the code above
except Exception:
   baxax = importlib.import_module(
       moduleimport
   )  # imports the generated argtypes from the code above
all_functions = getattr(baxax, "all_functions")

cinpy.get_cpp_functions(
   modulename=modulename,
   code=whole_c_code,
   all_functions=all_functions,
   vcvarsall_bat=vcvarsall_bat,
   cl_exe=cl_exe,
   link_exe=link_exe,
   recompile=True,
)
```

Now we created a couple of functions with different signatures. Let’s create a new file **radixsortallfunctionsimport.py** and do a Benchmark 

**parallel_radixsort vs. np.sort**

```python
import cinpy
import radixsortallfunctions
import numpy as np


indatarad = np.random.randint(1, 30000, size=15000000)
indatarad = indatarad.astype(np.int)
intx = cinpy.aa_radixsort_cpp_int(indatarad)
print(intx)
# %timeit cinpy.aa_radixsort_cpp_int(indatarad)
# %timeit np.sort(indatarad,kind='stable')
# 91.7 ms ± 289 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 953 ms ± 945 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)

indatarad = np.random.randint(1, 15000000, size=15000000)
indatarad = indatarad.astype(np.int32)
long = cinpy.aa_radixsort_cpp_long(indatarad)
print(long)

# %timeit cinpy.aa_radixsort_cpp_long(indatarad)
# %timeit np.sort(indatarad,kind='stable')
# 96.5 ms ± 1.25 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 1.19 s ± 2.94 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


indatarad = np.random.randint(1, 15000000, size=15000000)
indatarad = indatarad.astype(np.int64)
longlong = cinpy.aa_radixsort_cpp_longlong(indatarad)
print(longlong)
# %timeit cinpy.aa_radixsort_cpp_longlong(indatarad)
# %timeit np.sort(indatarad,kind='stable')
# 187 ms ± 4.32 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 1.25 s ± 2.07 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

indatarad = np.random.randint(1, 30000, size=15000000)
indatarad = indatarad.astype(np.short)
short = cinpy.aa_radixsort_cpp_short(indatarad)
print(short)
# %timeit cinpy.aa_radixsort_cpp_short(indatarad)
# %timeit np.sort(indatarad,kind='stable')
# 63.6 ms ± 1.24 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 63.9 ms ± 1.9 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

indatarad = np.random.randint(1, 150, size=15000000)
indatarad = indatarad.astype(np.ubyte)
ubyte = cinpy.aa_radixsort_cpp_ubyte(indatarad)
print(ubyte)
# %timeit cinpy.aa_radixsort_cpp_ubyte(indatarad)
# %timeit np.sort(indatarad,kind='stable')
# 47.8 ms ± 286 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 28.7 ms ± 214 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
indatarad = np.random.randint(1, 15000000, size=15000000)
indatarad = indatarad.astype(np.uint)
uint = cinpy.aa_radixsort_cpp_uint(indatarad)
print(uint)
# %timeit cinpy.aa_radixsort_cpp_uint(indatarad)
# %timeit np.sort(indatarad,kind='stable')
# 79.3 ms ± 1.03 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 1.15 s ± 1.06 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

indatarad = np.random.randint(1, 15000000, size=15000000)
indatarad = indatarad.astype(np.uint32)
ulong = cinpy.aa_radixsort_cpp_ulong(indatarad)
print(ulong)
# %timeit cinpy.aa_radixsort_cpp_ulong(indatarad)
# %timeit np.sort(indatarad,kind='stable')
# 78.9 ms ± 973 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 1.15 s ± 1.64 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

indatarad = np.random.randint(1, 15000, size=15000000)
indatarad = indatarad.astype(np.ushort)
ushort = cinpy.aa_radixsort_cpp_ushort(indatarad)
print(ushort)
# %timeit cinpy.aa_radixsort_cpp_ushort(indatarad)
# %timeit np.sort(indatarad,kind='stable')
# 43.8 ms ± 919 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 59.1 ms ± 31.2 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

As you can see, usually, radixsort is about 10 times as fast as Numpy. Numpy only wins when using small data types. Not bad for 10 minutes of work, isn’t it? 

That’s it. I have tested the module only on my computer (Python 3.9.13, Windows 10). If you experience any problems using it, please let me know. New ideas / improvements are always welcome.
