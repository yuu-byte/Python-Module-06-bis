from abc import ABC, abstractmethod
from typing import Any, Protocol


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


class ExportPlugin(Protocol):
    def process_output(
        self, data: list[tuple[int, str]]
    ) -> None:
        ...


class CSVPlugin:
    def process_output(
        self, data: list[tuple[int, str]]
    ) -> None:
        csv_values: list[str] = []

        for _, value in data:
            if "," in value or '"' in value or "\n" in value or "\r" in value:
                value = value.replace('"', '""')
                value = '"' + value + '"'
            csv_values.append(value)

        csv_string = ",".join(csv_values)
        print("CSV Output:")
        print(csv_string)


class JSONPlugin:
    def process_output(
        self, data: list[tuple[int, str]]
    ) -> None:
        json_entries: list[str] = []

        for index, value in data:
            value = value.replace("\\", "\\\\")
            value = value.replace('"', '\\"')
            value = value.replace("\n", "\\n")
            value = value.replace("\r", "\\r")
            value = value.replace("\t", "\\t")
            value = value.replace("\b", "\\b")
            value = value.replace("\f", "\\f")
            escaped_chars: list[str] = []
            for char in value:
                if ord(char) < 32:
                    escaped_char = f"\\u{ord(char):04x}"
                else:
                    escaped_char = char
                escaped_chars.append(escaped_char)

            value = "".join(escaped_chars)
            json_entry = f'"item_{index}": "{value}"'
            json_entries.append(json_entry)

        json_string = "{" + ", ".join(json_entries) + "}"
        print("JSON Output:")
        print(json_string)


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for input_data in stream:
            processed = False
            for registered_processor in self._processors:
                if registered_processor.validate(input_data):
                    registered_processor.ingest(input_data)
                    processed = True
                    break
            if not processed:
                print(
                    "DataStream error - Can't process "
                    f"element in stream: {input_data}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self._processors:
            print("No processor found, no data")
            return

        for processor in self._processors:
            name = type(processor).__name__
            name = name.replace("Processor", " Processor")

            remaining = len(processor._stored_data)
            total = processor._output_count + remaining

            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for processor in self._processors:
            output_data: list[tuple[int, str]] = []

            for _ in range(nb):
                if not processor._stored_data:
                    break
                output_data.append(processor.output())

            plugin.process_output(output_data)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===\n")
    print("Initialize Data Stream...\n")
    stream = DataStream()
    stream.print_processors_stats()
    print("\nRegistering Processors\n")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())
    first_batch = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {first_batch}")
    stream.process_stream(first_batch)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVPlugin())
    stream.print_processors_stats()

    second_batch = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"\nSend another batch of data: {second_batch}")
    stream.process_stream(second_batch)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONPlugin())
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
