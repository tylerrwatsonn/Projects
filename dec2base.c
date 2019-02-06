/*
 * Tyler Watson
 * 260867260
 * ECSE 202 Assignment 5
 */

#include <stdio.h>
#include <stdlib.h>

//Program to convert numbers between different bases

int find_length(int num, int base) { //function to determine length of str array
	int a = num;
	int size = 0;
	while(a>0) {
		int q = a/base;
		int r = a%base;

		a = q;
		size ++;
	}
	return size;
}

void revStr(char *str, int length) {
	//function to reverse array of chars
	char result[length]; //initialize
	for(int i = 0; i<length; i++) {
		result[i] = str[length-1-i]; // reversal occurs here
		printf("%c", result[i]); //prints out result of reversal

	}
}

void dec2base(int input, int base, char *str) {
	//function to compute remainders
	int i = 0; //initialize count in str
	while(input>0){
		int q = input/base; //new quotient
		int r = input%base; //remainder
		if(r<10) str[i] = r + '0' ; //convert remainder to char int
		else str[i] = 'A' + r - 10; //convert remainder to letter
		i++; //update count
		input = q; //new input
	}

}

int main(int argc, char *argv[]) {
	int a,b; //initialize ints
	if(argc < 2) { //if there aren't enough arguments supplied
		printf("Error: Not enough arguments supplied.\n");
		return -1;
	}
	if(argc > 3) { //if there are too many arguments supplied
		printf("Error: Too many arguments supplied.\n");
		return -2;
	}
	if(argc == 2){
		a = atoi(argv[1]);
		b = 2;
	}
	else {
		a = atoi(argv[1]);
		b = atoi(argv[2]);
	}
	int size = find_length(a,b); //determines array size needed
	char str[size];
	if(a<0||a>2147483647) {
		printf("Error: number must be in the range of [0, 2147483647]\n") ;
		return -3;
	}
	else {
		if(b<2||b>36) {
			printf("Error: base must be in the range [2,36]\n");
			return -4;
		}
		else {
			dec2base(a,b, str);
			printf("The Base-%d form of %d is: ", b, a);
			revStr(str, size);
			printf("\n");
		}
	}
	//TO ALLOCATE ARRAY MEMORY
	char* final_result = (char*)(malloc(2*sizeof(char))); //same as char final_result[n]

}
