#include <stdio.h>
#include <string.h> /*strlen*/
#include <stdlib.h>
#include <errno.h>
#include <unistd.h> /*close*/
#include <fcntl.h>
#include <arpa/inet.h> /*close*/
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/time.h> /*FD_SET, FD_ISSET, FD_ZERO macros*/
#include <curl/curl.h>
#include <binn.h>

#define SERVIDOR 2
#define ACESSO_PERMITIDO 1
#define ACESSO_NEGADO 0

#define MAX_CLIENT 30
#define MAX_DEVICE 30

#define TRUE 1
#define FALSE 0
#define PORT 8888

typedef struct
{
    char token[32];
    int file_description;
    int autenticacao;
    double coord[2];
} device_t;

typedef struct
{
    int file_description;
    device_t device[MAX_DEVICE];

} client_t;

struct string
{
    char *ptr;
    size_t len;
};

size_t writefunc(void *ptr, size_t size, size_t nmemb, struct string *s);
void init_string(struct string *s);
int request(char *token_recebido);
int token_check(char *token_recebido, int len);
binn *serialize_device(device_t *device);
void settings_socket(struct sockaddr_in *address, int *master_socket);
void bind_socket(struct sockaddr_in *address, int *master_socket);
void listen_socket(struct sockaddr_in *address, int *master_socket, int *addrlen);
void web_connection();

void init_string(struct string *s)
{
    s->len = 0;
    s->ptr = malloc(s->len + 1);
    if (s->ptr == NULL)
    {
        fprintf(stderr, "malloc() failed\n");
        exit(EXIT_FAILURE);
    }
    s->ptr[0] = '\0';
}

size_t writefunc(void *ptr, size_t size, size_t nmemb, struct string *s)
{
    size_t new_len = s->len + size * nmemb;
    s->ptr = realloc(s->ptr, new_len + 1);
    if (s->ptr == NULL)
    {
        fprintf(stderr, "realloc() failed\n");
        exit(EXIT_FAILURE);
    }
    memcpy(s->ptr + s->len, ptr, size * nmemb);
    s->ptr[new_len] = '\0';
    s->len = new_len;

    return size * nmemb;
}

int request(char *token_recebido)
{
    CURL *curl;
    CURLcode res;
    curl = curl_easy_init();
    if (curl)
    {
        struct string s;
        init_string(&s);
        char url[71] = {"http://localhost:8000/profile/resposta/"};
        strcat(url, token_recebido);
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writefunc);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &s);
        res = curl_easy_perform(curl);

        if (!(strcmp("OK", s.ptr)))
        {
            free(s.ptr);
            curl_easy_cleanup(curl);
            return ACESSO_PERMITIDO;
        }
        else
            return ACESSO_NEGADO;
    }
    return ACESSO_NEGADO;
}

int token_check(char *token_recebido, int len)
{

    if (!(strcmp("TOKENSERVIDOR", token_recebido)))
        return SERVIDOR;
    if (request(token_recebido))
        return ACESSO_PERMITIDO;
    else
        return ACESSO_NEGADO;
}

binn *serialize_device(device_t *device)
{
    binn *data, *coord;
    data = binn_object();

    coord = binn_list();
    binn_list_add_double(coord, device->coord[0]);
    binn_list_add_double(coord, device->coord[1]);

    binn_object_set_list(data, "coord", coord);
    binn_free(coord);

    return data;
}

binn *serialize_server(device_t *device)
{
    binn *data, *coord;

    double valor_coord_x, valor_coord_y;
    char coord_x[10];
    char coord_y[10];

    valor_coord_x = device->coord[0];
    valor_coord_y = device->coord[1];

    data = binn_object();
    binn_object_set_str(data, "id", device->token);
    coord = binn_list();

    sprintf(coord_x, "%f", valor_coord_x);
    binn_list_add_str(coord, coord_x);

    sprintf(coord_y, "%f", valor_coord_y);
    binn_list_add_str(coord, coord_y);

    binn_object_set_list(data, "coord", coord);

    binn_free(coord);

    return data;
}

