import os
import pandapower as pp
import pandas as pd
import numpy as np
import tempfile

from pandapower.timeseries import DFData
from pandapower.control import ConstControl
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
 
timesteps=70

class DataGenerator:
    def __init__(self) -> None:
        self.net = pp.create_empty_network()

    def source_network(self):

        #Create an empty network
        pp.set_user_pf_options(self.net, calculate_voltage_angles=True)
    
        bus1 = pp.create_bus(self.net, vn_kv=110 , name="Bus 1: Clark")
        bus2 = pp.create_bus(self.net, vn_kv=110 , name="Bus 2: Amherst")
        bus3 = pp.create_bus(self.net, vn_kv=110 , name="Bus 3: Winlock")
        bus4 = pp.create_bus(self.net, vn_kv=110 , name="Bus 4: Bowman")
        bus5 = pp.create_bus(self.net, vn_kv=110 , name="Bus 5: Troy")
        bus6 = pp.create_bus(self.net, vn_kv=110 , name="Bus 6: Maple")
        bus7 = pp.create_bus(self.net, vn_kv=110 , name="Bus 7: Grand")
        bus8 = pp.create_bus(self.net, vn_kv=110 , name="Bus 8: Wautaga")
        bus9 = pp.create_bus(self.net, vn_kv=110 , name="Bus 9: Cross")
        
        #Create transmission lines with length of 10 km
        line14 = pp.create_line(self.net, bus1, bus4, length_km=10, std_type='149-AL1/24-ST1A 110.0', name="Line 1 to 4")
        line28 = pp.create_line(self.net, bus2, bus8, length_km=10, std_type='149-AL1/24-ST1A 110.0', name='Line 2 to 8')
        line36 = pp.create_line(self.net, bus3, bus6, length_km=10, std_type='149-AL1/24-ST1A 110.0', name='Line 3 to 6')
        line45 = pp.create_line(self.net, bus4, bus5, length_km=10, std_type='149-AL1/24-ST1A 110.0', name='Line 4 to 5')
        line49 = pp.create_line(self.net, bus4, bus9, length_km=10, std_type='149-AL1/24-ST1A 110.0', name='Line 4 to 9')
        line56 = pp.create_line(self.net, bus5, bus6, length_km=10, std_type='149-AL1/24-ST1A 110.0', name='Line 5 to 6')
        line67 = pp.create_line(self.net, bus6, bus7, length_km=10, std_type='149-AL1/24-ST1A 110.0', name='Line 6 to 7')
        line78 = pp.create_line(self.net, bus7, bus8, length_km=10, std_type='149-AL1/24-ST1A 110.0', name='Line 7 to 8')
        line89 = pp.create_line(self.net, bus8, bus9, length_km=10, std_type='149-AL1/24-ST1A 110.0', name='Line 8 to 9')
        
        #Create generator elements
        gen1=pp.create_gen(self.net, bus1,p_mw= 0, slack=True, name='Generator 1')
        gen2=pp.create_gen(self.net, bus2,p_mw= 163, q_mvar=0, name='Generator 2')
        gen3=pp.create_gen(self.net, bus3,p_mw= 85, q_mvar=0, name='Generator 3')
        
        #Create load elements
        load5= pp.create_load(self.net, bus5, p_mw=90, q_mvar=30, name="Load 5")
        load7= pp.create_load(self.net, bus7, p_mw=100, q_mvar=35, name="Load 7")
        load9= pp.create_load(self.net, bus9, p_mw=125, q_mvar=50, name="Load 9")
        
        return self.net
    #Time series simulation for gernerating data set
    def source_data(self, net,time_steps):
    
        profiles = pd.DataFrame()
        #Normal Operation
        
        profiles['load5_p'] = 900 * 0.05 * np.random.random(time_steps)
        profiles['load5_q'] = 30* 0.05 * np.random.random(time_steps)
        
        profiles['load7_p'] = 100* 0.05 * np.random.random(time_steps)
        profiles['load7_q'] = 35* 0.05 * np.random.random(time_steps)
        
        profiles['load9_p'] = 125* 0.05 * np.random.random(time_steps)
        profiles['load9_q'] = 50* 0.05 * np.random.random(time_steps)
        
        ds = DFData(profiles)
        return profiles, ds        

    def highload_data(self, net,time_steps):
        #High Load Operation
        profiles = pd.DataFrame()   
        
        profiles['load5_p'] = 1.1 * 90 + (0.05 * np.random.random(time_steps) * 90)
        profiles['load5_q'] = 1.1 * 30 + (0.05 * np.random.random(time_steps) *30)
        
        profiles['load7_p'] = 1.1 * 100 + (0.05 * np.random.random(time_steps) * 100)
        profiles['load7_q'] = 1.1 * 35 + (0.05 * np.random.random(time_steps) *35)
        
        profiles['load9_p'] = 1.1 * 125 + (0.05 * np.random.random(time_steps) *15)
        profiles['load9_q'] = 1.1 * 50 + (0.05 * np.random.random(time_steps) *50)

        ds = DFData(profiles)
        return profiles, ds 

    def lowload_data(self, net,time_steps):
    #Low load Operation
        profiles = pd.DataFrame()    
        
        profiles['load5_p'] = 0.9 * 90 + (0.05 * np.random.random(time_steps) * 90)
        profiles['load5_q'] = 0.9 * 30 + (0.05 * np.random.random(time_steps) *30)
        
        profiles['load7_p'] = 0.9 * 100 + (0.05 * np.random.random(time_steps) * 100)
        profiles['load7_q'] = 0.9 * 35 + (0.05 * np.random.random(time_steps) *35)
        
        profiles['load9_p'] = 0.9 * 125 + (0.05 * np.random.random(time_steps) *15)
        profiles['load9_q'] = 0.9 * 50 + (0.05 * np.random.random(time_steps) *50)

        ds = DFData(profiles)
        return profiles, ds        

    #Create controllers to change the P and Q values of the load    
    def pq_controllers(self, net, ds):
        
            ConstControl(net, element='load', variable='p_mw', element_index=[0],
                        data_source=ds, profile_name=['load5_p'])
            ConstControl(net, element='load', variable='q_mvar', element_index=[0],
                        data_source=ds, profile_name=['load5_q'])
            ConstControl(net, element='load', variable='p_mw', element_index=[1],
                        data_source=ds, profile_name=['load7_p'])
            ConstControl(net, element='load', variable='q_mvar', element_index=[1],
                        data_source=ds, profile_name=['load7_q'])
            ConstControl(net, element='load', variable='p_mw', element_index=[2],
                        data_source=ds, profile_name=['load9_p'])
            ConstControl(net, element='load', variable='q_mvar', element_index=[2],
                        data_source=ds, profile_name=['load9_q'])
            return net


    def output_writer(self, net, time_steps,output_dir):
        ow = OutputWriter(net, time_steps, output_path=output_dir, output_file_type=".xlsx", log_variables=list())
        ow.log_variable('res_bus', 'vm_pu')
        ow.log_variable('res_bus', 'va_degree')
        return ow

    # net= source_network() 
    
    def operation_normal(self, net,timesteps):
        state_net=net
        network, ds = self.source_data(state_net,timesteps)
        controllers = self.pq_controllers(state_net, ds)
        ow = self.output_writer(state_net, timesteps,"./data/normal_operation/")
        run_timeseries(state_net,timesteps)

    def operation_highload(self,net,timesteps):
        state_net=net
        network, ds = self.highload_data(state_net,timesteps)
        controllers = self.pq_controllers(state_net, ds)
        ow = self.output_writer(state_net, timesteps,"./data/high_load/")
        run_timeseries(state_net,timesteps, calculate_voltage_angles=True)

    def operation_lowload(self, net,timesteps):
        state_net=net
        network, ds = self.lowload_data(state_net, timesteps)
        controllers = self.pq_controllers(state_net, ds)
        ow = self.output_writer(state_net, timesteps,"./data/low_load/")
        run_timeseries(state_net,timesteps, calculate_voltage_angles=True)

    def operation_genrdisconnect_highLoad(self, net,timesteps):
        state_net=net
        #Disconnect generator 3
        state_net.gen.in_service[2] = False
        network, ds = self.highload_data(state_net, timesteps)
        controllers = self.pq_controllers(state_net, ds)
        ow = self.output_writer(state_net, timesteps,"./data/disconnect_generator_3_high/")
        run_timeseries(state_net,timesteps, calculate_voltage_angles=True)
        state_net.gen.in_service[2] = True
        
    def operation_genrdisconnect_lowLoad(self, net,timesteps):
        state_net=net
        state_net.gen.in_service[2] = False
        network, ds = self.lowload_data(state_net, timesteps)
        controllers = self.pq_controllers(state_net, ds)
        ow = self.output_writer(state_net, timesteps,"./data/disconnect_generator_3_low/")
        run_timeseries(state_net,timesteps , calculate_voltage_angles=True)
        state_net.gen.in_service[2] = True    
        
    def operation_disconnectline_highLoad(self, net,timesteps):
        state_net=net
        #Disconnect line between bus 5 and 6 
        state_net.line.in_service[5] = False
        network, ds = self.highload_data(state_net, timesteps)
        controllers = self.pq_controllers(state_net, ds)
        ow = self.output_writer(state_net, timesteps,"./data/disconnect_line_bus_5_6_high/")
        run_timeseries(state_net,timesteps, calculate_voltage_angles=True)
        state_net.line.in_service[5] = True    

    def operation_disconnectline_lowLoad(self, net,timesteps):
        state_net=net
        state_net.line.in_service[5] = False
        network, ds = self.highload_data(state_net, timesteps)
        controllers = self.pq_controllers(state_net, ds)
        ow = self.output_writer(state_net, timesteps,"./data/disconnect_line_bus_5_6_low/")
        run_timeseries(state_net,timesteps, calculate_voltage_angles=True)
        state_net.gen.in_service[5] = True  

    def simulate(self, case, timesteps):
        operation = {
            'normal_operation': self.operation_normal,
            'high_load': self.operation_highload,
            'low_load': self.operation_lowload,
            'disconnect_generator_3_high': self.operation_genrdisconnect_highLoad,
            'disconnect_generator_3_low': self.operation_genrdisconnect_lowLoad,
            'disconnect_line_bus_5_6_high': self.operation_disconnectline_highLoad,
            'disconnect_line_bus_5_6_low': self.operation_disconnectline_lowLoad

        }
        operation[case](self.net, timesteps)
        return 1