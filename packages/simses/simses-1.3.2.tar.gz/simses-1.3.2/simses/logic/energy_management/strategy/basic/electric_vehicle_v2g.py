from simses.commons.config.simulation.general import GeneralSimulationConfig
from simses.commons.profile.power.power_profile import PowerProfile
from simses.commons.profile.power.v2g_profile import V2GProfile
from simses.commons.profile.technical.binary import BinaryProfile
from simses.commons.config.simulation.profile import ProfileConfig
from simses.commons.config.simulation.energy_management import EnergyManagementConfig
from simses.commons.state.energy_management import EnergyManagementState
from simses.commons.state.system import SystemState
from simses.logic.energy_management.strategy.operation_priority import OperationPriority
from simses.logic.energy_management.strategy.operation_strategy import OperationStrategy
import numpy as np


class ElectricVehicleV2G(OperationStrategy):

    """
    ElectricVehicle is a basic operation strategy which simulates an EV during trips and recharge. The algorithm
    requires the following profiles and parameters:
    - A load profile that contains the required (and recuperated) power while driving
    - A binary profile that contains ones when the EV is parked & can be charged and zeros if not
    - A string for the parameter 'EV_CHARGING_STRATEGY' which can be:
        - "Uncontrolled": Always recharge, if SOC<100% and parked at "home"
        - "Mean_Power": This strategy checks the next departure time (perfect foresight) and chooses the charging power
            to reach 100% SOC exactly at departure time.
        - "Paused, integer threshold value": This strategy charges immediately after arrival until a threshold value
            (e.g. 0.8 -> 80% SOC). Then the charging is paused. The charging continues with maximal grid power at the
            time (t = Delta_E/P) that allows 100% SOC to be reached at the next departure time (with 30 minutes buffer).

    - The maximal grid power is set in the 'ENERGY_MANAGEMENT' section as 'MAX_POWER'
    - Using load and binary profile from emobpy, the LOAD_SCALING_FACTOR in [PROFILE] section should be set to 1

    Whenever the EV is not parked & ready to charge (binary=0), the EMS just follows the load profile.
    If the car is parked & ready to charge (binary=1), it is recharged depending on 'EV_CHARGING_STRATEGY'.
    """

    def __init__(self, config: GeneralSimulationConfig, profile_config: ProfileConfig, ems_config: EnergyManagementConfig,
                 power_profile: PowerProfile, v2g_profile: V2GProfile):

        super().__init__(OperationPriority.MEDIUM)

        self.__load_profile_driving: PowerProfile = power_profile
        self.__binary_profile = BinaryProfile(config, profile_config)
        self.__v2g_profile: V2GProfile = v2g_profile

        self.__power: float = 0.0
        self.__binary: bool = False
        self.__soc_to_charge: float = 0.0
        self.__charging_strategy = ems_config.ev_charging_strategy
        self.__max_ac_grid_power = ems_config.max_power
        self.__fast_charging_event = 0
        self.__time_counter_postponed_trip = 0
        self.__postponed_trip = []
        self.__Wh_to_Ws = 3600
        self.__next_time_zero = None
        self.__timestep = config.timestep


    def next(self, time: float, system_state: SystemState, power: float = 0) -> float:
        self.__power = self.__load_profile_driving.next(time)
        self.__binary = bool(np.round(self.__binary_profile.next(time)))
        self.__v2g_power = self.__v2g_profile.next(time)

        if self.__binary != False and self.__binary != True:
            raise ValueError("The binary profile contains values different from 0 or 1!")

        if not self.__binary:                      # if EV is not at home: use load profile value
            # Possibly binary profile must also be shifted if fast charging is required on a long trip!
            # Right now, the break for fast charging is neglected (trip becomes shorter)
            if system_state.soc < 0.02:
                self.__fast_charging_event = 1
            if system_state.soc > 0.80:
                self.__fast_charging_event = 0

            if self.__fast_charging_event == 1:
                self.__postponed_trip.append(-1.0 * self.__power)

                power = 150000
            else:
                #if len(self.__postponed_trip):
                #    power = self.__postponed_trip.pop(0)
                #    self.__postponed_trip.append(-1.0 * self.__power)
                #else:
                power = 1.0 * self.__power
        elif system_state.soc == 1:                 # if EV is at home and SOC=100%: do nothing
            power = 0
        elif self.__charging_strategy == 'Uncontrolled':   # if EV is at home and SOC!=100%: Recharge with charging strategy
            power = self.__max_ac_grid_power

        elif self.__charging_strategy == 'Mean_power':  # Charge with mean power to be fully charged at departure time

            if self.__next_time_zero == None:
                self.__next_time_zero = self.__binary_profile.next_zero(time)

            charging_duration = self.__next_time_zero - time
            capacity_to_charge = (1 - system_state.soc) * system_state.capacity * self.__Wh_to_Ws
            if charging_duration > 0:
                power = capacity_to_charge / charging_duration
            else:
                power=0

            if charging_duration == self.__timestep:
                self.__next_time_zero = None


        elif self.__charging_strategy[0:6] == 'Paused':
            threshold = float(self.__charging_strategy[-3:])
            if system_state.soc < threshold:
                power = self.__max_ac_grid_power
            else:
                if self.__next_time_zero == None:
                    self.__next_time_zero = self.__binary_profile.next_zero(time)
                else:
                    charging_duration = (1-system_state.soc)*system_state.capacity*self.__Wh_to_Ws/self.__max_ac_grid_power
                    charging_restart_time = self.__next_time_zero - charging_duration - 1800
                    # start recharging after the pause, buffer of 30 minutes (1800s)
                    if time < charging_restart_time:
                        power = 0
                    else:
                        power = self.__max_ac_grid_power
                        if self.__next_time_zero - time < self.__timestep:
                            self.__next_time_zero = None


        return power

    def update(self, energy_management_state: EnergyManagementState) -> None:
        energy_management_state.load_power = self.__power

    def clear(self) -> None:
        self.__power = 0.0

    def close(self) -> None:
        self.__binary_profile.close()
        self.__load_profile_driving.close()
