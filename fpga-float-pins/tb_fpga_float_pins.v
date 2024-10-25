module tb_fpga_float_pins;

wire led0;
wire led1;
wire led2;
wire led3;
wire led4;
wire led5;
wire led6;
wire led7;
wire led8;
wire led9;
wire led10;
wire led11;
wire led12;
wire led13;
wire led14;
wire led15;

initial begin
    $to_myhdl(
        led0,
        led1,
        led2,
        led3,
        led4,
        led5,
        led6,
        led7,
        led8,
        led9,
        led10,
        led11,
        led12,
        led13,
        led14,
        led15
    );
end

fpga_float_pins dut(
    led0,
    led1,
    led2,
    led3,
    led4,
    led5,
    led6,
    led7,
    led8,
    led9,
    led10,
    led11,
    led12,
    led13,
    led14,
    led15
);

endmodule
