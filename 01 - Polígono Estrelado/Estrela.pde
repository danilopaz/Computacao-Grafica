void setup() {
  size(360, 360);
}

void draw() {
  background(128, 231, 100, 400);
  pushMatrix();
  translate(width/2, height/2);
  int raio2 = round(map(mouseY, 0, width, 87.5, 175));
  estrela(0, 0, 30, raio2, 5); 
  popMatrix();
}

void estrela(float x, float y, float raio1, float raio2, int npoints) {
  float angle = TWO_PI / npoints;
  float halfAngle = angle/2.0;
  rotate(frameCount/50);
  beginShape();
  for (float a = 0; a < TWO_PI; a += angle) {
    float sx = x + cos(a) * raio2;
    float sy = y + sin(a) * raio2;
    vertex(sx, sy);
    sx = x + cos(a+halfAngle) * raio1;
    sy = y + sin(a+halfAngle) * raio1;
    vertex(sx, sy);
  }
  endShape(CLOSE);
}
