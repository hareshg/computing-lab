/******************************************************************************
*	Haresh Gaikwad | 20CS60R09
*	Computing Lab II
*	Assignment 4
	>>  g++ server.cpp -o server && ./server
	>> NOTE: First compile and run server.cpp
******************************************************************************/
#include <iostream>
#include <cstring>
#include <fstream>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/time.h>
using namespace std;

#define SIZE 512000

void retr(const string fileName, string& data) {
	char line[SIZE];
	FILE* fp = fopen(fileName.c_str(), "r");
	if (fp == NULL) {
		data += "Error!";
		return;
	}
	fgets(line, SIZE, fp);
	string temp = " " + string(line);
	data += temp;
	while (true) {
		if (fgets(line, SIZE, fp) == NULL) break;
		temp = string(line);
		data += temp;
	}
	fclose(fp);
}

void stor(const string fileName, string& data, string in) {

	ofstream myfile(fileName);
	myfile << in;
	data += "\n >> Store Successful!\n";

}

void list(string& data) {

	char line[SIZE];
	FILE* fp = fopen("list.txt", "r");
	if (fp == NULL) {
		data += "Error!";
		return;
	}

	while (true) {
		if (fgets(line, SIZE, fp) == NULL) break;
		string temp = string(line);
		data += temp;
	}
	fclose(fp);
	data += "\n >> Listed!\n";
}

void dele(const string fileName, string& data) {
	if (remove(fileName.c_str()) == 0) {
		char line[SIZE];
		FILE* fp = fopen("list.txt", "r");
		if (fp == NULL) {
			data += "Error!";
			return;
		}
		string temp;
		while (true) {
			if (fgets(line, SIZE, fp) == NULL) break;
			temp += string(line);
		}
		fclose(fp);

		int idx = temp.find(fileName);
		temp.erase(idx, fileName.size() + 1);

		ofstream myfile("list.txt");
		myfile << temp;
		data += "\n >> Deleted successfully!\n";
	}
	else data += "Error!";

}

