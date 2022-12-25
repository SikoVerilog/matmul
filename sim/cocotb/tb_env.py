
from cocotb.triggers import RisingEdge, Timer

from uvm import *

from control.ctr_agent import ctr_agent
from scoreboard import scoreboard
from sequence import sequence

err_msg = ("Environment does not support jumping to phase %s from phase %s. " +
        "Only jumping to \"reset\" is supported")

timeout_ns = 200001 * 10


class tb_env(UVMEnv):

    #   local uvm_status_e   status
    #   local uvm_reg_data_t data
    #   local bit [1:0]      m_isr

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.vif = None
        self.ctr_agnt = None
        self.ingress = None
        self.seq = None

    def build_phase(self, phase):
        vif = []
        if not UVMConfigDb.get(self, "", "vif", vif):
           uvm_fatal("TB/ENV/NOVIF", "No virtual interface specified for environment instance")
        self.vif = vif[0]

        self.ctr_agnt = ctr_agent.type_id.create("ctr_agnt", self)

        self.ingress = scoreboard.type_id.create("ingress", self)

        UVMConfigDb.set(self, "self.ctr_agnt.sqr.main_phase", "default_sequence", sequence.type_id.get())
        # UVMConfigDb.set(self, "control_agent.main_phase","default_sequence", sequence.type_id.get())
        self.m_in_shutdown = 0

    def has_errors(self):
        return self.ingress.error


    def connect_phase(self, phase):
        self.ctr_agnt.mon.ap.connect(self.ingress.ingrs)


    # tpoikela: We should not fork anything in phase_started since it's not
    # async. The original SV example abuses this, and runs tasks.
    def phase_started(self, phase):
        name = phase.get_name()
        uvm_info("PHASE_STARTED/TB_ENV", "phase_started(): " + name, UVM_LOW)

        self.m_in_shutdown = 0
        #
        if name == "reset":
            uvm_info("PHASE_STARTED/TB_ENV", "In Reset Phase", UVM_LOW)

        elif name == "main":
            uvm_info("PHASE_STARTED/TB_ENV", "In Main Phase", UVM_LOW)

        elif name == "shutdown":
            uvm_info("PHASE_STARTED/TB_ENV", "In Shutdown Phase", UVM_LOW)
            self.m_in_shutdown = 1


    def phase_ended(self, phase):
        goto = phase.get_jump_target()
        name = phase.get_name()
        uvm_info("PHASE_ENDED/TB_ENV", "phase_ended(): " + name, UVM_LOW)

        # This environment supports jump to RESET *only*
        if goto is not None:
           if goto.get_name() != "reset":
               uvm_fatal("ENV/BADJMP", sv.sformatf(err_msg,
                   goto.get_name(), phase.get_name()))


        if phase.get_name() == "main":
            uvm_info("ENV/BADJMP", "In Main Phase", UVM_LOW)

        elif "shutdown":
            self.m_in_shutdown = 0


    async def pre_reset_phase(self, phase):
        phase.raise_objection(self, "Waiting for reset to be valid")
        while not (self.vif.arst_n.value.is_resolvable):
            await RisingEdge(self.vif.clk)
            uvm_info("WAIT_RST", "Waiting reset to become 0/1", UVM_MEDIUM)
        phase.drop_objection(self, "Reset is no longer X")

    async def reset_phase(self, phase):
        phase.raise_objection(self, "Env: Asserting reset for 10 clock cycles")

        uvm_info("TB/TRACE", "Resetting DUT...", UVM_NONE)

        self.vif.arst_n <= 0

        uvm_info("TB/TRACE", "Reset Asserted", UVM_NONE)
        for _ in range(10):
            await RisingEdge(self.vif.clk)
        self.vif.arst_n <= 1
        uvm_info("TB/TRACE", "Reset Deasserted", UVM_NONE)
        phase.drop_objection(self, "Env: HW reset done")


    async def pre_configure_phase(self, phase):
        phase.raise_objection(self, "Letting the interfaces go idle")
        uvm_info("TB/TRACE", "Configuring DUT...", UVM_NONE)
        for _ in range(10):
            await RisingEdge(self.vif.clk)
        phase.drop_objection(self, "Ready to configure")


    async def configure_phase(self, phase):
        phase.raise_objection(self, "Programming DUT")

        phase.drop_objection(self, "Everything is ready to go")

    async def main_phase(self, phase):
        uvm_info("TB/TRACE", "Applying primary stimulus...", UVM_NONE)
        phase.raise_objection(self, "control sequence OBJECTED")

        uvm_info("TEST_TOP", "Forking master_control Sequence now", UVM_LOW)
        master_seq = sequence("ctr_seq")
        master_proc = cocotb.fork(master_seq.start(self.ctr_agnt.sqr))
        # await self.seq.start(self.ctr_agnt.sqr)
        timeout_proc = cocotb.fork(self.timeout_and_finish(phase))
        await sv.fork_join_any([timeout_proc, master_proc])
        phase.drop_objection(self, "sequence or timeout occure")

    async def timeout_and_finish(self, phase):
        await Timer(timeout_ns, "NS")
        obj = phase.get_objection()
        obj.display_objections()
        uvm_fatal("ERR/TIMEOUT", "$finish. Timeout reached")
        # $finish

    async def shutdown_phase(self, phase):
        phase.raise_objection(self, "Draining the DUT")

        uvm_info("TB/TRACE", "Draining the DUT...", UVM_NONE)


        phase.drop_objection(self, "DUT is empty")


    def report_phase(self, phase):
        cs_ = UVMCoreService.get()
        svr = cs_.get_report_server()

        if (svr.get_severity_count(UVM_FATAL) +
                svr.get_severity_count(UVM_ERROR) == 0):
            print("** UVM TEST PASSED **\n")
        else:
            print("!! UVM TEST FAILED !!\n")

uvm_component_utils(tb_env)
