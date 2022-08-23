#!/bin/bash
cd /sys/class/pwm/pwmchip1
echo 0 > export
cd pwm0
echo 20000000 > period
echo normal > polarity
echo "Start servo test, initializing to 180deg."
echo 1500000 > duty_cycle
echo 1 > enable
sleep 1s

echo "Input testing position(deg, 0~360)"
read tp
fin=$((500000+$tp*50000/9))
echo $fin
sleep 1s


echo "Testing..."
echo $fin > duty_cycle

var=500000
while(( $var<=2500000 ))
do
#    echo $var > duty_cycle
#    echo $var
#    let var+=200000
    echo 2055555 > duty_cycle
    sleep 1s
    echo $fin > duty_cycle
    sleep 2s
done

cd /sys/class/pwm/pwmchip1
echo 0 > unexport
echo "Finish"
