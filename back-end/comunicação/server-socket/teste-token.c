#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define ACESSO_PERMITIDO 1
#define ACESSO_NEGADO 0

int token_check(char *token_recebido, int len )
{
    FILE *fp;
    char token_registrado[len];
    char *file_name = "tokens.txt";

    if ((fp = fopen(file_name, "r")) == NULL)
    {
        printf("Arquivo não pode ser aberto\n");
        exit(EXIT_FAILURE);
    }
    while (fgets(token_registrado, 100, fp) != NULL)
    {
        if (!(strcmp(token_registrado, token_recebido)))
        {
            return ACESSO_PERMITIDO;
        }
    }

    fclose(fp);
    return ACESSO_NEGADO;
}

int main()
{
    if (token_check("F1DC67CE4777EC8AC8F779840B6A9BE7",33))
        printf("Acesso permito");
    else 
        printf("Acesso negado\n");


    return 0;
}