#//
#// -------------------------------------------------------------
#//    Copyright 2004-2011 Synopsys, Inc.
#//    Copyright 2010 Mentor Graphics Corporation
#//    Copyright 2010 Cadence Design Systems, Inc.
#//    Copyright 2019-2020 Tuomas Poikela (tpoikela)
#//    All Rights Reserved Worldwide
#//
#//    Licensed under the Apache License, Version 2.0 (the
#//    "License"); you may not use this file except in
#//    compliance with the License.  You may obtain a copy of
#//    the License at
#//
#//        http://www.apache.org/licenses/LICENSE-2.0
#//
#//    Unless required by applicable law or agreed to in
#//    writing, software distributed under the License is
#//    distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#//    CONDITIONS OF ANY KIND, either express or implied.  See
#//    the License for the specific language governing
#//    permissions and limitations under the License.
#// -------------------------------------------------------------
#//

import cocotb
from cocotb.triggers import *

from uvm.base.sv import sv_if


class ctr_if(sv_if):

    #   logic [10:0] acc_wr_addr; // address to store the output matrix C of DPU array
    #   logic        acc_wr_en;   // enables writing wr_data into acc memory
    #   acc_width_t  acc_width;   // indicates whether to use 32, 64, or 128 bits of the accumulator per element 
    #   logic [$clog2(DPU_OUT_WIDTH)-1:0] byte_shft; // amount to shift data by (for multi-precision)
    #   logic acc_en; 

    def __init__(self, dut, bus_map=None, name="ctr"):
        if bus_map is None:
            bus_map  = { 
                    "clk"       : "clk",
                    "ping_pong" : "ping_pong",
                    "acc_we"    : "acc_wr_en",
                    "acc_addr"  : "acc_wr_addr",
                    "acc_width" : "acc_width",
                    "acc_shft"  : "byte_shft",
                    "acc_en"    : "acc_en",
                    "acc_data"  : "data_c",
                    "pre_en"    : "preload_acc_en",
                    "pre_data"  : "preload_acc_data",
                    "pre_we"    : "preload_acc_data_val",
                    "pre_waddr" : "preload_wr_addr",
                    "st_raddr"  : "st_rd_addr"}         
        super().__init__(dut, name, bus_map)
        self.rst = dut.rst_n


    
    async def start(self):
        await Timer(0)

    #   clocking mck @(posedge pclk)
    #      output paddr, psel, penable, pwrite, pwdata
    #      input  prdata
    #
    #      sequence at_posedge
    #         1
    #      endsequence : at_posedge
    #   endclocking: mck
    #
    #   clocking sck @(posedge pclk)
    #      input  paddr, psel, penable, pwrite, pwdata
    #      output prdata
    #
    #      sequence at_posedge_; // FIXME todo review
    #         1
    #      endsequence : at_posedge_
    #   endclocking: sck
    #
    #   clocking pck @(posedge pclk)
    #      input paddr, psel, penable, pwrite, prdata, pwdata
    #   endclocking: pck
    #
    #   modport master(clocking mck)
    #   modport slave(clocking sck)
    #   modport passive(clocking pck)
    #
    #endinterface: ctr_if
    #
    #`endif
