"""Module for basic labjack interactions."""
import datetime
import time

from labjack import ljm


class DaqLabjack:
    """Basic class to use labjack as a data acquisition system (daq)."""

    def __init__(self) -> None:
        """Open connection to labjack."""
        self.handle = ljm.openS("T7", "ANY", "ANY")
        self.counters: dict[str, str] = {}

    def read_port(self, port_name: str) -> float:
        """Read value from labjack port."""
        value = ljm.eReadName(self.handle, port_name)
        return value

    def add_counter(self, counter_name: str, port_name: str) -> None:
        """Set up counter on a port."""
        ljm.eWriteName(self.handle, f"{port_name}_EF_ENABLE", 0)
        ljm.eWriteName(self.handle, f"{port_name}_EF_INDEX", 8)
        ljm.eWriteName(self.handle, f"{port_name}_EF_ENABLE", 1)
        print(f"Counter enabled: {port_name}")
        self.counters[counter_name] = port_name

    def remove_counter(self, counter_name: str) -> None:
        """Deactivate counter."""
        port_name = self.counters[counter_name]
        ljm.eWriteName(self.handle, f"{port_name}_EF_ENABLE", 0)
        del self.counters[counter_name]

    def read_counter_by_port(self, port_name: str) -> int:
        """Read value from a counter using the name of its port (e.g. DIO2)."""
        count: float = ljm.eReadName(self.handle, f"{port_name}_EF_READ_A")
        count: int = int(count)
        return count

    def read_counter_by_name(self, counter_name: str) -> int:
        """Read value from a counter using user-specified name."""
        port_name = self.counters[counter_name]
        count = self.read_counter_by_port(port_name)
        return count

    def read_all_counters(self) -> dict:
        """Read all currently configured counters."""
        values = {}
        for counter_name, port_name in self.counters.items():
            values[counter_name] = self.read_counter_by_port(port_name)
        return values


if __name__ == "__main__":
    daq = DaqLabjack()
    daq.add_counter("eye_camera", "DIO2")
    while True:
        print(datetime.datetime.now(), daq.read_all_counters())
        time.sleep(1)
