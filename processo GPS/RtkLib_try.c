#include <stdio.h>
#include <time.h>
#include "rtklib.h"

void print_msg(raw_t raw, int i){
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

int main(void){
int i=0;
int msec = 0, trigger = 1000; /* 10ms */
int iterations=0;
clock_t before = clock();
int format = 4;
FILE *file;
FILE *log;
char *line = NULL;
size_t read;
size_t len = 0;
raw_t raw;

char c;
char filename[] = "/dev/ttyUSB0";

if ((file = fopen(filename, "r")) == NULL)
{
  printf("[*] The file can't be opened !");
  exit(EXIT_FAILURE);

}

if(init_raw(&raw)==0){
  printf("Erro ao gerar raw struct. Finalizando...\n");
  return 0;
}
else {printf("Sucesso ao gerar o raw struct. Continuando operação.\n");}

while (1) {

  if(input_rawf(&raw, format, file)==-1){
    printf("Ubx length error / ubx checksum error. Continuando...\n");
  }
  else if(input_rawf(&raw, format, file)==0){
  }
  else if(input_rawf(&raw, format, file)==-2){
    printf("EOF. Finalizando...\n");
    return 0;
  }

  else if(input_rawf(&raw, format, file)==1){
    printf("\nInput observation data.\n");

    print_msg(raw, i);

  }

  else if(input_rawf(&raw, format, file)==2){
    printf("\nInput ephemeris.\n");

    printf("Satélite com info: %d",raw.nav.eph->sat);

    print_msg(raw, i);
  }

  else if(input_rawf(&raw, format, file)==3){
    printf("\nInput sbas message.\n");

    print_msg(raw, i);

  }

  else if(input_rawf(&raw, format, file)==9){

    printf("\nInput ionosphere/UTC parameter.\n");

    print_msg(raw, i);

  }

  else if(input_rawf(&raw, format, file)==31){

    printf("\nInput lex message.\n");

  }

  i++;

}


fclose(file);
}
