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

class ctr_item (UVMSequenceItem):

    def __init__(self, name="ctr_item"):
        uvm_info("ctr_item", "item created", UVM_LOW)
        super().__init__(name)
        self.acc_we = 0  # Write enable
        self.acc_addr = 0  # Address
        self.acc_width = 0  # write with
        self.acc_shift = 0  # byte shift
        self.acc_en = 0 # accumlation enable
        self.acc_data = 0
        self.ping_pong = 0
        self.pre_en = 0
        self.pre_data = 0
        self.pre_we = 0
        self.pre_waddr = 0
        self.st_raddr = 0

    def convert2string(self):
        acc_ctr =sv.sformatf("Acc Control Write_enable=%0h Address=%0h Width=%0h Byte_shift=%0h Accumlation_enable=%0h Data=%0h",
                self.acc_we, self.acc_addr, self.acc_width, self.acc_shift, self.acc_en, self.acc_data)
        pre_acc = sv.sformatf("Preload Write_enable=%0h Address=%0h Ping_pong=%0h Enable=%0h Data=%0h ST_rd_addr=%0h",
                self.pre_we, self.pre_waddr, self.ping_pong, self.pre_en, self.pre_data, self.st_raddr)
        return acc_ctr + pre_acc

    def post_randomize(self):
        return 
    #endclass: ctr_item

uvm_object_utils_begin(ctr_item)
uvm_field_int("acc_we", UVM_ALL_ON)
uvm_field_int("acc_addr", UVM_ALL_ON)
uvm_field_int("acc_width", UVM_ALL_ON)
uvm_field_int("acc_shift", UVM_ALL_ON)
uvm_field_int("acc_en", UVM_ALL_ON)
uvm_field_int("acc_data", UVM_ALL_ON)
uvm_field_int("ping_pong", UVM_ALL_ON)
uvm_field_int("pre_en", UVM_ALL_ON)
uvm_field_int("pre_data", UVM_ALL_ON)
uvm_field_int("pre_we", UVM_ALL_ON)
uvm_field_int("pre_waddr", UVM_ALL_ON)
uvm_field_int("st_raddr", UVM_ALL_ON)
uvm_object_utils_end(ctr_item)

