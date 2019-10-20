#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <malloc.h>

static int
get_monitor_event(void *monitor, int *value, char **address)
{
    zmq_msg_t msg;
    zmq_msg_init(&msg);
    if (zmq_msg_recv(&msg, monitor, 0) == -1)
        return -1;
    assert(zmq_msg_more(&msg));

    uint8_t *data = (uint8_t *)zmq_msg_data(&msg);
    uint16_t event = *(uint16_t *)(data);
    if (value)
        *value = *(uint32_t *)(data + 2);

        zmq_msg_init(&msg);
    if (zmq_msg_recv(&msg, monitor, 0) == -1)
        return -1;
    assert(!zmq_msg_more(&msg));

    if (address)
    {
        uint8_t *data = (uint8_t *)zmq_msg_data(&msg);
        size_t size = zmq_msg_size(&msg);
        *address = (char *)malloc(size + 1);
        memcpy(*address, data, size);
        *address[size] = 0;
    }
    return event;
}

int main(void)
{

    void *context = zmq_ctx_new();
    void *responder = zmq_socket(context, ZMQ_REP);
    int rc = zmq_bind(responder, "tcp://*:5555");
    int valread;
    assert(rc == 0);

    while (1)
    {
        char buffer[10];
        valread = zmq_recv(responder, buffer, 10, 0);
        buffer[valread] = '\0';
        printf("Received: %s\n", buffer);
        sleep(1);
        if (strcmp(buffer, "paulo"))
            zmq_send(responder, "Henrique", 8, 0);
        else
            zmq_send(responder, "World", 5, 0);
    }
    return 0;
}