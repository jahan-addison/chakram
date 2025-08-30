main() {
  auto x,y;
  y = 10;
  goto ADD;
ADD:
  x = add(2,5);
}

add(a,b) {
  // return(a + b);
  return(a + b + b);
}