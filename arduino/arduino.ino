#define dt 5
unsigned int counter = 0;

enum Mode {
    mode_control,
    mode_command,
    mode_track
} mode = mode_control;

#include "src/Bluetooth.h"
#include "src/Sensor.h"
#include "src/Motor.h"
#include "src/RFID.h"
#include "src/Control.h"

//== setup and main loop ==============================

void setup() {
    BT.begin(9600);

    pinMode(ENA, OUTPUT);
    pinMode(ENB, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);

    pinMode(L2, INPUT);
    pinMode(L1, INPUT);
    pinMode(M0, INPUT);
    pinMode(R1, INPUT);
    pinMode(R2, INPUT);

    SPI.begin();
    mfrc522 = new MFRC522(SS_PIN, RST_PIN);
    mfrc522 -> PCD_Init();
}
void loop() {
    switch( mode ) {
        case mode_track:
            track();
            break;
        case mode_command:
            command();
            break;
        case mode_control:
            control();
            break;
    }
}
