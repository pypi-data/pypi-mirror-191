from env import Env
from scenarioOrganizer import ScenarioOrganizer
import time
import os
import shutil


def demo_for_opendrive_info(info) -> None:
    for discrete_lane in info.discretelanes:  # 遍历每一条lane
        print(discrete_lane.lane_id)  # 分别是road.id、lane_section.id、lane.id、width.id
        print(discrete_lane.left_vertices)  # 车道左边界散点序列: ndarray
        print(discrete_lane.right_vertices)  # 车道右边界散点序列：ndarray
        print(discrete_lane.center_vertices)  # 车道中心线散点序列：ndarray
        print(discrete_lane.predecessor)  # 车道前连接线的lane_id
        print(discrete_lane.successor)  # 车道后连接线的lane_id
    return


def check_dir(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)


# 指定输入输出文件夹位置
demo_input_dir = r"./demo/demo_inputs"
demo_output_dir = r"./demo/demo_outputs"
show_demo = False  # 是否演示openDrive信息的函数

# check dir
check_dir(demo_output_dir)

# 记录测试时间，用于评估效率，没有特殊用途
tic = time.time()
# 实例化场景管理模块（ScenairoOrganizer）和场景测试模块（Env）
so = ScenarioOrganizer()
env = Env()
# 根据配置文件config.py装载场景，指定输入文件夹即可，会自动检索配置文件
so.load(demo_input_dir, demo_output_dir)

while True:
    # 使用场景管理模块给出下一个待测场景
    scenario_to_test = so.next()
    if scenario_to_test is None:
        break  # 如果场景管理模块给出None，意味着所有场景已测试完毕。
    print("测试:", scenario_to_test)
    # 如果场景管理模块不是None，则意味着还有场景需要测试，进行测试流程。
    # 使用env.make方法初始化当前测试场景
    observation = env.make(scenario=scenario_to_test,
                           output_dir=demo_output_dir, visilize=True)
    # 解析后的openDrive信息调用接口
    opendrive_info = env.controller.control_info.road_info  # opendrive_info里面存放了所有信息
    if show_demo:
        demo_for_opendrive_info(opendrive_info)
    # 当测试还未进行完毕，即观察值中test_setting['end']还是-1的时候
    while observation.test_setting['end'] == -1:
        action = (-1, 0)  # 规划控制模块做出决策，在本demo中，以本车加速度-1，方向盘转角0为例。
        observation = env.step(action)  # 根据车辆的action，更新场景，并返回新的观测值。
    # 如果测试完毕，将测试结果传回场景管理模块（ScenarioOrganizer)
    so.add_result(scenario_to_test, observation.test_setting['end'])
toc = time.time()
print(toc - tic)
