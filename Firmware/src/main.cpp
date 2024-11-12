/// \file		main.cpp
///
/// \brief	
///
/// \author		Uriel Abe Contardi (urielcontardi@hotmail.com)
/// \date		09-11-2024
///
/// \version	1.0
///
/// \note		Revisions:
/// 			09-11-2024 <urielcontardi@hotmail.com>
/// 			First revision.
//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                               INCLUDES                                   //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////
#include <Arduino.h>
#include "AccelStepper.h"

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                           DEFINES AND MACROS                             //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////

// Define pin connections & motor settings
#define DIR_PIN 2
#define STEP_PIN 3
#define REED_PIN 12
#define DEFAULT_SPEED 500 // Default speed in steps per second
#define DEFAULT_ACCELERATION 5000 // Default acceleration in steps per second squared
#define DEFAULT_DISTANCE 200 // Default distance in steps
#define DEFAULT_TIME 5000 // Default time in milliseconds
#define MAX_DISTANCE 3500

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                      LOCAL TYPEDEFS AND STRUCTURES                       //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                        LOCAL FUNCTIONS PROTOTYPES                        //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////
void runMotor();
void resetMotor();

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                      STATIC VARIABLES AND CONSTANTS                      //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

// Variables for configuration
int motorSpeed = DEFAULT_SPEED;
int motorSpeed2 = DEFAULT_SPEED;
int motorDistance = DEFAULT_DISTANCE;
int motorTime = DEFAULT_TIME;

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                            MAIN FUNCTIONS                                //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////
void setup() {
    // Set reed switch as input with pull-up resistor
    pinMode(REED_PIN, INPUT_PULLUP);

    // Initialize Serial for receiving commands
    Serial.begin(9600);

    // Init App
    Serial.println("Aplicação Iniciada");
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');

        // Parse commands for SPEED, DISTANCE, and TIME
        if (command.startsWith("SPEED ")) {
            motorSpeed = command.substring(6).toInt();
            Serial.print("Motor speed set to: ");
            Serial.println(motorSpeed);
        }
        else if (command.startsWith("SPEED2 ")) {
            motorSpeed2 = command.substring(7).toInt();
            Serial.print("Motor speed2 set to: ");
            Serial.println(motorSpeed2);
        } 
        else if (command.startsWith("DISTANCE ")) {
            motorDistance = command.substring(9).toInt();
            if (motorDistance > MAX_DISTANCE) motorDistance = MAX_DISTANCE;
            Serial.print("Motor distance set to: ");
            Serial.println(motorDistance);
        } 
        else if (command.startsWith("TIME ")) {
            motorTime = command.substring(5).toInt();
            Serial.print("Motor time set to: ");
            Serial.println(motorTime);
        } 
        else if (command == "RUN") {
            Serial.println("RUNNING");
            runMotor();
        } 
        else if (command == "RESET") {
            Serial.println("RESET");
            resetMotor();
        }
    }
}

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//                              LOCAL FUNCTIONS                             //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////

// Function to initialize the motor by moving until the reed switch is triggered
void resetMotor() {
    // Move slowly until reed switch is triggered
    stepper.setAcceleration(DEFAULT_ACCELERATION);
    stepper.setSpeed(-DEFAULT_SPEED);
    stepper.setMaxSpeed(-DEFAULT_SPEED);

    Serial.println("Encontrando Fim de Curso...");
    while (digitalRead(REED_PIN) != LOW) {
        stepper.runSpeed(); // Keep stepping until reed switch is triggered
    }
    Serial.println("Encontrado!");
    
    // Stop motor
    stepper.stop();
}

// Function to run the motor based on configured settings and then return to INIT state
void runMotor() {
    // Set direction and target position
    stepper.setMaxSpeed(motorSpeed);
    stepper.setSpeed(motorSpeed);
    stepper.setAcceleration(DEFAULT_ACCELERATION);
    stepper.moveTo(motorDistance);

    // Move motor to target position with set speed
    while (stepper.distanceToGo() != 0) {
        stepper.run();
    }

    // Wait for the configured time
    delay(motorTime);

    // Go to end state
    stepper.setSpeed(motorSpeed2);
    int resto = MAX_DISTANCE - motorDistance;
    stepper.moveTo(resto);

    // Move motor to target position with set speed
    while (stepper.distanceToGo() != 0) {
        stepper.run();
    }
}