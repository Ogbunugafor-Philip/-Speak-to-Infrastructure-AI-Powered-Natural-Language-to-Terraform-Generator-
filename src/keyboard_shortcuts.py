# keyboard_shortcuts.py - Enhanced Version
# Comprehensive keyboard shortcuts integrated with full infrastructure system

class InfrastructureConfig:
    """Store selected infrastructure configuration."""
    def __init__(self):
        self.cloud_provider = None
        self.resource_type = None
        self.resource_details = {}
    
    def reset(self):
        """Reset configuration."""
        self.cloud_provider = None
        self.resource_type = None
        self.resource_details = {}
    
    def display_summary(self):
        """Display the current configuration summary."""
        print("\n" + "="*50)
        print("   CONFIGURATION SUMMARY")
        print("="*50)
        print(f"Cloud Provider: {self.cloud_provider or 'Not selected'}")
        print(f"Resource Type:  {self.resource_type or 'Not selected'}")
        if self.resource_details:
            print("\nConfiguration Details:")
            for key, value in self.resource_details.items():
                print(f"  - {key}: {value}")
        print("="*50)


def get_valid_choice(prompt, valid_options, show_shortcuts=True):
    """Get a valid choice with keyboard shortcuts."""
    if show_shortcuts:
        print("\n💡 Tip: Press 'b' to go back, 'q' to quit anytime")
    
    while True:
        choice = input(prompt).strip().lower()
        
        if choice == 'q':
            confirm_quit()
        elif choice == 'b':
            return 'back'
        elif choice in valid_options:
            return choice
        else:
            print(f"❌ Invalid choice! Valid options: {', '.join(valid_options)}")


def confirm_quit():
    """Confirm before quitting."""
    print("\n⚠️  Are you sure you want to quit?")
    confirm = input("Press 'y' to quit, any other key to continue: ").strip().lower()
    if confirm == 'y':
        print("\n👋 Thank you for using Speak to Infrastructure!")
        exit(0)


def quick_main_menu():
    """Display main menu with keyboard shortcuts."""
    print("\n" + "="*50)
    print("   SPEAK TO INFRASTRUCTURE")
    print("="*50)
    print("\nWhat would you like to do?\n")
    print("  [1/c] Create new infrastructure")
    print("  [2/v] View current infrastructure")
    print("  [3/m] Modify existing infrastructure")
    print("  [4/d] Destroy infrastructure")
    print("  [h]   Help & Shortcuts Guide")
    print("  [q]   Quit")
    print("-"*50)
    
    choice = input("\nEnter your choice: ").strip().lower()
    
    # Map shortcuts to main choices
    shortcut_map = {
        'c': '1',
        'v': '2',
        'm': '3',
        'd': '4'
    }
    
    return shortcut_map.get(choice, choice)


def quick_cloud_menu():
    """Display cloud provider menu with shortcuts."""
    print("\n" + "="*50)
    print("   CLOUD PROVIDER SELECTION")
    print("="*50)
    print("\nSelect cloud provider:\n")
    print("  [1/a] AWS (Amazon Web Services)")
    print("  [2/z] Azure (Microsoft Azure)")
    print("  [3/g] GCP (Google Cloud Platform)")
    print("  [b]   Back to main menu")
    print("  [q]   Quit")
    print("-"*50)
    
    providers = {
        "1": "AWS", "a": "AWS",
        "2": "Azure", "z": "Azure",
        "3": "GCP", "g": "GCP"
    }
    
    valid_keys = ['1', '2', '3', 'a', 'z', 'g', 'b', 'q']
    choice = get_valid_choice("\nEnter your choice: ", valid_keys, show_shortcuts=False)
    
    if choice == 'back':
        return 'back', None
    
    return choice, providers.get(choice)


