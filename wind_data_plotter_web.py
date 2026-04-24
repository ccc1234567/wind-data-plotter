# 导入所需库
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.colors as mcolors
import sys
import platform
import io
import matplotlib

# ========== 解决Matplotlib中文乱码核心配置 ==========
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']  # Windows中文字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示方块问题
matplotlib.rcParams['font.family'] = 'sans-serif'

# -------------------------- 隐藏控制台窗口（仅Windows）--------------------------
def hide_console():
    if platform.system() == "Windows":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            user32.ShowWindow(hwnd, 0)

# -------------------------- 预定义颜色列表 --------------------------
COLORS = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.BASE_COLORS.values())

# ================== 中英文列名映射表 ==================
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

class WindDataPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("金风风机B文件绘图工具")
        self.root.geometry("1280x750")

        # ========== Tkinter中文显示配置 ==========
        if platform.system() == "Windows":
            default_font = tk.font.nametofont("TkDefaultFont")
            default_font.configure(family="微软雅黑", size=9)
            self.root.option_add("*Font", default_font)

        self.file_path = tk.StringVar()
        self.df = None
        self.df_analog = None
        self.df_digital = None
        self.current_dataset = tk.StringVar(value="模拟信号")
        self.x_col_name = None
        self.filtered_cols = []      # 原始英文列名
        self.filtered_display_names = []  # 显示名称
        self.plot_type = tk.StringVar(value="line")
        self.translate = tk.BooleanVar(value=True)   # 汉译开关，默认开启

        # ========== 创建主框架 ==========
        # 顶部控制栏（文件、X轴、绘图类型等）
        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # 左侧列选择面板（宽度固定为280）
        self.left_frame = tk.Frame(root, width=280, bg='#f0f0f0')
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=5, pady=5)
        self.left_frame.pack_propagate(False)

        # 右侧绘图面板（自动填充剩余空间）
        self.right_frame = ttk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ---------- 顶部控件 ----------
        # 文件选择行
        file_frame = ttk.Frame(self.top_frame)
        file_frame.pack(fill=tk.X, pady=2)
        ttk.Label(file_frame, text="数据文件：").pack(side=tk.LEFT, padx=5)
        ttk.Entry(file_frame, textvariable=self.file_path, width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="选择文件", command=self.select_file).pack(side=tk.LEFT, padx=5)
        self.status_label = ttk.Label(file_frame, text="未读取数据", foreground="gray")
        self.status_label.pack(side=tk.LEFT, padx=20)

        # 数据集、X轴、绘图类型行
        ctrl_frame = ttk.Frame(self.top_frame)
        ctrl_frame.pack(fill=tk.X, pady=2)

        # 数据集选择（初始隐藏）
        self.dataset_label = ttk.Label(ctrl_frame, text="数据集：")
        self.dataset_combo = ttk.Combobox(ctrl_frame, values=["模拟信号"], state="readonly", width=15)
        self.dataset_combo.bind("<<ComboboxSelected>>", self.on_dataset_changed)
        self.dataset_label_created = False

        # X轴选择
        ttk.Label(ctrl_frame, text="X轴列：").pack(side=tk.LEFT, padx=5)
        self.x_axis_combo = ttk.Combobox(ctrl_frame, width=18, state="readonly")
        self.x_axis_combo.pack(side=tk.LEFT, padx=5)
        self.x_axis_combo.bind("<<ComboboxSelected>>", self.on_x_axis_changed)
        ttk.Button(ctrl_frame, text="刷新X轴", command=self.refresh_x_options).pack(side=tk.LEFT, padx=2)

        # 绘图类型
        ttk.Label(ctrl_frame, text="绘图类型：").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(ctrl_frame, text="散点图", variable=self.plot_type, value="scatter").pack(side=tk.LEFT)
        ttk.Radiobutton(ctrl_frame, text="折线图", variable=self.plot_type, value="line").pack(side=tk.LEFT, padx=5)

        # 汉译开关
        self.translate_cb = ttk.Checkbutton(ctrl_frame, text="中文", variable=self.translate, command=self.on_translate_toggled)
        self.translate_cb.pack(side=tk.LEFT, padx=10)

        # ---------- 左侧列选择面板 ----------
        search_frame = ttk.Frame(self.left_frame)
        search_frame.pack(fill=tk.X, pady=2, padx=5)
        ttk.Label(search_frame, text="搜索：").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", self.search_columns)
        self.plot_button = tk.Button(search_frame, text="绘图", command=self.plot_data,
                                     bg="#4caf50", fg="white", font=("微软雅黑", 9, "bold"))
        self.plot_button.pack(side=tk.LEFT, padx=5)

        # 列表框 + 双滚动条
        listbox_frame = ttk.Frame(self.left_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
        v_scroll = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        h_scroll = ttk.Scrollbar(listbox_frame, orient=tk.HORIZONTAL)
        self.col_listbox = tk.Listbox(
            listbox_frame,
            selectmode=tk.MULTIPLE,
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set,
            font=("微软雅黑", 9),
            width=40,
            height=20
        )
        v_scroll.config(command=self.col_listbox.yview)
        h_scroll.config(command=self.col_listbox.xview)
        self.col_listbox.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        listbox_frame.grid_rowconfigure(0, weight=1)
        listbox_frame.grid_columnconfigure(0, weight=1)

        # 按钮行
        btn_frame = ttk.Frame(self.left_frame)
        btn_frame.pack(fill=tk.X, pady=5, padx=5)
        ttk.Button(btn_frame, text="取消全部勾选", command=self.clear_selection).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="数据预览/诊断", command=self.show_data_preview).pack(side=tk.LEFT, padx=5)

        # ---------- 右侧绘图区域 ----------
        self.fig, self.ax = plt.subplots(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.right_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 菜单栏
        self.create_menubar()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # -------------------------- 菜单栏相关 --------------------------
    def create_menubar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_separator()
        help_menu.add_command(label="关于", command=self.show_about)

    def show_help(self):
        help_win = tk.Toplevel(self.root)
        help_win.title("使用说明")
        help_win.geometry("650x500")
        text = tk.Text(help_win, wrap=tk.WORD, font=("微软雅黑", 10))
        text.pack(fill=tk.BOTH, expand=True)
        help_str = """金风风机B文件绘图工具 使用说明
1. 点击“选择文件”打开B文件（.txt/.csv）。
2. 若文件包含数字信号，会自动显示“数据集”下拉框，可切换模拟/数字信号。
3. 左侧列表框中显示所有列（默认显示“中文(英文)”格式，可取消“中文”开关切换为纯英文）。
4. 可多选列（Ctrl+单击，Shift+连续选择）作为Y轴数据。
5. 选择X轴列（通常为时间戳）。
6. 选择绘图类型（散点图/折线图）。
7. 点击“绘图”生成曲线。
8. 工具栏支持缩放、平移、保存图片。
        """
        text.insert(tk.END, help_str)
        text.config(state=tk.DISABLED)
        ttk.Button(help_win, text="关闭", command=help_win.destroy).pack(pady=5)

    def show_about(self):
        messagebox.showinfo("关于", "金风风机B文件绘图工具\n版本 2.2\n作者：赵伟东\n联系方式：17600382113")

    # -------------------------- 列名显示相关 --------------------------
    def get_display_name(self, eng_name):
        """根据汉译开关返回显示名称"""
        if not self.translate.get():
            return eng_name
        cn = COLUMN_CN_MAP.get(eng_name, "")
        return f"{cn} ({eng_name})" if cn else eng_name

    def on_translate_toggled(self):
        """汉译开关切换时刷新显示"""
        self.refresh_all_display_names()

    def refresh_all_display_names(self):
        """刷新所有列的显示名称"""
        if self.df is None:
            return
        self.all_display_names = [self.get_display_name(col) for col in self.all_original_cols]
        # 重新应用搜索过滤
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            self.filtered_cols = self.all_original_cols.copy()
            self.filtered_display_names = self.all_display_names.copy()
        else:
            filtered = []
            disp_filtered = []
            for orig, disp in zip(self.all_original_cols, self.all_display_names):
                if keyword in orig.lower() or keyword in disp.lower():
                    filtered.append(orig)
                    disp_filtered.append(disp)
            self.filtered_cols = filtered
            self.filtered_display_names = disp_filtered
        self.refresh_listbox()
        # 刷新X轴下拉选项
        self.refresh_x_options()
        # 重置X轴显示
        if self.x_col_name:
            self.x_axis_combo.set(self.get_display_name(self.x_col_name))

    def refresh_listbox(self):
        """刷新列表框内容"""
        self.col_listbox.delete(0, tk.END)
        for name in self.filtered_display_names:
            self.col_listbox.insert(tk.END, name)

    def search_columns(self, event=None):
        """搜索列"""
        if self.df is None:
            return
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            self.filtered_cols = self.all_original_cols.copy()
            self.filtered_display_names = self.all_display_names.copy()
        else:
            self.filtered_cols = []
            self.filtered_display_names = []
            for orig, disp in zip(self.all_original_cols, self.all_display_names):
                if keyword in orig.lower() or keyword in disp.lower():
                    self.filtered_cols.append(orig)
                    self.filtered_display_names.append(disp)
        self.refresh_listbox()

    # -------------------------- 文件读取相关 --------------------------
    def detect_encoding(self, file_path):
        """检测文件编码"""
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin1']
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    f.read(1000)
                return enc
            except UnicodeDecodeError:
                continue
        return 'utf-8'

    def parse_file_sections(self, file_path, encoding):
        """解析文件的模拟/数字信号分区"""
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            lines = f.readlines()

        analog_col_line = None
        analog_start = None
        analog_end = None
        digital_col_line = None
        digital_start = None
        digital_end = None

        # 找模拟信号列名行
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

        # 找模拟信号数据起始行
        analog_start = analog_col_line + 1
        while analog_start < len(lines) and lines[analog_start].strip().startswith('#'):
            analog_start += 1
        if analog_start >= len(lines):
            raise ValueError("模拟信号无数据行")

        # 找数字信号分区
        for i in range(analog_start, len(lines)):
            line = lines[i].strip()
            if '# ------- digital signals' in line.lower():
                # 找数字信号列名行
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

    def select_file(self):
        """选择文件"""
        file = filedialog.askopenfilename(
            title="选择数据文件",
            filetypes=[("TXT文件", "*.txt"), ("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        if file:
            self.file_path.set(file)
            self.read_data_file()

    def read_data_file(self):
        """读取数据文件"""
        try:
            file_path = self.file_path.get()
            encoding = self.detect_encoding(file_path)
            (analog_col_names, analog_start, analog_end,
             digital_col_names, digital_start, digital_end) = self.parse_file_sections(file_path, encoding)

            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
            
            # 读取模拟信号数据
            analog_data_lines = lines[analog_start:analog_end]
            analog_str = ''.join(analog_data_lines)
            analog_io = io.StringIO(analog_str)
            df_analog_raw = pd.read_csv(analog_io, sep=';', header=None, low_memory=False, na_values=["", " ", "NA", "N/A"])

            # 对齐列数
            actual_analog_cols = df_analog_raw.shape[1]
            if actual_analog_cols != len(analog_col_names):
                if actual_analog_cols > len(analog_col_names):
                    df_analog_raw = df_analog_raw.iloc[:, :len(analog_col_names)]
                else:
                    analog_col_names = analog_col_names[:actual_analog_cols]
            df_analog_raw.columns = analog_col_names
            self.df_analog = df_analog_raw.apply(pd.to_numeric, errors='coerce')

            # 读取数字信号数据
            self.df_digital = None
            has_digital = (digital_start is not None and digital_end is not None and len(digital_col_names) > 0)
            ctrl_frame = self.top_frame.winfo_children()[1]
            
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
                self.df_digital = df_digital_raw.apply(pd.to_numeric, errors='coerce')

                # 显示数据集选择框
                if not self.dataset_label_created:
                    self.dataset_label.pack(side=tk.LEFT, padx=5)
                    self.dataset_combo.pack(side=tk.LEFT, padx=5)
                    self.dataset_label_created = True
                self.dataset_combo['values'] = ["模拟信号", "数字信号"]
                self.dataset_combo.set("模拟信号")
            else:
                # 隐藏数据集选择框
                if self.dataset_label_created:
                    self.dataset_label.pack_forget()
                    self.dataset_combo.pack_forget()
                    self.dataset_label_created = False
                self.dataset_combo['values'] = ["模拟信号"]
                self.dataset_combo.set("模拟信号")

            # 设置当前数据集
            self.current_dataset.set("模拟信号")
            self.df = self.df_analog
            self.after_dataset_switch()

            # 更新状态提示
            status_text = f"读取成功：模拟信号 {len(self.df_analog)}行 x {len(self.df_analog.columns)}列"
            if has_digital:
                status_text += f"，数字信号 {len(self.df_digital)}行 x {len(self.df_digital.columns)}列"
            self.status_label.config(text=status_text, foreground="green")
            
        except Exception as e:
            self.status_label.config(text=f"读取失败: {str(e)}", foreground="red")
            self.df = None
            self.filtered_cols = []
            self.filtered_display_names = []
            self.refresh_listbox()

    def on_dataset_changed(self, event=None):
        """切换数据集"""
        ds = self.dataset_combo.get()
        self.current_dataset.set(ds)
        self.df = self.df_analog if ds == "模拟信号" else self.df_digital
        self.after_dataset_switch()

    def after_dataset_switch(self):
        """数据集切换后初始化"""
        if self.df is None:
            return
        # 刷新X轴选项
        self.refresh_x_options()
        # 自动选择X轴（优先timestamp/Time）
        if 'timestamp' in self.df.columns:
            self.x_col_name = 'timestamp'
        elif 'Time' in self.df.columns:
            self.x_col_name = 'Time'
        else:
            num_cols = self.df.select_dtypes(include='number').columns
            if len(num_cols) > 0:
                self.x_col_name = num_cols[0]
        # 设置X轴显示
        if self.x_col_name:
            self.x_axis_combo.set(self.get_display_name(self.x_col_name))
        # 初始化列列表
        self.all_original_cols = self.df.columns.tolist()
        self.all_display_names = [self.get_display_name(col) for col in self.all_original_cols]
        self.filtered_cols = self.all_original_cols.copy()
        self.filtered_display_names = self.all_display_names.copy()
        self.refresh_listbox()

    # -------------------------- X轴相关 --------------------------
    def refresh_x_options(self):
        """刷新X轴下拉选项"""
        if self.df is None:
            self.x_axis_combo['values'] = []
            return
        # 获取所有数值型列的显示名称
        num_cols = self.df.select_dtypes(include='number').columns.tolist()
        x_options = [self.get_display_name(col) for col in num_cols]
        self.x_axis_combo['values'] = x_options

    def on_x_axis_changed(self, event=None):
        """X轴选择改变"""
        selected_display = self.x_axis_combo.get()
        if not selected_display or self.df is None:
            return
        # 反向查找原始列名
        for col in self.df.columns:
            if self.get_display_name(col) == selected_display:
                self.x_col_name = col
                break

    # -------------------------- 绘图相关 --------------------------
    def clear_selection(self):
        """取消列表框全部勾选"""
        self.col_listbox.selection_clear(0, tk.END)

    def show_data_preview(self):
        """数据预览/诊断"""
        if self.df is None:
            messagebox.showwarning("警告", "未读取数据！")
            return
        
        preview_win = tk.Toplevel(self.root)
        preview_win.title("数据预览/诊断")
        preview_win.geometry("800x600")

        # 创建文本框
        text = tk.Text(preview_win, wrap=tk.NONE, font=("微软雅黑", 9))
        v_scroll = ttk.Scrollbar(preview_win, orient=tk.VERTICAL, command=text.yview)
        h_scroll = ttk.Scrollbar(preview_win, orient=tk.HORIZONTAL, command=text.xview)
        text.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # 生成诊断信息
        info = f"数据集：{self.current_dataset.get()}\n"
        info += f"数据形状：{self.df.shape[0]} 行 × {self.df.shape[1]} 列\n\n"
        info += "前5行数据：\n"
        info += self.df.head().to_string() + "\n\n"
        info += "数据类型：\n"
        info += self.df.dtypes.to_string() + "\n\n"
        info += "缺失值统计：\n"
        missing = self.df.isnull().sum()
        info += missing[missing > 0].to_string() if missing.sum() > 0 else "无缺失值" + "\n\n"
        info += "数值统计：\n"
        info += self.df.describe().to_string()

        text.insert(tk.END, info)
        text.config(state=tk.DISABLED)

        ttk.Button(preview_win, text="关闭", command=preview_win.destroy).pack(pady=5)

    def plot_data(self):
        """绘图"""
        if self.df is None:
            messagebox.showwarning("警告", "未读取数据！")
            return
        if self.x_col_name is None or self.x_col_name not in self.df.columns:
            messagebox.showwarning("警告", "请选择有效的X轴列！")
            return
        
        # 获取选中的Y列
        selected_indices = self.col_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "请至少选择一列作为Y轴！")
            return
        
        selected_cols = [self.filtered_cols[i] for i in selected_indices]
        if not selected_cols:
            messagebox.showwarning("警告", "未选中有效列！")
            return

        # 清空绘图区
        self.ax.clear()

        # 获取X轴数据
        x_data = self.df[self.x_col_name].dropna()
        if len(x_data) == 0:
            messagebox.showwarning("警告", "X轴数据全为缺失值！")
            return

        # 绘制每条曲线
        for idx, col in enumerate(selected_cols):
            y_data = self.df[col].dropna()
            if len(y_data) == 0:
                continue
            # 对齐X/Y数据（去除缺失值）
            combined = pd.DataFrame({'x': x_data, 'y': y_data}).dropna()
            if len(combined) == 0:
                continue
            
            display_name = self.get_display_name(col).split(' (')[0]  # 只显示中文名称
            color = COLORS[idx % len(COLORS)]
            
            if self.plot_type.get() == "line":
                self.ax.plot(combined['x'], combined['y'], label=display_name, color=color, linewidth=1)
            else:
                self.ax.scatter(combined['x'], combined['y'], label=display_name, color=color, s=1)

        # 设置图表样式
        self.ax.set_xlabel(self.get_display_name(self.x_col_name).split(' (')[0], fontsize=10, fontfamily='Microsoft YaHei')
        self.ax.set_ylabel("数值", fontsize=10, fontfamily='Microsoft YaHei')
        self.ax.set_title("风机数据可视化", fontsize=12, fontweight='bold', fontfamily='Microsoft YaHei')
        self.ax.legend(loc='best', fontsize=8, prop={'family': 'Microsoft YaHei'})
        self.ax.grid(True, alpha=0.3)

        # 更新画布
        self.canvas.draw()

    def on_closing(self):
        """关闭窗口"""
        self.root.destroy()

# -------------------------- 主程序入口 --------------------------
if __name__ == "__main__":
    # 隐藏控制台窗口（仅Windows）
    hide_console()
    
    root = tk.Tk()
    app = WindDataPlotter(root)
    root.mainloop()
