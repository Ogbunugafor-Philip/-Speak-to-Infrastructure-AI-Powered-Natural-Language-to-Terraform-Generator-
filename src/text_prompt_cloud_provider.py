"""
text_prompt_cloud_provider.py - Enhanced Version
---------------------------------
Advanced text-based prompting for cloud provider selection.
Features: Keyboard shortcuts, detailed info, comparison mode, and history tracking.
"""

import time
from datetime import datetime


class CloudProviderData:
    """Comprehensive cloud provider information."""
    
    PROVIDERS = {
        "AWS": {
            "full_name": "Amazon Web Services",
            "description": "The most widely used cloud platform with 200+ services",
            "founded": "2006",
            "strengths": ["Largest market share", "Extensive service catalog", "Global infrastructure"],
            "popular_services": ["EC2", "S3", "Lambda", "RDS"],
            "icon": "🟧",
            "pricing": "Pay-as-you-go, most competitive for large scale"
        },
        "Azure": {
            "full_name": "Microsoft Azure",
            "description": "Microsoft's enterprise cloud platform with seamless integration",
            "founded": "2010",
            "strengths": ["Microsoft integration", "Hybrid cloud", "Enterprise ready"],
            "popular_services": ["Virtual Machines", "Azure AD", "SQL Database", "App Service"],
            "icon": "🔵",
            "pricing": "Competitive enterprise pricing, good Windows licensing"
        },
        "GCP": {
            "full_name": "Google Cloud Platform",
            "description": "Google's scalable and data-driven cloud platform",
            "founded": "2008",
            "strengths": ["Data analytics", "Machine learning", "Kubernetes expertise"],
            "popular_services": ["Compute Engine", "BigQuery", "Cloud Storage", "GKE"],
            "icon": "🔴",
            "pricing": "Sustained use discounts, best for data/ML workloads"
        }
    }
    
    @classmethod
    def get_provider(cls, key):
        """Get provider information."""
        return cls.PROVIDERS.get(key)
    
    @classmethod
    def get_all_providers(cls):
        """Get all provider keys."""
        return list(cls.PROVIDERS.keys())


class SelectionHistory:
    """Track selection history and statistics."""
    
    def __init__(self):
        self.history = []
    
    def add_selection(self, provider, method="text"):
        """Record a selection."""
        self.history.append({
            "provider": provider,
            "method": method,
            "timestamp": datetime.now()
        })
    
    def get_most_recent(self):
        """Get most recent selection."""
        return self.history[-1] if self.history else None
    
    def get_stats(self):
        """Get selection statistics."""
        if not self.history:
            return None
        
        provider_counts = {}
        for entry in self.history:
            provider = entry["provider"]
            provider_counts[provider] = provider_counts.get(provider, 0) + 1
        
        return {
            "total_selections": len(self.history),
            "provider_counts": provider_counts,
            "most_selected": max(provider_counts, key=provider_counts.get)
        }


