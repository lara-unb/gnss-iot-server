#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

#define ACESSO_PERMITIDO 1
#define ACESSO_NEGADO 0

#define PORT 8888

int main(int argc, char const *argv[])
{
    int sock = 0, valread;
    int acesso;
    double coord[2] = {44, 66};
    char *token = "2B03FC5C6FB7A54CBB09DA3582A08450";
    char buffer[1024] = {0};
    struct sockaddr_in serv_addr;

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    /* Convert IPv4 and IPv6 addresses from text to binary form */
    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0)
    {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed \n");
        return -1;
    }

    valread = read(sock, buffer, 1024);
    printf("%s\n", buffer);
    send(sock, token, strlen(token), 0);
    printf("%s\n", token);

    read(sock, &acesso, sizeof(acesso));

    while (1)
    {

        send(sock, coord, sizeof(coord), 0);
        read(sock, coord, sizeof(coord));

        printf("%lf\n", coord[0]);
        printf("%lf\n", coord[1]);
        sleep(1);
    }

    close(sock);

    return 0;
}