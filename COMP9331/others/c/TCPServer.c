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
    
    // create a TCP socket (using SOCK_STREAM), creation returns -1 on failure
    int listen_sock;
    if ((listen_sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("could not create listen socket\n");
        return 1;
    }
    
    // bind it to listen to the incoming connections on the created server
    // address, will return -1 on error
    if ((bind(listen_sock, (struct sockaddr *)&server_address,
              sizeof(server_address))) < 0) {
        printf("could not bind socket\n");
        return 1;
    }
    
    int wait_size = 5;  // maximum number of waiting clients
    if (listen(listen_sock, wait_size) < 0) {
        printf("could not open socket for listening\n");
        return 1;
    }
    
    // socket address used to store client address
    struct sockaddr_in client_address;
    socklen_t client_address_len=sizeof(client_address);
    
    // run indefinitely
    while (true) {
        // open a new socket to transmit data per connection
        //different from listen_sock
        int sock;
        if ((sock =
             accept(listen_sock, (struct sockaddr *)&client_address,
                    &client_address_len)) < 0) {
                 printf("could not open a socket to accept data\n");
                 return 1;
             }
        //prepare to receive
        int n = 0;
        int len = 0, maxlen = 100;
        char buffer[maxlen];
        char *pbuffer = buffer;
        
        printf("client connected with ip address: %s\n",
               inet_ntoa(client_address.sin_addr));
        
        while ((n = recv(sock, pbuffer, maxlen, 0)) > 0) {
            pbuffer += n;
            maxlen -= n;
            len += n;
            int i = 0;
            
            printf("received:'%s'\n", buffer);
            
            //change each character in string to Upper case
            for (i = 0; buffer[i]!='\0'; i++) {
                if(buffer[i] >= 'a' && buffer[i] <= 'z') {
                    buffer[i] = buffer[i] -32;
                }
            }
            printf("Modified: '%s'\n", buffer);
            // echo received content back
            send(sock, buffer, len, 0);
        }
        //close client specific socket
        close(sock);
    }
    //close listening socket
    close(listen_sock);
    return 0;
}
