/*
*	Nome: main.c
*	Autor: Paulo Henrique Rosa
*	Data: 09/06/2019
*
* 	Descrição: Programa para ler e armazenar dados do GPS 
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h> 
#include <fcntl.h>  
#include <termios.h>
#include <unistd.h> 
#include <errno.h>  

#define SIZE_BUFFER 10000

int open_port(int argc, char const *argv[]);

int read_data(int fd);
void settings_port();
void write_data(char data);
int kbhit(void);

int kbhit(void)
{
  struct termios oldt, newt;
  int ch;
  int oldf;
  
  tcgetattr(STDIN_FILENO, &oldt);
  newt = oldt;
  newt.c_lflag &= ~(ICANON | ECHO);
  tcsetattr(STDIN_FILENO, TCSANOW, &newt);
 
  // Eis a diferença essenaial entre este código e o
  // de getch().
  oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
  fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);
  
  ch = getchar();
  
  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
  fcntl(STDIN_FILENO, F_SETFL, oldf);
  
  // Se getchar() conseguiu ler uma tecla,
  // a deveolve para STDIN...
  if (ch != EOF)
  {
    ungetc(ch, stdin);
    return 1;
  }
  
  return 0;
}

int open_port(int argc, char const *argv[])
{

  int fd;

  char caminho[13] = "/dev/";
  if (argc != 2)
  {
    printf("Não foi informado a porta!\n");
    exit(EXIT_FAILURE);
  }

  strcat(caminho, argv[1]);

  fd = open(caminho, O_RDWR | O_NOCTTY);

  if (fd == -1)
  {
    perror("Unable open serial port");
    exit(EXIT_FAILURE);
  }
  else
  {
    printf("%s Opened Successfully\n", argv[1]);
    fcntl(fd, F_SETFL, 0);
  }

  return fd;
}

int read_data(int fd)
{

  tcflush(fd, TCIFLUSH);
  char read_buffer[SIZE_BUFFER];
  int bytes_read = 0;
  int i;

  bytes_read = read(fd, &read_buffer, sizeof(read_buffer));
  printf("\nBytes recebidos: %d", bytes_read);
  printf("\n");

  for (i = 0; i < bytes_read; i++)
  {
    printf("%c", read_buffer[i]);
    write_data(read_buffer[i]);
  }

return bytes_read;
}

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

void write_data(char data)
{
  FILE *file;
  char filename[] = "logfile.txt";

  if ((file = fopen(filename, "a")) == NULL)
  {
    printf("[*] The file can't be opened !");
    exit(EXIT_FAILURE);
  }
  fputc(data, file);
  fclose(file);
}

int main(int argc, char const *argv[])
{
  int fd;
  int maiorByte = 0;
  int byteLido = 0;

  fd = open_port(argc, argv);
  settings_port(fd);

  while (kbhit()!=1)
  {
    byteLido = read_data(fd);
    if (maiorByte<byteLido){
	maiorByte = byteLido;
	}
  }
  printf("\n\n Maior mensagem lida: %d \n\n", maiorByte);

  close(fd);
  return 0;
}
