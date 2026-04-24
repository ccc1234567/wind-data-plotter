# wind_data_plotter_web.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io
import platform

# ================== 核心配置 ==================
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# ================== 中英文列名映射表（完整保留）==================
COLUMN_CN_MAP = {
    # 模拟信号（Analog Signals）
    "timestamp": "时间戳",
    "grid_U1": "电网电压U1",
    "grid_U2": "电网电压U2",
    "grid_U3": "电网电压U3",
    "grid_I1": "电网电流I1",
    "grid_I2": "电网电流I2",
    "grid_I3": "电网电流I3",
    "grid_frequency": "电网频率",
    "converter_in_power": "变流器输入有功功率",
    "converter_in_reactive_power": "变流器输入无功功率",
    "converter_in_mains_voltage": "变流器输入电网电压",
    "converter_in_line_current": "变流器输入线路电流",
    "converter_in_torque": "变流器输入转矩",
    "converter_in_speed": "变流器输入转速",
    "converter_out_torque_reference": "变流器输出转矩给定",
    "converter_out_q_power_reference": "变流器输出无功功率给定",
    "acceleration_nacelle_x": "机舱X向加速度",
    "acceleration_nacelle_y": "机舱Y向加速度",
    "acceleration_nacelle_effective_value": "机舱合成加速度有效值",
    "generator_speed_momentary": "发电机瞬时转速",
    "overspeed_modul_generator_speed_signal_1": "超速模块发电机转速信号1",
    "overspeed_modul_generator_speed_signal_2": "超速模块发电机转速信号2",
    "yaw_position": "偏航位置",
    "wind_speed": "风速",
    "average_wind_vane_wind_direction_30s": "30秒平均风向",
    "generator_speed_momentary_to_gh": "发送给GH控制器的发电机瞬时转速",
    "gh_control.FB_GH_CONTROLLER_1.test_second_order": "GH控制器二阶测试信号",
    "gh_control.FB_GH_CONTROLLER_1.test_notch_pitch": "GH控制器陷波滤波测试信号",
    "gh_control.local_info_pitch_position_demand": "GH控制器本地桨角位置需求",
    "gh_control.local_gh_control_torque_demand": "GH控制器本地转矩需求",
    "gh_pitch_rate_demand_1": "GH变桨速率需求1",
    "visu_feedback_limit_power_demand": "可视化反馈限功率需求",
    "yaw_speed": "偏航速度",
    "grid_active_power": "电网有功功率",
    "grid_reactive_power": "电网无功功率",
    "generator_temperature_momentary_max": "发电机瞬时最高温度",
    "yaw_position_2": "偏航位置2",
    "converter_in_DC_voltage": "变流器输入直流电压",
    "converter_in_inner_state": "变流器内部状态",
    "converter_in_inner_temperature_word": "变流器内部温度字",
    "visu_stop_mode_word": "可视化停机模式字",
    "visu_total_limit_power_mode": "可视化总限功率模式",
    "force_test_parameter_1": "强制测试参数1",
    "force_test_parameter_2": "强制测试参数2",
    "gh_pitch_rate_demand_2": "GH变桨速率需求2",
    "gh_pitch_rate_demand_3": "GH变桨速率需求3",
    "main_loop_mode_number": "主循环模式号",
    "yaw_speed_2": "偏航速度2",
    "wind_speed_2": "风速2",
    "wind_vane_wind_direction_2": "风向标风向2",
    "WoodWard_Power_Meter.FB_WoodWard_Power_Meter_1.woodward_Errorld_real": "Woodward功率计错误ID实部",
    "WoodWard_Power_Meter.FB_WoodWard_Power_Meter_1.Modbus_RTU_Error_counter": "Woodward功率计Modbus RTU错误计数",
    "ptich_vensys_control.local_speed_demand_1": "VenSys变桨本地转速需求1",
    "pitch_control_motor_speed_setpoint_1": "变桨电机转速设定点1",
    "in_vensys_capacitor_voltage_hi_1": "VenSys高压电容电压1",
    "in_vensys_capacitor_voltage_hi_2": "VenSys高压电容电压2",
    "in_vensys_capacitor_voltage_hi_3": "VenSys高压电容电压3",
    "pitch_position_blade_1": "桨叶1桨距角位置",
    "pitch_position_blade_2": "桨叶2桨距角位置",
    "pitch_position_blade_3": "桨叶3桨距角位置",
    "in_vensys_speed_momentary_blade_1": "VenSys桨叶1瞬时转速",
    "in_vensys_speed_momentary_blade_2": "VenSys桨叶2瞬时转速",
    "in_vensys_speed_momentary_blade_3": "VenSys桨叶3瞬时转速",
    "in_vensys_capacitor_voltage_mid_1": "VenSys中压电容电压1",
    "in_vensys_capacitor_voltage_mid_2": "VenSys中压电容电压2",
    "in_vensys_capacitor_voltage_mid_3": "VenSys中压电容电压3",
    "in_vensys_error_word1_1": "VenSys错误字1-1",
    "in_vensys_error_word2_1": "VenSys错误字2-1",
    "in_vensys_error_word3_1": "VenSys错误字3-1",
    "in_vensys_error_word1_2": "VenSys错误字1-2",
    "in_vensys_error_word2_2": "VenSys错误字2-2",
    "in_vensys_error_word3_2": "VenSys错误字3-2",
    "in_vensys_error_word1_3": "VenSys错误字1-3",
    "in_vensys_error_word2_3": "VenSys错误字2-3",
    "in_vensys_error_word3_3": "VenSys错误字3-3",
    "in_goldwind_kehua_error_code_1": "金风/科华错误代码1",
    "in_goldwind_kehua_error_code_2": "金风/科华错误代码2",
    "in_goldwind_kehua_error_code_3": "金风/科华错误代码3",
    "in_vensys_motor_temperature_1": "VenSys电机温度1",
    "in_vensys_motor_temperature_2": "VenSys电机温度2",
    "in_vensys_motor_temperature_3": "VenSys电机温度3",
    "in_ac2_state_word_1": "AC2状态字1",
    "in_ac2_state_word_2": "AC2状态字2",
    "in_ac2_state_word_3": "AC2状态字3",
    "in_ac2_alarm_code_1": "AC2报警代码1",
    "in_ac2_alarm_code_2": "AC2报警代码2",
    "in_ac2_alarm_code_3": "AC2报警代码3",
    "in_ac2_motor_current_1": "AC2电机电流1",
    "in_ac2_motor_current_2": "AC2电机电流2",
    "in_ac2_motor_current_3": "AC2电机电流3",
    "in_ac2_motor_temp_1": "AC2电机温度1",
    "in_ac2_motor_temp_2": "AC2电机温度2",
    "in_ac2_motor_temp_3": "AC2电机温度3",
    "in_24V_brake_voltage_1": "24V制动电压1",
    "in_24V_brake_voltage_2": "24V制动电压2",
    "in_24V_brake_voltage_3": "24V制动电压3",
    "in_ac2_motor_voltage_1": "AC2电机电压1",
    "in_ac2_motor_voltage_2": "AC2电机电压2",
    "in_ac2_motor_voltage_3": "AC2电机电压3",
    "wPitch1DiagCode": "桨叶1诊断代码",
    "wPitch2DiagCode": "桨叶2诊断代码",
    "wPitch3DiagCode": "桨叶3诊断代码",
    "wPitch1BrakRlyCntNum": "桨叶1制动继电器计数",
    "wPitch2BrakRlyCntNum": "桨叶2制动继电器计数",
    "wPitch3BrakRlyCntNum": "桨叶3制动继电器计数",
    "_ClearanceSys.rLaserLOS1Clearance_m": "间隙系统激光LOS1间隙(m)",
    "_ClearanceSys.rLaserLOS2Clearance_m": "间隙系统激光LOS2间隙(m)",
    "_ClearanceSys.rLaserLOS3Clearance_m": "间隙系统激光LOS3间隙(m)",
    "gh_control.FB_GH_CONTROLLER_1.speed_set_point": "GH控制器转速设定点",
    "PitMinSelect.Out.rPitchMin": "最小桨角选择输出",
    "VisuWaterRunMode": "可视化水冷运行模式",
    "_ClearanceSys.MO_rMeasuredClearance_m": "间隙系统实测间隙(m)",
    "wCnvMainErrCode": "变流器主错误代码",
    "wCnvDynamicErrCode": "变流器动态错误代码",
    "wCnvMainWarningCode": "变流器主警告代码",
    "wCnvDynamicWarningCode": "变流器动态警告代码",
    "GenOverSpdMonitor": "发电机超速监视器",

    # 数字信号（Digital Signals）部分
    "converter_msw_rdy_on": "变流器主状态字_就绪开机",
    "converter_msw_rdy_run": "变流器主状态字_就绪运行",
    "converter_msw_rdy_ref": "变流器主状态字_就绪给定",
    "converter_msw_tripped": "变流器主状态字_跳闸",
    "converter_msw_alarm": "变流器主状态字_报警",
    "converter_msw_heating_request": "变流器主状态字_加热请求",
    "converter_msw_remote": "变流器主状态字_远程",
    "profi_in_converter_signal_ready_for_start": "Profibus输入_变流器准备启动",
    "safety_clamp_in_safety_system_ok_from_converter": "安全钳输入_安全系统正常（来自变流器）",
    "profi_out_converter_signal_start_enable": "Profibus输出_变流器启动使能",
    "profi_out_converter_signal_emergency_stop": "Profibus输出_紧急停机",
    "profi_out_converter_signal_emergency_stop_reset": "Profibus输出_紧急停机复位",
    "converter_mcw_start": "变流器控制字_启动",
    "converter_mcw_run": "变流器控制字_运行",
    "converter_mcw_reset": "变流器控制字_复位",
    "global_LVRT_flag": "全局低电压穿越标志",
    "converter_msw_lvrt_over": "变流器主状态字_低电压穿越结束",
    "converter_msw_line_unit_running": "变流器主状态字_线路单元运行",
    "converter_mcw_gird_run": "变流器控制字_并网运行",
    "profi_in_yaw_left_feedback": "Profibus输入_左偏航反馈",
    "profi_in_yaw_right_feedback": "Profibus输入_右偏航反馈",
    "profi_in_gen_cooling_high_speed_feedback": "Profibus输入_发电机高速冷却反馈",
    "profi_in_gen_cooling_low_speed_feedback": "Profibus输入_发电机低速冷却反馈",
    "converter_warm_up_wanted": "变流器需要预热",
    "converter_msw_HVRT_active": "变流器主状态字_高电压穿越激活",
    "converter_msw_HVRT_over_time": "变流器主状态字_高电压穿越超时",
    "visu_limit_active_power_flag": "可视化限有功功率标志",
    "force_test_actived": "强制测试激活",
    "force_test_finished": "强制测试完成",
    "profi_in_zero_contact_correction": "Profibus输入_零接触校正",
    "WoodWard_Power_Meter.FB_WoodWard_Power_Meter_1.busy": "Woodward功率计忙",
    "Com_ModbusRtu.Error": "Modbus RTU通信错误",
    "WoodWard_Power_Meter.FB_WoodWard_Power_Meter_1.local_woodward_comm_error": "Woodward本地通信错误",
    "WoodWard_Power_Meter.FB_WoodWard_Power_Meter_1.woodward_comm_error": "Woodward通信错误",
    "in_vensys_converter_ok_1": "VenSys变流器正常1",
    "in_vensys_converter_ok_2": "VenSys变流器正常2",
    "in_vensys_converter_ok_3": "VenSys变流器正常3",
    "in_vensys_end_switch_1": "VenSys限位开关1",
    "in_vensys_end_switch_2": "VenSys限位开关2",
    "in_vensys_end_switch_3": "VenSys限位开关3",
    "in_vensys_power_supply_ok_1": "VenSys电源正常1",
    "in_vensys_power_supply_ok_2": "VenSys电源正常2",
    "in_vensys_power_supply_ok_3": "VenSys电源正常3",
    "in_outside_safety_chain_1_ok_1": "外部安全链1正常1",
    "in_outside_safety_chain_1_ok_2": "外部安全链1正常2",
    "in_outside_safety_chain_1_ok_3": "外部安全链1正常3",
    "in_outside_safety_chain_2_ok_1": "外部安全链2正常1",
    "in_outside_safety_chain_2_ok_2": "外部安全链2正常2",
    "in_outside_safety_chain_2_ok_3": "外部安全链2正常3",
    "in_vensys_safety_system_ok_1_1": "VenSys安全系统正常1-1",
    "in_vensys_safety_system_ok_1_2": "VenSys安全系统正常1-2",
    "in_vensys_safety_system_ok_1_3": "VenSys安全系统正常1-3",
    "in_vensys_safety_system_ok_2_1": "VenSys安全系统正常2-1",
    "in_vensys_safety_system_ok_2_2": "VenSys安全系统正常2-2",
    "in_vensys_safety_system_ok_2_3": "VenSys安全系统正常2-3",
    "in_vensys_5_position_sensor_1": "VenSys5位位置传感器1",
    "in_vensys_5_position_sensor_2": "VenSys5位位置传感器2",
    "in_vensys_5_position_sensor_3": "VenSys5位位置传感器3",
    "in_vensys_87_position_sensor_1": "VenSys87位位置传感器1",
    "in_vensys_87_position_sensor_2": "VenSys87位位置传感器2",
    "in_vensys_87_position_sensor_3": "VenSys87位位置传感器3",
    "visu_ActivePowTAboveRated": "可视化有功功率超额定",
    "profi_in_yaw_position_input_1": "Profibus输入_偏航位置输入1",
    "profi_in_yaw_position_input_2": "Profibus输入_偏航位置输入2",

    # 另一套模拟信号（对应第一种文件格式）
    "WindSpeed": "风速",
    "WindDirction": "风向",
    "PowerLimitDemand": "功率限制需求",
    "GwCtrlPowerDemand": "金风控制器功率需求",
    "GridPower": "电网功率",
    "TorqueDemand": "转矩需求",
    "CnvTorque": "变流器转矩",
    "GeneratorSpeedToGwCtrl": "发送给金风控制器的发电机转速",
    "Cnv1Speed": "变流器1转速",
    "PowerLimitEvent": "功率限制事件",
    "OverSpeed1": "超速1",
    "OverSpeed2": "超速2",
    "ReactivePowerDemand": "无功功率需求",
    "CnvReactivePower": "变流器无功功率",
    "GridReactivePower": "电网无功功率",
    "GridU1": "电网电压U1",
    "GridU2": "电网电压U2",
    "GridU3": "电网电压U3",
    "GridI1": "电网电流I1",
    "GridI2": "电网电流I2",
    "GridI3": "电网电流I3",
    "GridFreq": "电网频率",
    "AccX": "X向加速度",
    "AccY": "Y向加速度",
    "AccEffectiveValue": "合成加速度有效值",
    "YawPositon": "偏航位置",
    "MainLoopNumber": "主循环号",
    "CnvGridSideVoltage": "变流器电网侧电压",
    "CnvGridSideCurrent": "变流器电网侧电流",
    "CnvGenSideVoltage": "变流器发电机侧电压",
    "CnvGenSideCurrent": "变流器发电机侧电流",
    "CnvDcVoltage": "变流器直流电压",
    "CnvIdCurrent": "变流器Id电流",
    "IncAngNacX": "机舱X倾角",
    "IncAngNacY": "机舱Y倾角",
    "Acc2X": "加速度2X",
    "Acc2Y": "加速度2Y",
    "Pitch1DCVoltage": "桨叶1直流电压",
    "Pitch1CapacitorU1": "桨叶1电容电压U1",
    "LidarRWS5": "激光雷达RWS5",
    "Pitch1ControlWord": "桨叶1控制字",
    "Pitch1CabState1": "桨叶1机柜状态1",
    "Pitch1CabState2": "桨叶1机柜状态2",
    "Pitch1MotorCurrent": "桨叶1电机电流",
    "Qmax": "Q最大值",
    "Pitch1CnvStatus": "桨叶1变流器状态",
    "Pitch1Position": "桨叶1位置",
    "LP_ShaftPowerSetpointTarget": "低速轴功率设定目标",
    "VsprFilteredSpeedTorque": "VSPR滤波转速/转矩",
    "Pitch2DCVoltage": "桨叶2直流电压",
    "Pitch2CapacitorU1": "桨叶2电容电压U1",
    "LidarRWS6": "激光雷达RWS6",
    "Pitch2ControlWord": "桨叶2控制字",
    "Pitch2CabState1": "桨叶2机柜状态1",
    "Pitch2CabState2": "桨叶2机柜状态2",
    "Pitch2MotorCurrent": "桨叶2电机电流",
    "rPitchDemand1": "变桨需求1",
    "Pitch2CnvStatus": "桨叶2变流器状态",
    "Pitch2Position": "桨叶2位置",
    "VsprSpeedSetpointTorque": "VSPR转速设定/转矩",
    "VsprDyRateExtra": "VSPR动态速率附加",
    "Pitch3DCVoltage": "桨叶3直流电压",
    "Pitch3CapacitorU1": "桨叶3电容电压U1",
    "LidarRWS7": "激光雷达RWS7",
    "Pitch3ControlWord": "桨叶3控制字",
    "Pitch3CabState1": "桨叶3机柜状态1",
    "Pitch3CabState2": "桨叶3机柜状态2",
    "Pitch3MotorCurrent": "桨叶3电机电流",
    "VsprDyExtra": "VSPR动态附加",
    "Pitch3CnvStatus": "桨叶3变流器状态",
    "Pitch3Position": "桨叶3位置",
    "AlgRotorAzimuth": "算法转子方位角",
    "PitDem0": "变桨需求0",
    "PitchMainFaultCode": "变桨主故障代码",
    "PitchDynaFaultCode": "变桨动态故障代码",
    "LidarU0LH2_MovAv": "激光雷达U0LH2移动平均",
    "PitchSysModeNumber": "变桨系统模式号",
    "PitchSysCtrlWord1": "变桨系统控制字1",
    "PitchSysCtrlWord2": "变桨系统控制字2",
    "VsprFilteredSpeedPitch": "VSPR滤波转速/桨角",
    "GearBoxOilPumpInletPress": "齿轮箱油泵入口压力",
    "Pitch3CtrlSysDmdSpd": "桨叶3控制系统需求转速",
    "CtrlSysPosDmd": "控制系统位置需求",
    "ShaftPowerSetpoint": "轴功率设定点",
    "AlgMinimumPitchAngle": "算法最小桨角",
    "GenTorqueSetPoint": "发电机转矩设定点",
    "GenSpeedSetPoint": "发电机转速设定点",
    "AlgSpeedSetpointLimit": "算法转速设定限制",
    "LimMinPitAngle": "最小桨角限制",
    "Qmin": "Q最小值",
    "VsprState": "VSPR状态",
    "StopLevel": "停机等级",
    "Torque0": "转矩0",
    "Cnv1ActivePower": "变流器1有功功率",
    "Filter_ExpectedPitchAngle1": "滤波后预期桨角1",
    "VSPR_ExpectedPitchAngle1": "VSPR预期桨角1",
    "VSPR_AlgPcsTorqueDemand": "VSPR算法PCS转矩需求",
    "MeasuredClearance_m": "实测间隙(m)",
    "iPit1PosDmd": "变桨1位置需求",
    "iPit2PosDmd": "变桨2位置需求",
    "iPit3PosDmd": "变桨3位置需求",
    "StateMachineAbnormalWord": "状态机异常字",
    "CtrlAbnormalWord": "控制异常字",
    "InputErrWord": "输入错误字",
    "rOveSpdGen1_rpm": "发电机超速1(rpm)",
    "rOveSpdGen2_rpm": "发电机超速2(rpm)",
    "AboveRated": "超额定",
    "iAvailLowCnt": "可用性低计数",
    "u_0LFF": "u_0LFF",
    "LowTurCtrllntensity": "低湍流控制强度",
    "FaultFlag": "故障标志",
    "LidarLOS": "激光雷达LOS",
    "LidarRWS0": "激光雷达RWS0",
    "LowTurCtrlMeanspd": "低湍流控制平均转速",
    "AGCMode": "AGC模式",
    "LidarRWS9": "激光雷达RWS9",
    "LidarRWS1": "激光雷达RWS1",
    "LidarU0LV1_MovAv": "激光雷达U0LV1移动平均",
    "LidarU0LV2_MovAv": "激光雷达U0LV2移动平均",
    "LidarU0LH1_MovAv": "激光雷达U0LH1移动平均",
    "LidarRWS2": "激光雷达RWS2",
    "LidarRWS3": "激光雷达RWS3",
    "rGearBoxOilPumpOutletPress": "齿轮箱油泵出口压力",
    "YawMotor1L1Current_A": "偏航电机1L1电流(A)",
    "LidarRWS8": "激光雷达RWS8",
    "iTorqDmd": "转矩需求",
    "GenSpeedCauXsLater": "发电机转速后续计算",
    "YawMotor2L1Current_A": "偏航电机2L1电流(A)",
    "DTQTorque": "DTQ转矩",
    "rAccXMaxMagA_g": "X向最大加速度幅值(g)",
    "rAccYMaxMagA_g": "Y向最大加速度幅值(g)",
    "Pitch1Speed": "桨叶1转速",
    "Pitch2Speed": "桨叶2转速",
    "Pitch3Speed": "桨叶3转速",
    "Pitch1Torque": "桨叶1转矩",
    "Pitch2Torque": "桨叶2转矩",
    "Pitch3Torque": "桨叶3转矩",
    "rAccXMaxFreqA_Hz": "X向最大加速度频率(Hz)",
    "rAccYMaxFreqA_Hz": "Y向最大加速度频率(Hz)",
    "GainCoefficient": "增益系数",
    "TestData": "测试数据",
    "ClearanceDataState": "间隙数据状态",
    "RotAz": "转子方位角",
    "WaveLen1": "波长1",
    "WaveLen2": "波长2",
    "WaveLen3": "波长3",
    "WaveLen5": "波长5",
    "WaveLen6": "波长6",
    "WaveLen7": "波长7",
    "WaveLen9": "波长9",
    "WaveLen10": "波长10",
    "WaveLen11": "波长11",
    "Edgewise1": "摆振方向1",
    "Edgewise2": "摆振方向2",
    "Edgewise3": "摆振方向3",
    "Flapwise1": "挥舞方向1",
    "Flapwise2": "挥舞方向2",
    "Flapwise3": "挥舞方向3",
    "iState": "状态",
    "MinPos": "最小位置",
    "MinPitchEvent": "最小桨角事件",
    "rTowAccAZero_g": "塔筒A向加速度零点(g)",
    "rTowAccBZero_g": "塔筒B向加速度零点(g)",
}

