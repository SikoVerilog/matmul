
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

from uvm import *
from tb_env import tb_env

from control.ctr_if import ctr_if

class test(UVMTest):

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.env = tb_env("env")

    def start_of_simulation_phase(self, phase):
        cs_ = UVMCoreService.get()
        top = cs_.get_root()

    def check_phase(self, phase):
        self.error = self.env.has_errors()
        if self.error:
            uvm_fatal("TEST FAILED", "check_phase of test threw fatal")


uvm_component_utils(test)


class tb_ctl_if():

    def __init__(self, clk, rst_n):
        self.clk = clk
        self.arst_n = rst_n


async def do_reset_and_start_clocks(dut):
    await Timer(100, "NS")
    dut.rst_n <= 0
    await Timer(200, "NS")
    dut.clk <= 0
    await Timer(500, "NS")
    cocotb.fork(Clock(dut.clk, 50, "NS").start())


@cocotb.test()
async def test(dut):

    # Create the interfaces and bus map for APB
    ctr_bus_map = { "clk"       : "clk",
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
    ctr_vif = ctr_if(dut, bus_map=ctr_bus_map, name="")

    rst_if = tb_ctl_if(
        clk=dut.clk,
        rst_n=dut.rst_n
    )

    UVMConfigDb.set(None, "env", "vif", rst_if)
    UVMConfigDb.set(None, "env.ctr_agnt", "vif", ctr_vif)

    cocotb.fork(do_reset_and_start_clocks(dut))

    await run_test()
