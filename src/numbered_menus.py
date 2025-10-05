# numbered_menus.py - Enhanced Version with Objective Selections
# All choices are now menu-based selections

class InfrastructureConfig:
    """Store selected infrastructure configuration."""
    def __init__(self):
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


def get_valid_choice(prompt, valid_options):
    """Get a valid choice from the user with input validation."""
    while True:
        choice = input(prompt).strip()
        if choice in valid_options:
            return choice
        print(f"❌ Invalid choice! Please enter a number between 1 and {len(valid_options)}.")


def cloud_provider_menu():
    """Display cloud provider selection menu."""
    print("\n" + "="*50)
    print("   CLOUD PROVIDER SELECTION")
    print("="*50)
    print("\nWhich cloud provider would you like to use?\n")
    print("  1. AWS (Amazon Web Services)")
    print("  2. Azure (Microsoft Azure)")
    print("  3. GCP (Google Cloud Platform)")
    print("  4. Back to main menu")
    print("-"*50)
    
    providers = {
        "1": "AWS",
        "2": "Azure",
        "3": "GCP",
        "4": "back"
    }
    
    choice = get_valid_choice("\nPlease choose (1-4): ", ["1", "2", "3", "4"])
    return choice, providers.get(choice)


def resource_type_menu():
    """Display resource type selection menu."""
    print("\n" + "="*50)
    print("   RESOURCE TYPE SELECTION")
    print("="*50)
    print("\nWhat type of resource would you like to create?\n")
    print("  1. Compute (Virtual Machines/Instances)")
    print("  2. Database")
    print("  3. Networking")
    print("  4. Storage")
    print("  5. Back to previous menu")
    print("-"*50)
    
    resources = {
        "1": "Compute",
        "2": "Database",
        "3": "Networking",
        "4": "Storage",
        "5": "back"
    }
    
    choice = get_valid_choice("\nPlease choose (1-5): ", ["1", "2", "3", "4", "5"])
    return choice, resources.get(choice)


def instance_type_menu(cloud_provider):
    """Display instance type selection based on cloud provider."""
    print("\n" + "="*50)
    print(f"   INSTANCE TYPE SELECTION - {cloud_provider}")
    print("="*50)
    
    instance_types = {
        "AWS": {
            "1": {"name": "t2.micro", "desc": "1 vCPU, 1 GB RAM - Free tier eligible"},
            "2": {"name": "t2.small", "desc": "1 vCPU, 2 GB RAM - Light workloads"},
            "3": {"name": "t3.medium", "desc": "2 vCPU, 4 GB RAM - Balanced"},
            "4": {"name": "m5.large", "desc": "2 vCPU, 8 GB RAM - General purpose"},
            "5": {"name": "c5.xlarge", "desc": "4 vCPU, 8 GB RAM - Compute optimized"},
            "6": {"name": "r5.large", "desc": "2 vCPU, 16 GB RAM - Memory optimized"}
        },
        "Azure": {
            "1": {"name": "Standard_B1s", "desc": "1 vCPU, 1 GB RAM - Burstable"},
            "2": {"name": "Standard_B2s", "desc": "2 vCPU, 4 GB RAM - Burstable"},
            "3": {"name": "Standard_D2s_v3", "desc": "2 vCPU, 8 GB RAM - General purpose"},
            "4": {"name": "Standard_D4s_v3", "desc": "4 vCPU, 16 GB RAM - General purpose"},
            "5": {"name": "Standard_F4s_v2", "desc": "4 vCPU, 8 GB RAM - Compute optimized"},
            "6": {"name": "Standard_E4s_v3", "desc": "4 vCPU, 32 GB RAM - Memory optimized"}
        },
        "GCP": {
            "1": {"name": "e2-micro", "desc": "0.25-2 vCPU, 1 GB RAM - Micro"},
            "2": {"name": "e2-small", "desc": "0.5-2 vCPU, 2 GB RAM - Small"},
            "3": {"name": "e2-medium", "desc": "1-2 vCPU, 4 GB RAM - Medium"},
            "4": {"name": "n2-standard-2", "desc": "2 vCPU, 8 GB RAM - Balanced"},
            "5": {"name": "c2-standard-4", "desc": "4 vCPU, 16 GB RAM - Compute optimized"},
            "6": {"name": "n2-highmem-2", "desc": "2 vCPU, 16 GB RAM - Memory optimized"}
        }
    }
    
    options = instance_types.get(cloud_provider, {})
    print("\nSelect instance type:\n")
    
    for key, value in options.items():
        print(f"  {key}. {value['name']:<20} - {value['desc']}")
    
    print("-"*50)
    
    choice = get_valid_choice("\nPlease choose (1-6): ", list(options.keys()))
    return options[choice]['name']


