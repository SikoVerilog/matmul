#//
#// -------------------------------------------------------------
#//    Copyright 2004-2011 Synopsys, Inc.
#//    Copyright 2010-2011 Mentor Graphics Corporation
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

from uvm.base.uvm_callback import *
from uvm.comps.uvm_monitor import UVMMonitor
from uvm.tlm1 import *
from uvm.macros import *

from .ctr_item import *


class ctr_monitor_cbs(UVMCallback):
    def trans_observed(self, xactor, cycle):
        pass


class ctr_monitor(UVMMonitor):

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.ap = UVMAnalysisPort("ap", self)
        self.sigs = None  # passive
        self.cfg = None  # ctr_config
        self.errors = 0
        self.num_items = 0
        self.tag = "CTR_MONITOR"


    def build_phase(self, phase):
        super().build_phase(phase)
        agent = self.get_parent()
        if agent is not None:
            self.sigs = agent.vif
        else:
            arr = []
            if UVMConfigDb.get(self, "", "vif", arr):
                uvm_info("Control Monitor", "Got vif through ConfigDb for control monitor instance")
                self.sigs = arr[0]
        if self.sigs is None:
            uvm_fatal("Control Monitor", "No virtual interface specified for self monitor instance")


    
    async def run_phase(self, phase):
        while True:
            tr = None

            # Wait for a SETUP cycle
            while True:
                await self.sample_delay()
                if (self.sigs.pre_we == 1 or
                   self.sigs.acc_we == 1):
                    break

            tr = ctr_item.type_id.create("tr", self)
            
            tr.ping_pong = self.sigs.ping_pong.value.integer
            
            if self.sigs.acc_we:
                tr.acc_we = self.sigs.acc_we.value.integer
                tr.acc_addr = self.sigs.acc_addr.value.integer
                tr.acc_width = self.sigs.acc_width.value.integer
                tr.acc_shft = self.sigs.acc_shft.value.integer
                tr.acc_en = self.sigs.acc_en.value.integer
                tr.acc_data = self.sigs.acc_data.value.integer
            if self.sigs.pre_we:
                tr.pre_en = self.sigs.pre_en.value.integer
                tr.pre_data = self.sigs.pre_data.value.integer
                tr.pre_we = self.sigs.pre_we.value.integer
                tr.pre_waddr = self.sigs.pre_waddr.value.integer
                tr.st_raddr = self.sigs.st_raddr.value.integer

            self.trans_observed(tr)
            #TODO uvm_do_callbacks(apb_monitor,apb_monitor_cbs, self.trans_observed(self, tr))
            self.num_items += 1
            self.ap.write(tr)
            uvm_info(self.tag, "Sampled CTR item: " + tr.convert2string(), UVM_HIGH)

    def trans_observed(self, tr):
        pass


    
    async def sample_delay(self):
        await RisingEdge(self.sigs.clk)

uvm_component_utils(ctr_monitor)