def quick_resource_menu():
    """Display resource type menu with shortcuts."""
    print("\n" + "="*50)
    print("   RESOURCE TYPE SELECTION")
    print("="*50)
    print("\nSelect resource type:\n")
    print("  [1/c] Compute (Virtual Machines)")
    print("  [2/d] Database")
    print("  [3/n] Networking")
    print("  [4/s] Storage")
    print("  [b]   Back to cloud selection")
    print("  [q]   Quit")
    print("-"*50)
    
    resources = {
        "1": "Compute", "c": "Compute",
        "2": "Database", "d": "Database",
        "3": "Networking", "n": "Networking",
        "4": "Storage", "s": "Storage"
    }
    
    valid_keys = ['1', '2', '3', '4', 'c', 'd', 'n', 's', 'b', 'q']
    choice = get_valid_choice("\nEnter your choice: ", valid_keys, show_shortcuts=False)
    
    if choice == 'back':
        return 'back', None
    
    return choice, resources.get(choice)


def quick_instance_type_menu(cloud_provider):
    """Display instance type menu with shortcuts."""
    print("\n" + "="*50)
    print(f"   INSTANCE TYPE - {cloud_provider}")
    print("="*50)
    
    instance_types = {
        "AWS": {
            "1": {"name": "t2.micro", "desc": "1 vCPU, 1 GB RAM", "shortcut": "t"},
            "2": {"name": "t3.medium", "desc": "2 vCPU, 4 GB RAM", "shortcut": "m"},
            "3": {"name": "m5.large", "desc": "2 vCPU, 8 GB RAM", "shortcut": "l"},
            "4": {"name": "c5.xlarge", "desc": "4 vCPU, 8 GB RAM", "shortcut": "x"},
        },
        "Azure": {
            "1": {"name": "Standard_B1s", "desc": "1 vCPU, 1 GB RAM", "shortcut": "t"},
            "2": {"name": "Standard_B2s", "desc": "2 vCPU, 4 GB RAM", "shortcut": "m"},
            "3": {"name": "Standard_D2s_v3", "desc": "2 vCPU, 8 GB RAM", "shortcut": "l"},
            "4": {"name": "Standard_D4s_v3", "desc": "4 vCPU, 16 GB RAM", "shortcut": "x"},
        },
        "GCP": {
            "1": {"name": "e2-micro", "desc": "0.25-2 vCPU, 1 GB RAM", "shortcut": "t"},
            "2": {"name": "e2-medium", "desc": "1-2 vCPU, 4 GB RAM", "shortcut": "m"},
            "3": {"name": "n2-standard-2", "desc": "2 vCPU, 8 GB RAM", "shortcut": "l"},
            "4": {"name": "c2-standard-4", "desc": "4 vCPU, 16 GB RAM", "shortcut": "x"},
        }
    }
    
    options = instance_types.get(cloud_provider, {})
    print("\nSelect instance type:\n")
    
    valid_keys = []
    shortcut_map = {}
    
    for key, value in options.items():
        shortcut = value['shortcut']
        print(f"  [{key}/{shortcut}] {value['name']:<20} - {value['desc']}")
        valid_keys.extend([key, shortcut])
        shortcut_map[shortcut] = value['name']
        shortcut_map[key] = value['name']
    
    print("  [b]   Back")
    print("  [q]   Quit")
    print("-"*50)
    
    valid_keys.extend(['b', 'q'])
    choice = get_valid_choice("\nEnter your choice: ", valid_keys, show_shortcuts=False)
    
    if choice == 'back':
        return 'back'
    
    return shortcut_map.get(choice)


def quick_instance_count_menu():
    """Display instance count menu with shortcuts."""
    print("\n" + "="*50)
    print("   INSTANCE COUNT")
    print("="*50)
    print("\nHow many instances?\n")
    print("  [1/s] Single (1)")
    print("  [2/m] Small cluster (2-3)")
    print("  [3/l] Medium cluster (4-5)")
    print("  [4/x] Large cluster (6-10)")
    print("  [b]   Back")
    print("-"*50)
    
    counts = {
        "1": "1", "s": "1",
        "2": "2-3", "m": "2-3",
        "3": "4-5", "l": "4-5",
        "4": "6-10", "x": "6-10"
    }
    
    valid_keys = ['1', '2', '3', '4', 's', 'm', 'l', 'x', 'b', 'q']
    choice = get_valid_choice("\nEnter your choice: ", valid_keys, show_shortcuts=False)
    
    if choice == 'back':
        return 'back'
    
    return counts.get(choice)


