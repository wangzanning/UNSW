/*
 *
 *  TCPClient from Kurose and Ross
 *  * Compile: java TCPClient.java
 *  * Run: java TCPClient
 */
import java.io.*;
import java.net.*;

public class TCPClient {

	public static void main(String[] args) throws Exception {

		// Define socket parameters, address and Port No
		String serverName = "localhost";
		int serverPort = 6789; 
		//change above port number if required
		
		// create socket which connects to server
		Socket clientSocket = new Socket(serverName, serverPort);
/*This line creates the client’s socket, called clientSocket. The first parameter indicates the server address and the second parameter indicates the port number of the Server. In Java, this also initiates the TCP 3 way handshake*/
        
		// get input from keyboard
		String sentence;
		BufferedReader inFromUser =
			new BufferedReader(new InputStreamReader(System.in));
		sentence = inFromUser.readLine();

		// write to server
		DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
		outToServer.writeBytes(sentence + '\n');

		// create read stream and receive from server
		BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
		String sentenceFromServer;
		sentenceFromServer = inFromServer.readLine();

		// print output
		System.out.println("From Server: " + sentenceFromServer);

		// close client socket
		clientSocket.close();

	} // end of main

} // end of class TCPClient
