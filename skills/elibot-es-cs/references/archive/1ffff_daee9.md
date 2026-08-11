# CS_ROS2软件包使用案例及说明

URL: https://docs.elibot.cn/cs/1ffff/daee9
Published: 发布时间: 2026-02-04

# **一、简介**



以下为使用c++编写的基于ros2的源码，该源码实现了机器人监听数字信号，沿固定线路进行搬运的功能



# **二、操作流程**



**1、**将第四章代码放入./Elite_Robots_CS_ROS2_Driver/eli_cs_robot_driver/example/cpp后，需要修改编译文件。进入 ./Elite_Robots_CS_ROS2_Driver/eli_cs_robot_driver文件夹



**2、**打开CMakeList.txt，添加以下代码，这里file_name请修改成真实的文件名



```
add_executable(
  file_name
  example/cpp/file_name.cpp
)
ament_target_dependencies(
  file_name
  ${THIS_PACKAGE_DEPENDENCIES}
)
install(
  TARGETS file_name
  DESTINATION lib/${PROJECT_NAME}
)
```



**3、**回到ROS2软件包存放的根目录./



**4、**重新编译ROS2软件包



```
colcon build
```



**5、**使用ros2 run指令执行编译好的二进制文件



# **三、常见问题**



**1、Q：**为什么打开的rviz里机器人所有关节全部摆放在原点



**A：**这是因为机器人位姿读取失败，大概率是没有连接上机器人，请优先检查线路连接是否正常，是否在同一网段内，是否在示教器上开启了远程模式，是否在启动机器人时指定了参数USE_HEADLESS_MODE:=True



# 四、代码和附件



ROS2 轨迹控制节点，走 `FollowJointTrajectory` action + IO 服务，实现一个带 IO 交互的多段取放料流程。



- `declare_parameter("controller", "scaled_joint_trajectory_controller")` 声明控制器参数
- `rclcpp_action::create_client<FollowJT>(..., "/控制器名/follow_joint_trajectory")` 创建轨迹 action 客户端
- `create_client<SetIO>(..., "/io_and_status_controller/set_io")` 创建 IO 服务客户端
- `create_subscription<JointState>("/joint_states", ..., jointCallback)` 订阅关节状态 → 存 `current_pos_`
- `create_subscription<IOState>("/io_and_status_controller/io_states", ..., ioStateCallback)` 订阅 IO 状态 → 存 `last_io_state_`



执行流程 `execute()`：



- `waitForJointStates(5.0)` 等关节状态就绪（`spin_some` + 轮询 `current_pos_`）
- `io_service_client_->wait_for_service(5s)` 等 IO 服务上线
- `moveToPosition({0, -1.57, 0, -1.57, 1.57, 0}, 6.0)` → Home 位



- 内部：`client_->wait_for_action_server(5s)` → `async_send_goal(goal_msg)` 含起点+目标点 → `async_get_result(goal_handle)` → 更新 `current_pos_`



- `setDigitalOutput(0, true)` DO[0] 拉高 → 内部 `async_send_request(set_io 服务)`
- 循环等待 DO[3] 为 true（`spin_some` + `checkDigitalOutput(3)` 每 100ms）
- DO[3] 触发后：`moveToPosition(pos1)` → `setDigitalOutput(1, true)`
- 循环等待 DO[4] 或 DO[5] 为 true（`spin_some` 每 1s）
- DO[4] 分支（取料成功）：



- `moveToPosition(pos2)` → `moveToPosition(pos3)` → `moveToPosition(pos4)` → `moveToPosition(pos5)` 四段取料轨迹
- `moveToPosition(pos6)` → `moveToPosition(pos7)` 两段返回轨迹
- `setDigitalOutput(4, false)` DO[4] 复位



- DO[5] 分支（流程结束）：



- 循环 `setDigitalOutput(i, false)` 清 DO[0]~[5] → `return true`



- `rclcpp::shutdown()` 退出



**流程逻辑图**：



```
Home → DO[0]=1 → 等DO[3]=1 → pos1 → DO[1]=1
                                       ↓
                              等DO[4]=1 或 DO[5]=1
                              ↙                ↘
                        pos2~pos5            清DO[0~5]
                        pos6~pos7              → 结束
                        DO[4]=0
```



**用到的接口一览**：



