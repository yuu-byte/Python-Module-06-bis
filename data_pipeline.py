from typing import Protocol


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
            value = value.replace("\"", "\\\"")
            json_entry = f'"item_{index}": "{value}"'
            json_entries.append(json_entry)

        json_string = "{" + ", ".join(json_entries) + "}"
        print("JSON Output:")
        print(json_string)
