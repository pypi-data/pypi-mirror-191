from configparser import ConfigParser

from simses.commons.config.generation.analysis import AnalysisConfigGenerator
from simses.commons.config.generation.simulation import SimulationConfigGenerator
from simses.commons.config.simulation.battery import BatteryConfig
from simses.simulation.batch_processing import BatchProcessing
from simses.simulation.simbas.room_tool_reader import RoomToolReader


class SimBAS(BatchProcessing):

    """
    This is the SimBAS example for BatchProcessing.
    """

    __CELL_CONFIG_FILE: str = 'cell_config.csv'
    __CELL_EXT: str = '.xml'

    def __init__(self, use_room_tool: bool = True):
        super().__init__(do_simulation=True, do_analysis=True)
        self.__use_room_tool: bool = use_room_tool

    def _setup_config(self) -> dict:
        # Example for config setup
        config_generator: SimulationConfigGenerator = SimulationConfigGenerator()
        # example: loading default config as base (not necessary)
        config_generator.load_default_config()
        config_generator.load_local_config()
        # defining parameters
        capacity: float = 22000.0
        ac_power: float = 105000.0
        voltage_ic: float = 300.0
        # generating config options
        config_generator.clear_storage_technology()
        dcdc_1: str = config_generator.add_fix_efficiency_dcdc(efficiency=0.98)
        acdc_1: str = config_generator.add_fix_efficiency_acdc()
        housing_1: str = config_generator.add_no_housing()
        hvac_1: str = config_generator.add_no_hvac()
        # generating storage systems
        config_generator.clear_storage_system_ac()
        config_generator.clear_storage_system_dc()
        # setting up multiple configurations with manual naming of simulations
        cell_config: [[str]] = self.__read_cell_config(self.__CELL_CONFIG_FILE)
        config_set: dict = dict()
        count: int = 0
        for cells in cell_config:
            serial, parallel = 1, 1
            config_generator.clear_storage_system_dc()
            config_generator.clear_storage_technology()
            for cell in cells:
                cell_type: str = 'IseaCellType;' + cell #+ self.__CELL_EXT
                if self.__use_room_tool:
                    room_tool_reader: RoomToolReader = RoomToolReader(cell=cell)
                    serial, parallel = room_tool_reader.get_battery_scale()
                    # print(serial, parallel)
                    capacity = room_tool_reader.get_energy()
                    voltage_ic = room_tool_reader.get_nominal_voltage()
                storage = config_generator.add_lithium_ion_battery(capacity=capacity, cell_type=cell_type)
                ac_system_1: str = config_generator.add_storage_system_ac(ac_power, voltage_ic, acdc_1, housing_1,
                                                                          hvac_1)
                config_generator.add_storage_system_dc(ac_system_1, dcdc_1, storage)
            count += 1
            config: ConfigParser = config_generator.get_config()
            # Attention: SimSES can only handle ONE serial/parallel config for ALL batteries
            # config.add_section('BATTERY')
            config.set(BatteryConfig.SECTION, BatteryConfig.CELL_SERIAL_SCALE, str(serial))
            config.set(BatteryConfig.SECTION, BatteryConfig.CELL_PARALLEL_SCALE, str(parallel))
            config_set['storage_' + str(count)] = config
            # for section in config.sections():
            #     print(section)
            #     print(dict(config.items(section)))
            # config_generator.show()
        return config_set

    def _analysis_config(self) -> ConfigParser:
        config_generator: AnalysisConfigGenerator = AnalysisConfigGenerator()
        config_generator.print_results(False)
        config_generator.do_plotting(True)
        config_generator.do_batch_analysis(True)
        return config_generator.get_config()

    def clean_up(self) -> None:
        pass

    def __read_cell_config(self, filename: str, delimiter: str = ',') -> [[str]]:
        cell_config: [[str]] = list()
        with open(filename, 'r', newline='') as file:
            for line in file:
                line: str = line.rstrip()
                if not line or line.startswith('#') or line.startswith('"'):
                    continue
                cell_config.append(line.split(delimiter))
        return cell_config


if __name__ == "__main__":
    batch_processing: BatchProcessing = SimBAS()
    batch_processing.run()
    batch_processing.clean_up()
