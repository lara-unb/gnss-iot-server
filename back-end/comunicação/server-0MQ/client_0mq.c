#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main(void)
{
    printf("Connecting to hello world server…\n");
    void *context = zmq_ctx_new();
    void *requester = zmq_socket(context, ZMQ_REQ);
    int rc = zmq_connect(requester, "tcp://localhost:5555");
    int valread;
    if (rc == -1)
    {
        printf("E: falha ao conectar: %s\n", strerror(errno));
        return -1;
    }

    int request_nbr;
    for (request_nbr = 0; request_nbr != 50; request_nbr++)
    {

        char buffer[10];
        printf("Sending paulo %d…\n", request_nbr);
        zmq_send(requester, "paulo", 6, 0);
        valread = zmq_recv(requester, buffer, 10, 0);
        buffer[valread] = '\0';
        printf("Received %s %d\n", buffer, request_nbr);
    }
    zmq_close(requester);
    zmq_ctx_destroy(context);
    return 0;
}