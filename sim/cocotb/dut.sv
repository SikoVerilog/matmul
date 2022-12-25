


module mm_acc(
    input  clk,
    input  rst_n,
    input         acc_wr_en,// Write enable
    input [10:0]  acc_wr_addr,//Address
    input [1:0] acc_width,// write with
    input [4:0] byte_shft,// byte shift
    input  acc_en,// accumlation enable
    input [31:0] data_c,
    input  ping_pong,
    input  preload_acc_en,
    input [31:0] preload_acc_data,
    input  preload_acc_data_val,
    input [10:0] preload_wr_addr,
    input [10:0] st_rd_addr
);
    
endmodule