# ================== 工具函数 ==================
def detect_encoding(file_content):
    """检测文件编码"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin1']
    for enc in encodings:
        try:
            file_content.decode(enc)
            return enc
        except UnicodeDecodeError:
            continue
    return 'utf-8'

def parse_file_sections(file_content, encoding):
    """解析B文件的模拟/数字信号分区"""
    lines = file_content.decode(encoding).splitlines()
    
    analog_col_line = None
    analog_start = None
    analog_end = None
    digital_col_line = None
    digital_start = None
    digital_end = None

    # 查找模拟信号列名行
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith('#'):
            break
        if stripped.count(';') >= 10:
            lower = stripped.lower()
            if any(kw in lower for kw in ['buffersave', 'version', '-------', 'analog signals']):
                continue
            analog_col_line = i
            break

    if analog_col_line is None:
        raise ValueError("未找到模拟信号列名行")

    # 确定模拟信号数据起始行
    analog_start = analog_col_line + 1
    while analog_start < len(lines) and lines[analog_start].strip().startswith('#'):
        analog_start += 1
    if analog_start >= len(lines):
        raise ValueError("模拟信号无数据行")

    # 查找数字信号分区
    for i in range(analog_start, len(lines)):
        line = lines[i].strip()
        if '# ------- digital signals' in line.lower():
            # 查找数字信号列名行
            for j in range(i+1, min(i+20, len(lines))):
                l = lines[j].strip()
                if l.startswith('#') and l.count(';') >= 10 and not any(kw in l.lower() for kw in ['buffersave', 'version', '-------']):
                    digital_col_line = j
                    break
            if digital_col_line is not None:
                digital_start = digital_col_line + 1
                while digital_start < len(lines) and lines[digital_start].strip().startswith('#'):
                    digital_start += 1
                digital_end = len(lines)
            break

    # 确定模拟信号结束行
    if digital_col_line is not None:
        analog_end = digital_col_line - 1
    else:
        analog_end = len(lines)

    # 解析列名
    analog_col_line_raw = lines[analog_col_line].lstrip('#').strip()
    analog_col_names = [c.strip() for c in analog_col_line_raw.split(';') if c.strip()]

    digital_col_names = []
    if digital_col_line is not None:
        digital_col_line_raw = lines[digital_col_line].lstrip('#').strip()
        digital_col_names = [c.strip() for c in digital_col_line_raw.split(';') if c.strip()]

    return (analog_col_names, analog_start, analog_end,
            digital_col_names, digital_start, digital_end)

def get_display_name(eng_name, translate=True):
    """获取列的显示名称（中英文切换）"""
    if not translate:
        return eng_name
    cn = COLUMN_CN_MAP.get(eng_name, "")
    return f"{cn} ({eng_name})" if cn else eng_name

# ================== 主应用逻辑 ==================
def main():
    st.set_page_config(
        page_title="金风风机B文件绘图工具（Web版）",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 金风风机B文件绘图工具（Web版）")
    
    # 初始化会话状态
    if 'df_analog' not in st.session_state:
        st.session_state.df_analog = None
    if 'df_digital' not in st.session_state:
        st.session_state.df_digital = None
    if 'current_df' not in st.session_state:
        st.session_state.current_df = None
    if 'translate' not in st.session_state:
        st.session_state.translate = True

    # ========== 侧边栏配置 ==========
    with st.sidebar:
        st.header("🔧 配置面板")
        
        # 1. 文件上传
        uploaded_file = st.file_uploader(
            "选择B文件（TXT/CSV）",
            type=["txt", "csv"],
            help="支持金风风机B格式的txt/csv数据文件"
        )

        # 2. 读取文件
        if uploaded_file is not None:
            try:
                file_content = uploaded_file.getvalue()
                encoding = detect_encoding(file_content)
                (analog_col_names, analog_start, analog_end,
                 digital_col_names, digital_start, digital_end) = parse_file_sections(file_content, encoding)

                # 解析模拟信号数据
                lines = file_content.decode(encoding).splitlines()
                analog_data_lines = lines[analog_start:analog_end]
                analog_str = '\n'.join(analog_data_lines)
                analog_io = io.StringIO(analog_str)
                df_analog_raw = pd.read_csv(analog_io, sep=';', header=None, low_memory=False, na_values=["", " ", "NA", "N/A"])
                
                # 列数对齐
                actual_analog_cols = df_analog_raw.shape[1]
                if actual_analog_cols != len(analog_col_names):
                    if actual_analog_cols > len(analog_col_names):
                        df_analog_raw = df_analog_raw.iloc[:, :len(analog_col_names)]
                    else:
                        analog_col_names = analog_col_names[:actual_analog_cols]
                df_analog_raw.columns = analog_col_names
                st.session_state.df_analog = df_analog_raw.apply(pd.to_numeric, errors='coerce')

                # 解析数字信号数据
                st.session_state.df_digital = None
                has_digital = (digital_start is not None and digital_end is not None and len(digital_col_names) > 0)
                if has_digital:
                    digital_data_lines = lines[digital_start:digital_end]
                    digital_str = '\n'.join(digital_data_lines)
                    digital_io = io.StringIO(digital_str)
                    df_digital_raw = pd.read_csv(digital_io, sep=';', header=None, low_memory=False, na_values=["", " ", "NA", "N/A"])
                    actual_digital_cols = df_digital_raw.shape[1]
                    if actual_digital_cols != len(digital_col_names):
                        if actual_digital_cols > len(digital_col_names):
                            df_digital_raw = df_digital_raw.iloc[:, :len(digital_col_names)]
                        else:
                            digital_col_names = digital_col_names[:actual_digital_cols]
                    df_digital_raw.columns = digital_col_names
                    st.session_state.df_digital = df_digital_raw.apply(pd.to_numeric, errors='coerce')

                st.success(f"文件读取成功！\n模拟信号：{len(st.session_state.df_analog)}行 x {len(st.session_state.df_analog.columns)}列" +
                           (f"\n数字信号：{len(st.session_state.df_digital)}行 x {len(st.session_state.df_digital.columns)}列" if has_digital else ""))

            except Exception as e:
                st.error(f"文件读取失败：{str(e)}")
                st.session_state.df_analog = None
                st.session_state.df_digital = None

        # 3. 数据集选择
        if st.session_state.df_analog is not None:
            dataset_options = ["模拟信号"]
            if st.session_state.df_digital is not None:
                dataset_options.append("数字信号")
            
            selected_dataset = st.selectbox(
                "选择数据集",
                dataset_options,
                index=0,
                help="选择要可视化的数据集类型"
            )

            # 更新当前数据集
            if selected_dataset == "模拟信号":
                st.session_state.current_df = st.session_state.df_analog
            else:
                st.session_state.current_df = st.session_state.df_digital

            # 4. 中英文切换
            st.session_state.translate = st.checkbox(
                "显示中文列名",
                value=True,
                help="勾选后列名显示为「中文(英文)」格式，取消则显示纯英文"
            )

            # 5. X轴选择
            all_cols = st.session_state.current_df.columns.tolist()
            display_names = [get_display_name(col, st.session_state.translate) for col in all_cols]
            x_col_display = st.selectbox(
                "选择X轴列",
                display_names,
                index=display_names.index(get_display_name('timestamp', st.session_state.translate)) if 'timestamp' in all_cols else 0,
                help="通常选择时间戳（timestamp/Time）作为X轴"
            )
            # 反向映射回原始英文列名
            x_col_name = all_cols[display_names.index(x_col_display)]

            # 6. 列搜索与选择
            st.subheader("📋 Y轴列选择")
            search_key = st.text_input("搜索列名", placeholder="输入关键词筛选列...")
            
            # 筛选列
            filtered_cols = []
            filtered_display = []
            for col, disp in zip(all_cols, display_names):
                if search_key.lower() in col.lower() or search_key.lower() in disp.lower():
                    filtered_cols.append(col)
                    filtered_display.append(disp)
            
            # 多选Y轴列
            selected_display = st.multiselect(
                "选择要绘制的列（可多选）",
                filtered_display,
                help="按住Ctrl/Shift可多选列"
            )
            selected_cols = [filtered_cols[filtered_display.index(disp)] for disp in selected_display]

            # 7. 绘图类型选择
            plot_type = st.radio(
                "选择绘图类型",
                ["折线图", "散点图"],
                index=0,
                horizontal=True
            )

            # 8. 功能按钮
            col1, col2 = st.columns(2)
            with col1:
                plot_btn = st.button("🎨 绘制图表", type="primary")
            with col2:
                preview_btn = st.button("📈 数据预览/诊断")

    # ========== 主内容区 ==========
    if uploaded_file is None:
        st.info("请在左侧面板上传金风风机B格式的TXT/CSV文件开始分析")
        # 显示使用说明
        with st.expander("📖 使用说明"):
            st.markdown("""
            ### 金风风机B文件绘图工具（Web版）使用说明
            1. **文件上传**：点击左侧「选择B文件」上传txt/csv格式的风机B文件
            2. **数据集选择**：文件解析后可选择「模拟信号」/「数字信号」数据集
            3. **列名切换**：勾选「显示中文列名」可切换列名的中英文显示
            4. **X轴选择**：选择作为X轴的列（推荐选择时间戳timestamp）
            5. **Y轴选择**：通过搜索框筛选列，多选需要绘制的Y轴列
            6. **绘图类型**：选择折线图/散点图
            7. **功能按钮**：
               - 绘制图表：生成选中列的可视化图表
               - 数据预览：查看数据的基本信息和诊断结果
            """)
        
        with st.expander("ℹ️ 关于"):
            st.markdown("""
            ### 关于工具
            - 版本：2.2（Web版）
            - 适配：金风风机B格式数据文件
            - 功能：解析模拟/数字信号、列名中英文映射、多列可视化、数据诊断
            """)
        return

    # 数据预览/诊断功能
    if preview_btn and st.session_state.current_df is not None:
        st.subheader("📈 数据预览/诊断")
        tab1, tab2, tab3 = st.tabs(["数据预览", "数据信息", "缺失值分析"])
        
        with tab1:
            st.dataframe(st.session_state.current_df.head(50), use_container_width=True)
        
        with tab2:
            buffer = io.StringIO()
            st.session_state.current_df.info(buf=buffer)
            st.text(buffer.getvalue())
        
        with tab3:
            missing_stats = st.session_state.current_df.isnull().sum()
            missing_stats = missing_stats[missing_stats > 0]
            if len(missing_stats) > 0:
                st.write("### 缺失值统计（仅显示有缺失值的列）")
                st.dataframe(
                    pd.DataFrame({
                        "缺失值数量": missing_stats,
                        "缺失值占比(%)": (missing_stats / len(st.session_state.current_df) * 100).round(2)
                    }),
                    use_container_width=True
                )
            else:
                st.success("✅ 数据无缺失值")

    # 绘图功能
    if plot_btn and st.session_state.current_df is not None and len(selected_cols) > 0:
        st.subheader(f"🎨 绘图结果：{plot_type}")
        
        # 准备绘图数据
        df_plot = st.session_state.current_df.copy()
        x_data = df_plot[x_col_name]
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
        colors = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.BASE_COLORS.values())
        
        for i, col in enumerate(selected_cols):
            y_data = df_plot[col]
            color = colors[i % len(colors)]
            disp_name = get_display_name(col, st.session_state.translate)
            
            if plot_type == "折线图":
                ax.plot(x_data, y_data, label=disp_name, color=color, linewidth=1)
            else:
                ax.scatter(x_data, y_data, label=disp_name, color=color, s=1, alpha=0.8)
        
        # 图表美化
        ax.set_xlabel(get_display_name(x_col_name, st.session_state.translate), fontsize=10)
        ax.set_ylabel("数值", fontsize=10)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # 显示图表
        st.pyplot(fig)

        # 下载图表按钮
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        st.download_button(
            label="📥 下载图表",
            data=buf,
            file_name=f"风机数据_{plot_type}_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.png",
            mime="image/png"
        )

    # 无选中列的提示
    if plot_btn and len(selected_cols) == 0 and st.session_state.current_df is not None:
        st.warning("⚠️ 请至少选择一个Y轴列进行绘图")

if __name__ == "__main__":
    main()