def quick_database_engine_menu():
    """Display database engine menu with shortcuts."""
    print("\n" + "="*50)
    print("   DATABASE ENGINE")
    print("="*50)
    print("\nSelect database engine:\n")
    print("  [1/m] MySQL")
    print("  [2/p] PostgreSQL")
    print("  [3/r] MariaDB")
    print("  [4/s] SQL Server")
    print("  [5/o] Oracle")
    print("  [b]   Back")
    print("-"*50)
    
    engines = {
        "1": "MySQL", "m": "MySQL",
        "2": "PostgreSQL", "p": "PostgreSQL",
        "3": "MariaDB", "r": "MariaDB",
        "4": "SQL Server", "s": "SQL Server",
        "5": "Oracle", "o": "Oracle"
    }
    
    valid_keys = ['1', '2', '3', '4', '5', 'm', 'p', 'r', 's', 'o', 'b', 'q']
    choice = get_valid_choice("\nEnter your choice: ", valid_keys, show_shortcuts=False)
    
    if choice == 'back':
        return 'back'
    
    return engines.get(choice)


def quick_size_menu(resource_name):
    """Generic size selection menu with shortcuts."""
    print("\n" + "="*50)
    print(f"   {resource_name.upper()} SIZE")
    print("="*50)
    print("\nSelect size:\n")
    
    if resource_name == "Database":
        sizes = {
            "1": "20 GB", "s": "20 GB",
            "2": "100 GB", "m": "100 GB",
            "3": "500 GB", "l": "500 GB",
            "4": "1 TB", "x": "1 TB",
        }
    else:  # Storage
        sizes = {
            "1": "50 GB", "s": "50 GB",
            "2": "250 GB", "m": "250 GB",
            "3": "1 TB", "l": "1 TB",
            "4": "5 TB", "x": "5 TB",
        }
    
    print("  [1/s] Small")
    print("  [2/m] Medium")
    print("  [3/l] Large")
    print("  [4/x] X-Large")
    print("  [b]   Back")
    print("-"*50)
    
    valid_keys = ['1', '2', '3', '4', 's', 'm', 'l', 'x', 'b', 'q']
    choice = get_valid_choice("\nEnter your choice: ", valid_keys, show_shortcuts=False)
    
    if choice == 'back':
        return 'back'
    
    return sizes.get(choice)


def show_help():
    """Display help and shortcuts guide."""
    print("\n" + "="*50)
    print("   KEYBOARD SHORTCUTS GUIDE")
    print("="*50)
    print("""
GLOBAL SHORTCUTS:
  [q] - Quit application (with confirmation)
  [b] - Go back to previous menu
  [h] - Show this help

MAIN MENU:
  [1/c] - Create infrastructure
  [2/v] - View infrastructure
  [3/m] - Modify infrastructure
  [4/d] - Destroy infrastructure

CLOUD PROVIDERS:
  [1/a] - AWS
  [2/z] - Azure
  [3/g] - GCP (Google Cloud)

RESOURCES:
  [1/c] - Compute
  [2/d] - Database
  [3/n] - Networking
  [4/s] - Storage

SIZES:
  [1/s] - Small
  [2/m] - Medium
  [3/l] - Large
  [4/x] - X-Large

INSTANCE TYPES:
  [t] - Tiny/Micro (cheapest)
  [m] - Medium (balanced)
  [l] - Large (general purpose)
  [x] - X-Large (high performance)
    """)
    print("="*50)
    input("\nPress Enter to continue...")


