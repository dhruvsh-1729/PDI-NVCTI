#include <SPI.h>
#include <SD.h>

File myFile;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
  SD.begin(10);
  myFile = SD.open("readings.txt");
  String data = myFile.readString();
  Serial.println(data);
  // close the file:
  myFile.close();
}

void loop() {
  // put your main code here, to run repeatedly:

}
