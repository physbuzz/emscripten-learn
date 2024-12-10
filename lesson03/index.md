<nav style="display: grid; grid-template-columns: 1fr 1fr 1fr; padding: 1rem 0;">
    <a href="../lesson02" style="text-decoration: none; color: #0366d6;">← Previous</a>
    <a href="../" style="text-decoration: none; color: #0366d6; text-align: center;">Up</a>
    <a href="../lesson04/" style="text-decoration: none; color: #0366d6; text-align: right;">Next →</a>
</nav>

# Problem 3: Reversing a String

## Question

Inside `bindings.c`, write a function `char* reverseString(const char* str)` that takes a string, reverses it, and returns a newly allocated reversed string. 

The last problem used `Module.HEAPF32.set` to copy a floating point array into the WASM heap. For this problem, use `Module.stringToUTF8` and `Module.lengthBytesUTF8` to copy string data into the WASM heap. 

## Hints

1. As mentioned, use commands `Module.stringToUTF8` for setting memory, `Module.lengthBytesUTF8` for finding how many bytes to malloc (remember to include the null terminator `\0`), and we'll also need `UTF8ToString` to read the string back into javascript.

2. To use the functions like `stringToUTF8`, make sure to add them to `EXPORTED_RUNTIME_METHODS`.

## Solution

* `bindings.c` is easy since we all are C experts here, right?

```c
#include <emscripten/emscripten.h>
#include <stdlib.h>
#include <string.h>

EMSCRIPTEN_KEEPALIVE
char* reverseString(const char* str){
    int length=strlen(str);
    char* reversed=(char*)malloc(length+1);
    for(int i=0;i<length;i++){
        reversed[i]=str[length-i-1];
    }
    reversed[length]='\0';
    return reversed;
}
```

* `demo.html` only has the added complication of using different methods to get and set WASM memory.

```html
<html><body>
<p>Original String: <span id="original">Hello world!</span></p>
<p>Reversed String: <span id="result">Calculating...</span></p>

<script>
var Module = {};
Module.onRuntimeInitialized = function () {
    const originalString = "Hello world!";
    document.getElementById("original").innerText = originalString;

    //Allocate the correct length string
    const length=Module.lengthBytesUTF8(originalString)+1;
    const inputPtr=Module._malloc(length);

    //Write the JS string to WASM memory, call the desired function, and convert the string back
    Module.stringToUTF8(originalString, inputPtr, length);
    const reversedPtr = Module._reverseString(inputPtr);
    document.getElementById("result").innerText = Module.UTF8ToString(reversedPtr);

    Module._free(inputPtr);
    Module._free(reversedPtr);
};
</script>
<script src="bindings.js"></script>
</body></html>
```

* To compile, we have to make sure the desired runtime methods are callable:

```bash
emcc bindings.c \
    -sEXPORTED_FUNCTIONS="['_reverseString', '_malloc', '_free']" \
    -sEXPORTED_RUNTIME_METHODS="['lengthBytesUTF8', 'stringToUTF8', 'UTF8ToString']" \
    -o bindings.js
```


## Demo

Demo.html iframe:

<div style="background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px; padding: 15px; margin: 15px 0;">
    <iframe 
        src="demo.html" 
        style="width: 100%; height: 200px; border: none; overflow: hidden;"
    ></iframe>
</div>
