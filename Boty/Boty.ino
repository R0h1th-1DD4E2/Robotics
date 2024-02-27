#include <ESP8266WiFi.h> // Include the ESP8266WiFi library to connect to the internet
#include <WiFiUdp.h> // Include the WiFiUdp library to send and receive UDP packets
#include <Arduino.h> // Include the Arduino library to use the Arduino functions
#include "DataParser.h" // Include the DataParser library to parse the CSV data

const char* ssid = "Redmi Note 11"; // The name of the WiFi network you want to connect to
const char* password = "01030507"; // The password of the WiFi network

DataParser dataParser; // Create an instance of DataParse

const int udpPort = 8080; // Change this to the desired UDP port

int in1u = 5; // Up Left 
int in2u = 4; 
int enau = 2; 
int in3u = 14; // Up Right 
int in4u = 12; 
int enbu = 13; 

// int in1d = 3; // Bottom Right
// int in2d = 15; 
// int enad = 1; 
// int in3d = 10; // Bottom Left
// int in4d = 11; 
// int enbd = 9; 

int left_top_speed = 0;
int left_bottom_speed = 0;
int right_top_speed = 0;
int right_bottom_speed = 0;

String Command;

WiFiUDP udp; // Create an instance of WiFiUDP

void setup() {
  Serial.begin(115200);

  pinMode(in1u, OUTPUT); 
  pinMode(in2u, OUTPUT); 
  pinMode(enau, OUTPUT);
  pinMode(in3u, OUTPUT);
  pinMode(in4u, OUTPUT);
  pinMode(enbu, OUTPUT);

  // pinMode(in1d, OUTPUT); 
  // pinMode(in2d, OUTPUT); 
  // pinMode(enad, OUTPUT);
  // pinMode(in3d, OUTPUT);
  // pinMode(in4d, OUTPUT);
  // pinMode(enbd, OUTPUT);


  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) { 
    delay(1000); 
    Serial.println("Connecting to WiFi..."); 
  }
  
  Serial.println("Connected to WiFi");

  udp.begin(udpPort); // Start listening on the UDP port

  Serial.print("UDP Listening on IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Check for incoming UDP packets
  int packetSize = udp.parsePacket();
  if (packetSize) {
    // Received UDP packet
    char packetBuffer[255]; // Adjust the buffer size accordingly
    int len = udp.read(packetBuffer, 255);
    if (len > 0) {
      packetBuffer[len] = 0;
      Serial.print("Received packet: ");
      Serial.println(packetBuffer);
      // Parse the CSV data into separate command arrays
      String IncomingData = packetBuffer; // Convert the packet data to a string and store it in a variable
      dataParser.parseData(IncomingData, ','); //Pass data and delimiter 

      // Extract the Movement command
      Command = dataParser.getField(0);

      // Extract the speed value
      left_top_speed = (dataParser.getField(1)).toInt();
      left_bottom_speed = (dataParser.getField(2)).toInt();
      // right_top_speed = (dataParser.getField(3)).toInt();
      // right_bottom_speed = (dataParser.getField(4)).toInt();
      
    }
  }


  move(Command,left_top_speed,left_bottom_speed,right_top_speed,right_bottom_speed);
}

void move(String command, int left_top_speed, int left_bottom_speed, int right_top_speed , int right_bottom_speed){
  
  analogWrite(enau, left_top_speed);
  analogWrite(enbu, right_top_speed); 
  // analogWrite(enbd, left_bottom_speed);
  // analogWrite(enad, right_bottom_speed);
  
  if (strcmp(command.c_str(), "FWD") == 0) {
    digitalWrite(in1u, HIGH); // Set the in1 pin to HIGH
    digitalWrite(in2u, LOW); // Set the in2 pin to LOW
    digitalWrite(in3u, HIGH); // Set the in3 pin to HIGH
    digitalWrite(in4u, LOW); // Set the in4 pin to LOW

    // digitalWrite(in1d, HIGH); // Set the in1 pin to HIGH
    // digitalWrite(in2d, LOW); // Set the in2 pin to LOW
    // digitalWrite(in3d, HIGH); // Set the in3 pin to HIGH
    // digitalWrite(in4d, LOW); // Set the in4 pin to LOW
  }

  else if (strcmp(command.c_str(), "BWD") == 0) {
    digitalWrite(in1u, LOW); // Set the in1 pin to LOW
    digitalWrite(in2u, HIGH); // Set the in2 pin to HIGH
    digitalWrite(in3u, LOW); // Set the in3 pin to LOW
    digitalWrite(in4u, HIGH); // Set the in4 pin to HIGH

    // digitalWrite(in1d, LOW); // Set the in1 pin to LOW
    // digitalWrite(in2d, HIGH); // Set the in2 pin to HIGH
    // digitalWrite(in3d, LOW); // Set the in3 pin to LOW
    // digitalWrite(in4d, HIGH); // Set the in4 pin to HIGH
  }

  else if (strcmp(command.c_str(), "RT") == 0) {
    digitalWrite(in1u, LOW); // Set the in1 pin to LOW
    digitalWrite(in2u, HIGH); // Set the in2 pin to HIGH
    digitalWrite(in3u, HIGH); // Set the in3 pin to HIGH
    digitalWrite(in4u, LOW); // Set the in4 pin to LOW

    // digitalWrite(in1d, HIGH); // Set the in1 pin to LOW
    // digitalWrite(in2d, LOW); // Set the in2 pin to HIGH
    // digitalWrite(in3d, LOW); // Set the in3 pin to HIGH
    // digitalWrite(in4d, HIGH); // Set the in4 pin to LOW
  }

  else if (strcmp(command.c_str(), "LT") == 0) {
    digitalWrite(in1u, HIGH); // Set the in1 pin to HIGH
    digitalWrite(in2u, LOW); // Set the in2 pin to LOW
    digitalWrite(in3u, LOW); // Set the in3 pin to LOW
    digitalWrite(in4u, HIGH); // Set the in4 pin to HIGH

    // digitalWrite(in1d, LOW); // Set the in1 pin to HIGH
    // digitalWrite(in2d, HIGH); // Set the in2 pin to LOW
    // digitalWrite(in3d, HIGH); // Set the in3 pin to LOW
    // digitalWrite(in4d, LOW); // Set the in4 pin to HIGH
  }

  else if (strcmp(command.c_str(), "STP") == 0) {
    digitalWrite(in1u, LOW); // Set the in1 pin to LOW
    digitalWrite(in2u, LOW); // Set the in2 pin to LOW
    digitalWrite(in3u, LOW); // Set the in3 pin to LOW
    digitalWrite(in4u, LOW); // Set the in4 pin to LOW

    // digitalWrite(in1d, LOW); // Set the in1 pin to LOW
    // digitalWrite(in2d, LOW); // Set the in2 pin to LOW
    // digitalWrite(in3d, LOW); // Set the in3 pin to LOW
    // digitalWrite(in4d, LOW); // Set the in4 pin to LOW
  }

  else {
    //Serial.println("Unkown Command");
  }
}