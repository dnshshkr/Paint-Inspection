#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

unsigned long previousTime = 0;
//unsigned long currentTime = 0;
float elapsedTime = 0;

int16_t aX, aY, aZ;
float accelX = 0;
float accelY = 0;
float accelZ = 0;

float velocityX = 0;
float velocityY = 0;
float velocityZ = 0;

float displacementX = 0;
float displacementY = 0;
float displacementZ = 0;

int16_t gX, gY, gZ;
float roll = 0;
float pitch = 0;
float yaw = 0;

float x = 0;
float y = 0;
float z = 0;

void setup() {
  Serial.begin(38400);

  Wire.begin();
  mpu.initialize();
  mpu.setDLPFMode(0);
  mpu.setFullScaleGyroRange(3);
  mpu.setFullScaleAccelRange(3);
}

void loop() {
  previousTime = millis();

  mpu.getAcceleration(&aX, &aY, &aZ);
  mpu.getRotation(&gX, &gY, &gZ);

  //currentTime = millis();
  elapsedTime = (float)(millis() - previousTime) / 1000.0;
  accelX = (float)aX;
  accelY = (float)aY;
  accelZ = (float)aZ;
  roll = (float)gX;
  pitch = (float)gY;
  yaw = (float)gZ;

  Serial.print("ax:"); Serial.print(accelX); Serial.print(',');
  Serial.print("ay:"); Serial.print(accelY); Serial.print(',');
  Serial.print("az:"); Serial.print(accelZ); Serial.println();
  // Convert accelerometer data to g's
  //  accelX = accelX / 16384.0;
  //  accelY = accelY / 16384.0;
  //  accelZ = accelZ / 16384.0;

  // Convert roll, pitch, and yaw to radians
  roll = roll * (PI / 180);
  pitch = pitch * (PI / 180);
  yaw = yaw * (PI / 180);
  // Calculate the acceleration in the x, y, and z directions
  //  x = accelX * cos(pitch) * cos(yaw) + accelY * (sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw)) + accelZ * (cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw));
  //  y = accelX * cos(pitch) * sin(yaw) + accelY * (sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw)) + accelZ * (cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw));
  //  z = -accelX * sin(pitch) + accelY * sin(roll) * cos(pitch) + accelZ * cos(roll) * cos(pitch);
  //  Serial.print("x:");
  //  Serial.print(x);
  //  Serial.print(',');
  //  Serial.print("y:");
  //  Serial.print(y);
  //  Serial.print(',');
  //  Serial.print("z:");
  //  Serial.println(z);
  //  velocityX += x * elapsedTime;
  //  velocityY += y * elapsedTime;
  //  velocityZ += z * elapsedTime;

  //  displacementX += velocityX * elapsedTime * 1000.0;
  //  displacementY += velocityY * elapsedTime * 1000.0;
  //  displacementZ += velocityZ * elapsedTime * 1000.0;

  //  Serial.print("Displacement X: ");
  //  Serial.println(displacementX);
  //  Serial.print("Displacement Y: ");
  //  Serial.println(displacementY);
  //  Serial.print("Displacement Z: ");
  //  Serial.println(displacementZ);

  //  Serial.print("dX:"); Serial.print(displacementX); Serial.print(',');
  //  Serial.print("dY:"); Serial.print(displacementY); Serial.print(',');
  //  Serial.print("dZ:"); Serial.print(displacementZ); Serial.println();
  //delay(500);
  //previousTime = currentTime;
}
