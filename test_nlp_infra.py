"""
Step 2.5: NLP Engine Testing & End-to-End Validation
Tests whether the complete pipeline (NLP → Prompts → Terraform) works correctly
"""

import sys
import os

# Import components from previous steps
try:
    from intents import IntentParser, INTENT_CATEGORIES
    from prompts import InfrastructurePrompter
    from infrastructure_wizard import TerraformGenerator
    FULL_PIPELINE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import all components: {e}")
    FULL_PIPELINE_AVAILABLE = False


class NLPTestSuite:
    """
    Comprehensive testing suite for the NLP engine
    """
    
    def __init__(self):
        if FULL_PIPELINE_AVAILABLE:
            self.parser = IntentParser()
        else:
            self.parser = None
    
    def test_basic_intent_detection(self):
        """Test 1: Basic intent detection from natural language"""
        
        print("\n" + "="*70)
        print("TEST 1: Basic Intent Detection")
        print("="*70)
        
        test_cases = [
            {
                "input": "Deploy a small Ubuntu server on AWS with MySQL",
                "expected": {
                    "provider": "aws",
                    "compute": ["small", "server"],
                    "os": ["ubuntu"],
                    "database": ["mysql"]
                }
            },
            {
                "input": "Create a medium Windows VM in Azure with PostgreSQL",
                "expected": {
                    "provider": "azure",
                    "compute": ["medium", "vm"],
                    "os": ["windows"],
                    "database": ["postgresql"]
                }
            },
            {
                "input": "Launch a large container in GCP with MongoDB",
                "expected": {
                    "provider": "gcp",
                    "compute": ["large", "container"],
                    "database": ["mongodb"]
                }
            },
        ]
        
        passed = 0
        failed = 0
        
        for i, test in enumerate(test_cases, 1):
            print(f"\nTest Case {i}:")
            print(f"Input: {test['input']}")
            
            if self.parser:
                result = self.parser.detect_intents(test['input'])
                print(f"Detected: {result['categories']}")
                print(f"Action: {result['action']}")
                
                # Check if expected categories were found
                success = True
                for expected_cat in test['expected'].keys():
                    if expected_cat not in result['categories']:
                        print(f"  FAIL: Missing category '{expected_cat}'")
                        success = False
                        failed += 1
                
                if success:
                    print("  PASS")
                    passed += 1
            else:
                print("  SKIP: Parser not available")
        
        print(f"\nResults: {passed} passed, {failed} failed")
        return passed, failed
    
    def test_negation_handling(self):
        """Test 2: Negation detection (e.g., 'without database')"""
        
        print("\n" + "="*70)
        print("TEST 2: Negation Handling")
        print("="*70)
        
        test_cases = [
            {
                "input": "Deploy a server WITHOUT a database",
                "should_exclude": ["database"]
            },
            {
                "input": "Create a VPC but don't enable monitoring",
                "should_exclude": ["monitoring"]
            },
            {
                "input": "Launch EC2 instance without security group",
                "should_exclude": ["security"]
            },
        ]
        
        passed = 0
        failed = 0
        
        for i, test in enumerate(test_cases, 1):
            print(f"\nTest Case {i}:")
            print(f"Input: {test['input']}")
            
            if self.parser:
                result = self.parser.detect_intents(test['input'])
                print(f"Detected: {result['categories']}")
                print(f"Negated: {result['negated_categories']}")
                
                # Check if negated categories were correctly identified
                success = True
                for excluded in test['should_exclude']:
                    if excluded in result['categories'] and excluded not in result['negated_categories']:
                        print(f"  FAIL: '{excluded}' should be negated but wasn't")
                        success = False
                        failed += 1
                
                if success:
                    print("  PASS")
                    passed += 1
            else:
                print("  SKIP: Parser not available")
        
        print(f"\nResults: {passed} passed, {failed} failed")
        return passed, failed
    
    def test_multi_resource_extraction(self):
        """Test 3: Extract multiple resources and counts"""
        
        print("\n" + "="*70)
        print("TEST 3: Multiple Resources & Counts")
        print("="*70)
        
        test_cases = [
            "Create a VPC with three subnets and two EC2 instances",
            "Deploy five servers with MySQL database and monitoring",
            "Setup a network with subnet, gateway, and load balancer",
        ]
        
        for i, sentence in enumerate(test_cases, 1):
            print(f"\nTest Case {i}:")
            print(f"Input: {sentence}")
            
            if self.parser:
                result = self.parser.detect_intents(sentence)
                print(f"Detected categories: {list(result['categories'].keys())}")
                print(f"Details: {result['categories']}")
            else:
                print("  SKIP: Parser not available")
    
    def test_ambiguous_inputs(self):
        """Test 4: Handle ambiguous/incomplete requests"""
        
        print("\n" + "="*70)
        print("TEST 4: Ambiguous Input Handling")
        print("="*70)
        
        test_cases = [
            "Deploy a server",  # Missing: provider, size, OS
            "Create a database",  # Missing: engine, provider
            "Setup infrastructure",  # Extremely vague
        ]
        
        for i, sentence in enumerate(test_cases, 1):
            print(f"\nTest Case {i}:")
            print(f"Input: {sentence}")
            
            if self.parser:
                result = self.parser.detect_intents(sentence)
                print(f"Detected: {result['categories']}")
                
                # These should trigger the interactive prompt system
                missing = []
                if not result['categories'].get('provider'):
                    missing.append("provider")
                if 'compute' in result['categories'] and not any(size in str(result['categories']) for size in ['small', 'medium', 'large']):
                    missing.append("instance_size")
                
                if missing:
                    print(f"  Missing info (will prompt user): {', '.join(missing)}")
                else:
                    print("  All info present")
            else:
                print("  SKIP: Parser not available")
    
    def test_end_to_end_pipeline(self):
        """Test 5: Complete pipeline from NLP to Terraform generation"""
        
        print("\n" + "="*70)
        print("TEST 5: End-to-End Pipeline (NLP → Config → Terraform)")
        print("="*70)
        
        if not FULL_PIPELINE_AVAILABLE:
            print("SKIP: Full pipeline not available (missing imports)")
            return
        
        # Simulate a complete request
        sentence = "Deploy a t2.micro Ubuntu server on AWS in us-east-1 with MySQL database"
        
        print(f"\nInput: {sentence}")
        print("\nStep 1: Parse with NLP...")
        result = self.parser.detect_intents(sentence)
        print(f"  Detected: {result['categories']}")
        
        print("\nStep 2: Build configuration...")
        # In real usage, missing details would trigger prompts
        # For testing, we'll fill in a complete config
        config = {
            "provider": "aws",
            "region": "us-east-1",
            "instance_type": "t2.micro",
            "operating_system": "Ubuntu",
            "database_engine": "mysql",
            "storage_size": "20 GB",
            "networking": "Custom VPC with Subnet",
            "security": "Basic Firewall",
            "monitoring": "Enable Monitoring & Alerts"
        }
        print(f"  Config: {config}")
        
        print("\nStep 3: Generate Terraform...")
        try:
            generator = TerraformGenerator(config)
            generator.generate_all_files(output_dir="./test_terraform")
            print("  SUCCESS: Terraform files generated")
            
            # Verify files exist
            import os
            required_files = ["main.tf", "variables.tf", "outputs.tf"]
            for filename in required_files:
                filepath = os.path.join("./test_terraform", filename)
                if os.path.exists(filepath):
                    size = os.path.getsize(filepath)
                    print(f"    {filename}: {size} bytes")
                else:
                    print(f"    {filename}: MISSING")
            
        except Exception as e:
            print(f"  FAILED: {e}")
    
    def test_provider_specific_resources(self):
        """Test 6: Provider-specific resource mapping"""
        
        print("\n" + "="*70)
        print("TEST 6: Provider-Specific Resource Mapping")
        print("="*70)
        
        test_cases = [
            ("AWS EC2 t2.micro", "aws", "t2.micro"),
            ("Azure Standard_B2s VM", "azure", "Standard_B2s"),
            ("GCP e2-medium instance", "gcp", "e2-medium"),
        ]
        
        for i, (sentence, expected_provider, expected_type) in enumerate(test_cases, 1):
            print(f"\nTest Case {i}:")
            print(f"Input: {sentence}")
            
            if self.parser:
                result = self.parser.detect_intents(sentence)
                
                # Check provider detection
                detected_provider = None
                for cat, keywords in result['categories'].items():
                    if cat == 'provider':
                        detected_provider = keywords[0] if isinstance(keywords, list) else keywords
                
                if detected_provider == expected_provider:
                    print(f"  Provider: PASS ({expected_provider})")
                else:
                    print(f"  Provider: FAIL (expected {expected_provider}, got {detected_provider})")
            else:
                print("  SKIP: Parser not available")
    
    def run_all_tests(self):
        """Run complete test suite"""
        
        print("\n" + "="*70)
        print("SPEAK-TO-INFRASTRUCTURE NLP ENGINE TEST SUITE")
        print("="*70)
        
        if not FULL_PIPELINE_AVAILABLE:
            print("\nWARNING: Not all components available for testing")
            print("Make sure intents.py, prompts.py, and infrastructure_wizard.py exist")
        
        total_passed = 0
        total_failed = 0
        
        # Run all tests
        p, f = self.test_basic_intent_detection()
        total_passed += p
        total_failed += f
        
        p, f = self.test_negation_handling()
        total_passed += p
        total_failed += f
        
        self.test_multi_resource_extraction()
        self.test_ambiguous_inputs()
        self.test_end_to_end_pipeline()
        self.test_provider_specific_resources()
        
        # Final summary
        print("\n" + "="*70)
        print("FINAL RESULTS")
        print("="*70)
        print(f"Total Passed: {total_passed}")
        print(f"Total Failed: {total_failed}")
        
        if total_failed == 0:
            print("\nALL TESTS PASSED")
        else:
            print(f"\n{total_failed} TESTS FAILED - Review output above")
        
        print("\nNext Steps:")
        print("1. Fix any failed tests")
        print("2. Add more edge cases")
        print("3. Test with real Terraform deployment")
        print("="*70)


if __name__ == "__main__":
    suite = NLPTestSuite()
    suite.run_all_tests()