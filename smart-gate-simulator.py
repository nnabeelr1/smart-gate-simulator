import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import json
import os

class SmartGateSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Gate System - Auto Flow Simulator")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1a1a1a")
        
        # System configuration
        self.max_capacity = 50
        self.current_capacity = 0
        self.parking_fee = 5000
        
        # Member database
        self.members_file = "members.json"
        self.load_members()
        
        # Current session
        self.current_plate = ""
        self.current_member_type = "visitor"
        self.current_state = "Idle"
        self.auto_flow_active = False
        self.flow_steps = []
        self.current_step = 0
        
        # State flow definitions
        self.define_flows()
        
        self.setup_gui()
        self.update_display()
        
    def load_members(self):
        """Load member database from JSON file"""
        try:
            if os.path.exists(self.members_file):
                with open(self.members_file, 'r') as f:
                    data = json.load(f)
                    self.vip_members = set(data.get('vip', []))
                    self.subscribers = set(data.get('subscribers', []))
            else:
                self.vip_members = {'B1234XX', 'B5678YY', 'D9999ZZ'}
                self.subscribers = {'B2222AA', 'B3333BB', 'B4444CC'}
                self.save_members()
        except:
            self.vip_members = {'B1234XX', 'B5678YY', 'D9999ZZ'}
            self.subscribers = {'B2222AA', 'B3333BB', 'B4444CC'}
            
    def save_members(self):
        """Save member database to JSON file"""
        try:
            data = {
                'vip': list(self.vip_members),
                'subscribers': list(self.subscribers)
            }
            with open(self.members_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving members: {e}")
            
    def define_flows(self):
        """Define different flow sequences based on member type and conditions"""
        self.flows = {
            'vip_flow': [
                ('Idle', 'vehicle_arrive'),
                ('Detected', 'plate_recognized'),
                ('AuthCheck', 'vip_verified'),
                ('OpenGate', 'gate_opens'),
                ('Closed', 'vehicle_passes'),
                ('Idle', 'flow_complete')
            ],
            'subscriber_flow': [
                ('Idle', 'vehicle_arrive'),
                ('Detected', 'plate_recognized'),
                ('AuthCheck', 'subscriber_verified'),
                ('OpenGate', 'gate_opens'),
                ('Closed', 'vehicle_passes'),
                ('Idle', 'flow_complete')
            ],
            'visitor_known_flow': [
                ('Idle', 'vehicle_arrive'),
                ('Detected', 'plate_recognized'),
                ('AuthCheck', 'payment_required'),
                ('WaitPayment', 'payment_processing'),
                ('Confirmation', 'payment_confirmed'),
                ('OpenGate', 'gate_opens'),
                ('Closed', 'vehicle_passes'),
                ('Idle', 'flow_complete')
            ],
            'visitor_unknown_flow': [
                ('Idle', 'vehicle_arrive'),
                ('Detected', 'plate_unknown'),
                ('WaitPayment', 'payment_processing'),
                ('Confirmation', 'payment_confirmed'),
                ('OpenGate', 'gate_opens'),
                ('Closed', 'vehicle_passes'),
                ('Idle', 'flow_complete')
            ],
            'reject_capacity_flow': [
                ('Idle', 'vehicle_arrive'),
                ('Detected', 'plate_recognized'),
                ('AuthCheck', 'capacity_full'),
                ('Reject', 'access_denied'),
                ('Idle', 'reset_complete')
            ],
            'reject_passback_flow': [
                ('Idle', 'vehicle_arrive'),
                ('Detected', 'anti_passback_detected'),
                ('Reject', 'access_denied'),
                ('Idle', 'reset_complete')
            ]
        }
        
    def setup_gui(self):
        # Main title
        title_frame = tk.Frame(self.root, bg="#1a1a1a")
        title_frame.pack(pady=15)
        
        tk.Label(title_frame, text="🚗 SMART GATE SYSTEM - AUTO FLOW", 
                font=("Arial", 24, "bold"), fg="#00ff88", bg="#1a1a1a").pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Left panel - Visual and flow
        self.setup_visual_panel(main_frame)
        
        # Right panel - Controls and management
        self.setup_control_panel(main_frame)
        
    def setup_visual_panel(self, parent):
        visual_frame = tk.Frame(parent, bg="#2d2d2d", relief=tk.RAISED, bd=2)
        visual_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Header
        header_frame = tk.Frame(visual_frame, bg="#2d2d2d")
        header_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(header_frame, text="🎯 SIMULATION VIEW", 
                font=("Arial", 16, "bold"), fg="#ffffff", bg="#2d2d2d").pack(side=tk.LEFT)
        
        # Capacity indicator
        self.capacity_label = tk.Label(header_frame, text="", 
                                      font=("Arial", 12, "bold"), fg="#00ff88", bg="#2d2d2d")
        self.capacity_label.pack(side=tk.RIGHT)
        
        # Gate visual area
        self.canvas = tk.Canvas(visual_frame, width=600, height=400, bg="#000000")
        self.canvas.pack(pady=20)
        
        # Flow progress bar
        flow_frame = tk.Frame(visual_frame, bg="#2d2d2d")
        flow_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(flow_frame, text="Flow Progress:", 
                font=("Arial", 10, "bold"), fg="#ffffff", bg="#2d2d2d").pack(anchor=tk.W)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(flow_frame, variable=self.progress_var, 
                                           maximum=100, length=580)
        self.progress_bar.pack(fill=tk.X, pady=2)
        
        # Current state and step info
        info_frame = tk.Frame(visual_frame, bg="#2d2d2d")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.state_label = tk.Label(info_frame, text="IDLE", 
                                   font=("Arial", 18, "bold"), 
                                   fg="#00ff88", bg="#2d2d2d")
        self.state_label.pack()
        
        self.step_label = tk.Label(info_frame, text="Ready for vehicle", 
                                  font=("Arial", 12), fg="#ffffff", bg="#2d2d2d")
        self.step_label.pack()
        
        # Vehicle and member info
        self.info_text = tk.Text(info_frame, height=8, width=70, 
                                bg="#1a1a1a", fg="#00ff88", 
                                font=("Consolas", 10))
        self.info_text.pack(pady=5)
        
    def setup_control_panel(self, parent):
        control_frame = tk.Frame(parent, bg="#2d2d2d", relief=tk.RAISED, bd=2)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        tk.Label(control_frame, text="🎮 SYSTEM CONTROL", 
                font=("Arial", 16, "bold"), fg="#ffffff", bg="#2d2d2d").pack(pady=10)
        
        # Vehicle simulation section
        self.setup_vehicle_simulation(control_frame)
        
        # System management section
        self.setup_system_management(control_frame)
        
        # Member management section
        self.setup_member_management(control_frame)
        
        # Activity log
        self.setup_activity_log(control_frame)
        
    def setup_vehicle_simulation(self, parent):
        sim_frame = tk.LabelFrame(parent, text="🚗 Vehicle Simulation", 
                                 bg="#2d2d2d", fg="#ffffff", font=("Arial", 12, "bold"))
        sim_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Plate input
        tk.Label(sim_frame, text="License Plate:", bg="#2d2d2d", fg="#ffffff").pack(anchor=tk.W)
        self.plate_entry = tk.Entry(sim_frame, font=("Arial", 12), width=20)
        self.plate_entry.pack(fill=tk.X, padx=5, pady=2)
        self.plate_entry.bind('<Return>', lambda e: self.start_auto_flow())
        
        # Quick plate buttons
        quick_frame = tk.Frame(sim_frame, bg="#2d2d2d")
        quick_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(quick_frame, text="VIP", command=lambda: self.set_quick_plate("vip"),
                 bg="#9C27B0", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=2)
        tk.Button(quick_frame, text="SUB", command=lambda: self.set_quick_plate("sub"),
                 bg="#00BCD4", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=2)
        tk.Button(quick_frame, text="NEW", command=lambda: self.set_quick_plate("new"),
                 bg="#FF9800", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=2)
        tk.Button(quick_frame, text="RANDOM", command=lambda: self.set_quick_plate("random"),
                 bg="#607D8B", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=2)
        
        # Control buttons
        btn_frame = tk.Frame(sim_frame, bg="#2d2d2d")
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.start_btn = tk.Button(btn_frame, text="▶️ START AUTO FLOW", 
                                  command=self.start_auto_flow,
                                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.start_btn.pack(fill=tk.X, pady=2)
        
        self.next_btn = tk.Button(btn_frame, text="➡️ NEXT STEP", 
                                 command=self.next_step,
                                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                                 state=tk.DISABLED)
        self.next_btn.pack(fill=tk.X, pady=2)
        
        self.reset_btn = tk.Button(btn_frame, text="🔄 RESET", 
                                  command=self.reset_system,
                                  bg="#607D8B", fg="white", font=("Arial", 10, "bold"))
        self.reset_btn.pack(fill=tk.X, pady=2)
        
        # Auto advance option
        self.auto_advance_var = tk.BooleanVar(value=True)
        tk.Checkbutton(sim_frame, text="Auto advance steps", 
                      variable=self.auto_advance_var,
                      bg="#2d2d2d", fg="#ffffff", selectcolor="#1a1a1a").pack(anchor=tk.W)
        
    def setup_system_management(self, parent):
        sys_frame = tk.LabelFrame(parent, text="🏢 System Management", 
                                 bg="#2d2d2d", fg="#ffffff", font=("Arial", 12, "bold"))
        sys_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Capacity control
        cap_frame = tk.Frame(sys_frame, bg="#2d2d2d")
        cap_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(cap_frame, text="Max Capacity:", bg="#2d2d2d", fg="#ffffff").pack(side=tk.LEFT)
        self.capacity_var = tk.IntVar(value=self.max_capacity)
        capacity_spin = tk.Spinbox(cap_frame, from_=10, to=200, width=8, 
                                  textvariable=self.capacity_var,
                                  command=self.update_capacity)
        capacity_spin.pack(side=tk.RIGHT)
        
        # Current occupancy
        occ_frame = tk.Frame(sys_frame, bg="#2d2d2d")
        occ_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(occ_frame, text="Current:", bg="#2d2d2d", fg="#ffffff").pack(side=tk.LEFT)
        self.current_var = tk.IntVar(value=self.current_capacity)
        current_spin = tk.Spinbox(occ_frame, from_=0, to=200, width=8,
                                 textvariable=self.current_var,
                                 command=self.update_current_capacity)
        current_spin.pack(side=tk.RIGHT)
        
        # Quick capacity buttons
        quick_cap_frame = tk.Frame(sys_frame, bg="#2d2d2d")
        quick_cap_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(quick_cap_frame, text="EMPTY", command=lambda: self.set_capacity(0),
                 bg="#4CAF50", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=1, fill=tk.X, expand=True)
        tk.Button(quick_cap_frame, text="HALF", command=lambda: self.set_capacity(self.max_capacity//2),
                 bg="#FF9800", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=1, fill=tk.X, expand=True)
        tk.Button(quick_cap_frame, text="FULL", command=lambda: self.set_capacity(self.max_capacity),
                 bg="#F44336", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=1, fill=tk.X, expand=True)
        
    def setup_member_management(self, parent):
        member_frame = tk.LabelFrame(parent, text="👥 Member Management", 
                                    bg="#2d2d2d", fg="#ffffff", font=("Arial", 12, "bold"))
        member_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Member lists display
        self.member_listbox = tk.Listbox(member_frame, height=6, bg="#1a1a1a", fg="#00ff88",
                                        font=("Consolas", 9))
        self.member_listbox.pack(fill=tk.X, padx=5, pady=2)
        
        # Member management buttons
        btn_frame = tk.Frame(member_frame, bg="#2d2d2d")
        btn_frame.pack(fill=tk.X, pady=2)
        
        tk.Button(btn_frame, text="➕ Add VIP", command=self.add_vip_member,
                 bg="#9C27B0", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=1, fill=tk.X, expand=True)
        tk.Button(btn_frame, text="➕ Add SUB", command=self.add_subscriber,
                 bg="#00BCD4", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=1, fill=tk.X, expand=True)
        tk.Button(btn_frame, text="🗑️ Remove", command=self.remove_member,
                 bg="#F44336", fg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=1, fill=tk.X, expand=True)
        
        self.update_member_list()
        
    def setup_activity_log(self, parent):
        log_frame = tk.LabelFrame(parent, text="📋 Activity Log", 
                                 bg="#2d2d2d", fg="#ffffff", font=("Arial", 10, "bold"))
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        log_container = tk.Frame(log_frame, bg="#2d2d2d")
        log_container.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_container, bg="#1a1a1a", fg="#00ff88",
                               font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(log_container, orient=tk.VERTICAL, command=self.log_text.yview)
        
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    def set_quick_plate(self, plate_type):
        if plate_type == "vip":
            plate = list(self.vip_members)[0] if self.vip_members else "B1234XX"
        elif plate_type == "sub":
            plate = list(self.subscribers)[0] if self.subscribers else "B2222AA"
        elif plate_type == "new":
            plate = f"B{int(time.time()) % 10000:04d}XX"
        else:  # random
            plate = f"{'BDHJK'[int(time.time()) % 5]}{int(time.time()) % 10000:04d}{'XYZNM'[int(time.time()) % 5]}{'ABCDE'[int(time.time()) % 5]}"
        
        self.plate_entry.delete(0, tk.END)
        self.plate_entry.insert(0, plate)
        
    def determine_member_type(self, plate):
        if plate in self.vip_members:
            return "vip"
        elif plate in self.subscribers:
            return "subscriber"
        else:
            return "visitor"
            
    def determine_flow_type(self, plate, member_type):
        # Check capacity first
        if self.current_capacity >= self.max_capacity:
            return "reject_capacity_flow"
        
        # Check anti-passback (simple simulation - if same plate within 30 seconds)
        # This is simplified for demo purposes
        
        if member_type == "vip":
            return "vip_flow"
        elif member_type == "subscriber":
            return "subscriber_flow"
        else:
            # Check if plate is known (has been seen before)
            if len(plate) > 0 and plate[0] in 'BD':  # Simple heuristic for known plates
                return "visitor_known_flow"
            else:
                return "visitor_unknown_flow"
    
    def start_auto_flow(self):
        plate = self.plate_entry.get().strip().upper()
        if not plate:
            messagebox.showwarning("Warning", "Please enter a license plate number!")
            return
            
        self.current_plate = plate
        self.current_member_type = self.determine_member_type(plate)
        flow_type = self.determine_flow_type(plate, self.current_member_type)
        
        self.flow_steps = self.flows[flow_type]
        self.current_step = 0
        self.auto_flow_active = True
        
        self.start_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL)
        
        self.log_event(f"🚀 Starting {flow_type} for {self.current_member_type.upper()}: {plate}")
        
        if self.auto_advance_var.get():
            self.next_step()
        
    def next_step(self):
        if not self.auto_flow_active or self.current_step >= len(self.flow_steps):
            return
            
        new_state, event = self.flow_steps[self.current_step]
        old_state = self.current_state
        self.current_state = new_state
        
        self.log_event(f"➡️ Step {self.current_step + 1}: {event.replace('_', ' ').title()}")
        self.log_event(f"   State: {old_state} → {new_state}")
        
        # Handle specific events
        if event == "vehicle_passes":
            if self.current_member_type != "reject":
                self.current_capacity += 1
                self.current_var.set(self.current_capacity)
        elif event == "flow_complete" or event == "reset_complete":
            self.complete_flow()
            return
            
        self.current_step += 1
        
        # Update progress
        progress = (self.current_step / len(self.flow_steps)) * 100
        self.progress_var.set(progress)
        
        self.update_display()
        
        # Auto advance to next step
        if self.auto_advance_var.get() and self.current_step < len(self.flow_steps):
            self.root.after(2000, self.next_step)  # 2 second delay
            
    def complete_flow(self):
        self.auto_flow_active = False
        self.current_step = 0
        self.progress_var.set(0)
        self.current_state = "Idle"
        
        self.start_btn.config(state=tk.NORMAL)
        self.next_btn.config(state=tk.DISABLED)
        
        self.log_event("✅ Flow completed - System ready for next vehicle")
        self.update_display()
        
    def update_capacity(self):
        self.max_capacity = self.capacity_var.get()
        
    def update_current_capacity(self):
        self.current_capacity = self.current_var.get()
        
    def set_capacity(self, value):
        self.current_capacity = value
        self.current_var.set(value)
        self.log_event(f"🏢 Parking capacity set to: {value}/{self.max_capacity}")
        
    def add_vip_member(self):
        plate = simpledialog.askstring("Add VIP Member", "Enter license plate:")
        if plate:
            plate = plate.strip().upper()
            self.vip_members.add(plate)
            if plate in self.subscribers:
                self.subscribers.remove(plate)
            self.save_members()
            self.update_member_list()
            self.log_event(f"👑 Added VIP member: {plate}")
            
    def add_subscriber(self):
        plate = simpledialog.askstring("Add Subscriber", "Enter license plate:")
        if plate:
            plate = plate.strip().upper()
            self.subscribers.add(plate)
            if plate in self.vip_members:
                self.vip_members.remove(plate)
            self.save_members()
            self.update_member_list()
            self.log_event(f"📋 Added subscriber: {plate}")
            
    def remove_member(self):
        selection = self.member_listbox.curselection()
        if selection:
            selected_text = self.member_listbox.get(selection[0])
            if "VIP:" in selected_text:
                plate = selected_text.split("VIP: ")[1]
                self.vip_members.discard(plate)
            elif "SUB:" in selected_text:
                plate = selected_text.split("SUB: ")[1]
                self.subscribers.discard(plate)
            
            self.save_members()
            self.update_member_list()
            self.log_event(f"🗑️ Removed member: {plate}")
            
    def update_member_list(self):
        self.member_listbox.delete(0, tk.END)
        
        self.member_listbox.insert(tk.END, "=== VIP MEMBERS ===")
        for vip in sorted(self.vip_members):
            self.member_listbox.insert(tk.END, f"VIP: {vip}")
            
        self.member_listbox.insert(tk.END, "")
        self.member_listbox.insert(tk.END, "=== SUBSCRIBERS ===")
        for sub in sorted(self.subscribers):
            self.member_listbox.insert(tk.END, f"SUB: {sub}")
            
    def reset_system(self):
        self.auto_flow_active = False
        self.current_step = 0
        self.current_state = "Idle"
        self.progress_var.set(0)
        self.current_plate = ""
        
        self.start_btn.config(state=tk.NORMAL)
        self.next_btn.config(state=tk.DISABLED)
        
        self.log_event("🔄 System Reset")
        self.update_display()
        
    def log_event(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def update_display(self):
        # Update capacity display
        capacity_percent = (self.current_capacity / self.max_capacity) * 100
        color = "#FF0000" if capacity_percent >= 100 else "#FF9800" if capacity_percent >= 80 else "#00ff88"
        self.capacity_label.config(text=f"🏢 {self.current_capacity}/{self.max_capacity} ({capacity_percent:.0f}%)", fg=color)
        
        # Update state display
        self.state_label.config(text=self.current_state.upper())
        
        colors = {
            "Idle": "#00ff88", "Detected": "#FFD700", "AuthCheck": "#FF8C00",
            "OpenGate": "#32CD32", "Closed": "#1E90FF", "WaitPayment": "#FF6347",
            "Confirmation": "#9370DB", "Reject": "#FF0000", "ErrorTimeout": "#DC143C"
        }
        self.state_label.config(fg=colors.get(self.current_state, "#ffffff"))
        
        # Update step info
        if self.auto_flow_active and self.current_step < len(self.flow_steps):
            step_info = f"Step {self.current_step + 1}/{len(self.flow_steps)}: {self.flow_steps[self.current_step][1].replace('_', ' ').title()}"
        else:
            step_info = "Ready for vehicle simulation"
        self.step_label.config(text=step_info)
        
        # Update canvas
        self.draw_gate_visual()
        
        # Update info text
        self.update_info_display()
        
    def draw_gate_visual(self):
        self.canvas.delete("all")
        
        # Draw road
        self.canvas.create_rectangle(0, 300, 600, 400, fill="#404040", outline="")
        
        # Draw lane markings
        for i in range(0, 600, 50):
            self.canvas.create_rectangle(i, 345, i+25, 355, fill="#FFFFFF")
        
        # Draw gate posts
        self.canvas.create_rectangle(150, 200, 170, 300, fill="#8B4513")
        self.canvas.create_rectangle(430, 200, 450, 300, fill="#8B4513")
        
        # Draw gate bar
        if self.current_state in ["OpenGate", "Closed"]:
            # Gate open
            self.canvas.create_rectangle(165, 180, 435, 190, fill="#00FF00")
            self.canvas.create_text(300, 160, text="🚪 GATE OPEN", fill="#00FF00", font=("Arial", 16, "bold"))
        else:
            # Gate closed
            self.canvas.create_rectangle(165, 290, 435, 300, fill="#FF0000")
            self.canvas.create_text(300, 160, text="🚫 GATE CLOSED", fill="#FF0000", font=("Arial", 16, "bold"))
        
        # Draw vehicle if present
        if self.current_state != "Idle" and self.current_plate:
            # Vehicle body
            self.canvas.create_rectangle(250, 320, 350, 380, fill="#4169E1", outline="#000080", width=2)
            # Windshield
            self.canvas.create_rectangle(260, 325, 340, 340, fill="#87CEEB")
            # Wheels
            self.canvas.create_oval(255, 370, 275, 390, fill="#2F2F2F")
            self.canvas.create_oval(325, 370, 345, 390, fill="#2F2F2F")
            
            # License plate
            self.canvas.create_rectangle(270, 360, 330, 375, fill="#FFFFFF", outline="#000000")
            self.canvas.create_text(300, 367, text=self.current_plate, fill="#000000", font=("Arial", 8, "bold"))
            
            # Member status indicator
            if self.current_member_type == "vip":
                self.canvas.create_text(300, 310, text="👑 VIP", fill="#FFD700", font=("Arial", 12, "bold"))
            elif self.current_member_type == "subscriber":
                self.canvas.create_text(300, 310, text="📋 SUB", fill="#00BCD4", font=("Arial", 12, "bold"))
            else:
                self.canvas.create_text(300, 310, text="🎫 VISITOR", fill="#FF9800", font=("Arial", 12, "bold"))
        
        # Draw sensors/camera
        self.canvas.create_oval(280, 260, 320, 300, fill="#FF69B4", outline="#8B008B", width=2)
        self.canvas.create_text(300, 280, text="📷", fill="#FFFFFF", font=("Arial", 16))
        
        # Draw capacity indicator
        capacity_percent = (self.current_capacity / self.max_capacity) * 100
        capacity_color = "#FF0000" if capacity_percent >= 100 else "#FF9800" if capacity_percent >= 80 else "#00FF00"
        
        # Capacity bar
        bar_width = 200
        bar_height = 20
        bar_x = 400
        bar_y = 50
        
        self.canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height, 
                                    fill="#333333", outline="#FFFFFF")
        
        filled_width = (self.current_capacity / self.max_capacity) * bar_width
        if filled_width > 0:
            self.canvas.create_rectangle(bar_x, bar_y, bar_x + filled_width, bar_y + bar_height, 
                                        fill=capacity_color, outline="")
        
        self.canvas.create_text(bar_x + bar_width/2, bar_y + bar_height/2, 
                               text=f"{self.current_capacity}/{self.max_capacity}", 
                               fill="#FFFFFF", font=("Arial", 10, "bold"))
        self.canvas.create_text(bar_x + bar_width/2, bar_y - 15, text="PARKING CAPACITY", 
                               fill="#FFFFFF", font=("Arial", 10, "bold"))
        
        # Status messages
        status_messages = {
            "Detected": "🎯 VEHICLE DETECTED - SCANNING PLATE",
            "AuthCheck": "🔍 CHECKING AUTHORIZATION",
            "WaitPayment": "💳 PAYMENT REQUIRED - RP 5,000",
            "Confirmation": "✅ PAYMENT CONFIRMED",
            "OpenGate": "🚪 OPENING GATE",
            "Closed": "🚙 VEHICLE PASSING THROUGH",
            "Reject": "🚫 ACCESS DENIED"
        }
        
        if self.current_state in status_messages:
            self.canvas.create_text(300, 120, text=status_messages[self.current_state], 
                                   fill="#FFFF00", font=("Arial", 14, "bold"))
        
        # Flow progress indicator
        if self.auto_flow_active and self.flow_steps:
            total_steps = len(self.flow_steps)
            for i, (state, event) in enumerate(self.flow_steps):
                x = 50 + (i * 500 / total_steps)
                y = 450
                
                if i < self.current_step:
                    color = "#00FF00"  # Completed
                elif i == self.current_step:
                    color = "#FFFF00"  # Current
                else:
                    color = "#666666"  # Pending
                
                self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, outline="white")
                
                if i < total_steps - 1:
                    next_x = 50 + ((i+1) * 500 / total_steps)
                    line_color = "#00FF00" if i < self.current_step else "#666666"
                    self.canvas.create_line(x+5, y, next_x-5, y, fill=line_color, width=2)
    
    def update_info_display(self):
        self.info_text.delete(1.0, tk.END)
        
        info = f"""
CURRENT SIMULATION STATUS
========================
License Plate: {self.current_plate if self.current_plate else 'None'}
Member Type: {self.current_member_type.upper()}
Current State: {self.current_state}

PARKING INFORMATION
==================
Current Capacity: {self.current_capacity} / {self.max_capacity}
Utilization: {(self.current_capacity/self.max_capacity)*100:.1f}%
Status: {'FULL' if self.current_capacity >= self.max_capacity else 'AVAILABLE'}

FLOW PROGRESS
=============
Active Flow: {'Yes' if self.auto_flow_active else 'No'}
Current Step: {self.current_step + 1 if self.auto_flow_active else 'N/A'}
Total Steps: {len(self.flow_steps) if self.flow_steps else 'N/A'}

MEMBER DATABASE
===============
VIP Members: {len(self.vip_members)}
Subscribers: {len(self.subscribers)}
Total Members: {len(self.vip_members) + len(self.subscribers)}
"""
        
        self.info_text.insert(1.0, info.strip())
    
    def run(self):
        self.log_event("🚀 Smart Gate System Started - Auto Flow Mode")
        self.log_event(f"📊 System initialized with {len(self.vip_members)} VIP members and {len(self.subscribers)} subscribers")
        self.update_display()
        self.root.mainloop()

if __name__ == "__main__":
    simulator = SmartGateSimulator()
    simulator.run()