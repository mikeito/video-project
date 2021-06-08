class Car {
  int gear;
  int _speed = 0;

  int get speed => _speed;

  Car(this.gear);

  void speedUp(int incre) {
    _speed += incre;
  }

  void applyBrake(int decre) {
    _speed -= decre;
  }

  @override
  String toString() => 'Car speed is: $_speed';
}

void main() {
  var result = Car(4);

  // result.speedUp(2);

  print(result);
}
