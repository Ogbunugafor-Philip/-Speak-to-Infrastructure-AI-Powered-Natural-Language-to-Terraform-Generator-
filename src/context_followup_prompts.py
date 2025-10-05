"""
context_followup_prompts.py - Enhanced Version
---------------------------------
Advanced context-aware follow-up system with intelligent branching,
validation, and multi-level decision trees.
"""

import datetime
import json


class ContextMemory:
    """Manages context and session state across the conversation."""
    
    def __init__(self):
        self.context = {
            "cloud_provider": None,
            "region": None,
            "resource_type": None,
            "configuration": {},
            "features_enabled": [],
            "decisions": [],
            "session_start": datetime.datetime.now(),
            "last_updated": None
        }
    
    def set(self, key, value):
        """Set a context value."""
        self.context[key] = value
        self.context["last_updated"] = datetime.datetime.now()
        
        # Track decision history
        self.context["decisions"].append({
            "key": key,
            "value": value,
            "timestamp": datetime.datetime.now()
        })
    
    def get(self, key, default=None):
        """Get a context value."""
        return self.context.get(key, default)
    
    def add_feature(self, feature):
        """Add an enabled feature."""
        if feature not in self.context["features_enabled"]:
            self.context["features_enabled"].append(feature)
    
    def add_config(self, key, value):
        """Add configuration item."""
        self.context["configuration"][key] = value
    
    def has_context(self, *keys):
        """Check if specific context keys exist."""
        return all(self.context.get(key) is not None for key in keys)
    
    def get_summary(self):
        """Get formatted summary of context."""
        return {
            "provider": self.context["cloud_provider"],
            "region": self.context["region"],
            "resource": self.context["resource_type"],
            "features": self.context["features_enabled"],
            "config_items": len(self.context["configuration"]),
            "decisions": len(self.context["decisions"]),
            "session_duration": (datetime.datetime.now() - self.context["session_start"]).seconds
        }
    
    def export_json(self):
        """Export context as JSON."""
        # Convert datetime objects to strings
        export_data = self.context.copy()
        export_data["session_start"] = export_data["session_start"].isoformat()
        if export_data["last_updated"]:
            export_data["last_updated"] = export_data["last_updated"].isoformat()
        
        for decision in export_data["decisions"]:
            decision["timestamp"] = decision["timestamp"].isoformat()
        
        return json.dumps(export_data, indent=2)


