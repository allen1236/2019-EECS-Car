#ifndef MOTOR
#define MOTOR

#define ENA 5
#define ENB 6
#define IN1 8
#define IN2 7
#define IN3 4
#define IN4 2

#define SCALE_VR 1
#define SCALE_VL 0.9

int vl = 0, vr = 0;
float dps = 210.0;
float dpms = dps / 1000;
float cmps = 20.0;
float cmpms = cmps / 1000;

enum Keyword {
    k_right,
    k_left
};


//== function declaration ==============================

void setSpd( int _vl, int _vr );
void motor();

// a complete loop that finish after
// the sensors have reach the center
void track_step_in();   
// just set the speed
void track_on_line();

void smooth_turn();
void turn( float _degree );
void go( float _distance );

//== function definition ==============================

void setSpd( int _vl, int _vr ) {
    vl = _vl * SCALE_VL;
    vr = _vr * SCALE_VR;
}
void motor() {
    analogWrite(ENA, vr>0?vr:-vr);
    analogWrite(ENB, vl>0?vl:-vl);
    digitalWrite(IN1, vl>=0?LOW:HIGH);
    digitalWrite(IN2, vl>=0?HIGH:LOW);
    digitalWrite(IN3, vr>=0?HIGH:LOW);
    digitalWrite(IN4, vr>=0?LOW:HIGH);
}
void track_step_in() {
    //TODO
    do {
        setSpd( 255, 255 );
        motor();
        delay( dt );
        sensors.update();
    } while ( sensors.get_center() != 0 );
}
void track_on_line() {
    if ( sensors.out_of_range() ) {
        setSpd( -255, -255 );
        return;
    }

    //TODO PID control

    int _vl = 255, _vr = 255;
    int line_pos = sensors.get_center();
    if( line_pos > 0 ) {
        _vr *= ( 2 - line_pos ) / 2.0;
        _vl *= ( 6 - line_pos ) / 6.0; 
    }
    else if( line_pos < 0 ) {
        _vl *= ( 2 - ( -line_pos ) ) / 2.0;
        _vr *= ( 6 - ( -line_pos ) ) / 6.0;
    }
    setSpd( _vl, _vr );
}
void smooth_turn( Keyword k ) {
    int t = 0;
    int ter = 25.0 / cmpms;
    int _vl, _vr;
    if ( k == k_left ) {
        _vl = 50;
        _vr = 255;
    } else {
        _vl = 255;
        _vr = 50;
    }
    while( t < ter ) {
        setSpd( _vl, _vr );
        motor();
        delay( dt );
        t += dt;
    }
}
void turn( float _degree ) {
    int _vl = 255, _vr = -255;
    if ( _degree < 0 ) {
        _vl = -255;
        _vr = 255;
        _degree = - _degree;
    }
    int t = 0;
    int ter = _degree / dpms;
    while( t < ter ) {
        setSpd( _vl, _vr );
        motor();
        delay( dt );
        t += dt;
    }
}
void go( float _distance ) {
    int _vl = 255, _vr = 255;
    if( _distance < 0 ) {
        _vl = _vr = -255;
        _distance = - _distance;
    }
    int t = 0;
    int ter = _distance / cmpms;
    while( t < ter ) {
        setSpd( _vl, _vr );
        motor();
        delay( dt );
        t += dt;
    }
}

#endif
