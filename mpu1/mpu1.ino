#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;
float idleX[50], idleY[50], idleZ[50];
bool isidleX, isidleY, isidleZ;
uint8_t iX;
const uint8_t iX_max = sizeof(idleX);

void setup() {
  Serial.begin(115200);

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  // set accelerometer range to +-8G
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);

  // set gyro range to +- 500 deg/s
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);

  // set filter bandwidth to 21 Hz
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);

  delay(100);
}

void loop() {
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  /* Print out the values */
  Serial.print("aX:"); Serial.print(-a.acceleration.x); Serial.print(',');
  Serial.print("aY:"); Serial.print(-a.acceleration.y); Serial.print(',');
  Serial.print("aZ:"); Serial.print(-a.acceleration.z); Serial.print(',');
  float big = 0, small = 50;
  for (int i = 0; i < sizeof(idleX); i++)
  {
    if (idleX[i] > big)
      big = idleX[i];
    if (idleX[i] < small)
      small = idleX[i];
  }
  Serial.print("small x:"); Serial.print(small); Serial.println();
}
