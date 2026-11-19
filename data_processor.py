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


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(value, str) for value in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Invalid text data")

        if isinstance(data, list):
            for value in data:
                self._stored_data.append(value)
        else:
            self._stored_data.append(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in data.items()
            )

        if isinstance(data, list):
            return all(
                isinstance(log, dict)
                and all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in log.items()
                )
                for log in data
            )
        return False

    def ingest(
        self, data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Invalid log data")

        if isinstance(data, list):
            for log in data:
                self._stored_data.append(self._format_log(log))
        else:
            self._stored_data.append(self._format_log(data))

    def _format_log(self, log: dict[str, str]) -> str:
        if "log_level" in log and "log_message" in log:
            return f"{log['log_level']}: {log['log_message']}"
        return str(log)


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    numeric_processor = NumericProcessor()

    print(f"Trying to validate input '42': {numeric_processor.validate(42)}")
    print(f"Trying to validate 'Hello': {numeric_processor.validate('Hello')}")

    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric_processor.ingest("foo")
    except ValueError as e:
        print(f"Got exception: {e}")

    numbers: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {numbers}")
    numeric_processor.ingest(numbers)

    print("Extracting 3 values...")
    for _ in range(3):
        count, value = numeric_processor.output()
        print(f"Numeric value {count}: {value}")

    print("\nTesting Text Processor...")
    text_processor = TextProcessor()

    print(f"Trying to validate input '42': {text_processor.validate(42)}")

    data = ["Hello", "Nexus", "World"]
    print(f"Validating {data}: {text_processor.validate(data)}")
    print(f"Processing data: {data}")
    text_processor.ingest(data)

    print("Extracting 1 value...")
    count, value = text_processor.output()
    print(f"Text value {count}: {value}")

    print("\nTesting Log Processor...")
    log_processor = LogProcessor()

    print(f"Trying to validate 'Hello': {log_processor.validate('Hello')}")

    logs = [
        {
            "log_level": "NOTICE",
            "log_message": "Connection to server"
        },
        {
            "log_level": "ERROR",
            "log_message": "Unauthorized access!!"
        }
    ]

    print(f"Trying to validate log list: {log_processor.validate(logs)}")
    print(f"Processing data: {logs}")
    log_processor.ingest(logs)

    print("Extracting 2 values...")
    for _ in range(2):
        count, value = log_processor.output()
        print(f"Log entry {count}: {value}")


if __name__ == "__main__":
    main()