void settings_socket(struct sockaddr_in *address, int *master_socket)
{
    int opt = TRUE;
    /*create a master socket*/
    if ((*master_socket = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    /*set master socket to allow multiple connections ,*/
    /*this is just a good habit, it will work without this*/
    if (setsockopt(*master_socket, SOL_SOCKET, SO_REUSEADDR, (char *)&opt,
                   sizeof(opt)) < 0)
    {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    /*type of socket created*/
    address->sin_family = AF_INET;
    address->sin_addr.s_addr = INADDR_ANY;
    address->sin_port = htons(PORT);
}

void bind_socket(struct sockaddr_in *address, int *master_socket)
{
    /*bind the socket to localhost port 8888*/
    if (bind(*master_socket, (struct sockaddr *)address, sizeof(*address)) < 0)
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    printf("\n\n================== Lara Server V1.0 ==================\n\n");
    printf("Listener on port %d \n", PORT);
}

void listen_socket(struct sockaddr_in *address, int *master_socket, int *addrlen)
{
    /*try to specify maximum of 3 pending connections for the master socket*/
    if (listen(*master_socket, 3) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    /*accept the incoming connection*/
    *addrlen = sizeof(*address);
    puts("Waiting for connections ...");
}

// void web_connection(int sock)
// {
//     char buffer[1024];
//     int valread;

//     while (1)
//     {
//         valread = read(sock, buffer, 1024);
//         buffer[valread] = '\0';
//         if ((!(strcmp("none", buffer))) || !(buffer) )
//             break;
//         printf("ID: %s \n", buffer);
//     }
// }

int main(int argc, char *argv[])
{
    int master_socket = 0, addrlen = 0, new_socket = 0;
    int activity = 0, i = 0, valread = 0, sd = 0, max_sd = 0;
    int server_fd = 0, x = 0;

    int client_socket[MAX_CLIENT];

    char buffer[1025];

    struct sockaddr_in address;

    device_t devices[MAX_CLIENT];
    client_t clientes[MAX_CLIENT];

    binn *data_device, *data_server;

    /*set of socket descriptors*/
    fd_set readfds;

    char *message = "Servidor GNSS - LARA  v1.0\n";

    /*initialise all client_socket[] to 0 so not checked*/
    for (i = 0; i < MAX_CLIENT; i++)
    {
        client_socket[i] = 0;
        clientes[i].file_description = 0;
        devices[i].autenticacao = ACESSO_NEGADO;
    }

    settings_socket(&address, &master_socket);
    bind_socket(&address, &master_socket);
    listen_socket(&address, &master_socket, &addrlen);

    while (TRUE)
    {
        /*clear the socket set*/
        FD_ZERO(&readfds);

        /*add master socket to set*/
        FD_SET(master_socket, &readfds);
        max_sd = master_socket;

        /*add child sockets to set*/
        for (i = 0; i < MAX_CLIENT; i++)
        {
            /*socket descriptor*/
            sd = client_socket[i];

            /*if valid socket descriptor then add to read list*/
            if (sd > 0)
                FD_SET(sd, &readfds);

            /*highest file descriptor number, need it for the select function*/
            if (sd > max_sd)
                max_sd = sd;
        }

        /*wait for an activity on one of the sockets , timeout is NULL ,*/
        /*so wait indefinitely*/
        activity = select(max_sd + 1, &readfds, NULL, NULL, NULL);

        if ((activity < 0) && (errno != EINTR))
        {
            printf("select error");
        }

        /*If something happened on the master socket ,*/
        /*then its an incoming connection*/
        if (FD_ISSET(master_socket, &readfds))
        {
            if ((new_socket = accept(master_socket,
                                     (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0)
            {
                perror("accept");
                exit(EXIT_FAILURE);
            }

            /*inform user of socket number - used in send and receive commands*/
            printf("New connection , socket fd is %d , ip is: %s , port: %d\n", new_socket, inet_ntoa(address.sin_addr), ntohs(address.sin_port));

            /*send new connection greeting message*/
            if (send(new_socket, message, strlen(message), 0) != strlen(message))
            {
                perror("enviar");
            }

            puts("Welcome message sent successfully");

            if ((valread = read(new_socket, buffer, 1024)) != 0)
            {

                buffer[valread] = '\0';

                switch (token_check(buffer, valread))
                {

                case ACESSO_PERMITIDO:
                    printf("Acesso permitido\n");
                    x = ACESSO_PERMITIDO;
                    if (send(new_socket, &x, sizeof(ACESSO_PERMITIDO), 0) >= 0)
                    {
                        /*add new socket to array of sockets*/
                        for (i = 0; i < MAX_CLIENT; i++)
                        {
                            /*if position is empty*/
                            if (client_socket[i] == 0)
                            {
                                client_socket[i] = new_socket;
                                printf("Adding to list of sockets as %d\n", i);
                                devices[i].file_description = new_socket;
                                devices[i].autenticacao = ACESSO_PERMITIDO;
                                strcpy(devices[i].token, buffer);

                                break;
                            }
                        }
                    }
                    else
                    {
                        close(new_socket);
                    }

                    break;

                case ACESSO_NEGADO:
                    printf("Acesso negado\n");
                    x = ACESSO_NEGADO;
                    send(new_socket, &x, sizeof(ACESSO_NEGADO), 0);
                    close(new_socket);
                    break;

                case SERVIDOR:
                    server_fd = new_socket;
                    // web_connection(new_socket);
                    printf("Servidor conectado\n");
                    break;
                }
            }
        }

        /*else its some IO operation on some other socket*/
        for (i = 0; i < MAX_CLIENT; i++)
        {
            sd = client_socket[i];

            if (FD_ISSET(sd, &readfds))
            {
                /*Check if it was for closing , and also read the*/
                /*incoming message*/

                data_device = serialize_device(&devices[i]);
                if ((read(sd, binn_ptr(data_device), binn_size(data_device))) != 0)
                {
                    void *list = binn_object_list(data_device, "coord");

                    devices[i].coord[0] = binn_list_double(list, 1);
                    devices[i].coord[1] = binn_list_double(list, 2);
                    devices[i].coord[0] = 0.01 + devices[i].coord[0];
                    devices[i].coord[1] = 0.01 + devices[i].coord[1];
                    printf("%lf %lf\n", devices[i].coord[0], devices[i].coord[1]);
                    printf("%s\n", devices[i].token);
                    data_device = serialize_device(&devices[i]);

                    if (server_fd)
                    {
                        data_server = serialize_server(&devices[i]);

                        if ((send(server_fd, binn_ptr(data_server), binn_size(data_server), MSG_NOSIGNAL)) == -1)
                        {
                            printf("SERVIDOR WEB DESCONECTADO...\n");
                            close(server_fd);
                            server_fd = 0;
                        }
                        binn_free(data_server);
                    }

                    send(sd, binn_ptr(data_device), binn_size(data_device), 0);
                    binn_free(data_device);
                }
                else
                {
                    getpeername(sd, (struct sockaddr *)&address,
                                (socklen_t *)&addrlen);
                    printf("Host disconnected , ip %s , port %d \n",
                           inet_ntoa(address.sin_addr), ntohs(address.sin_port));
                    close(sd);
                    client_socket[i] = 0;
                    devices[i].autenticacao = 0;
                }
            }
        }
    }
    return 0;
}
