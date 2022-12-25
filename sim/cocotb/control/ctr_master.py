#//
#// -------------------------------------------------------------
#//    Copyright 2004-2011 Synopsys, Inc.
#//    Copyright 2010 Mentor Graphics Corporation
#//    Copyright 2010-2011 Cadence Design Systems, Inc.
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

import cocotb
from cocotb.triggers import *

from uvm.base.uvm_callback import *
from uvm.base.uvm_config_db import *
from uvm.comps.uvm_driver import UVMDriver
from uvm.macros import *
from uvm.base.uvm_object_globals import UVM_MEDIUM

from .ctr_item import *


class ctr_master_cbs(UVMCallback):
    
    async def trans_received(self, xactor, cycle):
        await Timer(1, "NS")

    
    async def trans_executed(self, xactor, cycle):
        await Timer(1, "NS")


class ctr_master(UVMDriver):  #(ctr_item)


    #   event trig
    #   apb_vif sigs
    #   apb_config cfg
    #
    def __init__(self, name, parent=None):
        super().__init__(name,parent)
        self.trig = Event("trans_exec")  # event
        self.sigs = None  # apb_vif
        self.cfg = None  # apb_config
        self.tag = "CTR_MASTER"


    def build_phase(self, phase):
        super().build_phase(phase)
        agent = self.get_parent()
        if agent is not None:
            self.sigs = agent.vif
        else:
            arr = []
            if (not UVMConfigDb.get(self, "", "vif", arr)):
                uvm_fatal("CTR", "No virtual interface specified for self driver instance")
            else:
                self.sigs = arr[0]


    
    async def run_phase(self, phase):
        uvm_info("CTR_MASTER", "ctr_master run_phase started", UVM_MEDIUM)

        self.sigs.acc_we   <= 0
        self.sigs.acc_en   <= 0
        self.sigs.pre_en   <= 0
        self.sigs.pre_we   <= 0
        self.sigs.acc_shft <= 0

        while True:
            # await self.drive_delay()

            tr = []
            await self.seq_item_port.get_next_item(tr)
            tr = tr[0]
            uvm_info("CTR_MASTER", "Driving trans into DUT: " + tr.convert2string(), UVM_MEDIUM)

            # await self.trans_received(tr)
            #uvm_do_callbacks(apb_master,apb_master_cbs,trans_received(self,tr))

            await self.write(tr)

            # await self.trans_executed(tr)
            # uvm_do_callbacks(ctr_master,ctr_master_cbs,trans_executed(self,tr))

            self.seq_item_port.item_done()
            self.trig.set()
            #->trig
        #   endtask: run_phase
    
    async def write(self, trans):
        uvm_info(self.tag, "Doing CTR write to addr " + str(trans.acc_addr), UVM_MEDIUM)
        self.sigs.acc_addr   <= trans.acc_addr
        self.sigs.acc_we     <= trans.acc_we
        self.sigs.acc_width  <= trans.acc_width
        self.sigs.acc_shft   <= trans.acc_shift
        self.sigs.acc_en     <= trans.acc_en
        self.sigs.acc_data   <= trans.acc_data
        self.sigs.ping_pong  <= trans.ping_pong
        self.sigs.pre_en     <= trans.pre_en
        self.sigs.pre_data   <= trans.pre_data
        self.sigs.pre_we     <= trans.pre_we
        self.sigs.pre_waddr  <= trans.pre_waddr
        self.sigs.st_raddr   <= trans.st_raddr
        await self.drive_delay()
        self.sigs.acc_we <= 0
        self.sigs.acc_en <= 0
        self.sigs.pre_en <= 0
        self.sigs.pre_we <= 0
        uvm_info(self.tag, "Finished ctr write to addr " + str(trans.acc_addr), UVM_MEDIUM)
        #   endtask: write


    
    async def drive_delay(self):
        await RisingEdge(self.sigs.clk)

    
    async def trans_received(self, tr):
        await Timer(1, "NS")

    
    async def trans_executed(self, tr):
        await Timer(1, "NS")


uvm_component_utils(ctr_master)
