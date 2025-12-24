main() {
  auto *x;
  x = "hello world";
  print(call(x));
  return(0);
}

call(*x) {
  return(x);
}

print(x) {
}