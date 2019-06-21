
/*
*	Nome: main.c
*	Autor: Paulo Henrique Rosa
*	Data: 09/06/2019
*
* 	Descrição: Programa para ler e armazenar dados do GPS 
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>  /* String function definitions */
#include <fcntl.h>  /* File Control Definitions          */
#include <termios.h>/* POSIX Terminal Control Definitions*/
#include <unistd.h> /* UNIX Standard Definitions         */
#include <errno.h>  /* ERROR Number Definitions          */


int abrir_porta( int argc, char const *argv[]);

void ler_dados(int fd);
void configuracaoPortaSerial();

int abrir_porta( int argc, char const *argv[]){

  int fd;

  char caminho [13] ="/dev/";
  if (argc != 2){
    printf("Não foi informado a porta!\n");
    exit(EXIT_FAILURE);

  }

  strcat(caminho,argv[1]);

  fd = open(caminho, O_RDWR | O_NOCTTY);

  if (fd == -1){
    perror("Unable open serial port");
    exit(EXIT_FAILURE);
  }else
  {
    printf("%s Opened Successfully\n",argv[1]);
    fcntl(fd, F_SETFL,0);
  }
  
 return fd;
}
void configuracaoPortaSerial(int fd){
  
  struct termios  ConfigPortaSerial;

  tcgetattr(fd,&ConfigPortaSerial);
  cfsetispeed(&ConfigPortaSerial, B9600);
  cfsetospeed(&ConfigPortaSerial, B9600);
  
  ConfigPortaSerial.c_cflag &= ~PARENB;
  ConfigPortaSerial.c_cflag &= ~CSTOPB;
  ConfigPortaSerial.c_cflag &= ~CSIZE;
  ConfigPortaSerial.c_cflag |=  CS8;
  
  
  ConfigPortaSerial.c_cflag |= CREAD | CLOCAL;
  
  
  ConfigPortaSerial.c_iflag &= ~(IXON | IXOFF | IXANY);
  ConfigPortaSerial.c_iflag &= ~(ICANON | ECHO | ECHOE | ISIG);

  ConfigPortaSerial.c_oflag &= ~OPOST;
  
  
  ConfigPortaSerial.c_cc[VMIN] = 1; 
  ConfigPortaSerial.c_cc[VTIME] = 0; 


  if((tcsetattr(fd,TCSANOW,&ConfigPortaSerial)) != 0)
      printf("\n  ERROR ! in Setting attributes");
  else
    printf("\n  BaudRate = 9600 \n  StopBits = 1 \n  Parity   = none");
	


}
void ler_dados(int fd){

  tcflush(fd, TCIFLUSH);
  char read_buffer[128];
  int bytes_read = 0;
  int i = 0;

  bytes_read = read(fd, &read_buffer, sizeof(read_buffer));
  printf("\n\n  Bytes recebidos: %d", bytes_read);
  printf("\n  ");

  for ( i = 0; i < bytes_read; i++)
  {
    printf("%c",read_buffer[i]);
  }
  

}

int main(int argc, char const *argv[]){
  int fd;

  fd = abrir_porta(argc, argv);
  configuracaoPortaSerial(fd);

  while (1)
  {
    ler_dados(fd);
  }
  
  close(fd);
  return 0;
}