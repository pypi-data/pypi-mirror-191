"""Module for basic labjack interactions."""
from labjack import ljm


class DaqLabjack:
    """Basic class to use labjack as a data acquisition system (daq)."""

    def __init__(self) -> None:
        """Open connection to labjack."""
        self.handle = ljm.openS("T7", "ANY", "ANY")
        self.counters: list = []

    def read_port(self, port_name: str) -> float:
        """Read value from labjack port."""
        value = ljm.eReadName(self.handle, port_name)
        return value

    def set_up_counter(self, port_name: str) -> None:
        """Set up counter on a port."""
        ljm.eWriteName(self.handle, f"{port_name}_EF_ENABLE", 0)
        ljm.eWriteName(self.handle, f"{port_name}_EF_INDEX", 8)
        ljm.eWriteName(self.handle, f"{port_name}_EF_ENABLE", 1)
        print(f"Counter enabled: {port_name}")
        self.counters.append(port_name)

    def read_counter(self, port_name: str) -> int:
        """Read value from a counter."""
        count: float = ljm.eReadName(self.handle, f"{port_name}_EF_READ_A")
        count: int = int(count)
        return count


if __name__ == "__main__":
    daq = DaqLabjack()
    daq.set_up_counter("DIO2")
    while True:
        print(daq.read_counter("DIO2"))
