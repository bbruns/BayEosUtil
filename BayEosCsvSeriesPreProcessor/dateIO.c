#include "dateIO.h"
#include <string.h>

int cnt;


void stretchFromTo(FILE* pfin, FILE* pfout, double interval, char sep ){
	struct tm target, current;
	int sep_cnt, line_itr;
	char line[STR_SIZE];
	cnt=0;
	//Catch useless first lines
	for (line_itr=2; line_itr; line_itr--) {
		fgets(line,STR_SIZE,pfin);
		fprintf(pfout,"%s",line);
	}
	//set first values
	sep_cnt=limiter_cnt(line,sep);
	printf("Number of limiters: %d\n", sep_cnt);
	readTime(&target,line); 
	target.tm_sec+=interval;
	while(fgets(line,STR_SIZE,pfin)) {
		for (readTime(&current,line);difftime(mktime(&current),mktime(&target))>0; target.tm_sec+=interval) enterTime(&target,pfout,sep,sep_cnt);
		current.tm_sec+=interval;
		target=current;
		fprintf(pfout,"%s",line);	
	}
	printf("Added %d paddings.\ndone\n", cnt);
}


void readTime(struct tm* time_out, char* str)
{
  int mon, year;
  memset(time_out,0,sizeof(struct tm));
  sscanf(str, "%d.%d.%d %d:%d:%d",&time_out->tm_mday, &mon, &year, &time_out->tm_hour, &time_out->tm_min, &time_out->tm_sec);
  time_out->tm_year=year-1900;
  time_out->tm_mon=mon-1;
  time_out->tm_isdst=1;
}


void enterTime(struct tm* time, FILE* fout, char sep, int sep_cnt) {
  char str[STR_SIZE], cnst[STR_SIZE]= "%d.%m.%Y %H:%M:%S", *i;
  cnst[strlen(cnst)+sep_cnt]='\n';
  for (i=cnst+strlen(cnst); *i != '\n';i++) *i=sep;
  strftime(str, STR_SIZE, cnst,time);
  fputs(str,fout);
  cnt++;
}


int limiter_cnt(char* str, char sep){
  int ret=0;
  for(; *str; str++) if(*str==sep) ret++;
  return ret;
}
