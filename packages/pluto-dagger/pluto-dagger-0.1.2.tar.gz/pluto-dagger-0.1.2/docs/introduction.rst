===========
Quick Start
===========

Installation
-------------

If you have Python installed you can install the current release using either pip: ::

   pip install pluto-dagger


Installing the package from source
----------------------------------

1. Get the latest source by cloning this repo: ::

      git clone https://github.com/rohithvarma3000/dagger.git

2. Install the dependencies: ::

      pip install -r requirements.txt

3. Install dagger: ::

      pip install .


Python interface
~~~~~~~~~~~~~~~~
$ ``import dagger``

Connecting with Pluto Drone:
##### Make Sure you're connected with pluto's hotspot

$ ``Pluto_IP = "192.168.4.1"``

$ ``Pluto_PORT = 23``

$ ``pluto = dagger.PlutoConnection()``

$ ``pluto.connect((Pluto_IP, Pluto_PORT))``

Intiating the SetRawRc Object for Controlling the pluto Drone using the RC params:
$ ``rc = dagger.SetRawRC(pluto)``

Arming the DRONE:

$ ``rc.arm_drone()``

Disarming the DRONE:

$ ``rc.arm_drone()``

Intiating the SetCommand Object for sending the commands:

$ ``com = dagger.SetCommand(pluto)``


.. code-block:: python
   
   "Run the following script in separate terminal"

   def default_values(Pluto_IP, Pluto_PORT):
      t = PlutoConnection()
      t.connect((Pluto_IP, Pluto_PORT))
      cmd = SetRawRC(t)
      while True:
         cmd.box_arm()


   if __name__ == '__main__':
      Pluto_IP = "192.168.4.1"
      Pluto_PORT = 23
      default_values(Pluto_IP, Pluto_PORT)

 
Taking off the drone using the PlutoControl object:

$ ``pluto_control = dagger.PlutoControl(t)``

$ ``pluto_control.take_off()``