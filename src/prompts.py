"""
Step 2.3: Complete Interactive Prompt System
Extended version with all infrastructure options
"""

from typing import Dict, Any

class InfrastructurePrompter:
    """
    Interactive prompt system that asks users for infrastructure details.
    """
    
    def __init__(self):
        self.config = {}
    
    def prompt_provider(self) -> str:
        """Ask user to select cloud provider"""
        print("\n" + "="*60)
        print("SELECT CLOUD PROVIDER")
        print("="*60)
        
        providers = {
            1: {"name": "AWS", "full": "Amazon Web Services"},
            2: {"name": "Azure", "full": "Microsoft Azure"},
            3: {"name": "GCP", "full": "Google Cloud Platform"}
        }
        
        for key, value in providers.items():
            print(f"{key}. {value['name']} ({value['full']})")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-3): "))
                if choice in providers:
                    selected = providers[choice]["name"].lower()
                    print(f"Selected: {providers[choice]['name']}")
                    return selected
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except ValueError:
                print("Please enter a number (1, 2, or 3).")
    
    def prompt_region(self, provider: str) -> str:
        """Ask user to select region based on provider"""
        print("\n" + "="*60)
        print(f"SELECT REGION FOR {provider.upper()}")
        print("="*60)
        
        regions = {
            "aws": {
                1: "us-east-1 (N. Virginia)",
                2: "us-west-2 (Oregon)",
                3: "eu-west-1 (Ireland)",
                4: "ap-southeast-1 (Singapore)"
            },
            "azure": {
                1: "eastus (East US)",
                2: "westus (West US)",
                3: "westeurope (West Europe)",
                4: "southeastasia (Southeast Asia)"
            },
            "gcp": {
                1: "us-central1 (Iowa)",
                2: "us-east1 (South Carolina)",
                3: "europe-west1 (Belgium)",
                4: "asia-southeast1 (Singapore)"
            }
        }
        
        region_options = regions.get(provider, regions["aws"])
        
        for key, value in region_options.items():
            print(f"{key}. {value}")
        
        while True:
            try:
                choice = int(input(f"\nEnter your choice (1-{len(region_options)}): "))
                if choice in region_options:
                    selected = region_options[choice].split()[0]
                    print(f"Selected: {region_options[choice]}")
                    return selected
                else:
                    print(f"Invalid choice. Please enter 1-{len(region_options)}.")
            except ValueError:
                print("Please enter a valid number.")
    
    def prompt_instance_type(self, provider: str) -> str:
        """Ask user to select instance/VM size"""
        print("\n" + "="*60)
        print(f"SELECT INSTANCE SIZE FOR {provider.upper()}")
        print("="*60)
        
        instance_types = {
            "aws": {
                1: {"type": "t2.micro", "desc": "1 vCPU, 1 GB RAM (Free tier)"},
                2: {"type": "t3.small", "desc": "2 vCPUs, 2 GB RAM"},
                3: {"type": "t3.medium", "desc": "2 vCPUs, 4 GB RAM"},
                4: {"type": "m5.large", "desc": "2 vCPUs, 8 GB RAM"},
                5: {"type": "m5.xlarge", "desc": "4 vCPUs, 16 GB RAM"}
            },
            "azure": {
                1: {"type": "Standard_B1s", "desc": "1 vCPU, 1 GB RAM"},
                2: {"type": "Standard_B2s", "desc": "2 vCPUs, 4 GB RAM"},
                3: {"type": "Standard_D2s_v3", "desc": "2 vCPUs, 8 GB RAM"},
                4: {"type": "Standard_D4s_v3", "desc": "4 vCPUs, 16 GB RAM"}
            },
            "gcp": {
                1: {"type": "e2-micro", "desc": "0.25-2 vCPUs, 1 GB RAM"},
                2: {"type": "e2-small", "desc": "0.5-2 vCPUs, 2 GB RAM"},
                3: {"type": "e2-medium", "desc": "1-2 vCPUs, 4 GB RAM"},
                4: {"type": "n2-standard-2", "desc": "2 vCPUs, 8 GB RAM"},
                5: {"type": "n2-standard-4", "desc": "4 vCPUs, 16 GB RAM"}
            }
        }
        
        options = instance_types.get(provider, instance_types["aws"])
        
        for key, value in options.items():
            print(f"{key}. {value['type']:20s} - {value['desc']}")
        
        while True:
            try:
                choice = int(input(f"\nEnter your choice (1-{len(options)}): "))
                if choice in options:
                    selected = options[choice]["type"]
                    print(f"Selected: {selected}")
                    return selected
                else:
                    print(f"Invalid choice. Please enter 1-{len(options)}.")
            except ValueError:
                print("Please enter a valid number.")
    
    def prompt_operating_system(self) -> str:
        """Ask user to select operating system"""
        print("\n" + "="*60)
        print("SELECT OPERATING SYSTEM")
        print("="*60)
        
        operating_systems = {
            1: "Ubuntu",
            2: "Windows",
            3: "Amazon Linux"
        }
        
        for key, value in operating_systems.items():
            print(f"{key}. {value}")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-3): "))
                if choice in operating_systems:
                    selected = operating_systems[choice]
                    print(f"Selected: {selected}")
                    return selected
                else:
                    print("Invalid choice. Please enter 1-3.")
            except ValueError:
                print("Please enter a valid number.")
    
    def prompt_database_engine(self) -> str:
        """Ask user to select database engine"""
        print("\n" + "="*60)
        print("SELECT DATABASE ENGINE")
        print("="*60)
        
        engines = {
            1: {"name": "mysql", "desc": "MySQL"},
            2: {"name": "postgres", "desc": "PostgreSQL"},
            3: {"name": "mongodb", "desc": "MongoDB"}
        }
        
        for key, value in engines.items():
            print(f"{key}. {value['desc']}")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-3): "))
                if choice in engines:
                    selected = engines[choice]["name"]
                    print(f"Selected: {engines[choice]['desc']}")
                    return selected
                else:
                    print("Invalid choice. Please enter 1-3.")
            except ValueError:
                print("Please enter a valid number.")
    
    def prompt_storage_size(self) -> Dict[str, Any]:
        """Ask user for storage size"""
        print("\n" + "="*60)
        print("SPECIFY STORAGE SIZE")
        print("="*60)
        
        while True:
            try:
                size = int(input("Enter storage size in GB (e.g., 20, 100, 500): "))
                if size > 0:
                    print(f"Storage size: {size} GB")
                    return {"size": size, "unit": "GB"}
                else:
                    print("Storage size must be greater than 0.")
            except ValueError:
                print("Please enter a valid number.")
    
    def prompt_networking(self) -> str:
        """Ask user to select networking option"""
        print("\n" + "="*60)
        print("SELECT NETWORKING OPTION")
        print("="*60)
        
        networking = {
            1: "Default VPC",
            2: "Custom VPC with Subnet",
            3: "Private Network Only"
        }
        
        for key, value in networking.items():
            print(f"{key}. {value}")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-3): "))
                if choice in networking:
                    selected = networking[choice]
                    print(f"Selected: {selected}")
                    return selected
                else:
                    print("Invalid choice. Please enter 1-3.")
            except ValueError:
                print("Please enter a valid number.")
    
    def prompt_security(self) -> str:
        """Ask user to select security option"""
        print("\n" + "="*60)
        print("SELECT SECURITY OPTION")
        print("="*60)
        
        security = {
            1: "Basic Firewall",
            2: "Security Group (Strict Rules)",
            3: "Custom IAM Policy"
        }
        
        for key, value in security.items():
            print(f"{key}. {value}")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-3): "))
                if choice in security:
                    selected = security[choice]
                    print(f"Selected: {selected}")
                    return selected
                else:
                    print("Invalid choice. Please enter 1-3.")
            except ValueError:
                print("Please enter a valid number.")
    
    def prompt_monitoring(self) -> str:
        """Ask user to select monitoring option"""
        print("\n" + "="*60)
        print("SELECT MONITORING OPTION")
        print("="*60)
        
        monitoring = {
            1: "Enable Monitoring & Alerts",
            2: "Disable Monitoring"
        }
        
        for key, value in monitoring.items():
            print(f"{key}. {value}")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-2): "))
                if choice in monitoring:
                    selected = monitoring[choice]
                    print(f"Selected: {selected}")
                    return selected
                else:
                    print("Invalid choice. Please enter 1-2.")
            except ValueError:
                print("Please enter a valid number.")
    
    def confirm_configuration(self, config: Dict[str, Any]) -> bool:
        """Show final configuration and ask for confirmation"""
        print("\n" + "="*60)
        print("CONFIGURATION SUMMARY")
        print("="*60)
        
        for key, value in config.items():
            print(f"  {key:20s}: {value}")
        
        print("="*60)
        
        while True:
            confirm = input("\nProceed with this configuration? (yes/no): ").lower()
            if confirm in ["yes", "y"]:
                return True
            elif confirm in ["no", "n"]:
                return False
            else:
                print("Please enter 'yes' or 'no'.")


