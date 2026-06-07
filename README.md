32-PI A.K.A. Project Mauna Kea

This project involves the design and testing of custom Raspberry Pi-hats for implementation in a
Raspberry Pi cluster consisting of 32 Raspberry Pi 5 computers.

Each hat contains a Raspberry Pico, Lattice FPGA, temperature sensor, LED display, and 15 programmable LEDs.

All scripts were written by Isabell Hudnall using Python, C, Verilog, and Shell.

The goals of this project included:

- to be able to control the 15 LEDs from either the Pi 5, Pico, or Lattice FPGA,
without signal interference.
- have each display show whether a user is connected via remote desktop
- have each display show a constant temperature readout from the sensor (to monitor overheating)
- to have each Pi 5 be able to commincate with each other Pi 5 for performing more complex
computations.
