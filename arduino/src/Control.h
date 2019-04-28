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
    //TODO
    BT.write( "run cmd: " );
    BT.write( msgRead.c_str() );
    BT.write( '\n' );
    if ( msgRead == "sr" ) smooth_turn( k_right ); 
    else if ( msgRead == "sl" ) smooth_turn( k_left );
    else {
        mode = mode_control;
        run_command_after_track = false;
    }
}

#endif
