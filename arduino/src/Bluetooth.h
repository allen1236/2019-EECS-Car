#ifndef BLUETOOTH
#define BLUETOOTH

#include <SoftwareSerial.h>

#define Rx 0
#define Tx 1

#define SEND_RESPONSE

SoftwareSerial BT(Rx, Tx);

String msgRead;

//== function declaration ==============================

bool readMsg();     //read msg and return if there's a new msg

//== function definition ==============================

bool readMsg() {

    static String msgRead_buff = "";
    static char msgRead_char;

    if ( BT.available() ) {

        bool ter = false;

        while ( BT.available() ) {

            msgRead_char = (char) BT.read();
            if ( msgRead_char == '\n' ) {
                ter = true;
                msgRead = msgRead_buff;
                msgRead_buff = "";
                break;
            }
            msgRead_buff.concat( msgRead_char );
        }

        #ifdef SEND_RESPONSE
        if ( ter ) {
            BT.write( msgRead.c_str() );
            BT.write( '\n' );
        }
        #endif

        return ter;
    }

    return false;
    
}

#endif
