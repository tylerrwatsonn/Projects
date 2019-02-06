/*
 * Tyler Watson
 * 260867260
 *
 * Assignment 6
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//Student Database in C using binary tree

int MAXLEN = 100;

struct StudentRecord {
	char first [100];
	char last [100];
	int ID;
	int marks;
	struct StudentRecord *left;
	struct StudentRecord *right;
};

void addNode(struct StudentRecord** root, struct StudentRecord* input, int sort_option)
{
	// if the root is null
	if((*root) == NULL)
	{
		// create a root with input value
		(*root) = (struct StudentRecord*)malloc(sizeof(struct StudentRecord));
		(*root)-> ID = input ->ID;
		(*root)-> marks = input -> marks;

		strcpy((*root)-> first, input -> first);
		strcpy((*root)-> last, input -> last);


		(*root)->left = NULL;
		(*root)->right = NULL;
	}
	else
	{
		if(sort_option == 1) { //compare Last Names
			// the input is going to be addNodeed either to LEFT or RIGHT
			if(strcmp(input->last, (**root).last) < 0) // root -> val
			{
				// you addNode to left tree
				addNode(&((*root)->left), input, sort_option);
			}else
			{
				addNode(&((*root)->right), input, sort_option);
		}
		}
		else {
			if(input->ID < (**root).ID) { // root -> val
							// you addNode to left tree
				addNode(&((*root)->left), input,sort_option);
			}
			else {
				addNode(&((*root)->right), input, sort_option);
			}
		}
	}
}

//traverse the tree
void traverse_last(struct StudentRecord* root)
{
	// traverse left
	if(root->left != NULL)
	{
		traverse_last(root->left);
	}
	// print the middle
	printf("%-10s %-10s %-10d %-5d", root ->first, root->last, root->ID, root->marks);
	printf("\n");
	// traverse right
	if(root->right != NULL)
	{
		traverse_last(root->right);
	}
}
void traverse_ID(struct StudentRecord* root)
{
	// traverse left
	if(root->left != NULL)
	{
		traverse_ID(root->left);
	}
	// print the middle
	printf("%-10s %-10s %-10d %-5d", root ->first, root->last, root->ID, root->marks);
	printf("\n");
	// traverse right
	if(root->right != NULL)
	{
		traverse_ID(root->right);
	}
}

void record_by_name(struct StudentRecord* root, char* last_name, int* valid_input)
{
	// traverse left
	if(root->left != NULL)
	{
		record_by_name(root->left, last_name, valid_input);
	}
	// print the middle
	if(strcmp(root->last, last_name) == 0) {
	printf("%-15s %-s %-s\n", "Student Name: ", root ->first, root->last);
	printf("%-15s %d\n", "Student ID: ", root->ID);
	printf("%-15s %d\n", "Total Grade: ", root->marks);
	*valid_input = 1;
	}
	// traverse right
	if(root->right != NULL)
	{
		record_by_name(root->right, last_name, valid_input);
	}
}

void record_by_ID(struct StudentRecord* root, int id, int* valid_input)
{
	// traverse left
	if(root->left != NULL)
	{
		record_by_ID(root->left, id, valid_input);
	}
	// print the middle
	if(root->ID == id) {
		printf("%-15s %-s %-s\n", "Student Name: ", root ->first, root->last);
		printf("%-15s %d\n", "Student ID: ", root->ID);
		printf("%-15s %d\n", "Total Grade: ", root->marks);
		*valid_input = 1;
	}
	// traverse right
	if(root->right != NULL)
	{
		record_by_ID(root->right, id, valid_input);
	}
}


int main(int argc, char *argv[])
{
	printf("Building database...\n");

	struct StudentRecord data, *rootName, *rootID;
	FILE *NamesIDs;
	FILE *Marks;
	if ((NamesIDs = fopen(argv[1],"r")) == NULL) { // open Names IDs file
	printf("Can’t open %s\n",argv[1]);
	return -1;
	}

	if ((Marks = fopen(argv[2],"r")) == NULL) { // open marks file
		printf("Can’t open %s\n",argv[2]);
		return -2;
	}
	rootName=NULL; // initialize 2 B-Trees
	rootID=NULL;
	int numrecords=0;

	while (fscanf(NamesIDs,"%s%s%d", &(data.first[0]),&(data.last[0]),&(data.ID)) != EOF) {
		fscanf(Marks,"%d",&(data.marks)); // marks too
		numrecords++;
		addNode(&rootName,&data, 1); // copy to B-Tree sorted by last

		if (rootName==NULL) {
			printf("Error creating name B-Tree, aborted.\n");
			return -3;
		}

		addNode(&rootID,&data, 2); // copy to B-Tree sorted by last
		if (rootID==NULL) {
			printf("Error creating ID B-Tree, aborted.\n");
			return -4;
		}
	}
	fclose(NamesIDs);
	fclose(Marks);
	printf("Finished...\n");
	printf("\n");
	char command[4];
	printf("Enter a command: ");
	scanf("%s", command);

	while(strcmp(command,"Q") != 0) {
		if(strcmp(command, "LN") == 0) {
			printf("Student Record Database sorted by Last Name\n");
			traverse_last(rootName);
		}
		else if(strcmp(command, "LI")==0) {
			printf("Student Record Database sorted by Student ID\n");
			traverse_ID(rootID);
		}
		else if(strcmp(command, "FN")==0){
			char name[25];
			printf("Enter a last name: ");
			int valid_input=0; //variable to check if name exists in database
			scanf("%s", name);
			record_by_name(rootName, name, &valid_input);
			if (valid_input == 0) printf("There is no student with that name.\n");
		}
		else if(strcmp(command, "FI")==0){
			int id;
			int valid_input = 0; //variable to check if I exists in database
			printf("Enter an ID to search: ");
			scanf("%d", &id);
			record_by_ID(rootID, id, &valid_input);
			if (valid_input == 0) printf("There is no student with that ID.\n");
		}
		else if(strcmp(command, "HELP")==0 || strcmp(command, "?")==0) {
			printf("%-6s List all the records in the database ordered by last name.\n", "LN");
			printf("%-6s List all the records in the database ordered by student ID.\n", "FN");
			printf("%-6s Prompts for a name and lists the record of the student with the corresponding name.\n", "FN");
			printf("%-6s Prompts for a name and lists the record of the student with the Corresponding ID.\n", "FI");
			printf("%-6s Prints this list.\n", "HELP");
			printf("%-6s Prints this list.\n", "?");
			printf("%-6s Exits the Program.\n", "Q");
		}
		else printf("Error, invalid command.\n");
		printf("\n");
		printf("Enter a command please: ");
		scanf("%s", command);
	}
	printf("Program Terminated...\n");

	return 0;
}

