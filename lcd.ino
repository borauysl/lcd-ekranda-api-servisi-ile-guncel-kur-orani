#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  //lcd ekran özellikleri
unsigned long previousMillis = 0;
const long interval = 5000;  // 5 saniyede bir veri geçişi

String message1 = "";
String message2 = "";
bool showMessage1 = true;  // hangi mesajın gösterileceğini belirtir

void setup() {
  Serial.begin(9600);  // iletişim bilgisi
  lcd.init();  // lcd açma
  lcd.backlight();  // lcd arka ışığını açma
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readString();  // gelen veriyi okuma
    // gelen veriyi iki mesaja ayırma 
    int separatorIndex = data.indexOf(',');
    message1 = data.substring(0, separatorIndex);  
    message2 = data.substring(separatorIndex + 1);  
  }

  // zamanlayıcı ile mesaj geçişi
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    showMessage1 = !showMessage1;  // mesajlar arasında geçiş yap
    lcd.clear();  // ekranı sadece mesaj değişirken temizle
  }

  if (showMessage1) {
    int separatorIndex = message1.indexOf('|');
    String euroRate = message1.substring(0, separatorIndex);  
    String usdRate = message1.substring(separatorIndex + 1);  

    lcd.setCursor(0, 0);  
    lcd.print(euroRate);
    
    lcd.setCursor(0, 1);  
    lcd.print(usdRate);
  } else {
    int separatorIndex = message2.indexOf('|');
    String gbpRate = message2.substring(0, separatorIndex);  
    String chfRate = message2.substring(separatorIndex + 1);  

    lcd.setCursor(0, 0);  
    lcd.print(gbpRate);
    
    lcd.setCursor(0, 1);  
    lcd.print(chfRate);
  }
}