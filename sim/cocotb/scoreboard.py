from uvm.base import sv
from uvm.comps import UVMScoreboard
from uvm.macros import uvm_component_utils, uvm_info
from uvm.tlm1 import UVMAnalysisImp
from uvm import *

# uvm_analysis_imp_egr = uvm_analysis_imp_decl("_egr")
uvm_analysis_imp_ingrs = uvm_analysis_imp_decl("_ingrs")

class scoreboard(UVMScoreboard):

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        # self.egr = uvm_analysis_imp_egr("egr", self)
        self.ingrs = uvm_analysis_imp_ingrs("ingrs", self)
        self.n_obs_thresh = 10
        self.m_sb = []
        self.error = 0
        self.ingrs_cnt = 0
        self.m_n_obs = 0

    def build_phase(self, phase):
        thr = []
        if UVMConfigDb.get(self, "", "n_obs_thresh", thr):  # cast to 'void' removed
            self.n_obs_thresh = thr[0]
        uvm_info("SB Ingrs Port ", sv.sformatf("toatl number of transaction = %0d.", self.n_obs_thresh), UVM_LOW)


    def write_ingrs(self, tr):
        uvm_info("SB Ingrs Port", tr.convert2string(), UVM_LOW)
        self.m_sb.append(tr)
        self.ingrs_cnt += 1
        


    # def write_egr(self, tr):
    #     exp = 0x00
    #     uvm_info("SB Eger Port", tr.convert2string(), UVM_MEDIUM)
    #     exp = self.m_sb.pop(0)
    #     if tr.chr != exp:
    #         self.error = 1
    #         uvm_error("SB/MISMTCH", sv.sformatf("Symbol 0x%h observed instead of expected 0x%h",
    #             tr.chr, exp))
    #     self.m_n_obs += 1

    async def reset_phase(self, phase):
        self.m_n_obs = 0
        self.ingrs_cnt = 0
        self.m_sb = []

    async def main_phase(self, phase):
        phase.raise_objection(self, "Have not checked enough data")
        while True:
            uvm_info("SB Ingrs Port", sv.sformatf("ingrs_cnt = %0d, total = %0d",self.ingrs_cnt, self.n_obs_thresh), UVM_MEDIUM)
            await Timer(10, "NS")
            if self.ingrs_cnt >= self.n_obs_thresh:
                break
            # if self.m_n_obs > self.n_obs_thresh:
            #     break
        phase.drop_objection(self, "Enough data has been observed")
        uvm_info("SB", "all data abserved and main_phase droped in SB", UVM_MEDIUM)

    def check_phase(self, phase):
        if self.ingrs_cnt < self.n_obs_thresh:
        # if self.m_n_obs < self.n_obs_thresh:
            uvm_error("ERR/SCB", "Not enough items were observed")
            self.error = 1

uvm_component_utils(scoreboard)
