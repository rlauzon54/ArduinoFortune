#include <SPI.h>
#include <SD.h>
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_TFTLCD.h> // Hardware-specific library
#include <TouchScreen.h>

// The control pins for the LCD can be assigned to any digital or
// analog pins...but we'll use the analog pins as this allows us to
// double up the pins with the touch screen (see the TFT paint example).
#define LCD_CS A3 // Chip Select goes to Analog 3
#define LCD_CD A2 // Command/Data goes to Analog 2
#define LCD_WR A1 // LCD Write goes to Analog 1
#define LCD_RD A0 // LCD Read goes to Analog 0

#define LCD_RESET A4 // Can alternately just connect to Arduino's reset pin

Adafruit_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);

#define YP A3  // must be an analog pin, use "An" notation!
#define XM A2  // must be an analog pin, use "An" notation!
#define YM 9   // can be a digital pin
#define XP 8   // can be a digital pin
TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);

File myFile;
char fortune_file_name[20];
long file_num;
byte char_in;
int directory_num;

#define NUM_FILES 13071

void setup()
{
  Serial.begin(9600);
  Serial.print("Initializing SD card...");
  // On the Ethernet Shield, CS is pin 4. It's set as an output by default.
  // Note that even if it's not used as the CS pin, the hardware SS pin 
  // (10 on most Arduino boards, 53 on the Mega) must be left as an output 
  // or the SD library functions will not work. 
  pinMode(10, OUTPUT);
  pinMode(13, OUTPUT); // For the touch screen
    
  if (!SD.begin(10)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");

  // Initial display
  tft.reset();
  tft.begin(0x9341);
  //Serial.print("TFT size is "); Serial.print(tft.width()); Serial.print("x"); Serial.println(tft.height());
  tft.setRotation(1);
  tft.fillScreen(0x0000);  // Black
  tft.setTextSize(1);

  randomSeed(analogRead(1));

  tft.fillScreen(0x0000);  // Black
  tft.setCursor(0, 0);
  tft.setTextColor(0xF800); // Red

  ReadFortuneFile();
}


void ReadFortuneFile() {
  file_num = random(NUM_FILES);
  directory_num=int(file_num/255);
  
  sprintf(fortune_file_name,"f%03d/%05d.txt",directory_num,file_num);

  // Open the file for reading:
  myFile = SD.open(fortune_file_name,FILE_READ);
  if (myFile) {
    // read from the file until there's nothing else in it:
    while (myFile.available()) {
      char_in = myFile.read();

      tft.print((char)char_in);
    }
      
    // close the file:
    myFile.close();
  } else {
    // if the file didn't open, print an error:
    tft.println("error opening fortune file");
    tft.println(fortune_file_name);
    Serial.print("error opening ");
    Serial.println(fortune_file_name);
  }
}

#define MINPRESSURE 10
#define MAXPRESSURE 1000

void loop()
{
  // Read the touch screen
  digitalWrite(13, HIGH);
  TSPoint p = ts.getPoint();
  digitalWrite(13, LOW);

  // The touch screen uses the same pins as the LCD, so we need to do this
  pinMode(XM, OUTPUT);
  pinMode(YP, OUTPUT);

  // If someone touched the screen
  if (p.z > MINPRESSURE && p.z < MAXPRESSURE) {
    tft.fillScreen(0x0000);  // Black
    tft.setCursor(0, 0);
    tft.setTextColor(0xF800); // Red
    ReadFortuneFile();
  }

  // Mix up the random numbers more
  random(NUM_FILES);
}
