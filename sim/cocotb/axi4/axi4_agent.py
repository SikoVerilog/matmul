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

from uvm.comps.uvm_agent import UVMAgent
from uvm.base import UVMConfigDb, UVM_LOW
from uvm.macros import *
from uvm.tlm1 import *
from .axi4_master import axi4_master
from .axi4_sequencer import axi4_sequencer
from .axi4_monitor import aaxi4_monitor


class axi4_agent(UVMAgent):


    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.sqr = None  # axi4_sequencer
        self.drv = None  # axi4_master
        self.mon = None  # axi4_monitor
        self.vif = None  # axi4_vif
        self.error = False
        uvm_info("AXI4_agent", "Agent Created", UVM_LOW)
        #self.ap = UVMAnalysisExport("ap", self)


    def build_phase(self, phase):
        uvm_info("AXI4_agent", "In Build Phase", UVM_LOW)
        self.sqr = axi4_sequencer.type_id.create("sqr", self)
        self.drv = axi4_master.type_id.create("drv", self)
        self.mon = axi4_monitor.type_id.create("mon", self)

        arr = []
        if UVMConfigDb.get(self, "", "vif", arr):
            self.vif = arr[0]
        if self.vif is None:
            uvm_fatal("AXI4 Agent", "No virtual interface specified for axi4_agent instance")


    def connect_phase(self, phase):
        uvm_info("AXI4_agent", "In Connect Phase", UVM_LOW)
        self.drv.seq_item_port.connect(self.sqr.seq_item_export)
        #self.mon.ap.connect(self.ap)

    def extract_phase(self, phase):
        uvm_info("AXI4_agent", "In Extract Phase", UVM_LOW)
        if self.mon.errors > 0:
            self.error = True
        if self.mon.num_items == 0:
            uvm_error("AXI4 Agent", "AXI4 monitor did not get any items")
            self.error = True


uvm_component_utils(axi4_agent)
