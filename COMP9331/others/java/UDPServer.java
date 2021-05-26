/*
 *
 * UDPServer
 * Compile: javac UDPServer.java
 * Run: java UDPServer
 */

import java.io.*;
import java.net.*;

public class UDPServer {

	public static void main(String[] args)throws Exception {
        /* define socket parameters, Address + PortNo, Address will default to localhost */
		int serverPort = 6789; 
		/* change above port number if required */
		
		/*create server socket that is assigned the serverPort (6789)
        We will listen on this port for requests from clients
         DatagramSocket specifies that we are using UDP */
		DatagramSocket serverSocket = new DatagramSocket(serverPort);
        System.out.println("Server is ready :");
        
        //prepare buffers
        byte[] receiveData = new byte[1024];
        byte[] sendData = new byte[1024];
		
        while (true){
            //receive UDP datagram
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
            serverSocket.receive(receivePacket);
            
            //get data
            String sentence = new String( receivePacket.getData());
            System.out.println("RECEIVED: " + sentence);
            
            //get info of the client with whom we are communicating
            InetAddress IPAddress = receivePacket.getAddress();
            int port = receivePacket.getPort();
            
            //change case of message received
            String capitalizedSentence = sentence.toUpperCase();
            
            //prepare to send it back
            sendData = capitalizedSentence.getBytes();
            
            //send it back to client
            DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, port);
            serverSocket.send(sendPacket);
            
		} // end of while (true)

	} // end of main()

} // end of class UDPServer
