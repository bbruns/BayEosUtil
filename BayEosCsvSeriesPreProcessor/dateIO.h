/** @file dateIO.h
*/
#ifndef DATEIO_H
#define DATEIO_H


#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define STR_SIZE 100
#define _CRT_SECURE_NO_WARNINGS


/**
* Executes the CSV stretching.
* @param pfin a FILE pointer to the input File.
* @param pfout a FILE pointer to the output FILE.
* @param interval an interval that should be between all timestamps as a double.
* @param sep a character that seperates the timestamps and values.
*/
void stretchFromTo(FILE* pfin, FILE* pfout, double interval, char sep);


/**
* counts the limiter characters in a given line
* @param str the input string.
* @param sep the limiter character.
* @return The count of sep in str.
*/
int limiter_cnt(char* str, char sep);

/**
* enters a timestamp into the output file.
* @param time a pointer to a time struct that should be inserted as a time stamp.
* @param fout a pointer to the output file.
* @param sep a limiter character that indicates empty values.
* @param sep_cnt the amount of limiter characters to be inserted.
*/
void enterTime(struct tm* time, FILE* fout, char sep, int sep_cnt);


/**
* reads time from a string into a struct tm.
* @param time_out a struct tm that shoud be read into.
* @param str the string in the Format %d:%m:%Y %H:%M:%S which should be evaluated.
*/
void readTime(struct tm* time_out, char* str);

#endif // !DATEIO_H