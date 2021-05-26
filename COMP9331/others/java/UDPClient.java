/*
 *
 *  UDPClient
 *  * Compile: java UDPClient.java
 *  * Run: java UDPClient
 */
import java.io.*;
import java.net.*;

public class UDPClient {

	public static void main(String[] args) throws Exception {

		// Define socket parameters, address and Port No
        InetAddress IPAddress = InetAddress.getByName("localhost");
		int serverPort = 6789; 
		//change above port number if required
		
		// create socket which connects to server
		DatagramSocket clientSocket = new DatagramSocket();
/*This line creates the client’s socket, called clientSocket. DatagramSocket indicates that we are using UDP*/
        
		// get input from keyboard
		String sentence;
		BufferedReader inFromUser =
			new BufferedReader(new InputStreamReader(System.in));
		sentence = inFromUser.readLine();
        //prepare for sending
        byte[] sendData=new byte[1024];
        sendData=sentence.getBytes();
		// write to server, need to create DatagramPAcket with server address and port No
        DatagramPacket sendPacket=new DatagramPacket(sendData,sendData.length,IPAddress,serverPort);
        //actual send call
        clientSocket.send(sendPacket);
        
        //prepare buffer to receive reply
        byte[] receiveData=new byte[1024];
		// receive from server
        DatagramPacket receivePacket = new DatagramPacket(receiveData,receiveData.length);
        clientSocket.receive(receivePacket);
        
        String modifiedSentence = new String(receivePacket.getData());
        System.out.println("FROM SERVER:" + modifiedSentence);
        //close the scoket
        clientSocket.close();
		
	} // end of main

} // end of class UDPClient
