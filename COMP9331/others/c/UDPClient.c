#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main() {
    //server credentials
    const char* server_name = "localhost";
    const int server_port = 1500;
    //change this port No if required
    
    int length;
    
    struct sockaddr_in server_address,from;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    
    // http://beej.us/guide/bgnet/output/html/multipage/inet_ntopman.html
    inet_pton(AF_INET, server_name, &server_address.sin_addr);
    
    // htons: port in network order format
    server_address.sin_port = htons(server_port);
    
    // open a UDP socket using SOCK_DGRAM, -1 on failure
    int sock;
    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        printf("could not open socket\n");
        return 1;
    }
    
    // send
    char data_to_send[100];
    printf("\nEnter a string :  ");
    fgets(data_to_send,100,stdin);
    
    //fgets reads in the newline character in buffer, get rid of it
    strtok(data_to_send,"\n");

    // data that will be sent to the server
    printf("read : %s\n",data_to_send);
    int len=sendto(sock, data_to_send, strlen(data_to_send)+1, 0,(struct sockaddr*)&server_address, sizeof(server_address));
    
    // prepare to receive
    
    int n = 0;
    int maxlen = 100;
    char buffer[maxlen];
    length=sizeof(struct sockaddr_in);
    //printf("Waiting for reply\n");
    // ready to receive back the reply from the server
    n = recvfrom(sock, buffer, len, 0, &from, &length);
    if(n<0){
        printf("Error in recvfrom");
    }
    buffer[n] = '\0';
    printf("received: '%s'\n", buffer);
    
    // close the socket
    close(sock);
    return 0;
}
