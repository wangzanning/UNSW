#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>


int main(int argc, char *argv[]) {
    // port to start the server on
    int SERVER_PORT = 1500;
    //change this port No if required
    
    // socket address used for the server
    struct sockaddr_in server_address;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    
    // htons: host to network short: transforms a value in host byte
    // ordering format to a short value in network byte ordering format
    server_address.sin_port = htons(SERVER_PORT);
    
    // htonl: host to network long: same as htons but to long
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    
    // create a UDP socket using SOCK_DGRAM, creation returns -1 on failure
    int sock;
    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        printf("could not create listen socket\n");
        return 1;
    }
    
    // bind it to listen to the incoming requests on the created server
    // address, will return -1 on error
    if ((bind(sock, (struct sockaddr *)&server_address,
              sizeof(server_address))) < 0) {
        printf("could not bind socket\n");
        return 1;
    }
    
    // socket address used to store client address
    struct sockaddr_in client_address;
    socklen_t client_address_len=sizeof(client_address);
    
    // run indefinitely
    while (true) {
        //prepare buffer
        int maxlen = 100;
        char buffer[maxlen];
        
        // read content into buffer from an incoming client
        int len = recvfrom(sock, buffer, sizeof(buffer), 0,
                           (struct sockaddr *)&client_address,
                           &client_address_len);
       buffer[len]='\0';
        int i = 0;
        printf("received: '%s' from client %s\n", buffer,
               inet_ntoa(client_address.sin_addr));
            //printf("received:'%s'\n", buffer);
        
        //change each character in string to Upper case
            for (i = 0; buffer[i]!='\0'; i++) {
                if(buffer[i] >= 'a' && buffer[i] <= 'z') {
                    buffer[i] = buffer[i] -32;
                }
            }
            printf("Modified: '%s'\n", buffer);
            // echo received content back
        // send same content back to the client ("echo")
        if(sendto(sock, buffer, len, 0, (struct sockaddr *)&client_address,
                  sizeof(client_address))<0){
            printf("nothing sent");
        }
        
    
    }
    return 0;
}