**接口****类型****用途**`declare_parameter`参数控制器名`create_client<FollowJT>`Action Client关节轨迹执行`create_client<SetIO>`Service Client数字 IO 读写`create_subscription<JointState>`Topic Sub订阅关节位置`create_subscription<IOState>`Topic Sub订阅 IO 状态`wait_for_action_server`Action等 action 服务就绪`async_send_goal` / `async_get_result`Action发轨迹+等结果`wait_for_service`Service等服务上线`async_send_request`Service调 set_io 服务`spin_some` / `spin_until_future_complete`ROS2非阻塞轮询 / 同步等 Future



```
#include <chrono>
#include <memory>
#include <string>
#include <vector>
#include <unordered_map>
#include <optional>
#include <thread>

#include "control_msgs/action/follow_joint_trajectory.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "trajectory_msgs/msg/joint_trajectory_point.hpp"
#include "eli_common_interface/srv/set_io.hpp"
#include "eli_common_interface/msg/io_state.hpp"

namespace {
const std::vector<std::string> JOINTS = {
    "shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", 
    "wrist_1_joint", "wrist_2_joint", "wrist_3_joint",
};
}  // namespace

class EliteTrajectoryNode : public rclcpp::Node {
public:
    using FollowJT = control_msgs::action::FollowJointTrajectory;
    using GoalHandle = rclcpp_action::ClientGoalHandle<FollowJT>;
    using SetIO = eli_common_interface::srv::SetIO;
    using IOState = eli_common_interface::msg::IOState;

    EliteTrajectoryNode() : rclcpp::Node("elite_trajectory_node") {
        // 参数声明
        controller_ = this->declare_parameter<std::string>(
            "controller", 
            "scaled_joint_trajectory_controller"
        );

        // 创建动作客户端
        client_ = rclcpp_action::create_client<FollowJT>(
            this, 
            "/" + controller_ + "/follow_joint_trajectory"
        );

        // 创建IO服务客户端
        io_service_client_ = this->create_client<SetIO>(
            "/io_and_status_controller/set_io"
        );

        // 订阅关节状态
        joint_sub_ = this->create_subscription<sensor_msgs::msg::JointState>(
            "/joint_states", 
            10,
            std::bind(&EliteTrajectoryNode::jointCallback, this, std::placeholders::_1)
        );

        // 订阅IO状态
        io_state_sub_ = this->create_subscription<IOState>(
            "/io_and_status_controller/io_states", 
            10,
            std::bind(&EliteTrajectoryNode::ioStateCallback, this, std::placeholders::_1)
        );

        RCLCPP_INFO(get_logger(), "Elite Trajectory Node initialized");
    }

    bool execute() {
        RCLCPP_INFO(get_logger(), "Starting execution sequence");
        
        // 1. 等待关节状态
        if (!waitForJointStates(5.0)) {
            RCLCPP_ERROR(get_logger(), "Failed to get joint states");
            return false;
        }

        // 2. 等待IO服务
        if (!io_service_client_->wait_for_service(std::chrono::seconds(5))) {
            RCLCPP_ERROR(get_logger(), "IO service not available");
            return false;
        }

        // 3. 执行Home轨迹
        RCLCPP_INFO(get_logger(), "Executing home trajectory");
        std::vector<double> home_position = {0, -1.57, 0, -1.57, 1.57, 0};
        if (!moveToPosition(home_position, 6.0)) {
            RCLCPP_ERROR(get_logger(), "Failed to move to home position");
            return false;
        }

        // 4. 设置IO输出0为true
        RCLCPP_INFO(get_logger(), "Setting digital output 0 to true");
        if (!setDigitalOutput(0, true)) {
            RCLCPP_ERROR(get_logger(), "Failed to set digital output 0");
            return false;
        }

        // 5. 等待IO输出3触发
        RCLCPP_INFO(get_logger(), "Waiting for digital output 3 to be true...");
        while (rclcpp::ok()) {
            rclcpp::spin_some(shared_from_this());
            
            if (checkDigitalOutput(3)) {
                RCLCPP_INFO(get_logger(), "Digital output 3 is true!");
                
                // 执行第一段轨迹
                std::vector<double> position1 = {0.8, -1.5, -1.9, -1.2, 1.5, 0.1};
                RCLCPP_INFO(get_logger(), "Moving to position 1");
                if (!moveToPosition(position1, 4.0)) {
                    RCLCPP_ERROR(get_logger(), "Failed to execute position 1");
                    return false;
                }

                // 设置IO输出1为true
                RCLCPP_INFO(get_logger(), "Setting digital output 1 to true");
                if (!setDigitalOutput(1, true)) {
                    RCLCPP_ERROR(get_logger(), "Failed to set digital output 1");
                    return false;
                }
                
                break;
            }
            
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }

        // 6. 等待IO输出4或5触发
        RCLCPP_INFO(get_logger(), "Waiting for digital output 4 or 5...");
        while (rclcpp::ok()) {
            rclcpp::spin_some(shared_from_this());
            
            if (checkDigitalOutput(4)) {
                RCLCPP_INFO(get_logger(), "Digital output 4 is true!");
                
                std::vector<double> position2 = {0.8, -1.7, -2.1, -0.8, 1.5, 0.1};
                if (!moveToPosition(position2, 4.0)) {
                    RCLCPP_ERROR(get_logger(), "Failed to execute joint trajectory 2");
                    return false;
                }

                RCLCPP_INFO(get_logger(), "Executing joint trajectory to get goods succ");
                std::vector<double> position3 = {0.8, -1.5, -1.9, -1.2, 1.5, 0.1};
                std::vector<double> position4 = {0.5, -1.5, -1.9, -1.2, 1.5, 0.1};
                if (!moveToPosition(position3, 4.0)) {
                    RCLCPP_ERROR(get_logger(), "Failed to execute joint trajectory 3");
                    return false;
                }
                if (!moveToPosition(position4, 4.0)) {
                    RCLCPP_ERROR(get_logger(), "Failed to execute joint trajectory 4");
                    return false;
                }
                
                std::vector<double> position5 = {0.5, -1.7, -2.1, -0.8, 1.5, 0.1};
                if (!moveToPosition(position5, 4.0)) {
                    RCLCPP_ERROR(get_logger(), "Failed to execute Cartesian trajectory 5");
                    return false;
                }

                RCLCPP_INFO(get_logger(), "Executing return trajectory to put goods succ");
                std::vector<double> position6 = {0.5, -1.5, -1.9, -1.2, 1.5, 0.1};
                std::vector<double> position7 = {0.8, -1.5, -1.9, -1.2, 1.5, 0.1};
                if (!moveToPosition(position6, 4.0)) {
                    RCLCPP_ERROR(get_logger(), "Failed to execute joint trajectory 6");
                    return false;
                }
                if (!moveToPosition(position7, 4.0)) {
                    RCLCPP_ERROR(get_logger(), "Failed to execute joint trajectory 7");
                    return false;
                }

                // 设置IO输出4为false (
                RCLCPP_INFO(get_logger(), "Setting digital output 4 to false");
                if (!setDigitalOutput(4, false)) {
                    RCLCPP_ERROR(get_logger(), "Failed to set digital output 4");
                }
                
            } else if (checkDigitalOutput(5)) {
                RCLCPP_INFO(get_logger(), "Digital output 5 is true!");
                
                // 清除所有IO输出
                RCLCPP_INFO(get_logger(), "Clearing all digital outputs");
                for (int i = 0; i <= 5; i++) {
                    setDigitalOutput(i, false);
                }
                
                RCLCPP_INFO(get_logger(), "All trajectories completed successfully!");
                return true;
            }
            
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }

        return false;
    }

private:
    // ==================== 关节状态处理 ====================
    void jointCallback(const sensor_msgs::msg::JointState::SharedPtr msg) {
        std::vector<double> positions;
        positions.reserve(JOINTS.size());
        std::unordered_map<std::string, double> joint_map;
        
        for (size_t i = 0; i < msg->name.size(); ++i) {
            if (i < msg->position.size()) {
                joint_map[msg->name[i]] = msg->position[i];
            }
        }
        
        for (const auto& joint_name : JOINTS) {
            auto it = joint_map.find(joint_name);
            if (it == joint_map.end()) {
                return;  // 等待完整的数据集
            }
            positions.push_back(it->second);
        }
        
        current_pos_ = positions;
    }

    bool waitForJointStates(double timeout_sec) {
        RCLCPP_INFO(get_logger(), "Waiting for joint states...");
        
        auto start_time = this->now();
        rclcpp::Rate rate(50);
        
        while (rclcpp::ok()) {
            rclcpp::spin_some(shared_from_this());
            
            if (current_pos_.has_value()) {
                RCLCPP_INFO(get_logger(), "Received joint states");
                return true;
            }
            
            if ((this->now() - start_time).seconds() > timeout_sec) {
                RCLCPP_ERROR(get_logger(), "Timeout waiting for joint states");
                return false;
            }
            
            rate.sleep();
        }
        
        return false;
    }

    // ==================== IO状态处理 ====================
    void ioStateCallback(const IOState::SharedPtr msg) {
        // 保存最新的IO状态
        last_io_state_ = *msg;
    }

    bool checkDigitalOutput(int pin) {
        if (!last_io_state_.has_value()) {
            return false;
        }
        
        const auto& io_state = last_io_state_.value();
        
        // 检查引脚是否在有效范围内
        if (pin < 0 || pin >= static_cast<int>(io_state.standard_out.size())) {
            RCLCPP_WARN(get_logger(), "Pin %d is out of range (max: %zu)", 
                       pin, io_state.standard_out.size());
            return false;
        }
        
        return io_state.standard_out[pin];
    }

    bool setDigitalOutput(int pin, bool state) {
        auto request = std::make_shared<SetIO::Request>();
        request->fun = SetIO::Request::FUN_SET_DIGITAL_OUT;
        request->pin = pin;
        request->state = state ? SetIO::Request::STATE_ON : SetIO::Request::STATE_OFF;
        
        auto future = io_service_client_->async_send_request(request);
        
        // 等待响应
        if (rclcpp::spin_until_future_complete(shared_from_this(), future) != 
            rclcpp::FutureReturnCode::SUCCESS) {
            RCLCPP_ERROR(get_logger(), "Failed to call set_io service");
            return false;
        }
        
        auto response = future.get();
        
        if (response->success) {
            RCLCPP_INFO(get_logger(), "Successfully set digital output pin %d to %s", 
                       pin, state ? "true" : "false");
            return true;
        } else {
            RCLCPP_ERROR(get_logger(), "Failed to set digital output pin %d", pin);
            return false;
        }
    }

    // ==================== 轨迹执行 ====================
    bool moveToPosition(const std::vector<double>& target, double duration) {
        if (target.size() != JOINTS.size()) {
            RCLCPP_ERROR(get_logger(), "Target size mismatch");
            return false;
        }

        if (!client_->wait_for_action_server(std::chrono::seconds(5))) {
            RCLCPP_ERROR(get_logger(), "Action server not available");
            return false;
        }

        auto goal_msg = FollowJT::Goal();
        goal_msg.trajectory.joint_names = JOINTS;

        // 添加起始点（当前位置）
        if (current_pos_.has_value()) {
            trajectory_msgs::msg::JointTrajectoryPoint start;
            start.positions = current_pos_.value();
            start.time_from_start = rclcpp::Duration(0, 0);
            goal_msg.trajectory.points.push_back(start);
        }

        // 添加目标点
        trajectory_msgs::msg::JointTrajectoryPoint target_pt;
        target_pt.positions = target;
        target_pt.time_from_start = rclcpp::Duration::from_seconds(duration);
        goal_msg.trajectory.points.push_back(target_pt);

        // 发送目标
        auto goal_future = client_->async_send_goal(goal_msg);
        if (rclcpp::spin_until_future_complete(shared_from_this(), goal_future) != 
            rclcpp::FutureReturnCode::SUCCESS) {
            RCLCPP_ERROR(get_logger(), "Failed to send goal");
            return false;
        }
        
        auto goal_handle = goal_future.get();
        if (!goal_handle) {
            RCLCPP_ERROR(get_logger(), "Goal rejected");
            return false;
        }

        // 等待结果
        auto result_future = client_->async_get_result(goal_handle);
        if (rclcpp::spin_until_future_complete(shared_from_this(), result_future) != 
            rclcpp::FutureReturnCode::SUCCESS) {
            RCLCPP_ERROR(get_logger(), "Failed to get result");
            return false;
        }
        
        auto result = result_future.get();
        bool success = result.result->error_code == 0;
        
        if (success) {
            current_pos_ = target;
            RCLCPP_INFO(get_logger(), "Move to position successful");
        } else {
            RCLCPP_ERROR(get_logger(), "Move failed with error code: %d", result.result->error_code);
        }
        
        return success;
    }

    // ==================== 成员变量 ====================
    std::string controller_;
    
    rclcpp_action::Client<FollowJT>::SharedPtr client_;
    rclcpp::Client<SetIO>::SharedPtr io_service_client_;
    rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr joint_sub_;
    rclcpp::Subscription<IOState>::SharedPtr io_state_sub_;
    
    std::optional<std::vector<double>> current_pos_;
    std::optional<IOState> last_io_state_;
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<EliteTrajectoryNode>();
    bool ok = node->execute();
    rclcpp::shutdown();
    return ok ? 0 : 1;
}
```
