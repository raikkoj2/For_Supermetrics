#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>


#define MAX_NAME 21 // max length of name = 20


//Struct for Games
typedef struct Games{
    char *name;
    float price;
    float earnings;
    struct Games *next;
}Game;





//add new game to the linked list
void addGame(Game *games){

	//define new variables
    char name[MAX_NAME];
    char *newName;
	float price;
	Game *stepper;
	Game *current;
	Game *newGame;

	stepper = games;

	// read off space character
	getchar();
	//read the parameters and save data of success to variable res
	int res = scanf("%s %f", name, &price);

	//check if reading worked
	if( res != 2 ){
		printf("Error, make sure you give adding command in format 'A name price' where name is string and price is float.\n");
		return;
	}
	//check that price is greater than zero
	if (price <= 0) { 
		printf("Error, price has to be greater than zero.\n");
		return;
	}

	//check that there isn't already a game with given name
	while (stepper->next != NULL) {

		current = stepper->next;
		if (strcmp(name, current->name) == 0) {
			// found match
			printf("You have '%s' already in your database.\n", current->name);
			return;
		}
		stepper = current;
	}

	//add game after the to the end of the list and allocate memory for it
	newGame = (Game*)malloc(sizeof(Game));
	newName = (char*)malloc((strlen(name) + 1) * sizeof(char));
	strcpy(newName, name);
	newGame->name = newName;
	newGame->price = price;
	newGame->earnings = 0;
	newGame->next = NULL;
	stepper->next = newGame;

	//print confirmation about successfull execution
	printf("Game '%s' added.\n", newGame->name);
    
}






//buy games
void buyGame(Game *games){

	//create new variables
    Game *stepper;
	Game *current;
	int count;
    char name[MAX_NAME];

	stepper = games;

	//read off space character
	getchar();
	//read parameters and save data about success to res
	int res = scanf("%s %d", name, &count);

	//check if reading worked
	if(res != 2){
		printf("Error, make sure you give buying command in format 'B name count' where name is string and count is int.\n");
		return;
	}
	//check that count is positive int
	if(count < 0){
		printf("Error, count has to be positive integer.\n");
		return;
	}

	//try to find the game and buy it count times
	while (stepper->next != NULL) {

		current = stepper->next;

		if (strcmp(current->name, name) == 0) {
			//found match
			current->earnings += count * current->price;
			printf("%d games bought.\n", count);
			return;
		}
		else {
			stepper = current;
		}
	}

	//Game not found
	printf("Game '%s' not found.\n", name);

}






//Method for comaring two games with their earnings.
//Used inside qsort.
int compareGames(const void *inputA, const void *inputB){

	//make two Game variables
	const Game *a = inputA;
	const Game *b = inputB;

	//If a->earnings is greater return -1 and if it's lower return +1.
	//Else make comparison with the names.
	if(a->earnings > b->earnings){
		return -1;
	}else if(a->earnings < b->earnings){
		return 1;
	}else{
		return strcmp(a->name, b->name);
	}
}






//print all Games on the list
void printGames(Game *games){
	//define variables for the funktion
	Game *stepper;
	Game *current;
	stepper = games;
	int count = 0;

	//check how many games are on the list
	while(stepper->next != NULL) {
		stepper = stepper->next;
		count++;
	}

	stepper = games;

	//allocate memory for a table that will contain all the games
	Game *orderedGames = malloc(count * sizeof(Game));

	current = orderedGames;
	int i = 0;

	//make copies af the games to the table
	while(i < count){
		stepper = stepper->next;
		current->name = malloc(MAX_NAME * sizeof(char));
		strcpy(current->name, stepper->name);
		current->price = stepper->price;
		current->earnings = stepper->earnings;
		current->next = NULL;
		i++;
		current++;
	}
	
	//sort the table by the earnngs
	qsort((void *) orderedGames, count, sizeof(Game), compareGames);
	
	i = 0;
	current = orderedGames;

	//print the games on the sorted table
	while(i < count){
		printf("%s %.2f %.2f\n", current->name, current->price, current->earnings);
		current++;
		i++;
	}

	i = 0;
	stepper = orderedGames;

	//free the names of the games on the sorted table
	while(i < count){
        current = stepper;
        stepper++;
		free(current->name);
		i++;
	}
	//free the table
	free(orderedGames);

}






//saves Games to a file
void saveGames(Game *games){
	//define variables for the function
	char filename[80];
	Game *stepper;

	stepper = games;

	//read off space character
	getchar();
	//read the filename and save data of success to res
	int res = scanf("%s", filename);

	//check if reading worked
	if(res != 1){
		printf("Error, make sure that you give printing command in format 'W filename' where filename is string.\n");
	}

	//open file
	FILE* file = fopen(filename, "w");
	//check if opening worked
	if(!file){
		printf("Error, file not found.\n");
		return;
	}

	//print confirmation text
	printf("Saving following data to file %s:\n", filename);
	//save games to file and also print them so user knows which data was saved
	while (stepper->next != NULL) {
		stepper = stepper->next;
		fprintf(file, "%s %f %f\n", stepper->name, stepper->price, stepper->earnings);
		printf("%s %f %f\n", stepper->name, stepper->price, stepper->earnings);
	}

	//close the file
	fclose(file);

	//print confirmation
	printf("Saving completed.\n");
}






