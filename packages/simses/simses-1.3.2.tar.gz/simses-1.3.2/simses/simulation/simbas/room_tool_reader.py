from pandas import DataFrame, read_csv


class RoomToolReader:

    __ROOM_TOOL_REPORT_FILE: str = 'report.csv'

    __MANUFACTURER: str = "Manufacturer"
    __MODEL: str = "Model"
    __FORMAT: str = "Format"
    __CONFIGURATION: str = "Configuration"
    __VOLTAGE_MAX: str = "Voltage_max (V)"
    __VOLTAGE_MIN: str = "Voltage_min (V)"
    __VOLTAGE_NOM: str = "Voltage_nom (V)"
    __WEIGHT: str = "Weight (kg)"
    __VOLUME: str = "Volume (m^3)"
    __COOLING_TYPE: str = "Cooling type"
    __ENERGY: str = "Energy (Wh)"

    def __init__(self, cell: str):
        # * We need a matching between selected cell and room tool
        # * we need to adapt not only serial / parallel but also voltage and capacity -> overwriting config
        # * How could we scale such a solution?
        # -> maybe we should not try to solve the interface on this low level but maybe on a high level e.g. batch
        #    processing
        self.__data: DataFrame = self.__read_room_tool_report(cell)

    def __read_room_tool_report(self, cell: str):
        data: DataFrame = read_csv(self.__ROOM_TOOL_REPORT_FILE, header=0)
        # Workaround for selecting multiple reports from room tool
        first_row: DataFrame = data.iloc[0]
        print("RoomToolReader: Only first row is considered")
        print("RoomToolReader: Cell matching is not available")
        # Note: Please consider a name matching of cell names between SimSES and room tool
        cell_data: DataFrame = data.loc[(data[self.__MODEL] == cell)]
        return first_row

    def get_battery_scale(self) -> (int, int):
        first_values_serial_parallel: str = self.__data[self.__CONFIGURATION]
        serial: int = int(first_values_serial_parallel.partition("s")[0])
        parallel: int = int(first_values_serial_parallel.partition("s")[2][0:-1])
        return serial, parallel

    def get_energy(self) -> float:
        return float(self.__data[self.__ENERGY])

    def get_nominal_voltage(self) -> float:
        return float(self.__data[self.__VOLTAGE_NOM])
