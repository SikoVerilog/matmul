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
from .ctr_master import ctr_master
from .ctr_sequencer import ctr_sequencer
from .ctr_monitor import ctr_monitor


class ctr_agent(UVMAgent):


    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.sqr = None  # ctr_sequencer
        self.drv = None  # ctr_master
        self.mon = None  # ctr_monitor
        self.vif = None  # ctr_vif
        self.error = False
        uvm_info("Ctr_agent", "Agent Created", UVM_LOW)
        #self.ap = UVMAnalysisExport("ap", self)


    def build_phase(self, phase):
        uvm_info("Ctr_agent", "In Build Phase", UVM_LOW)
        self.sqr = ctr_sequencer.type_id.create("sqr", self)
        self.drv = ctr_master.type_id.create("drv", self)
        self.mon = ctr_monitor.type_id.create("mon", self)

        arr = []
        if UVMConfigDb.get(self, "", "vif", arr):
            self.vif = arr[0]
        if self.vif is None:
            uvm_fatal("Control Agent", "No virtual interface specified for ctr_agent instance")


    def connect_phase(self, phase):
        uvm_info("Ctr_agent", "In Connect Phase", UVM_LOW)
        self.drv.seq_item_port.connect(self.sqr.seq_item_export)
        #self.mon.ap.connect(self.ap)

    def extract_phase(self, phase):
        uvm_info("Ctr_agent", "In Extract Phase", UVM_LOW)
        if self.mon.errors > 0:
            self.error = True
        if self.mon.num_items == 0:
            uvm_error("Control Agent", "CTR monitor did not get any items")
            self.error = True


uvm_component_utils(ctr_agent)