class ProviderSpecificQuestions:
    """Provider-specific question configurations."""
    
    AWS_QUESTIONS = {
        "region": {
            "prompt": "Which AWS region would you like to use?",
            "options": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
            "recommendations": {
                "compute": "us-east-1 (lowest latency for NA)",
                "database": "us-west-2 (good RDS availability)",
                "storage": "eu-west-1 (GDPR compliance)"
            }
        },
        "features": [
            {
                "name": "S3 Versioning",
                "key": "s3_versioning",
                "description": "Keep multiple versions of objects in S3",
                "benefit": "Protects against accidental deletions",
                "cost": "Additional storage costs"
            },
            {
                "name": "EC2 Spot Instances",
                "key": "spot_instances",
                "description": "Use spare EC2 capacity at discounted rates",
                "benefit": "Up to 90% cost savings",
                "cost": "Instances can be interrupted"
            },
            {
                "name": "CloudWatch Alarms",
                "key": "cloudwatch_alarms",
                "description": "Automated monitoring and alerting",
                "benefit": "Proactive issue detection",
                "cost": "Per-alarm pricing"
            }
        ],
        "networking": {
            "vpc_config": ["Default VPC", "Custom VPC", "Multi-VPC Setup"],
            "subnet_strategy": ["Single AZ", "Multi-AZ", "Multi-Region"]
        }
    }
    
    AZURE_QUESTIONS = {
        "region": {
            "prompt": "Which Azure region would you like to deploy in?",
            "options": ["eastus", "westus2", "northeurope", "southeastasia"],
            "recommendations": {
                "compute": "eastus (largest region)",
                "database": "westus2 (good for SQL)",
                "storage": "northeurope (GDPR compliance)"
            }
        },
        "features": [
            {
                "name": "Hybrid Cloud Integration",
                "key": "hybrid_cloud",
                "description": "Connect on-premises to Azure",
                "benefit": "Seamless hybrid scenarios",
                "cost": "ExpressRoute or VPN costs"
            },
            {
                "name": "VM Auto-scaling",
                "key": "vm_autoscaling",
                "description": "Automatically scale VMs based on demand",
                "benefit": "Cost optimization and performance",
                "cost": "Standard VM pricing"
            },
            {
                "name": "Azure AD Integration",
                "key": "azure_ad",
                "description": "Enterprise identity management",
                "benefit": "Single sign-on and security",
                "cost": "Premium tier required"
            }
        ],
        "networking": {
            "vnet_config": ["Basic VNet", "Hub-Spoke", "Virtual WAN"],
            "connectivity": ["Internet Only", "ExpressRoute", "Site-to-Site VPN"]
        }
    }
    
    GCP_QUESTIONS = {
        "region": {
            "prompt": "Which GCP zone would you prefer?",
            "options": ["us-central1-a", "us-west1-b", "europe-west1-b", "asia-southeast1-a"],
            "recommendations": {
                "compute": "us-central1-a (best for compute)",
                "database": "us-west1-b (good for databases)",
                "storage": "europe-west1-b (GDPR compliance)"
            }
        },
        "features": [
            {
                "name": "Cloud Storage Lifecycle",
                "key": "storage_lifecycle",
                "description": "Automated object lifecycle management",
                "benefit": "Optimize storage costs",
                "cost": "Minimal management fees"
            },
            {
                "name": "Stackdriver Monitoring",
                "key": "stackdriver",
                "description": "Full-stack monitoring and logging",
                "benefit": "Comprehensive observability",
                "cost": "Usage-based pricing"
            },
            {
                "name": "Preemptible VMs",
                "key": "preemptible_vms",
                "description": "Short-lived compute instances at low cost",
                "benefit": "Up to 80% cost savings",
                "cost": "Can be preempted anytime"
            }
        ],
        "networking": {
            "vpc_config": ["Auto Mode VPC", "Custom Mode VPC", "Shared VPC"],
            "load_balancing": ["Global HTTP(S)", "Regional TCP/UDP", "Internal"]
        }
    }
    
    @classmethod
    def get_questions(cls, provider):
        """Get questions for specific provider."""
        mapping = {
            "AWS": cls.AWS_QUESTIONS,
            "Azure": cls.AZURE_QUESTIONS,
            "GCP": cls.GCP_QUESTIONS
        }
        return mapping.get(provider)


