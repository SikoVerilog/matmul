from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_info
from uvm.macros.uvm_sequence_defines import uvm_do_with
from uvm.base import sv, UVM_LOW
from control.ctr_item import ctr_item


#   acc_we = 0  # Write enable
#   acc_addr = 0  # Address
#   acc_width = 0  # write with
#   acc_shift = 0  # byte shift
#   acc_en = 0 # accumlation enable
#   acc_data = 0
#   ping_pong = 0
#   pre_en = 0
#   pre_data = 0
#   pre_we = 0
#   pre_waddr = 0
#   st_raddr = 0

class sequence(UVMSequence):

    def __init__(self, name="sequence"):
        UVMSequence.__init__(self, name)
        self.set_automatic_phase_objection(1)

    async def body(self):
        for i in range(10):
            req = ctr_item()
            uvm_info(self.get_name(), "item Started", UVM_LOW)
            await self.start_item(req)
            if i < 2047:
                req.ping_pong = 0
            else:
                req.ping_pong = 1
            req.pre_en = 1
            req.pre_we = 1
            req.pre_waddr = i
            req.pre_data = i
            req.st_raddr = 0
            req.acc_we = 0
            req.acc_en = 0
            await self.finish_item(req)
        uvm_info(self.get_name(), "Sequence finish", UVM_LOW)
        
        # await uvm_do_with(self, self.req, lambda addr: addr == self.start_addr)
        #      { req.addr == start_addr
        #        req.read_write == READ
        #        req.size == 1
        #        req.error_pos == 1000
        #        req.transmit_delay == transmit_del; } )
        # rsp = []
        # await self.get_response(rsp)
        # self.rsp = rsp[0]
        # uvm_info(self.get_name(),
        #     sv.sformatf("%s read : addr = `x{}, data[0] = `x{}",
        #         self.get_sequence_path(), self.rsp.addr, self.rsp.data[0]),
        #     UVM_HIGH)


uvm_object_utils(sequence)