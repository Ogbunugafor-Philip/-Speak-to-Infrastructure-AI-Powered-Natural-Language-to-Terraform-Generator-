# Step 2.2 FIXED: Intent Categories with Proper Detection

import re
from typing import Dict, List, Set, Optional

# Multi-cloud resource mappings
INTENT_CATEGORIES = {
    "networking": {
        "keywords": ["vpc", "vnet", "network", "subnet", "gateway", "load balancer", 
                     "alb", "nlb", "vpn", "dns", "route", "peering"],
        "cloud_resources": {
            "aws": ["vpc", "subnet", "internet_gateway", "nat_gateway", "route_table", 
                    "elastic_load_balancer", "application_load_balancer"],
            "azure": ["virtual_network", "subnet", "vpn_gateway", "load_balancer"],
            "gcp": ["compute_network", "compute_subnetwork", "compute_vpn_gateway", 
                    "compute_forwarding_rule"]
        }
    },
    
    "compute": {
        "keywords": ["server", "instance", "ec2", "vm", "virtual machine", "compute", 
                     "container", "auto scaling", "asg", "vmss", "small", "medium", "large"],
        "cloud_resources": {
            "aws": ["ec2_instance", "autoscaling_group", "launch_template"],
            "azure": ["linux_virtual_machine", "windows_virtual_machine", 
                      "virtual_machine_scale_set"],
            "gcp": ["compute_instance", "compute_instance_group_manager"]
        }
    },
    
    "database": {
        "keywords": ["database", "db", "rds", "sql", "mysql", "postgres", "postgresql",
                     "dynamodb", "cosmosdb", "firestore", "mongodb", "mariadb"],
        "cloud_resources": {
            "aws": ["db_instance", "dynamodb_table", "rds_cluster"],
            "azure": ["mssql_server", "mysql_server", "postgresql_server", 
                      "cosmosdb_account"],
            "gcp": ["sql_database_instance", "firestore_database"]
        }
    },
    
    "storage": {
        "keywords": ["storage", "bucket", "blob", "s3", "ebs", "disk", "volume",
                     "file storage", "object storage"],
        "cloud_resources": {
            "aws": ["s3_bucket", "ebs_volume", "efs_file_system"],
            "azure": ["storage_account", "storage_blob", "managed_disk"],
            "gcp": ["storage_bucket", "compute_disk"]
        }
    },
    
    "security": {
        "keywords": ["iam", "role", "policy", "security group", "firewall", "acl",
                     "kms", "key vault", "secrets", "certificate", "strict"],
        "cloud_resources": {
            "aws": ["iam_role", "iam_policy", "security_group", "kms_key"],
            "azure": ["role_assignment", "key_vault", "network_security_group"],
            "gcp": ["project_iam_binding", "compute_firewall", "kms_crypto_key"]
        }
    },
    
    "monitoring": {
        "keywords": ["monitor", "monitoring", "logs", "alerts", "metrics", "cloudwatch",
                     "log analytics", "stackdriver"],
        "cloud_resources": {
            "aws": ["cloudwatch_log_group", "cloudwatch_metric_alarm", "sns_topic"],
            "azure": ["monitor_metric_alert", "log_analytics_workspace"],
            "gcp": ["monitoring_alert_policy", "logging_metric"]
        }
    },
    
    "container": {
        "keywords": ["container", "docker", "kubernetes", "k8s", "ecs", "eks", "aks",
                     "gke", "fargate", "pod", "deployment"],
        "cloud_resources": {
            "aws": ["ecs_cluster", "ecs_service", "eks_cluster"],
            "azure": ["kubernetes_cluster", "container_group"],
            "gcp": ["container_cluster", "container_node_pool"]
        }
    },
    
    "serverless": {
        "keywords": ["lambda", "function", "serverless", "cloud function", 
                     "azure function"],
        "cloud_resources": {
            "aws": ["lambda_function", "api_gateway_rest_api"],
            "azure": ["function_app"],
            "gcp": ["cloudfunctions_function"]
        }
    },
    
    "provider": {
        "keywords": ["aws", "amazon web services", "azure", "microsoft azure", 
                     "gcp", "google cloud", "google cloud platform"],
        "cloud_resources": {}
    },
    
    "os": {
        "keywords": ["ubuntu", "windows", "amazon linux", "centos", "rhel", 
                     "debian", "fedora"],
        "cloud_resources": {}
    }
}

# Action verbs for intent detection
ACTION_VERBS = {
    "create": ["create", "deploy", "launch", "provision", "setup", "set up", "add", "build"],
    "delete": ["delete", "remove", "destroy", "terminate", "tear down"],
    "modify": ["modify", "update", "change", "edit", "configure"],
    "query": ["show", "list", "describe", "get", "what", "which"]
}

# Negation patterns
NEGATION_PATTERNS = [
    r'\b(no|not|without|don\'t|dont|never|exclude)\b',
    r'\b(except|excluding)\b'
]


