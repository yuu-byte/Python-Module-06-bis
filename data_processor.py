from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._stored_data: list[str] = []
        self._output_count: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        value = self._stored_data.pop(0)
        count = self._output_count
        self._output_count += 1
        return (count, value)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(value, (int, float)) for value in data)
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Invalid numeric data")

        if isinstance(data, list):
            for value in data:
                self._stored_data.append(str(value))
        else:
            self._stored_data.append(str(data))


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    processor = NumericProcessor()

    print(f"Trying to validate input '42': {processor.validate(42)}")
    print(f"Trying to validate input 'Hello': {processor.validate('Hello')}")

    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        processor.ingest("foo")
    except ValueError as e:
        print(f"Got exception: {e}")

    numbers = [1, 2, 3, 4, 5]
    print(f"Processing data: {numbers}")
    processor.ingest(numbers)

    print("Extracting 3 values...")
    for _ in range(3):
        count, value = processor.output()
        print(f"Numeric value {count}: {value}")



if __name__ == "__main__":
    main()
