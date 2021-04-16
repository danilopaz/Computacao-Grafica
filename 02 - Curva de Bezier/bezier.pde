float p1x = 4*(width/5);
float p1y = 4*(height/2);

float p2x = 4*(2*width/5);
float p2y = 4*(height/4);

float p3x = 4*(3*width/5);
float p3y = 4*(3*height/4);

float p4x = 4*(4*width/5);
float p4y = 4*(height/2);
  
void setup()
{
  size(400,400);
}

void draw()
{
  background(128, 231, 100, 400);
  noFill();
  stroke(129, 123, 198, 350);
  strokeWeight(1.5);
  beginShape();
  for(float t = 0.01; t <= 1; t += 0.01)
  {
    float ax = p1x + t*(p2x-p1x);
    float bx = p2x + t*(p3x-p2x);
    float cx = p3x + t*(p4x-p3x);
    float dx = ax + t*(bx-ax);
    float ex = bx + t*(cx-bx);
    float fx = dx + t*(ex-dx);
    
    float ay = p1y + t*(p2y-p1y);
    float by = p2y + t*(p3y-p2y);
    float cy = p3y + t*(p4y-p3y);
    float dy = ay + t*(by-ay);
    float ey = by + t*(cy-by);
    float fy = dy + t*(ey-dy);
    
    vertex(fx, fy);
  }
  endShape();
}
