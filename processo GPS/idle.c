
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char const *argv[])
{
    char s1[80] = "Paulo";
    char s2[80] = "Henrique";

    strcat(s1,s2);
    printf(s1);
        
    return 0;
}
