import tzlocal

from stable_ethereum_rpc.stable_web3 import StableWeb3
from apscheduler.schedulers.background import BackgroundScheduler


class AvailableStableWeb3(StableWeb3):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        _job_mode = kwargs.get("job_mode")
        self.job_mode = _job_mode if _job_mode else "sufficient"
        self._schedule_module = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))
        self._callback_func = kwargs.get("callback_func")

    def run_job(self, **kwargs):
        if self.job_mode == "best":
            self._run_best_job(**kwargs)
        else:
            self._run_sufficient_job(**kwargs)

    def _run_sufficient(self):
        result = self.set_sufficient_web3()
        if callable(self._callback_func):
            self._callback_func(result)

    def _run_best(self):
        result = self.set_best_web3()
        if callable(self._callback_func):
            self._callback_func(result)

    def _run_sufficient_job(self, **kwargs):
        kwargs["id"] = "run_sufficient"
        kwargs["func"] = self._run_sufficient
        self._schedule_module.add_job(**kwargs)
        self._schedule_module.start()

    def _run_best_job(self, **kwargs):
        kwargs["id"] = "run_best"
        kwargs["func"] = self._run_best
        self._schedule_module.add_job(**kwargs)
        self._schedule_module.start()