def get_resource_details_quick(cloud_provider, resource_type):
    """Gather resource details using quick menus."""
    details = {}
    
    if resource_type == "Compute":
        instance_type = quick_instance_type_menu(cloud_provider)
        if instance_type == 'back':
            return 'back'
        details['Instance Type'] = instance_type
        
        instance_count = quick_instance_count_menu()
        if instance_count == 'back':
            return 'back'
        details['Instance Count'] = instance_count
        
    elif resource_type == "Database":
        db_engine = quick_database_engine_menu()
        if db_engine == 'back':
            return 'back'
        details['Database Engine'] = db_engine
        
        db_size = quick_size_menu("Database")
        if db_size == 'back':
            return 'back'
        details['Storage Size'] = db_size
        
    elif resource_type == "Networking":
        print("\n📝 Network configuration (simplified for demo)")
        details['CIDR Block'] = "10.0.0.0/16"
        details['Subnet Count'] = "2"
        
    elif resource_type == "Storage":
        print("\n📝 Storage configuration")
        details['Storage Type'] = "Premium SSD"
        
        storage_size = quick_size_menu("Storage")
        if storage_size == 'back':
            return 'back'
        details['Storage Capacity'] = storage_size
    
    return details


def main_quick_flow():
    """Main program flow with keyboard shortcuts."""
    print("\n" + "="*50)
    print("   SPEAK TO INFRASTRUCTURE")
    print("   Quick Navigation Mode Enabled!")
    print("="*50)
    print("\n💡 Tip: Use keyboard shortcuts for faster navigation")
    print("   Press 'h' anytime for shortcuts guide\n")
    
    config = InfrastructureConfig()
    
    while True:
        main_choice = quick_main_menu()
        
        if main_choice == 'h':
            show_help()
            continue
            
        elif main_choice == 'q':
            confirm_quit()
            
        elif main_choice == '1':  # Create infrastructure
            print("\n✅ Create infrastructure selected")
            
            while True:
                cloud_choice, cloud_provider = quick_cloud_menu()
                
                if cloud_choice == 'back':
                    config.reset()
                    break
                
                config.cloud_provider = cloud_provider
                print(f"\n✅ Selected: {cloud_provider}")
                
                while True:
                    resource_choice, resource_type = quick_resource_menu()
                    
                    if resource_choice == 'back':
                        config.resource_type = None
                        config.resource_details = {}
                        break
                    
                    config.resource_type = resource_type
                    print(f"\n✅ Selected: {resource_type}")
                    
                    details = get_resource_details_quick(cloud_provider, resource_type)
                    
                    if details == 'back':
                        continue
                    
                    config.resource_details = details
                    
                    # Show summary and confirm
                    config.display_summary()
                    
                    confirm = input("\nProceed? (y/n/b for back): ").strip().lower()
                    
                    if confirm == 'y':
                        print("\n" + "="*50)
                        print("✅ Infrastructure configuration complete!")
                        print("🚀 Ready to provision...")
                        print("="*50 + "\n")
                        config.reset()
                        break
                    elif confirm == 'b':
                        continue
                    else:
                        print("\n🔄 Reconfiguring...")
                        continue
                
                break
                
        elif main_choice == '2':  # View
            print("\n📊 Viewing current infrastructure...")
            print("(No infrastructure deployed yet)")
            input("\nPress Enter to continue...")
            
        elif main_choice == '3':  # Modify
            print("\n🔧 Modify infrastructure")
            print("(Feature coming soon)")
            input("\nPress Enter to continue...")
            
        elif main_choice == '4':  # Destroy
            print("\n⚠️  Destroy infrastructure")
            confirm = input("Type 'DELETE' to confirm: ")
            if confirm == 'DELETE':
                print("🗑️  Infrastructure destroyed")
            else:
                print("❌ Cancelled")
            input("\nPress Enter to continue...")
            
        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    try:
        main_quick_flow()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")