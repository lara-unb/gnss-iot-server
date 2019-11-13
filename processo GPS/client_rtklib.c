#include <stdio.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "rtklib.h"

#define STR_NTRIPCLI 7
#define STR_MODE_R  0x1
#define SIZE_BUFFER 256

int main (void) {

  char *path = "[gustavo[:4842]]@127.0.0.1[:8888][/moutpoint]";
  FILE *file;
  char *msg = NULL;
  unsigned char *buff;
  int type = 0;
  stream_t stream;

  strinit(&stream);

  if (stropen(&stream, STR_NTRIPCLI, STR_MODE_R, path) == 0){

    printf("Erro ao abrir stream em comunicação NTRIP. Finalizando...");
    return(1);

  }

  while(strstat(&stream, msg) != -1){
    strread(&stream, buff, SIZE_BUFFER);
    printf("%s\n",buff);
  }

  printf("Abertura de stream completa!\n");

}
