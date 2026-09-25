#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"

class NumberCounter : public rclcpp::Node
{
public:
    NumberCounter() : Node("number_counter"), count_(0)
    {
        subscription_ = this->create_subscription<example_interfaces::msg::Int64>(
            "number", 10,
            std::bind(&NumberCounter::callbackNumber, this, std::placeholders::_1));
    }

private:
    void callbackNumber(const example_interfaces::msg::Int64::SharedPtr msg)
    {
        count_ += msg->data;
        RCLCPP_INFO(this->get_logger(), "Total count: %ld", count_);
    }

    int64_t count_;
    rclcpp::Subscription<example_interfaces::msg::Int64>::SharedPtr subscription_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<NumberCounter>());
    rclcpp::shutdown();
    return 0;
}
