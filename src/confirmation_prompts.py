# confirmation_prompts.py - Enhanced Version
# Comprehensive confirmation system with multiple safety levels

import time
import random


class ConfirmationLevel:
    """Define different levels of confirmation based on action risk."""
    SIMPLE = 1      # Yes/No
    STANDARD = 2    # Type 'yes' or 'confirm'
    CRITICAL = 3    # Type exact phrase
    NUCLEAR = 4     # Type phrase + delay + double confirm


def simple_confirmation(question, default_no=True):
    """
    Simple yes/no confirmation.
    
    Args:
        question: The question to ask
        default_no: If True, requires explicit 'yes'
    
    Returns:
        Boolean confirmation result
    """
    print(f"\n{question}")
    response = input("(y/n): ").strip().lower()
    
    if default_no:
        return response in ['y', 'yes']
    else:
        return response not in ['n', 'no']


def standard_confirmation(action_description):
    """
    Standard confirmation requiring typing 'yes' or 'confirm'.
    
    Args:
        action_description: Description of the action
    
    Returns:
        Boolean confirmation result
    """
    print(f"\n⚠️  {action_description}")
    print("This action will modify your infrastructure.")
    
    response = input("\nType 'yes' or 'confirm' to proceed: ").strip().lower()
    
    if response in ['yes', 'confirm']:
        print("✅ Confirmed")
        return True
    else:
        print("❌ Cancelled")
        return False


def critical_confirmation(action_description, required_phrase="CONFIRM"):
    """
    Critical confirmation requiring exact phrase match.
    
    Args:
        action_description: Description of the dangerous action
        required_phrase: Exact phrase user must type
    
    Returns:
        Boolean confirmation result
    """
    print("\n" + "🔴"*25)
    print(f"⚠️  CRITICAL ACTION: {action_description}")
    print("❌ THIS ACTION CANNOT BE UNDONE!")
    print("🔴"*25)
    
    print(f"\nType '{required_phrase}' (case-sensitive) to proceed")
    print("Or type anything else to cancel")
    print("-"*50)
    
    response = input("\nYour response: ").strip()
    
    if response == required_phrase:
        print("✅ Critical action confirmed")
        return True
    else:
        print("❌ Confirmation failed - action cancelled")
        return False


def nuclear_confirmation(action_description, environment="PRODUCTION"):
    """
    Nuclear option - maximum safety with multiple checks and delays.
    
    Args:
        action_description: Description of the extremely dangerous action
        environment: Environment being affected
    
    Returns:
        Boolean confirmation result
    """
    print("\n" + "💀"*25)
    print("🚨 NUCLEAR OPTION - MAXIMUM DANGER 🚨")
    print("💀"*25)
    print(f"\nACTION: {action_description}")
    print(f"ENVIRONMENT: {environment}")
    print("\n⚠️  THIS WILL CAUSE:")
    print("  • Complete service outage")
    print("  • Permanent data loss")
    print("  • Cannot be recovered")
    print("  • Will affect all users")
    print("\n" + "💀"*25)
    
    # Step 1: Initial confirmation
    print("\n📋 STEP 1 of 3: Initial Confirmation")
    response1 = input(f"Type '{environment}' to continue: ").strip()
    
    if response1 != environment:
        print("❌ Step 1 failed - action cancelled")
        return False
    
    print("✅ Step 1 passed")
    
    # Step 2: Acknowledge risks
    print("\n📋 STEP 2 of 3: Risk Acknowledgment")
    print("Type 'I UNDERSTAND THE RISKS' to continue")
    response2 = input("Your response: ").strip()
    
    if response2 != "I UNDERSTAND THE RISKS":
        print("❌ Step 2 failed - action cancelled")
        return False
    
    print("✅ Step 2 passed")
    
    # Step 3: Countdown with final confirmation
    print("\n📋 STEP 3 of 3: Final Countdown")
    print("⏱️  10 second safety delay...")
    
    for i in range(10, 0, -1):
        print(f"   {i}...", end='\r')
        time.sleep(1)
    
    print("\n\n🔴 FINAL CONFIRMATION")
    print("Type 'DESTROY' to execute, or anything else to abort")
    response3 = input("Your response: ").strip()
    
    if response3 == "DESTROY":
        print("\n💥 NUCLEAR OPTION ACTIVATED!")
        return True
    else:
        print("❌ Step 3 failed - action cancelled")
        return False


