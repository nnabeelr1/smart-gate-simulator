# 🚗 Smart Gate System - Auto Flow Simulator

A comprehensive Python GUI application that simulates intelligent parking gate operations with automated flow sequences, member management, and real-time capacity monitoring.

![Smart Gate Demo](demo-screenshot.png)

## ✨ Features

### 🎯 Core Functionality
- **Automated Flow Simulation** - Complete vehicle entry/exit workflows
- **Multi-tier Member System** - VIP, Subscribers, and Visitors with different access levels
- **Real-time Capacity Management** - Dynamic parking space monitoring
- **Visual Gate Simulation** - Interactive canvas showing gate operations
- **Activity Logging** - Complete audit trail of all system events

### 👥 Member Management
- **VIP Members** - Instant access with premium privileges
- **Subscribers** - Pre-registered users with streamlined entry
- **Visitor Support** - Payment processing for non-members
- **JSON Database** - Persistent member data storage

### 🛡️ Security Features
- **License Plate Recognition** - Automated plate scanning simulation
- **Anti-Passback Protection** - Prevents unauthorized re-entry
- **Capacity Enforcement** - Automatic rejection when parking is full
- **Payment Validation** - Secure transaction processing for visitors

### 🎮 Simulation Controls
- **Multiple Flow Types** - Different scenarios for various user types
- **Manual/Auto Progression** - Step-through or automated flow execution
- **Quick Setup** - Pre-configured test scenarios
- **Real-time Monitoring** - Live system status updates

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.7+
tkinter (usually included with Python)
```

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-gate-simulator.git
cd smart-gate-simulator
```

2. Run the application:
```bash
python smart_gate_simulator.py
```

### First Run
The application will automatically create a `members.json` file with sample data including:
- **VIP Members**: B1234XX, B5678YY, D9999ZZ
- **Subscribers**: B2222AA, B3333BB, B4444CC

## 📖 How to Use

### Basic Operation
1. **Enter License Plate** - Type a plate number or use quick buttons
2. **Start Auto Flow** - Click "START AUTO FLOW" to begin simulation
3. **Monitor Progress** - Watch the visual simulation and progress bar
4. **View Logs** - Check the activity log for detailed events

### Quick Test Scenarios
- **VIP Button** - Test VIP member instant access
- **SUB Button** - Test subscriber verification flow
- **NEW Button** - Test visitor payment flow
- **RANDOM Button** - Generate random plate for testing

### System Management
- **Capacity Control** - Adjust max capacity and current occupancy
- **Member Management** - Add/remove VIP members and subscribers
- **Flow Control** - Manual step-through or auto-advance modes

## 🔧 Configuration

### System Settings
- **Max Capacity**: Adjustable parking space limit (default: 50)
- **Parking Fee**: Visitor payment amount (default: Rp 5,000)
- **Auto Advance**: Automatic flow progression toggle

### Flow Types
- **VIP Flow**: Instant access for premium members
- **Subscriber Flow**: Quick verification for registered users
- **Visitor Known Flow**: Payment processing for known plates
- **Visitor Unknown Flow**: Full registration and payment
- **Rejection Flows**: Capacity full or anti-passback detection

## 📁 Project Structure

```
smart-gate-simulator/
├── smart_gate_simulator.py    # Main application file
├── members.json              # Member database (auto-created)
├── README.md                 # This file
├── demo-screenshot.png       # Application screenshot
└── requirements.txt          # Python dependencies
```

## 🎨 User Interface

### Left Panel - Simulation View
- **Visual Gate Display** - Animated gate and vehicle representation
- **Flow Progress Bar** - Real-time step progression
- **System Status** - Current state and capacity information
- **Detailed Info Panel** - Complete system status breakdown

### Right Panel - System Control
- **Vehicle Simulation** - License plate entry and flow controls
- **System Management** - Capacity and configuration settings
- **Member Management** - Add/remove members with real-time updates
- **Activity Log** - Timestamped event history

## 🛠️ Technical Details

### Built With
- **Python 3.7+** - Core application language
- **Tkinter** - GUI framework for cross-platform interface
- **JSON** - Lightweight database for member storage
- **Canvas Graphics** - Custom drawing for visual simulation

### Key Components
- **State Machine** - Robust flow control system
- **Event Logging** - Comprehensive activity tracking
- **Member Database** - Persistent storage with JSON serialization
- **Visual Simulation** - Real-time graphical representation

## 📋 Flow Sequences

### VIP Member Flow
1. Vehicle Detection → 2. Plate Recognition → 3. VIP Verification → 4. Gate Opens → 5. Vehicle Passes

### Subscriber Flow
1. Vehicle Detection → 2. Plate Recognition → 3. Subscriber Verification → 4. Gate Opens → 5. Vehicle Passes

### Visitor Flow
1. Vehicle Detection → 2. Plate Recognition → 3. Payment Required → 4. Payment Processing → 5. Confirmation → 6. Gate Opens → 7. Vehicle Passes

### Rejection Scenarios
- **Capacity Full**: Immediate rejection when parking is at maximum
- **Anti-Passback**: Prevention of unauthorized re-entry attempts

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

For questions, issues, or suggestions:
- **Create an Issue** - Use GitHub Issues for bug reports and feature requests
- **Discussions** - Join the community discussions for general questions

## 🔄 Version History

- **v1.0.0** - Initial release with core simulation features
- **v1.1.0** - Added member management and enhanced UI
- **v1.2.0** - Implemented visual simulation and flow controls

## 📸 Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)

### Flow Simulation
![Flow Simulation](screenshots/flow-simulation.png)

### Member Management
![Member Management](screenshots/member-management.png)

---

**Built with ❤️ for smart parking solutions and IoT simulation**