#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main() {
    //prepare server credentials
    const char* server_name = "localhost";
    const int server_port = 1500;
    //change this port No if required
    
    //this struct will contain address + port No
    struct sockaddr_in server_address;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    
    // http://beej.us/guide/bgnet/output/html/multipage/inet_ntopman.html
    inet_pton(AF_INET, server_name, &server_address.sin_addr);
    
    // htons: port in network order format
    server_address.sin_port = htons(server_port);
    
    // open a TCP stream socket using SOCK_STREAM, verify if socket successfuly opened
    int sock;
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("could not open socket\n");
        return 1;
    }
    
    // TCP is connection oriented, a reliable connection
    // **must** be established before any data is exchanged
    //initiate 3 way handshake
    //verify everything ok
    if (connect(sock, (struct sockaddr*)&server_address,
                sizeof(server_address)) < 0) {
        printf("could not connect to server\n");
        return 1;
    }
    
    // get input from the user
    char data_to_send[100];
    printf("\nEnter a string :  ");
    fgets(data_to_send,100,stdin);
    //fgets reads in the newline character in buffer, get rid of it
    strtok(data_to_send,"\n");

    // data that will be sent to the server
    printf("read : %s\n",data_to_send);
    
    //actual send call for TCP socket
    send(sock, data_to_send, strlen(data_to_send)+1, 0);
    
    // prepare to receive
    int len = 0, maxlen = 100;
    char buffer[maxlen];
    char* pbuffer = buffer;
    
    // ready to receive back the reply from the server
    len = recv(sock, pbuffer, maxlen, 0);
        
    buffer[len] = '\0';
    printf("received: '%s'\n", buffer);
    
    
    // close the socket
    close(sock);
    return 0;
}
