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

echo "Cycle:1->mid->2->mid->1"
echo "Input testing position 1(deg, 0~360)"
read tp1
fin1=$((500000+$tp1*50000/9))
echo $fin1
sleep 1s

echo "Input testing position 2(deg, 0~360)"
read tp2
fin2=$((500000+$tp2*50000/9))
echo $fin2
sleep 1s

echo "Input mid position(deg, 0~360)"
read tp3
fin3=$((500000+$tp3*50000/9))
echo $fin3
sleep 1s

echo "Testing..."
while(true)
do
    echo $fin1 > duty_cycle
    sleep 2s
    echo $fin3 > duty_cycle
    sleep 3s
    echo $(($fin1+2777)) > duty_cycle
    sleep 3s
    echo $fin3 > duty_cycle
    sleep 3s
done



cd /sys/class/pwm/pwmchip1
echo 0 > unexport
echo "Finish"
