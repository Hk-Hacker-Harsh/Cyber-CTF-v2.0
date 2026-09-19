/*
 *  Arcade Mainframe Beacon v1.0
 *  Hardware Diagnostic Interface
 *  
 *  Note: Signals are output on Pin 13.
 */

const int LED_PIN = 13;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void sig_a() {
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  delay(500);
}

void sig_b() {
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
  delay(500);
}

void sig_gap() {
  delay(2000);
}

void loop() {
  sig_a(); sig_a(); sig_gap();
  sig_a(); sig_a(); sig_gap();
  sig_b(); sig_gap();
  sig_b(); sig_b(); sig_gap();
  sig_b(); sig_a(); sig_b(); sig_a(); sig_gap();
  sig_b(); sig_a(); sig_b(); sig_a(); sig_gap();
  sig_b(); sig_a(); sig_b(); sig_b(); sig_a(); sig_b(); sig_gap();
  sig_a(); sig_b(); sig_a(); sig_a(); sig_gap();
  sig_a(); sig_b(); sig_b(); sig_b(); sig_b(); sig_gap();
  sig_b(); sig_b(); sig_a(); sig_gap();
  sig_a(); sig_a(); sig_a(); sig_a(); sig_gap();
  sig_b(); sig_gap();
  sig_a(); sig_a(); sig_b(); sig_b(); sig_a(); sig_b(); sig_gap();
  sig_b(); sig_b(); sig_gap();
  sig_b(); sig_b(); sig_b(); sig_b(); sig_b(); sig_gap();
  sig_a(); sig_b(); sig_a(); sig_gap();
  sig_a(); sig_a(); sig_a(); sig_gap();
  sig_a(); sig_a(); sig_a(); sig_b(); sig_b(); sig_gap();
  sig_a(); sig_a(); sig_b(); sig_b(); sig_a(); sig_b(); sig_gap();
  sig_b(); sig_a(); sig_b(); sig_a(); sig_gap();
  sig_b(); sig_b(); sig_b(); sig_b(); sig_b(); sig_gap();
  sig_b(); sig_a(); sig_a(); sig_gap();
  sig_a(); sig_a(); sig_a(); sig_b(); sig_b(); sig_gap();
  sig_b(); sig_a(); sig_b(); sig_b(); sig_a(); sig_b(); sig_gap();

  // Reset sequence gap
  delay(5000);
}