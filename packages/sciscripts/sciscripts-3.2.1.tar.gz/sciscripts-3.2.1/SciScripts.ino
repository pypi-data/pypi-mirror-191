/*
@author: T. Malfatti <malfatti@disroot.org>
@date: 2018-06-06
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

Serial-controlled TTL generator. Useful for triggering recordings and/or
devices.

    A = Pulse on Pins[0] with duration set in line 30 as `Delay`
    B = Pulse on Pins[1] with duration set in line 30 as `Delay`
    C = Pulse on Pins[2] with duration set in line 30 as `Delay`
    D = Pulse on Pins[3] with duration set in line 30 as `Delay`
    E = Pulse on Pins[4] with duration set in line 30 as `Delay`
    F = Pulse on Pins[5] with duration set in line 30 as `Delay`
    G = Pulse on Pins[6] with duration set in line 30 as `Delay`
    P = Pulse on Pins[7] with duration set in line 30 as `Delay`
  
    a = Keeps Pins[0] high until z is received
    b = Keeps Pins[1] high until y is received
    c = Keeps Pins[2] high until x is received
    d = Keeps Pins[3] high until w is received
    e = Keeps Pins[4] high until v is received
    f = Keeps Pins[5] high until u is received
    g = Keeps Pins[6] high until t is received
    p = Keeps Pins[7] high until s is received
  
    T = Custom protocol (User playground :) )
*/

const int PinNo = 8;
const int Pins[PinNo] = {2, 4, 7, 8, 10, 11, 12, 13};
const int Delay = 10;

void setup() {
  Serial.begin(115200);

  for (int Pin = 0; Pin < PinNo; Pin++) {
    pinMode(Pins[Pin], OUTPUT);
    digitalWrite(Pins[Pin], LOW);
  }

  char ch = 0;
  int inPinV = 0;
}

void loop() {
  char ch = 0;
  int inPinV = 0;

  while (ch == 0) { ch = Serial.read(); }

  if (ch == 'A') {
    digitalWrite(Pins[0], HIGH);
    delay(Delay);
    digitalWrite(Pins[0], LOW);
  }

  if (ch == 'a') {
    digitalWrite(Pins[0], HIGH);
    while (ch != 'z') {
      ch = Serial.read();
    }
    digitalWrite(Pins[0], LOW);
  }


  if (ch == 'B') {
    digitalWrite(Pins[1], HIGH);
    delay(Delay);
    digitalWrite(Pins[1], LOW);
  }

  if (ch == 'b') {
    digitalWrite(Pins[1], HIGH);
    while (ch != 'y') {
      ch = Serial.read();
    }
    digitalWrite(Pins[1], LOW);
  }

  if (ch == 'C') {
    digitalWrite(Pins[2], HIGH);
    delay(Delay);
    digitalWrite(Pins[2], LOW);
  }

  if (ch == 'c') {
    digitalWrite(Pins[2], HIGH);
    while (ch != 'x') {
      ch = Serial.read();
    }
    digitalWrite(Pins[2], LOW);
  }

  if (ch == 'D') {
    digitalWrite(Pins[3], HIGH);
    delay(Delay);
    digitalWrite(Pins[3], LOW);
  }

  if (ch == 'd') {
    digitalWrite(Pins[3], HIGH);
    while (ch != 'w') {
      ch = Serial.read();
    }
    digitalWrite(Pins[3], LOW);
  }

  if (ch == 'E') {
    digitalWrite(Pins[4], HIGH);
    delay(Delay);
    digitalWrite(Pins[4], LOW);
  }

  if (ch == 'e') {
    digitalWrite(Pins[4], HIGH);
    while (ch != 'v') {
      ch = Serial.read();
    }
    digitalWrite(Pins[4], LOW);
  }

  if (ch == 'F') {
    digitalWrite(Pins[5], HIGH);
    delay(Delay);
    digitalWrite(Pins[5], LOW);
  }

  if (ch == 'f') {
    digitalWrite(Pins[5], HIGH);
    while (ch != 'u') {
      ch = Serial.read();
    }
    digitalWrite(Pins[5], LOW);
  }

  if (ch == 'G') {
    digitalWrite(Pins[6], HIGH);
    delay(Delay);
    digitalWrite(Pins[6], LOW);
  }

  if (ch == 'g') {
    digitalWrite(Pins[6], HIGH);
    while (ch != 't') {
      ch = Serial.read();
    }
    digitalWrite(Pins[6], LOW);
  }

  if (ch == 'P') {
    digitalWrite(Pins[7], HIGH);
    delay(Delay);
    digitalWrite(Pins[7], LOW);
  }

  if (ch == 'p') {
    digitalWrite(Pins[7], HIGH);
    while (ch != 's') {
      ch = Serial.read();
    }
    digitalWrite(Pins[7], LOW);
  }

  if (ch == 'T') {
    delay(Delay);

    while (true) {
      for (int Pulse = 0; Pulse < 10; Pulse++) {
        digitalWrite(Pins[7], HIGH); delay(15); 
        digitalWrite(Pins[7], LOW); delay(85);
      }
      
      digitalWrite(Pins[7], HIGH); delay(5000); 
      digitalWrite(Pins[7], LOW);
      delay(15000);
    }
  }
}

