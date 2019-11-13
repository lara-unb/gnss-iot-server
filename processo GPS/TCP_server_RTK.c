#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "rtklib.h"

#define STR_NTRIPSVR 6
#define STR_MODE_W  0x2
#define SIZE_BUFFER 256

typedef struct {
  int bytes_read;
  char read_buffer[SIZE_BUFFER];
} read_t;

void settings_port(int fd)
{

  struct termios ConfigPortaSerial;

  tcgetattr(fd, &ConfigPortaSerial);
  cfsetispeed(&ConfigPortaSerial, B9600);
  cfsetospeed(&ConfigPortaSerial, B9600);

  ConfigPortaSerial.c_cflag &= ~PARENB;
  ConfigPortaSerial.c_cflag &= ~CSTOPB;
  ConfigPortaSerial.c_cflag &= ~CSIZE;
  ConfigPortaSerial.c_cflag |= CS8;

  ConfigPortaSerial.c_cflag |= CREAD | CLOCAL;

  ConfigPortaSerial.c_iflag &= ~(IXON | IXOFF | IXANY);
  ConfigPortaSerial.c_iflag &= ~(ICANON | ECHO | ECHOE | ISIG);

  ConfigPortaSerial.c_oflag &= ~OPOST;

  ConfigPortaSerial.c_cc[VMIN] = 1;
  ConfigPortaSerial.c_cc[VTIME] = 0;

  if ((tcsetattr(fd, TCSANOW, &ConfigPortaSerial)) != 0)
    printf("\n  ERROR ! in Setting attributes");
  else
    printf("\n  BaudRate = 9600 \n  StopBits = 1 \n  Parity   = none");
}

int open_port()
{

  int fd;

  char caminho[] = "/dev/ttyUSB0";


  fd = open(caminho, O_RDWR | O_NOCTTY);

  if (fd == -1)
  {
    perror("Unable open serial port");
    exit(EXIT_FAILURE);
  }
  else
  {
    printf("Opened Successfully\n");
    fcntl(fd, F_SETFL, 0);
  }

  return fd;
}

void print_msg(raw_t raw){
  time_t t = raw.time.time;
  time_t t1 = raw.obs.data->time.time;
  double *value_carrier = raw.obs.data->L;
  double *value_pseudo = raw.obs.data->P;
  float *value_doppler = raw.obs.data->D;
  char sat = raw.obs.data->sat;

  printf("Tipo de mensagem recebida: %s\n", raw.msgtype);
  printf("Tempo registrado pelo receptor: %s\n  ", ctime(&t));
  printf("Número de dados observáveis: %d\n", raw.obs.n);
  printf("Máximo de dados observáveis alocados: %d\n", raw.obs.nmax);
  printf("Tempo registrado pelo satélite: %s", ctime(&t1));
  printf("Número do satélite do sinal correspondente: %c\n", sat);
  printf("Tipo de mensagem recebida: %d\n", raw.outtype);
  printf("Valor de número de ciclos pelo método de carrier phase: %f\n", *value_carrier);
  printf("Valor de distância pelo método de pseudorange (m): %f\n", *value_pseudo);
  printf("Frequência Doppler : %f\n", *value_doppler);
}

read_t read_data(int fd)
{

  char read_buffer[SIZE_BUFFER];
  read_t readReturn;
  int i;

  tcflush(fd, TCIFLUSH);


  readReturn.bytes_read = read(fd, &read_buffer, sizeof(read_buffer));

  for (i = 0; i < readReturn.bytes_read; i++)
  {
    readReturn.read_buffer[i] = read_buffer[i];
    /*printf("%c", read_buffer[i]);*/
  }

return readReturn;
}

int main (void) {

  char *path = "[gustavo[:4842]]@127.0.0.1[:8888]/moutpoint[:string]";
  unsigned char *unsbuff;

  raw_t raw;
  rtcm_t *out;

  int ret;
  int format = 4;
  int i, bytes = 1;
  int fd;
  int type = 0;

  FILE *file;

  read_t readReturn = {0};

  /*stream_t stream;

  strinit(&stream);

  if(init_rtcm(out) == 0){

    printf("Memory allocation error");
    exit(EXIT_FAILURE);

  }
  */

  if(init_raw(&raw)==0){
    printf("Erro ao gerar raw struct. Finalizando...\n");
    return 0;
  }

  else {printf("Sucesso ao gerar o raw struct. Continuando operação.\n");}

  /*if (stropen(&stream, STR_NTRIPSVR, STR_MODE_W, path) == 0){

    printf("Erro ao abrir stream em comunicação NTRIP. Finalizando...");
    return(1);

  }

  printf("Abertura de stream completa!\n");
*/

  fd = open_port();
  settings_port(fd);

  while(bytes != 0){

    if(input_rawf(&raw, format, file)==-1){
      printf("Ubx length error / ubx checksum error. Continuando...\n");
    }
    else if(input_rawf(&raw, format, file)==0){
      printf("No message. Continuando...\n");
    }
    else if(input_rawf(&raw, format, file)==-2){
      printf("EOF. Finalizando...\n");
      return 0;
    }

    else if(input_rawf(&raw, format, file)==1){
      printf("\nInput observation data.\n");

      print_msg(raw);

    }

    else if(input_rawf(&raw, format, file)==2){
      printf("\nInput ephemeris.\n");

      printf("Satélite com info: %d",raw.nav.eph->sat);

      print_msg(raw);
    }

    else if(input_rawf(&raw, format, file)==3){
      printf("\nInput sbas message.\n");

      print_msg(raw);

    }

    else if(input_rawf(&raw, format, file)==9){

      printf("\nInput ionosphere/UTC parameter.\n");

      print_msg(raw);

    }

    else if(input_rawf(&raw, format, file)==31){

      printf("\nInput lex message.\n");



    }

    /*raw2rtcm(&out, &raw, ret);

    readReturn = read_data(fd);

    bytes = readReturn.bytes_read;

    strcpy((char *)unsbuff, readReturn.read_buffer);

    strwrite(&stream, unsbuff, SIZE_BUFFER);*/

  }

return 0;

}
