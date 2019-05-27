#ifndef CONTROL
#define CONTROL

bool command_loaded = false;

//== function declaration ==============================

void track();
void control();
void command();

//== function definition ==============================

void track() {
    BT.write( "track\n" );
    //TODO make sure it is receiving commands

    while( mode == mode_track ) {
        if ( readMsg() ) {
            switch( msgRead[0] ) {
                case 'p': mode = mode_control; break;
            }
        }
        sensors.update();
        if( sensors.reach_the_edge() ) {
            if ( msgRead == "" ) {
                setSpd( 0, 0 );
                motor();
                while( msgRead == "" ) {
                    readMsg();
                    delay( 10 * dt );
                }
            }
            mode = mode_command;
            BT.write( "reach\n" );
        }
        track_on_line();    
        motor();
        delay( dt );
    }
}
void control() {
    setSpd( 0, 0 );
    while( mode == mode_control ) {
        if ( readMsg() ) {
            switch( msgRead[0] ){

                case 'w': setSpd(255, 255); break;
                case 'a': setSpd(-255, 255); break; 
                case 's': setSpd(0, 0); break;
                case 'd': setSpd(255, -255); break;
                case 'x': setSpd(-255, -255); break;
                case 'r': 
                    for (int i = 0; i < 4; ++i) {
                        turn( -90 );
                        go( 5 );
                    }
                    setSpd( 0, 0 );
                    break;
                case 't': 
                    turn( 180 );
                    go( 5 );
                    turn( 180 );
                    go( 5 );
                    setSpd( 0, 0 );
                    break;
                case 'y':
                    for (int i = 0; i < 4; ++i) {
                        turn( 90 );
                        go( 5 );
                    }
                    setSpd( 0, 0 );
                    break;

                case 'o': 
                    mode = mode_track;
                    break;
                case 'i': 
                    mode = mode_track;
                    msgRead = "";
                    break;
            }
        }
        read_RFID();
        motor();
        delay( dt );
    }
}
void command() {
    BT.write( "run: " );
    BT.write( msgRead.c_str() );
    BT.write( '\n' );
    
    // execute shortcut cmd first
    if ( msgRead[0] == 'c' ) {

        if ( msgRead[1] == 'g' ) {
            go_and_get();
            msgRead.remove( 1 );
        }

        go( 20.0 );
        go_and_seek();

        if ( msgRead[1] == 'f' ) {
            if ( msgRead[2] == 'g' ) {
                bool get = false;
                for (int i = 0; i < 5; ++i) {
                    if ( ! get ) {
                        if ( read_RFID() ) get = true;
                    }
                }
                msgRead = "";
                mode = mode_track;
                return;
            }
            else {
                msgRead.remove( 0, 2 );
            }
        }
        else {
            go( 7 ); //TODO adjust the distance

            if ( msgRead[1] == 'r' ) turn( 90 );
            else turn( -90 );

            go( 4 );

            if ( msgRead[2] == 't' ) {
                sensors.update();
                if ( sensors.reach_the_edge() ) {
                    while( sensors.reach_the_edge() ) {
                        setSpd( -255, -255 );
                        motor();
                        delay( dt );
                        sensors.update();
                    }
                    go( -3 );
                }
                while ( ! sensors.reach_the_edge() ) {
                    track_on_line();    
                    motor();
                    delay( dt );
                    sensors.update();
                }
                msgRead.remove( 0, 3 );
            }
            else {          // execute normal get
                msgRead.remove( 0, 2 );
            }
        }
    }
   
    // if-else expression of cmds
    if ( msgRead == "nr" ) {
        smooth_turn( k_right );
    }
    else if ( msgRead == "nl" ) {
        smooth_turn( k_left );
    }
    else if ( msgRead == "nf") {
        go( 20.0 );
    }
    else if ( msgRead == "ng" ) {
        int i = 0;
        for (; i < 15; ++i) {
            if ( read_RFID() ) break;
            go( 1.0 );
        }
        go( - i );
        //turn( 120.0 );
        //turn_and_seek( 60.0 );
        turn( 180.0 );
    }
    else {
        BT.write( "cmd error, return to control mode\n" );
        msgRead = "";
        mode = mode_control;
        return;
    }
    msgRead = "";
    mode = mode_track;
}

#endif
