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

from uvm.seq.uvm_sequence_item import UVMSequenceItem
from uvm.base.uvm_object_globals import *
from uvm.macros import *
from uvm.macros.uvm_message_defines import uvm_info
from uvm.base import sv, UVM_LOW

class axi4_item (UVMSequenceItem):

    def __init__(self, name="axi4_item"):
        uvm_info("axi4_item", "item created", UVM_LOW)
        super().__init__(name)
        self.addr = 0  # Address
        self.data = 0  # Data
        self.rw   = 0  # Read/Write
        self.resp = 0  # responce

    def convert2string(self):
        axi4_trn=sv.sformatf("AXI4 Address= %0h Data= %0h Read/Write= %0h.",
                self.addr, self.addr, self.rw, self.resp)
        return axi4_trn

    def post_randomize(self):
        return 
    #endclass: axi4_item

uvm_object_utils_begin(axi4_item)
uvm_field_int("addr", UVM_ALL_ON)
uvm_field_int("addr", UVM_ALL_ON)
uvm_field_int("rw", UVM_ALL_ON)
uvm_field_int("resp", UVM_ALL_ON)
uvm_object_utils_end(axi4_item)

