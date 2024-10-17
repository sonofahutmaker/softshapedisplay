# SILICONE DREAM
The complexity of meshing physical design requirements with data-driven logic has long been the focus and vexation of artists and engineers wanting to build kinetic sculptural and data display artifacts. Traditional shape displays require high complexity, as previous models require a one to one ratio between actuator number and data resolution. We present SILICONE DREAM, an open-source system for building soft shape display devices which can convey trends about continuous data as well as function in artistic installations. SILICONE DREAM utilizes a silicone top layer over a grid of actuator controlled shafts in order to interpolate between data values without added design complexity. SILICONE DREAM functions as a kinetic sculptural object which can be positioned either horizontally or vertically and has been designed for live collaboration with performing artists and as a self-contained system for generating changing 3D shapes. Because the SILICONE DREAM system is modular, it can easily expand to incorporate other forms of media such as screen-based visuals and generative audio. SILICONE DREAM is controlled by an embedded system with custom software, and contributes a generalizable system for future shape display design for both artistic and scientific use cases.

https://vimeo.com/1020710513?share=copy#t=0

The first SILICONE DREAM soft shape display device replicating changing generated terrain (example application wave-terrain-synth-visual).

https://youtu.be/o8n0LYaVpVw?si=xBZ51qVCjUL302s2

The first SILICONE DREAM soft shape display device responding to music in real time.

## Software Setup Guide
This setup guide relates only to the software side of building a shape display. Please follow the Instructables link for building directions for the hardware portion of the shape display. The software libraries can be used with different shape display hardware setups, including changing number of actuators, so the hardware can be changed to better fit your use cases.

### **1. On Raspberry Pi, clone repo:**

<code>git clone https://github.com/sonofahutmaker/softshapedisplay.git</code>

### **2. Install requirements:**

<code>cd softshapedisplay</code>

<code>pip install -r requirements.txt</code>

### **3. Connect data source:**

The soft shape display system receives data over OSC. The first time you run the application, you must include the IP address of the Raspberry Pi device you are running the app on and the port number to receive data on. The device must be connected to the same Wifi network as the device sending data. See Example Apps section for details on sending data to your application from another source.

Run <code>python main.py --help</code> for details on all command line arguments.

The first time you run the app, you must also include the number of servo motors being used. The example build uses 16.

<code>python main.py -ip RASPI_IP_ADDRESS_HERE --port RECEIVING_PORT_HERE -n NUMBER_SERVOS_HERE</code>

### **4. Customize settings:**

The first time you run main.py a config file, config.ini, will be generated with preset values. You can change these settings through command line arguments or directly in config.ini.

Important settings include 

    - data_range: which is the full possible range of incoming data
    - servo_type: standard or continuous. Standard is recommended and enable by default, but continuous is supported if this argument is set.
    - angle_range: if using a standard servo, what is the full angle range it can turn to. Switch high and low values if the servo is installed upside down.
    - shaft_len, traversal_time, forward_throttle, backward_throttle, zero_throttle, speed only need to be set if using continuous rotation servos.

The full list of command line arguments is as follows:
```
  -h, --help            show this help message and exit
  -ip IP                ip address of device this is running on to receive
                        data
  -p PORT, --port PORT  port number to receive OSC messages on
  -n NUM_SERVOS, --num_servos NUM_SERVOS
  -d DATA_RANGE [DATA_RANGE ...], --data_range DATA_RANGE [DATA_RANGE ...]
                        possible range of data values low to high like '0.0
                        1.0'
  -a ANGLE_RANGE [ANGLE_RANGE ...], --angle_range ANGLE_RANGE [ANGLE_RANGE ...]
                        for standard servo, angle range low to high like '180
                        0' with order dependent on orientation
  -s {standard,cont}, --servo_type {standard,cont}
  --shaft_len SHAFT_LEN
                        for cont. rot servos, length of pusher shaft in mm
  -t TRAVERSAL_TIME, --traversal_time TRAVERSAL_TIME
                        for cont. rot servos, time in secs to move shaft all
                        the way up at full throttle
  -f FORWARD_THROTTLE, --forward_throttle FORWARD_THROTTLE
                        for cont. rot servos, direction and full power value
                        for moving shafts up
  -b BACKWARD_THROTTLE, --backward_throttle BACKWARD_THROTTLE
                        for cont. rot servos, direction and full power value
                        for moving shafts down
  -z ZERO_THROTTLE, --zero_throttle ZERO_THROTTLE
                        for cont. rot. servos, throttle value that stops servo
                        spinning
  --speed SPEED         for cont. rot. servos, multiplier for throttle
```

### **5. Run Application and Receive Data:**

Run the application with <code>python main.py</code>. Add any settings needed to this command as shown above. Once the application is running, it can recieve data over OSC from another source at the IP address and port configured. 

OSC Messages should be sent with either address <code>/block</code> or <code>/list</code>

Servo number is determined by which position it is attached to on the servo hat on the Raspberry Pi.

OSC Message formats which can be received:

To change the data value (and corresponding position) of a single servo:
```
/block SERVO_NUM DATA_VAL
```
i.e.
```
/block 3 0.5
```
will set the (0 indexed) servo of index 3 to the position corresponding to the data value of 0.5. If the set data range is 0 to 1, this means the servo will push its shaft to halfway up.


To change the data values (and corresponding positions) of all servos:
```
/list DATA_VAL DATA_VAL DATA_VAL DATA_VAL ...
```
with data values for all servos.

i.e. if you have set the servo number to be 4, a message of
```
/list 0.0 0.2 0.5 1.0
```
will set the 0th servo to the position corresponding to the data value of 0.0, the 1st to 0.2, the 2nd to 0.5, and the last to 1.0

## Example Apps -- slidersui.maxpat and wave-terrain-synth-visual.maxpat
Both example applications are Max Patchers (Max application can be downloaded [here](https://cycling74.com/products/max)) which send data over OSC to a running soft shape display application. There are built in OSC libraries for many programming languages, including Python, and applications, so these example applications by no means cover all the ways data can be sent to a soft shape display device.

They both make use of the <code>/list</code> message address to send data values to a shape display with 16 servos. You can look at and edit these patchers even without an active Max license, and use them to test, just not save changes.

### **1. First look at the slidersui.maxpat:**
It has 16 sliders, which correspond to the levels of the 16 servos, with a data range between 0.0 and 1.0. This is a great tester application to make sure you are able to receive data over OSC and that your servos are behaving as expected.

When a slider or sliders change, a message is generated in the /list message format like <code>/list 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.</code>. 

This message is sent as soon as it is generated to the (example) IP address 192.168.86.37 and port number 1338. This happens in the the object with <code>udpsend 192.168.86.37 1338</code>. Change the IP address and port number to that of your Raspberry Pi, making sure the Raspberry Pi and the device running the Max Patch are on the same Wifi. Make sure you have set the data range in your soft shape display application to 0.0 - 1.0. Move each slider and verify that you are receiving data and that your device's servos are moving as expected.

### **2. wave-terrain-synth-visual.maxpat:**
This patcher also generates a list of values to be sent to all 16 servos and sends them using the same <code>udpsend 192.168.86.37 1338</code> message. But this patcher generates the values using a wave terrain synthesis algorithm. After enabling your microphone (options > audio status > power button), the audio input is used to generate a changing terrain which is visualized. This terrain is then downsampled to 16 points across its surface, and these values are sent to the Raspberry Pi every 60ms, turning the surface of the shape display into the same terrain as the generated output. This application can also produce audio from exploring the surface of the terrain. This example application demonstrates one way an algorithm can be used to continually change the surface of a soft shape display device.