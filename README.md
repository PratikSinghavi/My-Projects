# My-Projects


## Neural Network for MNIST Dataset

Requirements : 
* Python(v3) or above
* numpy/pandas

Steps to run the code:

0. Clone the repository to your local machine
1. Unzip Datasets.zip in order to obtain a split of train/test images and labels in csv format
2. Execute the following command
```
python3 NeuralNetwork3.py train_image.csv train_label.csv test_image.csv
```


## Smart IoT Network

Requirements : 
* Python(v3.4) or above
* Python libraries : matplotlib,serial,tkinter
* Arduino (code originally written for UNO but can be adapted to other boards) 
* [HC-SR04 Ultrasonnic Ranging Sensor](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)
* Zigbee Modules - One Co-ordinator and N End Devices (for N sensor nodes)
* Raspberry Pi running raspbian OS

Steps to run the code:

0. Clone the repository to your local machine
1. Make the connections between the arduino UNO and HC-SR04 sensor (connections specified in the .ino file)
2. Connect pins Tx,Rx (Arduino) -- Rx,Tx (Zigbee configured as END Device) - Do this for # of sensor nodes 
3. Flash code to the Arduino UNO using Arduino IDE
4. Make connections between Raspberry Pi and Zigbee module setup as Co-Ordinator
5. Execute the below command on the raspbian shell 
```
python3 GUIfinal.py
```

*The command can be configured using cron to run on boot and the reports can be seen using VNCviewer after connecting to Raspberry pi on the same network for autonomous operation.*

Notes: 
* The other files have to be placed in the same directory as the GUIfinal.py for generating graphs for each nodes - The current setup works is made for 3 nodes and raspberry pi as gateway
* The sensor code is configured to the application of detecting level of container contents when planted on the bottom face of the lid of the container.
* This can be adapted to a different application for eg. Smart PostBox by switching the sensor with a [weight/load sensor](https://www.sparkfun.com/products/10245) (along with appropriate hardware) and code changes.


