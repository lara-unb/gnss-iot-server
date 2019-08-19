#include <stdio.h>
#include <stdlib.h>

int main(int argc, char const *argv[])
{
    char filename[] = "logfile.txt";
    int ch = 0;
    FILE *file;

    if ((file = fopen(filename, "r")) == NULL)
    {
        printf("O arquivo não pode ser aberto");
        exit(1);
    }

    do
    {
        ch = getc(file);
        putchar(ch);
    } while (ch != EOF);

    fclose(file);

    return 0;
}