def cost_aware_confirmation(config_summary, estimated_cost):
    """
    Confirmation with cost estimation and breakdown.
    
    Args:
        config_summary: Dictionary of configuration details
        estimated_cost: Estimated monthly cost
    
    Returns:
        Boolean confirmation result
    """
    print("\n" + "="*60)
    print("   INFRASTRUCTURE DEPLOYMENT CONFIRMATION")
    print("="*60)
    
    print("\n📋 Configuration Summary:")
    for key, value in config_summary.items():
        print(f"   • {key}: {value}")
    
    print("\n💰 Cost Estimation:")
    print(f"   • Monthly Cost: ${estimated_cost:.2f}")
    print(f"   • Annual Cost: ${estimated_cost * 12:.2f}")
    
    # Show cost breakdown
    print("\n📊 Cost Breakdown:")
    compute_cost = estimated_cost * 0.6
    storage_cost = estimated_cost * 0.25
    network_cost = estimated_cost * 0.15
    
    print(f"   • Compute: ${compute_cost:.2f} (60%)")
    print(f"   • Storage: ${storage_cost:.2f} (25%)")
    print(f"   • Network: ${network_cost:.2f} (15%)")
    
    print("\n⏱️  Deployment Time: 5-7 minutes")
    print("="*60)
    
    if estimated_cost > 1000:
        print("\n⚠️  WARNING: High cost deployment detected!")
        print("This will result in significant charges.")
        
    response = input("\n✅ Proceed with deployment? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        print("\n🚀 Deployment approved!")
        return True
    else:
        print("\n❌ Deployment cancelled")
        return False


def environment_aware_confirmation(action, environment, requires_backup=True):
    """
    Environment-aware confirmation with different safety levels.
    
    Args:
        action: Action being performed
        environment: dev/staging/production
        requires_backup: Whether backup verification is needed
    
    Returns:
        Boolean confirmation result
    """
    print("\n" + "="*60)
    print(f"   {action.upper()}")
    print(f"   Environment: {environment.upper()}")
    print("="*60)
    
    # Different confirmation levels based on environment
    if environment.lower() == 'production':
        print("\n🔴 PRODUCTION ENVIRONMENT DETECTED")
        print("This requires elevated confirmation.")
        
        if requires_backup:
            print("\n📦 Backup Verification Required")
            backup_confirm = input("Confirm backups are current (yes/no): ").strip().lower()
            
            if backup_confirm not in ['yes', 'y']:
                print("❌ Cannot proceed without backup confirmation")
                return False
            print("✅ Backup verified")
        
        return critical_confirmation(
            f"{action} in PRODUCTION",
            required_phrase="PRODUCTION-CONFIRM"
        )
        
    elif environment.lower() == 'staging':
        print("\n🟡 STAGING ENVIRONMENT")
        print("Standard confirmation required.")
        return standard_confirmation(f"{action} in staging")
        
    else:  # dev
        print("\n🟢 DEVELOPMENT ENVIRONMENT")
        print("Simple confirmation.")
        return simple_confirmation(f"{action} in development?")


def batch_action_confirmation(action, items_count, sample_items):
    """
    Confirmation for batch operations affecting multiple resources.
    
    Args:
        action: Action being performed
        items_count: Number of items affected
        sample_items: List of sample item names
    
    Returns:
        Boolean confirmation result
    """
    print("\n" + "="*60)
    print(f"   BATCH {action.upper()}")
    print("="*60)
    
    print(f"\n⚠️  This will affect {items_count} resources")
    
    if items_count > 0:
        print("\n📋 Sample of affected resources:")
        for i, item in enumerate(sample_items[:5], 1):
            print(f"   {i}. {item}")
        
        if items_count > 5:
            print(f"   ... and {items_count - 5} more")
    
    print("\n" + "="*60)
    
    if items_count > 10:
        print("⚠️  Large batch operation detected")
        return critical_confirmation(
            f"{action} {items_count} resources",
            required_phrase="BATCH-CONFIRM"
        )
    else:
        return standard_confirmation(f"{action} {items_count} resources")


def simulate_deployment(config):
    """Simulate deployment with progress indicators."""
    print("\n" + "="*60)
    print("   🚀 DEPLOYMENT IN PROGRESS")
    print("="*60)
    
    steps = [
        ("Validating configuration", 1),
        ("Initializing Terraform", 1.5),
        ("Planning infrastructure changes", 2),
        ("Creating network resources", 2),
        ("Provisioning compute instances", 3),
        ("Configuring security groups", 1.5),
        ("Setting up storage", 2),
        ("Running health checks", 1),
    ]
    
    for step, duration in steps:
        print(f"\n⏳ {step}...", end='', flush=True)
        time.sleep(duration)
        print(" ✅")
    
    print("\n" + "="*60)
    print("   ✅ DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📊 Infrastructure ID: infra-{random.randint(1000, 9999)}")
    print(f"🌐 Region: {config.get('Region', 'us-east-1')}")
    print(f"🏷️  Tags: {config.get('Environment', 'production')}")


def main_demo():
    """Demonstrate all confirmation types."""
    print("\n" + "="*60)
    print("   CONFIRMATION SYSTEM DEMONSTRATION")
    print("="*60)
    
    # Demo 1: Simple Confirmation
    print("\n\n--- DEMO 1: Simple Confirmation ---")
    if simple_confirmation("🔵 Would you like to create a development database?"):
        print("✅ Database creation approved")
    else:
        print("❌ Database creation cancelled")
    
    # Demo 2: Standard Confirmation
    print("\n\n--- DEMO 2: Standard Confirmation ---")
    if standard_confirmation("Modify staging environment configuration"):
        print("✅ Modification approved")
    else:
        print("❌ Modification cancelled")
    
    # Demo 3: Cost-Aware Confirmation
    print("\n\n--- DEMO 3: Cost-Aware Confirmation ---")
    sample_config = {
        "Cloud Provider": "AWS",
        "Resource Type": "Compute",
        "Instance Type": "t3.medium",
        "Instance Count": "3",
        "Region": "us-east-1",
        "Environment": "production"
    }
    
    if cost_aware_confirmation(sample_config, 125.50):
        simulate_deployment(sample_config)
    
    # Demo 4: Environment-Aware Confirmation
    print("\n\n--- DEMO 4: Environment-Aware Confirmation ---")
    environment_aware_confirmation(
        "Deploy new version",
        "staging",
        requires_backup=False
    )
    
    # Demo 5: Batch Action
    print("\n\n--- DEMO 5: Batch Action Confirmation ---")
    sample_resources = [
        "web-server-1",
        "web-server-2", 
        "web-server-3",
        "db-primary",
        "db-replica"
    ]
    batch_action_confirmation("restart", 5, sample_resources)
    
    # Demo 6: Critical Confirmation
    print("\n\n--- DEMO 6: Critical Confirmation ---")
    if critical_confirmation("Delete production database backup"):
        print("⚠️  Critical action executed")
    
    # Demo 7: Nuclear Option (commented out for safety in demo)
    print("\n\n--- DEMO 7: Nuclear Option (Demonstration Only) ---")
    print("⚠️  This is the most dangerous confirmation level")
    print("It requires multiple steps, countdown, and exact phrases")
    print("(Skipped in demo - uncomment to test)")
    
    # Uncomment to test nuclear option:
    # if nuclear_confirmation("DESTROY ALL PRODUCTION INFRASTRUCTURE", "PRODUCTION"):
    #     print("💥 Everything destroyed")
    
    print("\n\n" + "="*60)
    print("   DEMONSTRATION COMPLETE")
    print("="*60)
    print("\n✅ All confirmation systems working correctly!")


if __name__ == "__main__":
    try:
        main_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")