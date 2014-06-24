#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "setUp.h"
#include "dateIO.h"


#define ERREXIT(X) do {if(X) return  -1;} while(0)

/**
* main function.
* @param argc integer argument count
* @param argv string array, arguments
* @return success code
*/
int main(int argc, char *argv[])
{
  FILE * pfin=NULL, *pfout=NULL;
  char* fname=NULL,*oname=NULL,**argv_ptr, line[STR_SIZE], sep=';';
  double interval=30*60;
  struct tm current, target;
  int line_itr, sep_cnt;

  ERREXIT(parseCmdPars(argc, argv, &pfin, &pfout, &interval,&sep));
  stretchFromTo(pfin,pfout,interval,sep);

  fclose(pfin);
  fclose(pfout);
}