void codejud(const string fileName, string& data) {
// 1. Compilation phase -
// COMPILE_ERROR - The judge’s compiler can not compile client’s source code.
// COMPILE_SUCCESS - The judge’s compiler compile code successfully.

	string temp_name = fileName;

	char *fname = (char*)fileName.c_str(); // get filename without extension
	char* tok = strtok(fname, ".");
	string name = string(tok);

	string comfile = "compilation_" + name + ".txt";
	string comfile_temp = "compilation_" + name + ".txt";

	string cmd1 = "g++ " + temp_name + " 2> " + comfile;
	char *compile = (char*)cmd1.c_str();

	if (system(compile) < 0) {
		data += "Error!";
		return;
	}

	char line[SIZE];
	string temp;


	FILE* fp = fopen(comfile.c_str(), "r");
	if (fp == NULL) {
		data += "Error!";
		return;
	}
	while (true) {
		if (fgets(line, SIZE, fp) == NULL) break;
		temp += string(line);
	}
	fclose(fp);

	if (temp.empty()) {
		data += "COMPILE_SUCCESS!\n";
		remove(comfile_temp.c_str());
	}
	else {
		data += "COMPILE_ERROR\n" + temp;
		return;
	}

// 2. Execution Phase -
// TIME LIMIT EXCEEDED (TLE)- Client’s program failed to finish executing before the established time limit (1 sec) for the problem.
// RUN_ERROR - The judge find error occurs during program execution(run-time).
// RUN_SUCCESS - The judge find no error during program execution(run-time).

	char line_temp[SIZE]; bzero(line_temp, SIZE);

	string in = "input_" + name + ".txt";
	FILE* infile = fopen(in.c_str(), "r");
	if (infile == NULL) {
		data += "Error!";
		return;
	}

	string out = "output_" + name + ".txt";
	FILE* outFile = fopen(out.c_str(), "w");
	if (outFile == NULL) {
		data += "Error!";
		return;
	}
	fclose(outFile);

	string cmd2 = "timeout 2 ./a.out < tempfile.txt >> output_" + name + ".txt" + " 2> runtime_error.txt";
	char *exec = (char*)cmd2.c_str();

	timeval tv;
	timeval start_tv;
	FILE* tempFile;

	gettimeofday(&start_tv, NULL);

	while (true) {
		if (fgets(line_temp, SIZE, infile) == NULL) break;
		tempFile = fopen("tempfile.txt", "w");
		if (tempFile == NULL) {
			data += "Error!";
			return;
		}
		fprintf(tempFile, "%s", line_temp);
		fflush(tempFile);

		if (system(exec) < 0) {
			data += "Error!";
			return;
		}
		fclose(tempFile);
	}
	fclose(infile);

	gettimeofday(&tv, NULL);
	double elapsed = (tv.tv_sec - start_tv.tv_sec) + (tv.tv_usec - start_tv.tv_usec) / 1000000.0;
	remove("a.out");

	if (elapsed >= 1) {
		data += "RUN_ERROR: TIME LIMIT EXCEEDED (TLE)\n";
		return;
	}

	data += "RUN_SUCCESS\n";
	data += ">> Time taken: " + to_string(elapsed) + " seconds\n";

// 3. Matching Phase -
// ACCEPTED - All the test cases passed.
// WRONG_ANSWER - Test cases failed.

	char line1[SIZE];
	char line2[SIZE];

	string opfile = "output_" + name + ".txt";
	string tcfile = "testcase_" + name + ".txt";

	FILE* fpop = fopen(opfile.c_str(), "r");
	if (fpop == NULL) {
		data += "Error!";
		return;
	}
	FILE* fptc = fopen(tcfile.c_str(), "r");
	if (fptc == NULL) {
		data += "Error!";
		return;
	}

	int total = 0, passed = 0;

	while (true) {
		if (fgets(line2, SIZE, fptc) == NULL) break;
		if (fgets(line1, SIZE, fpop) == NULL) break;
		string op = string(line1);
		string tc = string(line2);

		// line handling
		int i;
		for (i = 0; i < tc.size(); i++) {
			if (tc[i] == '\r' or tc[i] == '\n') {
				tc[i] = '\0';
				break;
			}
		}
		tc = tc.substr(0, i);

		for (i = 0; i < op.size(); i++) {
			if (op[i] == '\r' or op[i] == '\n') {
				op[i] = '\0';
				break;
			}
		}
		op = op.substr(0, i);

		// cout << op << ":" << tc << endl;
		// cout << op.size() << ":" << tc.size() << endl;		// for testing

		if (op == tc) passed++;

		if (!op.empty() and !tc.empty()) total++;
	}
	fclose(fpop);
	fclose(fptc);


	if (total == passed) {
		data += "ACCEPTED\n";
	}
	else {
		data += "WRONG_ANSWER\n";
	}

	data += "Test cases passed: " + to_string(passed) + " / " + to_string(total) + "\n";
	return;
}

bool is_valid_cmd(const string command) {

	string commands[10] = {"RETR", "STOR", "LIST", "QUIT", "DELE", "retr", "stor", "list", "quit", "dele"};
	for (int i = 0; i < 10; i++) {
		if (command == commands[i]) return true;
	}
	return false;
}

string get_filename(string total_cmd) {
	char* cmd = (char*)total_cmd.c_str();
	char* tok = strtok(cmd, " ");
	tok = strtok(NULL, " ");
	return string(tok);
}

bool file_exists(const string name) {

	char line[SIZE];
	FILE* fp = fopen("list.txt", "r");
	if (fp == NULL) return false;

	while (true) {
		if (fgets(line, SIZE, fp) == NULL) break;
		string temp = string(line);
		if (temp == name + '\n') {
			return true;
		}
	}
	fclose(fp);
	return false;
}