def instance_count_menu():
    """Display instance count selection menu."""
    print("\n" + "="*50)
    print("   INSTANCE COUNT SELECTION")
    print("="*50)
    print("\nHow many instances do you need?\n")
    print("  1. Single instance (1)")
    print("  2. Small cluster (2-3 instances)")
    print("  3. Medium cluster (4-5 instances)")
    print("  4. Large cluster (6-10 instances)")
    print("-"*50)
    
    counts = {
        "1": "1",
        "2": "2-3",
        "3": "4-5",
        "4": "6-10"
    }
    
    choice = get_valid_choice("\nPlease choose (1-4): ", ["1", "2", "3", "4"])
    return counts[choice]


def database_engine_menu(cloud_provider):
    """Display database engine selection menu."""
    print("\n" + "="*50)
    print(f"   DATABASE ENGINE SELECTION - {cloud_provider}")
    print("="*50)
    print("\nSelect database engine:\n")
    print("  1. MySQL")
    print("  2. PostgreSQL")
    print("  3. MariaDB")
    print("  4. SQL Server")
    print("  5. Oracle")
    print("-"*50)
    
    engines = {
        "1": "MySQL",
        "2": "PostgreSQL",
        "3": "MariaDB",
        "4": "SQL Server",
        "5": "Oracle"
    }
    
    choice = get_valid_choice("\nPlease choose (1-5): ", ["1", "2", "3", "4", "5"])
    return engines[choice]


def database_size_menu():
    """Display database size selection menu."""
    print("\n" + "="*50)
    print("   DATABASE SIZE SELECTION")
    print("="*50)
    print("\nSelect database storage size:\n")
    print("  1. Small (20 GB)")
    print("  2. Medium (100 GB)")
    print("  3. Large (500 GB)")
    print("  4. X-Large (1 TB)")
    print("  5. XX-Large (2 TB)")
    print("-"*50)
    
    sizes = {
        "1": "20 GB",
        "2": "100 GB",
        "3": "500 GB",
        "4": "1 TB",
        "5": "2 TB"
    }
    
    choice = get_valid_choice("\nPlease choose (1-5): ", ["1", "2", "3", "4", "5"])
    return sizes[choice]


def network_cidr_menu():
    """Display network CIDR block selection menu."""
    print("\n" + "="*50)
    print("   NETWORK CIDR BLOCK SELECTION")
    print("="*50)
    print("\nSelect IP address range for your network:\n")
    print("  1. 10.0.0.0/16 (65,536 addresses)")
    print("  2. 172.16.0.0/16 (65,536 addresses)")
    print("  3. 192.168.0.0/16 (65,536 addresses)")
    print("  4. 10.0.0.0/24 (256 addresses)")
    print("  5. 172.16.0.0/24 (256 addresses)")
    print("-"*50)
    
    cidrs = {
        "1": "10.0.0.0/16",
        "2": "172.16.0.0/16",
        "3": "192.168.0.0/16",
        "4": "10.0.0.0/24",
        "5": "172.16.0.0/24"
    }
    
    choice = get_valid_choice("\nPlease choose (1-5): ", ["1", "2", "3", "4", "5"])
    return cidrs[choice]


def subnet_count_menu():
    """Display subnet count selection menu."""
    print("\n" + "="*50)
    print("   SUBNET COUNT SELECTION")
    print("="*50)
    print("\nHow many subnets do you need?\n")
    print("  1. Single subnet (1)")
    print("  2. Multi-AZ (2 subnets)")
    print("  3. Multi-AZ with backup (3 subnets)")
    print("  4. Complex network (4+ subnets)")
    print("-"*50)
    
    counts = {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4+"
    }
    
    choice = get_valid_choice("\nPlease choose (1-4): ", ["1", "2", "3", "4"])
    return counts[choice]