class ContextAwareFollowUp:
    """Main class for handling context-aware follow-up questions."""
    
    def __init__(self, context_memory):
        self.memory = context_memory
    
    def validate_region(self, region, valid_regions):
        """Validate region input."""
        region_lower = region.lower().strip()
        
        # Check exact match
        if region_lower in [r.lower() for r in valid_regions]:
            return True, region_lower
        
        # Check partial match
        for valid_region in valid_regions:
            if region_lower in valid_region.lower():
                return True, valid_region
        
        return False, None
    
    def ask_region(self, provider_questions):
        """Ask about region with validation and recommendations."""
        region_config = provider_questions["region"]
        
        print("\n" + "═"*70)
        print("   🌍 REGION SELECTION")
        print("═"*70)
        
        print(f"\n{region_config['prompt']}")
        print("\nAvailable regions:")
        
        for i, region in enumerate(region_config["options"], 1):
            print(f"  [{i}] {region}")
        
        # Show recommendations based on resource type
        resource_type = self.memory.get("resource_type")
        if resource_type and resource_type in region_config["recommendations"]:
            print(f"\n💡 Recommended for {resource_type}:")
            print(f"   {region_config['recommendations'][resource_type]}")
        
        print("\n💡 Tip: Enter number or type region name")
        
        while True:
            region_input = input("\n🌍 Your choice: ").strip()
            
            if not region_input:
                print("❌ Please enter a region")
                continue
            
            # Check if number was entered
            if region_input.isdigit():
                idx = int(region_input) - 1
                if 0 <= idx < len(region_config["options"]):
                    return region_config["options"][idx]
                else:
                    print(f"❌ Please enter a number between 1 and {len(region_config['options'])}")
                    continue
            
            # Validate text input
            valid, validated_region = self.validate_region(region_input, region_config["options"])
            
            if valid:
                return validated_region
            else:
                print(f"❌ Invalid region. Please choose from: {', '.join(region_config['options'])}")
    
    def ask_feature(self, feature_config):
        """Ask about enabling a specific feature."""
        print("\n" + "─"*70)
        print(f"   ⚙️  {feature_config['name']}")
        print("─"*70)
        
        print(f"\n📝 Description:")
        print(f"   {feature_config['description']}")
        
        print(f"\n✅ Benefit:")
        print(f"   {feature_config['benefit']}")
        
        print(f"\n💰 Cost Consideration:")
        print(f"   {feature_config['cost']}")
        
        print("\n" + "─"*70)
        
        while True:
            choice = input("\n❓ Enable this feature? (y/n/skip/info): ").strip().lower()
            
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            elif choice == 'skip':
                return None
            elif choice in ['info', 'i', '?']:
                print(f"\n📋 More about {feature_config['name']}:")
                print(f"   Key: {feature_config['key']}")
                print(f"   Benefit: {feature_config['benefit']}")
                print(f"   Cost: {feature_config['cost']}")
            else:
                print("❌ Please enter 'y' (yes), 'n' (no), or 'skip'")
    
    def ask_networking(self, provider_questions, provider):
        """Ask networking-related questions."""
        networking = provider_questions["networking"]
        
        print("\n" + "═"*70)
        print("   🌐 NETWORKING CONFIGURATION")
        print("═"*70)
        
        # VPC/VNet configuration
        if provider == "Azure":
            config_key = "vnet_config"
            config_label = "Virtual Network"
        else:
            config_key = "vpc_config"
            config_label = "VPC"
        
        print(f"\n{config_label} Configuration:")
        vpc_options = networking[config_key]
        
        for i, option in enumerate(vpc_options, 1):
            print(f"  [{i}] {option}")
        
        while True:
            vpc_choice = input(f"\n🌐 Select {config_label} strategy (1-{len(vpc_options)}): ").strip()
            
            if vpc_choice.isdigit() and 1 <= int(vpc_choice) <= len(vpc_options):
                selected_vpc = vpc_options[int(vpc_choice) - 1]
                self.memory.add_config(f"{config_key}", selected_vpc)
                print(f"✅ {config_label}: {selected_vpc}")
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(vpc_options)}")
        
        # Additional networking options for Azure
        if provider == "Azure" and "connectivity" in networking:
            print("\nConnectivity Option:")
            conn_options = networking["connectivity"]
            
            for i, option in enumerate(conn_options, 1):
                print(f"  [{i}] {option}")
            
            while True:
                conn_choice = input(f"\n🔗 Select connectivity (1-{len(conn_options)}): ").strip()
                
                if conn_choice.isdigit() and 1 <= int(conn_choice) <= len(conn_options):
                    selected_conn = conn_options[int(conn_choice) - 1]
                    self.memory.add_config("connectivity", selected_conn)
                    print(f"✅ Connectivity: {selected_conn}")
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(conn_options)}")
        
        # GCP-specific load balancing
        if provider == "GCP" and "load_balancing" in networking:
            print("\nLoad Balancing Strategy:")
            lb_options = networking["load_balancing"]
            
            for i, option in enumerate(lb_options, 1):
                print(f"  [{i}] {option}")
            
            while True:
                lb_choice = input(f"\n⚖️  Select load balancer (1-{len(lb_options)}): ").strip()
                
                if lb_choice.isdigit() and 1 <= int(lb_choice) <= len(lb_options):
                    selected_lb = lb_options[int(lb_choice) - 1]
                    self.memory.add_config("load_balancing", selected_lb)
                    print(f"✅ Load Balancing: {selected_lb}")
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(lb_options)}")
    
    def display_summary(self, provider):
        """Display comprehensive configuration summary."""
        print("\n" + "╔"*70)
        print("║" + " 📊 CONFIGURATION SUMMARY ".center(138) + "║")
        print("╚"*70)
        
        print(f"\n☁️  Cloud Provider: {provider}")
        print(f"🌍 Region: {self.memory.get('region')}")
        
        if self.memory.get("resource_type"):
            print(f"📦 Resource Type: {self.memory.get('resource_type')}")
        
        features = self.memory.get("features_enabled")
        if features:
            print(f"\n⚙️  Enabled Features: ({len(features)})")
            for feature in features:
                print(f"   ✓ {feature}")
        else:
            print("\n⚙️  Enabled Features: None")
        
        config = self.memory.get("configuration")
        if config:
            print(f"\n🔧 Configuration Options:")
            for key, value in config.items():
                print(f"   • {key}: {value}")
        
        # Session info
        summary = self.memory.get_summary()
        print(f"\n📈 Session Statistics:")
        print(f"   • Decisions made: {summary['decisions']}")
        print(f"   • Duration: {summary['session_duration']} seconds")
        print(f"   • Last updated: {self.memory.get('last_updated').strftime('%H:%M:%S') if self.memory.get('last_updated') else 'N/A'}")
        
        print("\n" + "═"*70)
    
    def ask_follow_up(self):
        """Main method to ask context-aware follow-up questions."""
        provider = self.memory.get("cloud_provider")
        
        if not provider:
            print("\n⚠️  No previous context found.")
            print("💡 Please select a cloud provider first.")
            return None
        
        print("\n" + "╔"*70)
        print("║" + f" 🧩 CONTEXT-AWARE FOLLOW-UP: {provider} ".center(138) + "║")
        print("╚"*70)
        
        print(f"\n💡 Since you selected {provider}, let's configure your environment...")
        
        # Get provider-specific questions
        provider_questions = ProviderSpecificQuestions.get_questions(provider)
        
        if not provider_questions:
            print(f"❌ No questions configured for {provider}")
            return None
        
        # Step 1: Ask about region
        region = self.ask_region(provider_questions)
        self.memory.set("region", region)
        print(f"\n✅ Region selected: {region}")
        
        # Step 2: Ask about features
        print("\n" + "═"*70)
        print("   ⚙️  FEATURE CONFIGURATION")
        print("═"*70)
        print(f"\nLet's configure some {provider}-specific features...")
        
        features_enabled = []
        
        for feature in provider_questions["features"]:
            result = self.ask_feature(feature)
            
            if result is True:
                features_enabled.append(feature["name"])
                self.memory.add_feature(feature["name"])
                self.memory.add_config(feature["key"], True)
                print(f"✅ {feature['name']} enabled")
            elif result is False:
                print(f"⏭️  {feature['name']} skipped")
            elif result is None:
                print(f"⏩ Skipping remaining features...")
                break
        
        # Step 3: Networking configuration
        configure_network = input("\n🌐 Configure networking? (y/n): ").strip().lower()
        
        if configure_network in ['y', 'yes']:
            self.ask_networking(provider_questions, provider)
        
        # Final summary
        self.display_summary(provider)
        
        # Export option
        export_choice = input("\n💾 Export configuration to JSON? (y/n): ").strip().lower()
        
        if export_choice in ['y', 'yes']:
            json_data = self.memory.export_json()
            filename = f"{provider.lower()}_config_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            try:
                with open(filename, 'w') as f:
                    f.write(json_data)
                print(f"✅ Configuration exported to: {filename}")
            except Exception as e:
                print(f"❌ Export failed: {e}")
                print("\nConfiguration JSON:")
                print(json_data)
        
        return self.memory.context


def main():
    """Main function to demonstrate context-aware follow-up."""
    print("\n" + "╔"*70)
    print("║" + " 🎯 CONTEXT-AWARE FOLLOW-UP SYSTEM ".center(138) + "║")
    print("╚"*70)
    
    # Initialize context memory
    context_memory = ContextMemory()
    
    # Simulate or get previous provider selection
    print("\n📋 Previous Selection Required")
    print("─"*70)
    
    provider = input("Enter previously selected provider (AWS/Azure/GCP): ").strip()
    
    if provider not in ["AWS", "Azure", "GCP"]:
        print("❌ Invalid provider")
        return
    
    context_memory.set("cloud_provider", provider)
    
    # Optional: set resource type for better recommendations
    resource = input("What type of resource? (compute/database/storage): ").strip().lower()
    if resource in ["compute", "database", "storage"]:
        context_memory.set("resource_type", resource)
    
    # Run follow-up questions
    follow_up = ContextAwareFollowUp(context_memory)
    result = follow_up.ask_follow_up()
    
    if result:
        print("\n✅ Configuration complete!")
        print("🚀 Ready to provision infrastructure")
    else:
        print("\n❌ Configuration incomplete")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuration cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")