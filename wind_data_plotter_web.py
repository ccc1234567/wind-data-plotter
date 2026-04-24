# 导入所需库
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.font_manager as fm
import io
import os
import glob
import tempfile

# ================== 中英文列名映射表（请将您的完整映射粘贴至此）==================
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

def get_display_name(eng_name, translate=True):
    if not translate:
        return eng_name
    cn = COLUMN_CN_MAP.get(eng_name, "")
    return f"{cn} ({eng_name})" if cn else eng_name

# -------------------------- 静默加载字体（无任何输出）--------------------------
def load_custom_font():
    """静默加载 fonts 文件夹下的微软雅黑字体，不显示任何消息"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fonts_dir = os.path.join(base_dir, "fonts")
    font_path = None
    if os.path.exists(fonts_dir):
        for ext in ['*.ttf', '*.otf', ''.ttc']:
            matches = glob.glob(os.path.join(fonts_dir, ext))
            for match in matches:
                if 'msyh' in os.path.basename(match).lower():
                    font_path = match
                    break
            if font_path:
                break
    if font_path and os.path.exists(font_path):
        try:
            fm.fontManager.addfont(font_path)
            prop = fm.FontProperties(fname=font_path)
            font_name = prop.get_name()
            plt.rcParams['font.family'] = font_name
            plt.rcParams['axes.unicode_minus'] = False
        except Exception:
            pass  # 静默失败，使用默认字体

# -------------------------- 核心工具函数（保持不变）--------------------------
def detect_encoding(file_path):
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin1']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read(1000)
            return enc
        except UnicodeDecodeError:
            continue
    return 'utf-8'

def parse_file_sections(file_path, encoding):
    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
        lines = f.readlines()

    analog_col_line = None
    analog_start = None
    analog_end = None
    digital_col_line = None
    digital_start = None
    digital_end = None

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

    analog_start = analog_col_line + 1
    while analog_start < len(lines) and lines[analog_start].strip().startswith('#'):
        analog_start += 1
    if analog_start >= len(lines):
        raise ValueError("模拟信号无数据行")

    for i in range(analog_start, len(lines)):
        line = lines[i].strip()
        if '# ------- digital signals' in line.lower():
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

    if digital_col_line is not None:
        analog_end = digital_col_line - 1
    else:
        analog_end = len(lines)

    analog_col_line_raw = lines[analog_col_line].lstrip('#').strip()
    analog_col_names = [c.strip() for c in analog_col_line_raw.split(';') if c.strip()]

    digital_col_names = []
    if digital_col_line is not None:
        digital_col_line_raw = lines[digital_col_line].lstrip('#').strip()
        digital_col_names = [c.strip() for c in digital_col_line_raw.split(';') if c.strip()]

    return (analog_col_names, analog_start, analog_end,
            digital_col_names, digital_start, digital_end)

# -------------------------- Streamlit 主应用 --------------------------
def main():
    load_custom_font()

    st.set_page_config(page_title="B文件绘图工具", page_icon="🌬️", layout="wide")
    st.title("🌬️ 欢迎使用B文件绘图工具")

    with st.sidebar:
        st.header("📁 文件上传")
        uploaded_file = st.file_uploader("选择B文件（.txt/.csv）", type=["txt", "csv"])
        st.divider()
        st.header("⚙️ 绘图配置")
        translate = st.checkbox("显示中文列名", value=True)
        plot_type = st.radio("绘图类型", ["折线图", "散点图"], horizontal=True)
        show_preview = st.checkbox("显示数据预览", value=False)

    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            encoding = detect_encoding(tmp_file_path)
            (analog_col_names, analog_start, analog_end,
             digital_col_names, digital_start, digital_end) = parse_file_sections(tmp_file_path, encoding)

            with open(tmp_file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
            analog_data_lines = lines[analog_start:analog_end]
            analog_str = ''.join(analog_data_lines)
            analog_io = io.StringIO(analog_str)
            df_analog_raw = pd.read_csv(analog_io, sep=';', header=None, low_memory=False, na_values=["", " ", "NA", "N/A"])
            actual_analog_cols = df_analog_raw.shape[1]
            if actual_analog_cols != len(analog_col_names):
                if actual_analog_cols > len(analog_col_names):
                    df_analog_raw = df_analog_raw.iloc[:, :len(analog_col_names)]
                else:
                    analog_col_names = analog_col_names[:actual_analog_cols]
            df_analog_raw.columns = analog_col_names
            df_analog = df_analog_raw.apply(pd.to_numeric, errors='coerce')

            df_digital = None
            has_digital = (digital_start is not None and digital_end is not None and len(digital_col_names) > 0)
            if has_digital:
                digital_data_lines = lines[digital_start:digital_end]
                digital_str = ''.join(digital_data_lines)
                digital_io = io.StringIO(digital_str)
                df_digital_raw = pd.read_csv(digital_io, sep=';', header=None, low_memory=False, na_values=["", " ", "NA", "N/A"])
                actual_digital_cols = df_digital_raw.shape[1]
                if actual_digital_cols != len(digital_col_names):
                    if actual_digital_cols > len(digital_col_names):
                        df_digital_raw = df_digital_raw.iloc[:, :len(digital_col_names)]
                    else:
                        digital_col_names = digital_col_names[:actual_digital_cols]
                df_digital_raw.columns = digital_col_names
                df_digital = df_digital_raw.apply(pd.to_numeric, errors='coerce')

            # ========== 紧凑布局：一行显示数据集、X轴、Y轴 ==========
            with st.container():
                st.markdown("### 📐 绘图设置")

                dataset_options = ["模拟信号"]
                if has_digital:
                    dataset_options.append("数字信号")
                
                col_dataset, col_x, col_y = st.columns([1, 2, 3])
                
                with col_dataset:
                    selected_dataset = st.selectbox("选择数据集", dataset_options, key="dataset_select")
                
                if selected_dataset == "模拟信号":
                    df = df_analog
                    col_names = analog_col_names
                else:
                    df = df_digital
                    col_names = digital_col_names
                
                display_names = [get_display_name(col, translate) for col in col_names]
                col_name_map = {disp: orig for disp, orig in zip(display_names, col_names)}
                
                with col_x:
                    default_x_display = get_display_name("timestamp", translate) if "timestamp" in col_names else display_names[0]
                    selected_x_display = st.selectbox("X轴列", display_names, index=display_names.index(default_x_display), key="x_axis")
                    x_col = col_name_map[selected_x_display]
                
                with col_y:
                    default_y_display = [get_display_name("wind_speed", translate)] if "wind_speed" in col_names else []
                    selected_y_display = st.multiselect("Y轴列（多选）", display_names, default=default_y_display, key="y_axis")
                    y_cols = [col_name_map[disp] for disp in selected_y_display]

                if show_preview:
                    with st.expander("📈 数据预览（前10行）"):
                        st.dataframe(df.head(10), use_container_width=True)

                enable_zoom = st.checkbox("启用X轴范围限制（放大局部）", value=False)
                x_min_val = None
                x_max_val = None
                if enable_zoom and x_col in df.columns:
                    x_data = df[x_col].dropna()
                    if len(x_data) > 0:
                        x_min_global = float(x_data.min())
                        x_max_global = float(x_data.max())
                        zoom_col1, zoom_col2, zoom_col3 = st.columns(3)
                        with zoom_col1:
                            x_min_val = st.number_input(f"{selected_x_display} 最小值", value=x_min_global, format="%.6f")
                        with zoom_col2:
                            x_max_val = st.number_input(f"{selected_x_display} 最大值", value=x_max_global, format="%.6f")
                        with zoom_col3:
                            if st.button("重置范围"):
                                x_min_val = x_min_global
                                x_max_val = x_max_global
                                st.experimental_rerun()
                        if x_min_val >= x_max_val:
                            st.error("最小值必须小于最大值")
                            enable_zoom = False
                    else:
                        enable_zoom = False
                        st.warning("X轴列无有效数据，无法缩放")

            col_btn_left, col_btn_center, col_btn_right = st.columns([1, 2, 1])
            with col_btn_center:
                generate = st.button("🚀 生成图表", type="primary", use_container_width=True)

            if generate and y_cols:
                plot_df = df[[x_col] + y_cols].dropna()
                if len(plot_df) == 0:
                    st.error("❌ 所选列无有效数据，无法绘图！")
                else:
                    if enable_zoom and x_min_val is not None and x_max_val is not None:
                        mask = (plot_df[x_col] >= x_min_val) & (plot_df[x_col] <= x_max_val)
                        plot_df = plot_df[mask]
                        if len(plot_df) == 0:
                            st.warning("当前X轴范围内无数据，请扩大范围")
                            st.stop()

                    fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
                    colors = list(mcolors.TABLEAU_COLORS.values())
                    for idx, y_col in enumerate(y_cols):
                        y_display = get_display_name(y_col, translate)
                        if plot_type == "折线图":
                            ax.plot(plot_df[x_col], plot_df[y_col],
                                    label=y_display, color=colors[idx % len(colors)],
                                    linewidth=1.5, alpha=0.8)
                        else:
                            ax.scatter(plot_df[x_col], plot_df[y_col],
                                      label=y_display, color=colors[idx % len(colors)],
                                      s=2, alpha=0.6)

                    ax.set_xlabel(selected_x_display, fontsize=10)
                    ax.set_ylabel("数值", fontsize=10)
                    ax.set_title(f"{selected_dataset} - {plot_type}", fontsize=12, fontweight='bold')

                    # ========== 图例放在标题下方、图表上方（顶部居中，自动换行） ==========
                    # 根据 Y 轴列数动态设置图例列数（最多 5 列，避免过于拥挤）
                    ncol = min(len(y_cols), 5)
                    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=ncol, fontsize=8)

                    ax.grid(True, alpha=0.3)
                    plt.tight_layout()

                    # 图表居中显示
                    center_col1, center_col2, center_col3 = st.columns([1, 6, 1])
                    with center_col2:
                        st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ 处理文件失败：{str(e)}")
            st.exception(e)
    else:
        st.info("👆 请在左侧侧边栏上传B文件（.txt/.csv格式）")
        with st.expander("📖 使用说明", expanded=True):
            st.markdown("""
            ### 使用说明
            1. 上传文件后，在「绘图设置」区域选择数据集、X轴、Y轴（三个控件在同一行）；
            2. 可选「启用X轴范围限制」进行局部放大；
            3. 点击生成图表，图形会自动居中显示，图例会显示在标题下方。
            """)

if __name__ == "__main__":
    main()