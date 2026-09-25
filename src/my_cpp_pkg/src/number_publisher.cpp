#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"

class NumberPublisherNode : public rclcpp::Node
{
public:
    NumberPublisherNode() : Node("number_publisher")
    {
        // Declare parameters
        this->declare_parameter<int>("number", 2);
        this->declare_parameter<double>("timer_period", 1.0);

        // Read parameters
        number_ = this->get_parameter("number").as_int();
        timer_period_ = this->get_parameter("timer_period").as_double();

        // Publisher
        number_publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number", 10);

        // Timer
        number_timer_ = this->create_wall_timer(
            std::chrono::duration<double>(timer_period_),
            std::bind(&NumberPublisherNode::publishNumber, this)
        );

        RCLCPP_INFO(this->get_logger(), "Number publisher has been started.");
    }

private:
    void publishNumber()
    {
        auto msg = example_interfaces::msg::Int64();
        msg.data = number_;
        number_publisher_->publish(msg);
        RCLCPP_INFO(this->get_logger(), "Published: %ld", msg.data);
    }

    int number_;
    double timer_period_;

    rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr number_publisher_;
    rclcpp::TimerBase::SharedPtr number_timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<NumberPublisherNode>());
    rclcpp::shutdown();
    return 0;
}