class IntentParser:
    """Enhanced intent parser with proper case handling and category detection"""
    
    def __init__(self):
        self.categories = INTENT_CATEGORIES
        self.actions = ACTION_VERBS
        
    def has_negation(self, text: str, keyword_position: int) -> bool:
        """Check if keyword appears in a negated context"""
        words_before = text[:keyword_position].split()[-5:]
        for word in words_before:
            for pattern in NEGATION_PATTERNS:
                if re.search(pattern, word, re.IGNORECASE):
                    return True
        return False
    
    def extract_action(self, sentence: str) -> str:
        """Determine what action user wants to perform"""
        sentence_lower = sentence.lower()
        for action_type, verbs in self.actions.items():
            for verb in verbs:
                if re.search(rf'\b{verb}\b', sentence_lower):
                    return action_type
        return "create"
    
    def detect_intents(self, sentence: str) -> Dict[str, any]:
        """
        Detect intents with proper case handling and category separation.
        Returns dict with detected categories, action, and confidence.
        """
        sentence_lower = sentence.lower()
        detected = {
            "action": self.extract_action(sentence),
            "categories": {},
            "negated_categories": set(),
            "raw_sentence": sentence
        }
        
        for category, data in self.categories.items():
            keywords = data["keywords"]
            
            for keyword in keywords:
                # Find all occurrences (case-insensitive)
                pattern = rf'\b{re.escape(keyword)}\b'
                matches = list(re.finditer(pattern, sentence_lower, re.IGNORECASE))
                
                for match in matches:
                    if self.has_negation(sentence_lower, match.start()):
                        detected["negated_categories"].add(category)
                    else:
                        if category not in detected["categories"]:
                            detected["categories"][category] = []
                        # Avoid duplicates
                        if keyword not in detected["categories"][category]:
                            detected["categories"][category].append(keyword)
        
        return detected
    
    def validate_intent(self, detected: Dict) -> bool:
        """Validate that detected intent makes sense"""
        # If user says "without database" but we detect database, that's wrong
        if detected["negated_categories"] & set(detected["categories"].keys()):
            return False
        
        # If no categories detected, invalid
        if not detected["categories"]:
            return False
            
        return True
    
    def normalize_provider(self, detected: Dict) -> Optional[str]:
        """
        Extract and normalize provider name from detected intents.
        Returns: 'aws', 'azure', or 'gcp' (lowercase, normalized)
        """
        if "provider" not in detected["categories"]:
            return None
        
        provider_keywords = detected["categories"]["provider"]
        if not provider_keywords:
            return None
        
        # Take first detected provider keyword
        keyword = provider_keywords[0].lower()
        
        # Normalize variations
        if "aws" in keyword or "amazon" in keyword:
            return "aws"
        elif "azure" in keyword or "microsoft" in keyword:
            return "azure"
        elif "gcp" in keyword or "google" in keyword:
            return "gcp"
        
        return None
    
    def extract_os(self, detected: Dict) -> Optional[str]:
        """Extract operating system from detected intents"""
        if "os" not in detected["categories"]:
            return None
        
        os_keywords = detected["categories"]["os"]
        if not os_keywords:
            return None
        
        # Return first detected OS, capitalized
        os_name = os_keywords[0]
        
        # Special case handling
        if os_name == "amazon linux":
            return "Amazon Linux"
        elif os_name == "rhel":
            return "RHEL"
        else:
            return os_name.capitalize()


# Testing function
def test_intent_parser():
    parser = IntentParser()
    
    test_cases = [
        "Create a VPC with two subnets and a load balancer",
        "Deploy an EC2 instance WITHOUT a database",
        "I don't want any monitoring or logging",
        "Setup a MySQL database with RDS",
        "Remove the security group from my server",
        "Launch a Kubernetes cluster with auto-scaling",
        "Create storage bucket and enable logging",
        "Deploy a small Ubuntu server on AWS with MySQL",
        "AWS EC2 t2.micro",
        "Azure Standard_B2s VM",
        "GCP e2-medium instance"
    ]
    
    print("Testing Enhanced Intent Parser\n")
    print("=" * 70)
    
    for sentence in test_cases:
        result = parser.detect_intents(sentence)
        valid = parser.validate_intent(result)
        provider = parser.normalize_provider(result)
        os = parser.extract_os(result)
        
        print(f"\nSentence: {sentence}")
        print(f"Action: {result['action']}")
        print(f"Detected Categories: {dict(result['categories'])}")
        if provider:
            print(f"Provider (normalized): {provider}")
        if os:
            print(f"Operating System: {os}")
        if result['negated_categories']:
            print(f"Negated (excluded): {result['negated_categories']}")
        print(f"Valid Intent: {'Yes' if valid else 'No'}")
        print("-" * 70)


if __name__ == "__main__":
    # Show categories
    print("Defined Intent Categories:\n")
    for category, data in INTENT_CATEGORIES.items():
        print(f"{category.upper()}:")
        print(f"  Keywords: {', '.join(data['keywords'][:5])}...")
        if data['cloud_resources']:
            print(f"  Clouds: {', '.join(data['cloud_resources'].keys())}")
        print()
    
    print("\n" + "=" * 70 + "\n")
    
    # Run tests
    test_intent_parser()