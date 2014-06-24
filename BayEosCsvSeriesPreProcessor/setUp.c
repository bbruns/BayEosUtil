#include "setUp.h"
#include "stdlib.h"
#include "string.h"

#define ERROUT(X) {fputs(X,stderr); return -1;}
#define PAR_LISTINGS "Possible Combinations:\n-i <csv_input_file> [-o <csv_output_file>]\n[-t <series_interval_min>] [-c <csv_separator _char>]"
#define STR_SIZE 100
#define ERROPEN(FILE_PTR, MODE,FILE_NAME) do {FILE_PTR=fopen(FILE_NAME,MODE); if(!FILE_PTR){fprintf(stderr,"Failed to open %s", FILE_NAME); return -1;}} while(0)

const char par_listing[]=PAR_LISTINGS;
const char par_err_str[]="Parameter Error. Please provide sufficient parameters.\n"//
	PAR_LISTINGS;

///return
int parseCmdPars(int argc, char**argv,FILE** pfin, FILE** pfout, double *interval, char* sep){
	char* fname=NULL,*oname=NULL,**argv_ptr, line[STR_SIZE];
	if (argc>1 && strlen(argv[1])>1 &&argv[1][1]=='h') {printf(par_listing); return -1;}
	if(!(argc%2)||argc==1) ERROUT(par_err_str);
	for(argv_ptr=argv+1; argv_ptr<argv+argc; argv_ptr+=2)
	{
		if (strlen(*argv_ptr)<2) ERROUT(par_err_str);
		switch((*argv_ptr)[1])
		{
			case 'i': ERROPEN(*pfin,"r",argv_ptr[1]); fname=argv_ptr[1]; break;
			case 'o': oname=argv_ptr[1]; break;
			case 't': sscanf(argv_ptr[1],"%lf",interval); *interval*=60; break;
			case 'c': *sep= argv_ptr[1][0]; break;
			default: ERROUT(par_err_str);
		} 
	} 
	if(!fname) ERROUT("No Input File indicated. Please indicate a workload.");
	if(!oname) {
		sscanf(fname, "%s.csv", (oname=calloc(STR_SIZE, sizeof(char))) );
		sprintf(&oname[strlen(oname)-4],"-corr.csv");
	}
	ERROPEN(*pfout,"w",oname);
	printf("Input: %s\nOutput: %s\nTime Interval: %lf mins\nLimiter: \'%c\'\n",fname,oname,*interval/60,*sep);
	return 0;
}