class TextCloudProviderSelector:
    """Enhanced text-based cloud provider selector."""
    
    def __init__(self):
        self.history = SelectionHistory()
        self.show_details = False
    
    def display_menu(self, show_shortcuts=True):
        """Display enhanced provider selection menu."""
        print("\n" + "═"*70)
        print("   ☁️  CLOUD PROVIDER SELECTION")
        print("═"*70)
        
        providers = CloudProviderData.get_all_providers()
        
        for i, provider_key in enumerate(providers, 1):
            provider = CloudProviderData.get_provider(provider_key)
            
            print(f"\n{provider['icon']} [{i}/{provider_key[0].lower()}] {provider_key}")
            print(f"   {provider['full_name']}")
            print(f"   {provider['description']}")
            
            if self.show_details:
                print(f"   💪 Strengths: {', '.join(provider['strengths'][:2])}")
                print(f"   🔧 Popular: {', '.join(provider['popular_services'][:3])}")
        
        print("\n" + "─"*70)
        
        if show_shortcuts:
            print("SHORTCUTS:")
            print("  [1-3]   Select by number")
            print("  [a/z/g] Select by letter (AWS/Azure/GCP)")
            print("  [i]     Toggle detailed info")
            print("  [c]     Compare all providers")
            print("  [h]     Show selection history")
            print("  [q]     Quit")
        
        print("─"*70)
    
    def show_provider_details(self, provider_key):
        """Show detailed information about a provider."""
        provider = CloudProviderData.get_provider(provider_key)
        
        print("\n" + "╔"*70)
        print("║" + f" {provider['icon']} {provider_key} - DETAILED INFORMATION ".center(138) + "║")
        print("╚"*70)
        
        print(f"\n📋 Full Name: {provider['full_name']}")
        print(f"📅 Founded: {provider['founded']}")
        print(f"\n📝 Description:")
        print(f"   {provider['description']}")
        
        print(f"\n💪 Key Strengths:")
        for strength in provider['strengths']:
            print(f"   • {strength}")
        
        print(f"\n🔧 Popular Services:")
        for service in provider['popular_services']:
            print(f"   • {service}")
        
        print(f"\n💰 Pricing Model:")
        print(f"   {provider['pricing']}")
        
        print("\n" + "═"*70)
    
    def compare_providers(self):
        """Display side-by-side comparison of all providers."""
        print("\n" + "╔"*70)
        print("║" + " 📊 PROVIDER COMPARISON ".center(138) + "║")
        print("╚"*70)
        
        providers = {key: CloudProviderData.get_provider(key) for key in CloudProviderData.get_all_providers()}
        
        # Market share comparison
        print("\n┌─────────────────────────────────────────────────────────────────┐")
        print("│ OVERVIEW                                                        │")
        print("├──────────────┬──────────────────┬────────────────────────────────┤")
        print("│ Provider     │ Founded          │ Primary Focus                  │")
        print("├──────────────┼──────────────────┼────────────────────────────────┤")
        
        for key, provider in providers.items():
            focus = provider['strengths'][0][:28]
            print(f"│ {key:<12} │ {provider['founded']:<16} │ {focus:<30} │")
        
        print("└──────────────┴──────────────────┴────────────────────────────────┘")
        
        # Strengths comparison
        print("\n┌─────────────────────────────────────────────────────────────────┐")
        print("│ KEY STRENGTHS                                                   │")
        print("└─────────────────────────────────────────────────────────────────┘")
        
        for key, provider in providers.items():
            print(f"\n{provider['icon']} {key}:")
            for strength in provider['strengths']:
                print(f"   ✓ {strength}")
        
        # Pricing comparison
        print("\n┌─────────────────────────────────────────────────────────────────┐")
        print("│ PRICING MODELS                                                  │")
        print("└─────────────────────────────────────────────────────────────────┘")
        
        for key, provider in providers.items():
            print(f"\n{provider['icon']} {key}:")
            print(f"   {provider['pricing']}")
        
        print("\n" + "═"*70)
    
    def show_history(self):
        """Display selection history."""
        stats = self.history.get_stats()
        
        if not stats:
            print("\n📊 No selection history yet")
            return
        
        print("\n" + "═"*70)
        print("   📊 SELECTION HISTORY")
        print("═"*70)
        
        print(f"\n📈 Total selections: {stats['total_selections']}")
        print(f"⭐ Most selected: {stats['most_selected']}")
        
        print("\n📋 Provider breakdown:")
        for provider, count in stats['provider_counts'].items():
            percentage = (count / stats['total_selections']) * 100
            bar = "█" * int(percentage / 5)
            print(f"   {provider:<10} [{bar:<20}] {count} ({percentage:.1f}%)")
        
        # Recent selections
        print("\n🕐 Recent selections:")
        for entry in self.history.history[-5:]:
            time_str = entry['timestamp'].strftime("%H:%M:%S")
            print(f"   {time_str} - {entry['provider']} ({entry['method']})")
        
        print("═"*70)
    
    def validate_input(self, choice):
        """
        Validate and normalize user input.
        
        Returns:
            Tuple of (valid, provider_key, action)
        """
        choice = choice.lower().strip()
        
        # Check for special actions
        if choice == 'i':
            return True, None, 'toggle_info'
        elif choice == 'c':
            return True, None, 'compare'
        elif choice == 'h':
            return True, None, 'history'
        elif choice == 'q':
            return True, None, 'quit'
        
        # Provider selection
        provider_map = {
            '1': 'AWS', 'a': 'AWS', 'aws': 'AWS',
            '2': 'Azure', 'z': 'Azure', 'azure': 'Azure',
            '3': 'GCP', 'g': 'GCP', 'gcp': 'GCP'
        }
        
        if choice in provider_map:
            return True, provider_map[choice], 'select'
        
        return False, None, None
    
    def confirm_selection(self, provider_key):
        """
        Confirm the provider selection.
        
        Returns:
            Boolean indicating if confirmed
        """
        provider = CloudProviderData.get_provider(provider_key)
        
        print("\n" + "┌"*70)
        print(f"│ {provider['icon']} SELECTION CONFIRMATION")
        print("└"*70)
        
        print(f"\n✅ You selected: {provider_key}")
        print(f"📋 Full name: {provider['full_name']}")
        print(f"📝 Description: {provider['description']}")
        
        print("\n" + "─"*70)
        print("OPTIONS:")
        print("  [y/yes]     ✅ Confirm this selection")
        print("  [n/no]      ❌ Choose a different provider")
        print("  [d/details] 📋 View detailed information")
        print("─"*70)
        
        while True:
            confirm = input("\nYour choice: ").strip().lower()
            
            if confirm in ['y', 'yes', 'confirm']:
                return True
            elif confirm in ['n', 'no', 'back']:
                return False
            elif confirm in ['d', 'details', 'info']:
                self.show_provider_details(provider_key)
                print("\n" + "─"*70)
                print("Now, do you want to confirm this selection?")
            else:
                print("❌ Please enter 'y' (yes), 'n' (no), or 'd' (details)")
    
    def show_final_summary(self, provider_key):
        """Display final selection summary."""
        provider = CloudProviderData.get_provider(provider_key)
        
        print("\n" + "╔"*70)
        print("║" + " ✅ SELECTION COMPLETE ".center(138) + "║")
        print("╚"*70)
        
        print(f"\n{provider['icon']} Cloud Provider: {provider_key}")
        print(f"📋 Full Name: {provider['full_name']}")
        print(f"📝 Description: {provider['description']}")
        
        print(f"\n🚀 Next Steps:")
        print(f"   • Set up your {provider_key} account")
        print(f"   • Configure authentication credentials")
        print(f"   • Choose your primary region")
        print(f"   • Begin resource provisioning")
        
        print("\n💡 Pro Tips:")
        for i, strength in enumerate(provider['strengths'][:2], 1):
            print(f"   {i}. Leverage {provider_key}'s {strength.lower()}")
        
        print("\n" + "═"*70)
    
    def ask_cloud_provider_text(self):
        """
        Main method to ask for cloud provider via text.
        
        Returns:
            Dictionary with provider information
        """
        print("\n" + "╔"*70)
        print("║" + " ☁️  TEXT-BASED CLOUD PROVIDER SELECTION ".center(138) + "║")
        print("╚"*70)
        
        print("\n💡 Use numbers, letters, or commands for quick selection")
        
        while True:
            self.display_menu()
            
            choice = input("\n👉 Enter your choice: ").strip()
            
            if not choice:
                print("❌ Please enter a valid option")
                continue
            
            valid, provider_key, action = self.validate_input(choice)
            
            if not valid:
                print("❌ Invalid choice. Please try again.")
                continue
            
            # Handle special actions
            if action == 'toggle_info':
                self.show_details = not self.show_details
                status = "enabled" if self.show_details else "disabled"
                print(f"\n💡 Detailed information {status}")
                time.sleep(1)
                continue
            
            elif action == 'compare':
                self.compare_providers()
                input("\n📍 Press Enter to return to menu...")
                continue
            
            elif action == 'history':
                self.show_history()
                input("\n📍 Press Enter to return to menu...")
                continue
            
            elif action == 'quit':
                print("\n👋 Selection cancelled")
                return None
            
            elif action == 'select':
                # Confirm selection
                if self.confirm_selection(provider_key):
                    # Record in history
                    self.history.add_selection(provider_key, "text")
                    
                    # Show final summary
                    self.show_final_summary(provider_key)
                    
                    # Return complete provider data
                    provider = CloudProviderData.get_provider(provider_key)
                    return {
                        "short": provider_key,
                        "full": provider['full_name'],
                        "desc": provider['description'],
                        "icon": provider['icon'],
                        "strengths": provider['strengths'],
                        "services": provider['popular_services'],
                        "selection_time": datetime.now()
                    }
                else:
                    print("\n🔄 Let's choose again...")
                    time.sleep(1)


def ask_cloud_provider_text():
    """
    Main function to ask for cloud provider via text.
    
    Returns:
        Dictionary with selected provider information
    """
    selector = TextCloudProviderSelector()
    return selector.ask_cloud_provider_text()


if __name__ == "__main__":
    print("\n" + "╔"*70)
    print("║" + " 🎯 ENHANCED TEXT CLOUD PROVIDER SELECTOR ".center(138) + "║")
    print("╚"*70)
    
    try:
        result = ask_cloud_provider_text()
        
        if result:
            print("\n" + "═"*70)
            print("   ✨ SELECTION SAVED")
            print("═"*70)
            print(f"\n🎯 Provider: {result['short']}")
            print(f"📅 Selected at: {result['selection_time'].strftime('%Y-%m-%d %H:%M:%S')}")
            print("\n✅ Ready to proceed with infrastructure setup!")
        else:
            print("\n❌ No provider selected")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Selection cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")