
/* 
 * ##### requires modified 
 *
 * 5.9222222 steps per degree.
 * too much error.
 * 
 */

#include <Stepper.h>
#define MIN_MILLIS_PER_STEP 3
#define STEPPER_STEPS 200
#define STEPS_PER_REVOLUTION 2132                                    // for your motor
#define INBUFFERLENGTH 100
char inbuffer[INBUFFERLENGTH];
int bufferIndex;
int yellowGoal=0;
int blueGoal=0;
int yellowPosition=0;
int bluePosition=0;
int stepCount = 0;         // number of steps the motor has taken
long int lastStepMillis;

Stepper blue(STEPPER_STEPS, 8,9,10,11,1);            
Stepper yellow(STEPPER_STEPS, 2,3,4,5,1);            

void setup() {
  // initialize the serial port:
  Serial.begin(115200);
}

void loop() {
  int target;
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    if (bufferIndex<INBUFFERLENGTH)
      inbuffer[bufferIndex++]=inChar;
    if (inChar == '\n') {
      inbuffer[bufferIndex]=0;
      if ((inbuffer[0]=='d') && bufferIndex>3) {
        target=atoi(inbuffer+3);
        if (target>STEPS_PER_REVOLUTION)target=STEPS_PER_REVOLUTION;
        if (inbuffer[1]=='1') {
          blueGoal=target;//analogWrite(MOTOR1PWM,bike1speed);
          Serial.println(inbuffer+3);
          Serial.print("blueGoal="); Serial.println(blueGoal);
          Serial.print("bluePosition="); Serial.println(bluePosition);
        } else {
          yellowGoal=target;//analogWrite(MOTOR2PWM,bike1speed);
        } 
      } else if (inbuffer[0]=='v') {
        Serial.println("RaceClock 0.1");
        Serial.flush();
      } else if (inbuffer[0]=='s') {
        blueGoal=yellowGoal=STEPS_PER_REVOLUTION;
      }

      bufferIndex=0; //reset input

    }
  }
  if ((millis()-lastStepMillis)>MIN_MILLIS_PER_STEP){ 
      if ((blueGoal>bluePosition) && (bluePosition<=STEPS_PER_REVOLUTION)){
        blue.step(-1);
        bluePosition++;
      }

      if ((yellowGoal>yellowPosition) && (yellowPosition<=STEPS_PER_REVOLUTION)) {
        yellow.step(-1);
        yellowPosition++;
      }
      lastStepMillis=millis();
    }
   if ((bluePosition==STEPS_PER_REVOLUTION)&&(blueGoal==bluePosition)){
       blueGoal=bluePosition=0;
   }
   if ((yellowPosition==STEPS_PER_REVOLUTION)&&(yellowGoal==yellowPosition)){
       yellowGoal=yellowPosition=0;
   }
   
}


