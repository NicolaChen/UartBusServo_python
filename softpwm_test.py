import wiringpi

OUTPUT = 1

PIN_TO_PWM = 5

wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN_TO_PWM, OUTPUT)
wiringpi.softPwmCreate(PIN_TO_PWM,15,200) # Setup PWM using Pin, Initial Value and Range parameters

wiringpi.delay(1000)
dc = input("5~25:")
wiringpi.softPwmWrite(PIN_TO_PWM, dc)
wiringpi.delay(1000)
print("Done!")

