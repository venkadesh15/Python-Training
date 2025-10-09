import streamlit as st

# ---------------- Classes ----------------
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

class Bike(Vehicle):
    def kick_start(self): return "Yes"
    def horn(self): return "Yes"

class Car(Vehicle):
    def play_music(self): return "Yes"
    def ac(self): return "Yes"
    def lock(self): return "Yes"

class SmartVehicle(Vehicle):
    def wifi_connection(self): return "Yes"
    def auto_drive(self): return "Yes"

class ElectricVehicle(SmartVehicle):
    def charge(self): return "Yes"

# ---------------- Vehicle Options ----------------
vehicle_options = {
    "Bike": {
        "Regular": {"brands": ["Honda", "Yamaha"], "models": {"Honda": ["CBR250R"], "Yamaha": ["R15"]}},
        "Smart": {"brands": ["TVS"], "models": {"TVS": ["iQube"]}}
    },
    "Car": {
        "Regular": {"brands": ["Maruti"], "models": {"Maruti": ["Swift"]}},
        "Smart": {"brands": ["Tesla"], "models": {"Tesla": ["Model 3"]}},
        "Electric": {"brands": ["Tesla"], "models": {"Tesla": ["Model S"]}}
    }
}

# ---------------- Streamlit UI ----------------
st.title("🚗 Vehicle Feature Simulator 🏍️")

vehicle_category = st.selectbox("Select Vehicle Category", ["Bike", "Car"])
vehicle_type = st.selectbox("Select Vehicle Type", list(vehicle_options[vehicle_category].keys()))
brand = st.selectbox("Select Brand", vehicle_options[vehicle_category][vehicle_type]["brands"])
model = st.selectbox("Select Model", vehicle_options[vehicle_category][vehicle_type]["models"][brand])

if st.button("Create Vehicle"):
    # ---------------- Create Vehicle Object ----------------
    if vehicle_category == "Bike":
        vehicle = Bike(brand, model) if vehicle_type == "Regular" else SmartVehicle(brand, model)
    elif vehicle_category == "Car":
        if vehicle_type == "Regular":
            vehicle = Car(brand, model)
        elif vehicle_type == "Smart":
            vehicle = SmartVehicle(brand, model)
        else:
            vehicle = ElectricVehicle(brand, model)

    # ---------------- Define Features per Vehicle Type ----------------
    feature_mapping = {
        "Regular": ["Kick Start", "Horn", "Play Music", "AC", "Lock"],
        "Smart": ["Kick Start", "Horn", "WiFi", "Auto Drive", "Play Music", "AC", "Lock"],
        "Electric": ["Kick Start", "Horn", "WiFi", "Auto Drive", "Play Music", "AC", "Lock", "Charge"]
    }

    # ---------------- Detect Features Automatically ----------------
    all_features = {
        "Kick Start": getattr(vehicle, "kick_start", lambda: "No")(),
        "Horn": getattr(vehicle, "horn", lambda: "No")(),
        "WiFi": getattr(vehicle, "wifi_connection", lambda: "No")(),
        "Auto Drive": getattr(vehicle, "auto_drive", lambda: "No")(),
        "Play Music": getattr(vehicle, "play_music", lambda: "No")(),
        "AC": getattr(vehicle, "ac", lambda: "No")(),
        "Lock": getattr(vehicle, "lock", lambda: "No")(),
        "Charge": getattr(vehicle, "charge", lambda: "No")()
    }

    # ---------------- Filter Features Based on Vehicle Type ----------------
    features_to_show = {k: v for k, v in all_features.items() if k in feature_mapping[vehicle_type]}

    # ---------------- Display Vehicle Info in One Box (Separate Lines) ----------------
    vehicle_info = f"**Brand:** {brand}  \n**Model:** {model}  \n**Type:** {vehicle_type} {vehicle_category}"
    st.info(vehicle_info, icon="🚘")

    # ---------------- Prepare Table Data ----------------
    table_data = [{"Feature": k, "Available": v} for k, v in features_to_show.items()]

    # ---------------- Display Table ----------------
    st.table(table_data)
