#ifndef SENSOR
#define SENSOR

#define L2 A4
#define L1 A3
#define M0 A2
#define R1 A1
#define R2 A0
 
//== function declaration ==============================

class Sensors{
    private:
        bool _sensor[5];
        int _center;
        int _width;
        void update_array();
    public:
        void update();
        int get_center() { return _center; }
        int get_width() { return _width; }
        bool reach_the_edge() { return ( _width == 5 ); }
        bool out_of_range() { return ( _width == 0 ); }
};

Sensors sensors;

//== function difinition ==============================

void Sensors::update_array() {
    _sensor[0] = analogRead(L2) < 700 ? false : true;
    _sensor[1] = analogRead(L1) < 700 ? false : true;
    _sensor[2] = analogRead(M0) < 700 ? false : true;
    _sensor[3] = analogRead(R1) < 700 ? false : true;
    _sensor[4] = analogRead(R2) < 700 ? false : true;
}
void Sensors::update() { 
    update_array();

    bool line_start = false;
    int line_pos = 0;
    int last_line_pos = 4;

    for (int i = 0; i < 5; ++i) {
        if( !line_start ) {
            if( _sensor[i] ) {
                line_start = true;
                line_pos = i;
            }
        }
        else {
            if( !_sensor[i] ) {
                last_line_pos = i-1;
                break;
            }
        }
    }
    if( line_start ) {
         _center = ( line_pos + last_line_pos ) - 4;
         _width = last_line_pos - line_pos + 1;
    }
    else {
        _center = 0;
        _width = 0;
    }
}

#endif
