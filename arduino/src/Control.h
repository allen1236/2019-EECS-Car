#ifndef CONTROL
#define CONTROL

bool run_command_after_track = false;
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
            if ( run_command_after_track ) {
                //TODO verify the command
                mode = mode_command;
                BT.write( "reach\n" );
            }
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

                case 'o': 
                    mode = mode_track;
                    run_command_after_track = false;
                    break;
                case 'i': 
                    mode = mode_track;
                    run_command_after_track = true;
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
        go( 5.0 );
        int i = 0
        for (; i < 10; ++i) {
            if ( read_RFID() ) break;
            go( 1.0 )
        }
        go( -5.0 - i );
        turn( 120.0 );
        turn_and_seek( 60.0 );
    }
    else if ( msgRead == "test" ) {
        go( 200 );
    }
    else if ( msgRead[0] == 'c' ) {     //shortcut

    }
    else {
        BT.write( "cmd error, return to control mode\n" );
        mode = mode_control;
        run_command_after_track = false;
        return;
    }
    mode = mode_track;
}

#endif
