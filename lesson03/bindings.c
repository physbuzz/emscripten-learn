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
