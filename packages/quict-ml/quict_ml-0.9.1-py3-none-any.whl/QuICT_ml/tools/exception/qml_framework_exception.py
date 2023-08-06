from QuICT.tools.exception import QuICTException


class AnsatzAppendError(QuICTException):
    """Ansatz Append Operator Error."""

    def __init__(self, msg: str = None):
        super().__init__(3001, msg)


class AnsatzForwardError(QuICTException):
    """Ansatz Forward Operator Error."""

    def __init__(self, msg: str = None):
        super().__init__(3002, msg)


class GpuSimulatorForwardError(QuICTException):
    """GPU Simulator Forward Operator Error."""

    def __init__(self, msg: str = None):
        super().__init__(3003, msg)


class GpuSimulatorBackwardError(QuICTException):
    """GPU Simulator Backward Operator Error."""

    def __init__(self, msg: str = None):
        super().__init__(3004, msg)


class ModelRestoreError(QuICTException):
    """Model Restore Operator Error."""

    def __init__(self, msg: str = None):
        super().__init__(3005, msg)