//Clear the list except the first member.
//Used while quitting the program and in function loadGames
void clearGames(Game *games) {
	//define variables
	Game *stepper;
	Game *current;

	stepper = games->next;
	
	//go through the list and free all members except the first one
	while (stepper != NULL) {
		current = stepper->next;
		free(stepper->name);
		free(stepper);
		stepper = current;
	}

	//initialize first members variable next to NULL
	games->next = NULL;
}







//load games from a file
void loadGames(Game *games){

	//define variables for the funktion
	char name[MAX_NAME];
    char *newName;
	float price;
	float earnings;
	Game *stepper;
	Game *current;
	Game *newGame;
	char filename[80];
	int isEnd = 0;

	//create start of a new list
	Game newFirst = {NULL, 0, 0, NULL};

	// read off space character
	getchar();
	//read the filename and store data of success to res
	int res = scanf("%s", filename);
	
	//check that reading worked
	if(res != 1){
		printf("Error, make sure you give loading command in format 'O filename' where filename is string.\n");
		return;
	}

	//open file for reading
	FILE* file = fopen(filename, "r");
	//check that opening file worked
	if (file == NULL) { 
		printf("Error, file not found.\n");
		return;
	}
	
	//read first line before the loop
	res = fscanf(file, "%s %f %f\n", name, &price, &earnings);
	//check that reading worked and if it's the end of the file
	if(res == EOF){
		isEnd = 1;
	}else if(res != 3){
		printf("Error, make sure data in file is in format 'name price earnings' where name is string and price and earnings are floats and there aren't empty rows.\n");
		fclose(file);
		return;
	}

	stepper = &newFirst;


	//read data from file until you reach end of file
	while (isEnd == 0) {

		//check that price and earnings are correct
		if (price <= 0 || earnings < 0) { 
			printf("Error, price and earnings has to be positive floats.\n");
			return;
		}

		//check that game isn't already on the list
		while (stepper->next != NULL) {
			current = stepper->next;
			if (strcmp(name, current->name) == 0) {
				// found match
				//clear new list
				printf("Error, can't add two games with same name.\n");
				clearGames(&newFirst);
				return;
			}
			stepper = current;
		}

		// allocate memory and add game to the list
		newGame = (Game*)malloc(sizeof(Game));
		newName = (char*)malloc((strlen(name) + 1) * sizeof(char));
		strcpy(newName, name);
		newGame->name = newName;
		newGame->price = price;
		newGame->earnings = earnings;
		newGame->next = NULL;
		stepper->next = newGame;

		stepper = &newFirst;
		
		//read next line of the file
		res = fscanf(file, "%s %f %f\n", name, &price, &earnings);
		//check that reading worked and if it's the end of the file
		if(res == EOF){
			isEnd = 1;
		}else if(res != 3){
			printf("Error, make sure data in file is in format 'name price earnings' where name is string and price and earnings are float.\n");
			fclose(file);
			//clear new list
			clearGames(&newFirst);
			return;
		}
	}

	//clear old games
	clearGames(games);

	//move new list to games
	games->next = newFirst.next;

	//close the file
	fclose(file);

	// print confirmation
	printf("Following data read from file %s:\n", filename);
	printGames(games);
}






//read the end of the line and return 0 if EOF is found
int readLine(Game *games) {
	//create variable
	char c = 'X';

	//while not end of the line, read next
	while (c != '\n') {
		if(c == EOF){
			//EOF found
			printf("Quitting execution of the program.\n");
			clearGames(games);
			return 1;
		}
		c = getchar();
	}

	//return confirmation about success
	return 0;
}





int main() {

	//create variables
	Game first = { NULL, 0, 0, NULL };
	char c;
	int end = 0;

	//loop until end command or EOF
	while (end == 0) {
		//variable for looping through lines
		char d = ' ';
		//get next char
		c = getchar();

		//decide which function to call
		switch (c) {
		
		//add game
		case 'A':
			addGame(&first);
			//read off rest of line
			end = readLine(&first);
			break;
		//buy game
		case 'B':
			buyGame(&first);
			//read off rest of line
			end = readLine(&first);
			break;
		//print games
		case 'L':
			printGames(&first);
			//print confirmation
			printf("Printing completed.\n");
			//read off rest of line
			end = readLine(&first);
			break;
		//save games to a file
		case 'W':
			saveGames(&first);
			//read off rest of line
			end = readLine(&first);
			break;
		//read games from a file
		case 'O':
			loadGames(&first);
			//read off rest of line
			end = readLine(&first);
			break;
		//Quit program
		case EOF:
		case 'Q':
			printf("Quitting execution of the program.\n");
			clearGames(&first);
			//make the loop end
			end = 1;
			break;
		//line starts with a space
		case ' ':
			//loop through the line and if there is something else than space, return Error
			while(d != '\n'){
				d = getchar();
				if(!isspace(d)){
					printf("Error! Make sure that you start your command with 'A', 'B', 'L', 'W', 'O' or 'Q'\n");
					//read off rest of line
					end = readLine(&first);
					break;
				}
			}
			break;
		//empty line -> skip it
		case '\n':
			break;
		//Wrongly formatted command
		default:
			printf("Error! Make sure that you start your command with 'A', 'B', 'L', 'W', 'O' or 'Q'\n");
			//read off rest of line
			end = readLine(&first);
			break;
		}
    }

	return 0;
}