def storage_type_menu(cloud_provider):
    """Display storage type selection menu."""
    print("\n" + "="*50)
    print(f"   STORAGE TYPE SELECTION - {cloud_provider}")
    print("="*50)
    print("\nSelect storage performance tier:\n")
    print("  1. Standard (HDD-based, lower cost)")
    print("  2. Premium (SSD-based, better performance)")
    print("  3. Ultra Performance (NVMe, highest performance)")
    print("-"*50)
    
    types = {
        "1": "Standard",
        "2": "Premium",
        "3": "Ultra Performance"
    }
    
    choice = get_valid_choice("\nPlease choose (1-3): ", ["1", "2", "3"])
    return types[choice]


def storage_capacity_menu():
    """Display storage capacity selection menu."""
    print("\n" + "="*50)
    print("   STORAGE CAPACITY SELECTION")
    print("="*50)
    print("\nSelect storage capacity:\n")
    print("  1. Small (50 GB)")
    print("  2. Medium (250 GB)")
    print("  3. Large (1 TB)")
    print("  4. X-Large (5 TB)")
    print("  5. XX-Large (10 TB)")
    print("-"*50)
    
    capacities = {
        "1": "50 GB",
        "2": "250 GB",
        "3": "1 TB",
        "4": "5 TB",
        "5": "10 TB"
    }
    
    choice = get_valid_choice("\nPlease choose (1-5): ", ["1", "2", "3", "4", "5"])
    return capacities[choice]


def get_resource_details(cloud_provider, resource_type):
    """Gather additional details based on resource type using menus."""
    details = {}
    
    print(f"\n📝 Configuring {resource_type} on {cloud_provider}...")
    
    if resource_type == "Compute":
        details['Instance Type'] = instance_type_menu(cloud_provider)
        details['Instance Count'] = instance_count_menu()
        
    elif resource_type == "Database":
        details['Database Engine'] = database_engine_menu(cloud_provider)
        details['Storage Size'] = database_size_menu()
        
    elif resource_type == "Networking":
        details['CIDR Block'] = network_cidr_menu()
        details['Subnet Count'] = subnet_count_menu()
        
    elif resource_type == "Storage":
        details['Storage Type'] = storage_type_menu(cloud_provider)
        details['Storage Capacity'] = storage_capacity_menu()
    
    return details


def confirm_configuration(config):
    """Ask user to confirm the configuration."""
    config.display_summary()
    
    while True:
        confirm = input("\nProceed with this configuration? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            return True
        elif confirm in ['no', 'n']:
            return False
        print("Please enter 'yes' or 'no'.")


def main_flow():
    """Main program flow with improved navigation and validation."""
    print("\n" + "="*50)
    print("   SPEAK TO INFRASTRUCTURE")
    print("   Infrastructure Management System")
    print("="*50)
    
    config = InfrastructureConfig()
    
    while True:
        # Step 1: Cloud Provider Selection
        cloud_choice, cloud_provider = cloud_provider_menu()
        
        if cloud_choice == "4":
            print("\n👋 Returning to main menu...")
            return
        
        config.cloud_provider = cloud_provider
        print(f"\n✅ Selected: {cloud_provider}")
        
        # Step 2: Resource Type Selection
        while True:
            resource_choice, resource_type = resource_type_menu()
            
            if resource_choice == "5":
                print("\n⬅️  Going back to cloud provider selection...")
                break
            
            config.resource_type = resource_type
            print(f"\n✅ Selected: {resource_type}")
            
            # Step 3: Get additional details through menus
            config.resource_details = get_resource_details(cloud_provider, resource_type)
            
            # Step 4: Confirm configuration
            if confirm_configuration(config):
                print("\n" + "="*50)
                print("✅ Configuration captured successfully!")
                print("="*50)
                print("\n🚀 Ready to provision infrastructure...")
                print("(In a real system, this would create the resources)\n")
                return
            else:
                print("\n🔄 Let's reconfigure...")
                config.resource_details = {}
                continue
        
        # If user went back, reset the configuration
        config.cloud_provider = None
        config.resource_type = None
        config.resource_details = {}


if __name__ == "__main__":
    try:
        main_flow()
        print("\n👋 Thank you for using Speak to Infrastructure!")
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please try again or contact support.")