def test_complete_wizard():
    """Test the complete interactive prompt system"""
    
    prompter = InfrastructurePrompter()
    
    print("\n" + "="*60)
    print("SPEAK-TO-INFRASTRUCTURE SETUP WIZARD")
    print("="*60)
    print("\nLet's configure your infrastructure step by step.\n")
    
    # Collect configuration
    config = {}
    
    config["provider"] = prompter.prompt_provider()
    config["region"] = prompter.prompt_region(config["provider"])
    config["instance_type"] = prompter.prompt_instance_type(config["provider"])
    config["operating_system"] = prompter.prompt_operating_system()
    config["database_engine"] = prompter.prompt_database_engine()
    config["storage_size"] = f"{prompter.prompt_storage_size()['size']} GB"
    config["networking"] = prompter.prompt_networking()
    config["security"] = prompter.prompt_security()
    config["monitoring"] = prompter.prompt_monitoring()
    
    # Confirm
    if prompter.confirm_configuration(config):
        print("\nConfiguration confirmed!")
        print("Ready to generate Terraform code...")
        return config
    else:
        print("\nConfiguration cancelled.")
        return None


if __name__ == "__main__":
    result = test_complete_wizard()
    
    if result:
        print("\n" + "="*60)
        print("NEXT STEP: Generate Terraform files with this configuration")
        print("="*60)