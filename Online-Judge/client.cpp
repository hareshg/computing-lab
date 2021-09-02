/******************************************************************************
*	Haresh Gaikwad | 20CS60R09
*	Computing Lab II
*	Assignment 4
	>>  g++ client.cpp -o client && ./client
	>> NOTE: First compile and run server.cpp
******************************************************************************/
#include <iostream>
#include <cstring>
#include <fstream>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
using namespace std;

#define SIZE 512000

void error(const string& message) {
	cout << message << endl;
	exit(1);
}

string get_filename(string total_cmd) {
	char* cmd = (char*)total_cmd.c_str();
	char* tok = strtok(cmd, " ");
	tok = strtok(NULL, " ");
	return string(tok);
}

int main(int argc, char const *argv[]) {

	// create socket
	int client = socket(AF_INET, SOCK_STREAM, 0);
	if (client < 0) error("\t\tError: Unable to create socket.\n");

	char addr[20] = "127.0.0.1";
	int port = 8888;
	if (argc > 1) {
		port = atoi(argv[2]);
		bzero(addr, 20);
		strcpy(addr, argv[1]);
	}

	//create address for socket
	sockaddr_in cli_addr;
	bzero((char*)&cli_addr, sizeof(cli_addr));
	cli_addr.sin_family = AF_INET;
	cli_addr.sin_port = htons(port);
	cli_addr.sin_addr.s_addr = inet_addr(addr);
	memset(cli_addr.sin_zero, '\0', 8);

	// connecting to server
	if (connect(client, (sockaddr*)&cli_addr, sizeof(cli_addr)) < 0) {
		error("Start server first! | Connection failed.");
	}
	cout << "\n\t+++ NOTE: Enter QUIT to exit +++" << endl;

	while (true) {
		// send data to server
		printf("\n---------------------------------------------------------\n");
		printf("\t\tEnter command: ");
		string total_cmd;
		getline(cin, total_cmd);
		if (total_cmd.size() < 3) {
			cout << "\nError!" << endl;
			continue;
		}
		string command = total_cmd.substr(0, 4);

		if (command == "QUIT" or command == "quit") {
			cout << "\n\t\tThank You!\n" << endl;
			break;
		}
		else if (command == "STOR" or command == "stor") {

			if (total_cmd.size() < 10) {
				cout << "\nError!" << endl;
				continue;
			}
			char line[SIZE];
			string fileName = get_filename(total_cmd);

			if (access(fileName.c_str(), F_OK) == 0) {
				FILE* fp = fopen(fileName.c_str(), "r");
				if (fp == NULL) {
					cout << "\nFile not Exist!" << endl;
					continue;
				}
				fgets(line, SIZE, fp);
				string temp = " " + string(line);
				total_cmd += temp;
				while (true) {
					if (fgets(line, SIZE, fp) == NULL) break;
					temp = string(line);
					total_cmd += temp;
				}
				fclose(fp);
			}
			else {
				cout << "\nFile not Exist!" << endl;
				continue;
			}
		}
		else if (total_cmd.substr(0, 7) == "CODEJUD" or total_cmd.substr(0, 7) == "codejud") {
			if (total_cmd.size() < 13) {
				cout << "\nError!" << endl;
				continue;
			}
			char line[SIZE];
			string temp = total_cmd;

			char* cmd1 = (char*)temp.c_str();
			char* tok = strtok(cmd1, " ");
			tok = strtok(NULL, " ");

			string fileName = string(tok);

			tok = strtok(NULL, " ");
			if (tok == NULL) {
				cout << "\nError!" << endl;
				continue;
			}
			string ext = string(tok);
			if ((ext == "cpp" and  fileName.substr(fileName.size() - 3) == "cpp") or (ext == "c" and fileName.substr(fileName.size() - 1) == "c")) {
				if (access(fileName.c_str(), F_OK) == 0) {
					FILE* fp = fopen(fileName.c_str(), "r");
					if (fp == NULL) {
						cout << "\nFile not Exist!" << endl;
						continue;
					}
					fgets(line, SIZE, fp);
					string temp = "*" + string(line);
					total_cmd += temp;
					while (true) {
						if (fgets(line, SIZE, fp) == NULL) break;
						temp = string(line);
						total_cmd += temp;
					}
					fclose(fp);
				}
				else {
					cout << "\nFile not Exist!" << endl;
					continue;
				}
			}
			else {
				cout << "\n\t > only .cpp/ .c allowed!" << endl;
				continue;
			}
		}
		else if (command == "RETR" or command == "retr") {
			if (total_cmd.size() < 8) {
				cout << "\nError!" << endl;
				continue;
			}
		}
		else if (command == "DELE" or command == "dele") {
			if (total_cmd.size() < 8) {
				cout << "\nError!" << endl;
				continue;
			}
		}

		char* message = (char*)total_cmd.c_str();

		if (send(client, message, strlen(message), 0) < 0) {
			error("\nError sending!\n");
		}

		cout << "Sent to server!\n" << endl;

		// read acknowledgement
		char ack[SIZE];
		bzero(ack, SIZE);

		if (recv(client, ack, SIZE, 0) < 0) {
			error("\nError!\n");
		}

		string data = string(ack);

		if (data == "Error!") {
			cout << "Received from server:\n" << ack << endl;
			continue;
		}

		if (command == "RETR" or command == "retr") {

			string fileName = get_filename(total_cmd);
			string fileData = data.substr(1);
			ofstream myfile(fileName);
			myfile << fileData;
			total_cmd.clear();
			cout << "SUCCESS!" << endl;
			continue;
		}
		total_cmd.clear();
		cout << ack << endl;
	}

	close(client);
	return 0;
}