int main(int argc, char const *argv[]) {

	// create list at server side
	FILE* fp = fopen("list.txt", "w");
	fclose(fp);

	// create serv_fd socket
	int serv_fd = socket(AF_INET, SOCK_STREAM, 0);
	if (serv_fd < 0) {
		printf("\nError: Unable to create socket.\n");
		exit(1);
	}

	char addr[20] = "127.0.0.1";
	int port = 8888;
	if (argc > 1) {
		port = atoi(argv[1]);
	}

	//create address for socket
	sockaddr_in serv_addr;
	bzero((char*)&serv_addr, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(port);
	serv_addr.sin_addr.s_addr = inet_addr(addr);
	memset(serv_addr.sin_zero, '\0', 8);

	// bind the socket
	if (bind(serv_fd, (sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
		printf("\nError: Unable to bind.\n");
		exit(1);
	}

	// listen for incoming request
	cout << "++ Waiting for client..." << endl;
	sockaddr_in client;
	bzero((char*)&client, sizeof(client));

	if (listen(serv_fd, 10) < 0) {  // 10 connection can be done
		printf("\nError: Unable to listen.\n");
		exit(1);
	}
	socklen_t sockaddr_in_size = sizeof(sockaddr_in);

	// select stuff
	fd_set master;                   // Master File Descriptor - list
	fd_set read_fds;                 // Temp fileName descriptor for read
	int fd_max = serv_fd;

	FD_ZERO(&master);
	FD_ZERO(&read_fds);

	FD_SET(serv_fd, &master); // Add socket address to master
	int new_fd = 0;


	while (true) {

		read_fds = master; // for accept function
		if (select(fd_max + 1, &read_fds, NULL, NULL, NULL) < 0) {
			perror("\n\t\t Select() Error!\n");
			exit(1);
		}

		int i;
		for (i = 0; i <= fd_max; i++) {

			if (FD_ISSET(i, &read_fds)) {
				if (i == serv_fd) {
					new_fd = accept(serv_fd, (sockaddr*)&client , &sockaddr_in_size);
					if (new_fd < 0) {
						perror("\n\t\t accept() error!\n");
						exit(1);
					}

					FD_SET(new_fd, &master); // Add to master set
					if (new_fd > fd_max) fd_max = new_fd;
					printf("\t++ Connection Established with Client: %d \n", client.sin_port);

				}
				else {

					char msg[SIZE];
					bzero(msg, SIZE); // initialize

					if (recv(i, msg, SIZE, 0) == 0) {
						printf("\t\t\t -- Client %d left.\n", client.sin_port);
						close(i);
						FD_CLR(i, &master);
					}
					else {// serve client

						string data;
						printf("Received message from Client %d\n", client.sin_port);

						string total_cmd = string(msg);
						string command = total_cmd.substr(0, 4);

						if (is_valid_cmd(command) or total_cmd.substr(0, 7) == "CODEJUD" or total_cmd.substr(0, 7) == "codejud") {
							if (command == "RETR" or command == "retr") {
								string fileName = get_filename(total_cmd);
								if (!file_exists(fileName)) { data += "Error!";}
								else retr(fileName, data);
							}
							else if (command == "STOR" or command == "stor") {

								string fileName = get_filename(total_cmd);
								if (!fileName.empty()) {
									if (!file_exists(fileName)) {
										FILE* fp = fopen("list.txt", "a+");
										fprintf(fp, "%s\n", fileName.c_str());
										fclose(fp);
										string fileData = total_cmd.substr(6 + fileName.size());
										stor(fileName, data, fileData);
									}
									else data += "Error!";

								}
								else data += "Error!";

							}
							else if (total_cmd.substr(0, 7) == "CODEJUD" or total_cmd.substr(0, 7) == "codejud") {

								string fileName = get_filename(total_cmd);
								if (!fileName.empty()) {
									if (!file_exists(fileName)) {
										FILE* fp = fopen("list.txt", "a+");
										fprintf(fp, "%s\n", fileName.c_str());
										fclose(fp);
										string s = total_cmd;
										char* cmd = (char*)s.c_str();
										char* tok = strtok(cmd, "*");
										string temp = string(tok);
										string fileData = total_cmd.substr(temp.size() + 1);
										stor(fileName, data, fileData);
										// CODE judge
										codejud(fileName, data);
									}
									else data += "Error!";
								}
								else data += "Error!";

							}
							else if (command == "LIST" or command == "list") { list(data); }
							else if (command == "DELE" or command == "dele") {
								string fileName = get_filename(total_cmd);
								if (!file_exists(fileName) or fileName.empty()) {
									data += "Error!";
								}
								else dele(fileName, data);
							}
							else {
								data += "Error!";
							}
						}
						else {
							data += "Error!";
						}
						if (data.empty()) { data += "ok!";}
						const char* ack = (char*)data.c_str();
						if (send(i, ack, strlen(ack), 0) < 0) {
							printf("\nError sending!\n");
							exit(1);
						}

						printf("\t\tAcknowledgement sent!\n");
					}
				}
			}
		}
	}

	close(new_fd);
	close(serv_fd);
	return 0;
}