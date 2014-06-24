/** @file setup.h
*/
#ifndef SETUP_H
#define SETUP_H

#include <stdio.h>


/**
* parses command line arguments.
* @param argc argument count.
* @param argv aruments pointer.
* @param pfin input File.
* @param pfout output File.
* @param interval an interval in which timestamps should be inserted.
* @param sep a seperation character.
*/
int parseCmdPars(int argc, char**argv,FILE** pfin, FILE** pfout, double *interval, char* sep);

#endif