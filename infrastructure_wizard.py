"""
Step 2.4: Terraform Code Generator
Takes configuration from Step 2.3 and generates complete, valid Terraform files
"""

import os
from typing import Dict, Any

class TerraformGenerator:
    """
    Generates complete, production-ready Terraform configurations
    from user selections collected in Step 2.3
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get("provider", "aws")
        self.region = config.get("region", "us-east-1")
        
    def generate_provider_block(self) -> str:
        """Generate provider configuration"""
        
        provider_configs = {
            "aws": f'''
terraform {{
  required_version = ">= 1.0"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = var.region
}}
''',
            "azure": f'''
terraform {{
  required_version = ">= 1.0"
  required_providers {{
    azurerm = {{
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }}
  }}
}}

provider "azurerm" {{
  features {{}}
}}
''',
            "gcp": f'''
terraform {{
  required_version = ">= 1.0"
  required_providers {{
    google = {{
      source  = "hashicorp/google"
      version = "~> 5.0"
    }}
  }}
}}

provider "google" {{
  project = var.project_id
  region  = var.region
}}
'''
        }
        
        return provider_configs.get(self.provider, provider_configs["aws"])
    
    def generate_networking(self) -> str:
        """Generate networking resources"""
        
        network_choice = self.config.get("networking", "Default VPC")
        
        if self.provider == "aws":
            if "Custom VPC" in network_choice:
                return '''
# VPC Configuration
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.subnet_cidr
  map_public_ip_on_launch = true
  
  tags = {
    Name = "public-subnet"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "main-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}
'''
            else:
                return '# Using default VPC\n'
        
        elif self.provider == "azure":
            if "Custom VPC" in network_choice:
                return '''
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.region
}

resource "azurerm_virtual_network" "main" {
  name                = "main-vnet"
  address_space       = [var.vpc_cidr]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "main" {
  name                 = "main-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.subnet_cidr]
}
'''
            else:
                return '''
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.region
}
'''
        
        elif self.provider == "gcp":
            if "Custom VPC" in network_choice:
                return '''
resource "google_compute_network" "main" {
  name                    = "main-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "main" {
  name          = "main-subnet"
  ip_cidr_range = var.subnet_cidr
  region        = var.region
  network       = google_compute_network.main.id
}
'''
            else:
                return '# Using default network\n'
        
        return ""
    
    def generate_security_group(self) -> str:
        """Generate security group/firewall rules"""
        
        security_choice = self.config.get("security", "Basic Firewall")
        
        if self.provider == "aws":
            if "Strict" in security_choice:
                return '''
resource "aws_security_group" "main" {
  name        = "main-sg"
  description = "Strict security group with limited access"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH from specific IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_ip]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "main-sg"
  }
}
'''
            else:
                return '''
resource "aws_security_group" "main" {
  name        = "main-sg"
  description = "Basic security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "main-sg"
  }
}
'''
        
        elif self.provider == "azure":
            return '''
resource "azurerm_network_security_group" "main" {
  name                = "main-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}
'''
        
        elif self.provider == "gcp":
            return '''
resource "google_compute_firewall" "ssh" {
  name    = "allow-ssh"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
}
'''
        
        return ""
    
    def generate_compute(self) -> str:
        """Generate compute instance"""
        
        instance_type = self.config.get("instance_type", "t2.micro")
        os_choice = self.config.get("operating_system", "Ubuntu")
        
        if self.provider == "aws":
            # AMI mapping based on OS choice
            ami_map = {
                "Ubuntu": "data.aws_ami.ubuntu.id",
                "Amazon Linux": "data.aws_ami.amazon_linux.id",
                "Windows": "data.aws_ami.windows.id"
            }
            
            ami_data_source = ""
            if os_choice == "Ubuntu":
                ami_data_source = '''
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}
'''
            
            return ami_data_source + f'''
resource "aws_instance" "main" {{
  ami                    = {ami_map.get(os_choice, 'data.aws_ami.ubuntu.id')}
  instance_type          = "{instance_type}"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.main.id]
  
  tags = {{
    Name = "main-server"
    OS   = "{os_choice}"
  }}
}}
'''
        
        elif self.provider == "azure":
            return f'''
resource "azurerm_network_interface" "main" {{
  name                = "main-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {{
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
  }}
}}

resource "azurerm_linux_virtual_machine" "main" {{
  name                = "main-vm"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "{instance_type}"
  admin_username      = "adminuser"
  
  network_interface_ids = [
    azurerm_network_interface.main.id,
  ]

  admin_ssh_key {{
    username   = "adminuser"
    public_key = file("~/.ssh/id_rsa.pub")
  }}

  os_disk {{
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }}

  source_image_reference {{
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }}
}}
'''
        
        elif self.provider == "gcp":
            return f'''
resource "google_compute_instance" "main" {{
  name         = "main-instance"
  machine_type = "{instance_type}"
  zone         = "${{var.region}}-a"

  boot_disk {{
    initialize_params {{
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }}
  }}

  network_interface {{
    subnetwork = google_compute_subnetwork.main.id
    
    access_config {{
      // Ephemeral public IP
    }}
  }}
}}
'''
        
        return ""
    
    def generate_database(self) -> str:
        """Generate database resource"""
        
        db_engine = self.config.get("database_engine", "mysql")
        storage_size = self.config.get("storage_size", "20 GB")
        size_value = int(storage_size.split()[0])
        
        if self.provider == "aws":
            engine_version_map = {
                "mysql": "8.0",
                "postgres": "15.3",
                "mongodb": None
            }
            
            version = engine_version_map.get(db_engine)
            if not version:
                return "# MongoDB not natively supported in AWS RDS\n"
            
            return f'''
resource "aws_db_subnet_group" "main" {{
  name       = "main-db-subnet"
  subnet_ids = [aws_subnet.public.id]
}}

resource "aws_db_instance" "main" {{
  identifier             = "main-database"
  engine                 = "{db_engine}"
  engine_version         = "{version}"
  instance_class         = "db.t3.micro"
  allocated_storage      = {size_value}
  storage_type           = "gp2"
  db_name                = "mydb"
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.main.id]
  skip_final_snapshot    = true
  
  tags = {{
    Name = "main-db"
  }}
}}
'''
        
        elif self.provider == "azure":
            if db_engine == "mysql":
                return f'''
resource "azurerm_mysql_server" "main" {{
  name                = "main-mysql-server"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  administrator_login          = var.db_username
  administrator_login_password = var.db_password

  sku_name   = "B_Gen5_2"
  storage_mb = {size_value * 1024}
  version    = "8.0"

  ssl_enforcement_enabled = true
}}
'''
            elif db_engine == "postgres":
                return f'''
resource "azurerm_postgresql_server" "main" {{
  name                = "main-postgresql-server"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  administrator_login          = var.db_username
  administrator_login_password = var.db_password

  sku_name   = "B_Gen5_2"
  storage_mb = {size_value * 1024}
  version    = "11"

  ssl_enforcement_enabled = true
}}
'''
        
        elif self.provider == "gcp":
            version_map = {
                "mysql": "MYSQL_8_0",
                "postgres": "POSTGRES_15"
            }
            
            return f'''
resource "google_sql_database_instance" "main" {{
  name             = "main-db-instance"
  database_version = "{version_map.get(db_engine, 'MYSQL_8_0')}"
  region           = var.region

  settings {{
    tier = "db-f1-micro"
    
    ip_configuration {{
      ipv4_enabled = true
      authorized_networks {{
        value = "0.0.0.0/0"
      }}
    }}
  }}
}}

resource "google_sql_user" "main" {{
  name     = var.db_username
  instance = google_sql_database_instance.main.name
  password = var.db_password
}}
'''
        
        return ""
    
    def generate_monitoring(self) -> str:
        """Generate monitoring resources"""
        
        monitoring_choice = self.config.get("monitoring", "Disable Monitoring")
        
        if "Disable" in monitoring_choice:
            return "# Monitoring disabled by user choice\n"
        
        if self.provider == "aws":
            return '''
resource "aws_cloudwatch_log_group" "main" {
  name              = "/aws/ec2/main-server"
  retention_in_days = 7
}

resource "aws_cloudwatch_metric_alarm" "cpu" {
  alarm_name          = "main-server-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "This metric monitors ec2 cpu utilization"
  
  dimensions = {
    InstanceId = aws_instance.main.id
  }
}
'''
        
        return "# Monitoring configuration\n"
    
    def generate_variables(self) -> str:
        """Generate variables.tf"""
        
        base_vars = f'''
variable "region" {{
  description = "Cloud region"
  type        = string
  default     = "{self.region}"
}}

variable "vpc_cidr" {{
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}}

variable "subnet_cidr" {{
  description = "Subnet CIDR block"
  type        = string
  default     = "10.0.1.0/24"
}}

variable "db_username" {{
  description = "Database administrator username"
  type        = string
  default     = "admin"
}}

variable "db_password" {{
  description = "Database administrator password"
  type        = string
  sensitive   = true
}}

variable "admin_ip" {{
  description = "Admin IP for SSH access"
  type        = string
  default     = "0.0.0.0/0"
}}
'''
        
        if self.provider == "azure":
            base_vars += '''
variable "resource_group_name" {
  description = "Resource group name"
  type        = string
  default     = "main-resources"
}
'''
        
        if self.provider == "gcp":
            base_vars += '''
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}
'''
        
        return base_vars
    
    def generate_outputs(self) -> str:
        """Generate outputs.tf"""
        
        if self.provider == "aws":
            return '''
output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.main.id
}

output "instance_public_ip" {
  description = "Public IP address"
  value       = aws_instance.main.public_ip
}

output "database_endpoint" {
  description = "Database endpoint"
  value       = try(aws_db_instance.main.endpoint, "N/A")
}
'''
        
        elif self.provider == "azure":
            return '''
output "vm_id" {
  description = "Virtual machine ID"
  value       = azurerm_linux_virtual_machine.main.id
}

output "vm_private_ip" {
  description = "Private IP address"
  value       = azurerm_network_interface.main.private_ip_address
}
'''
        
        elif self.provider == "gcp":
            return '''
output "instance_id" {
  description = "Compute instance ID"
  value       = google_compute_instance.main.id
}

output "instance_external_ip" {
  description = "External IP address"
  value       = google_compute_instance.main.network_interface[0].access_config[0].nat_ip
}
'''
        
        return ""
    
    def generate_all_files(self, output_dir: str = "."):
        """Generate all Terraform files"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate main.tf
        main_content = (
            self.generate_provider_block() +
            self.generate_networking() +
            self.generate_security_group() +
            self.generate_compute() +
            self.generate_database() +
            self.generate_monitoring()
        )
        
        with open(os.path.join(output_dir, "main.tf"), "w") as f:
            f.write(main_content)
        
        # Generate variables.tf
        with open(os.path.join(output_dir, "variables.tf"), "w") as f:
            f.write(self.generate_variables())
        
        # Generate outputs.tf
        with open(os.path.join(output_dir, "outputs.tf"), "w") as f:
            f.write(self.generate_outputs())
        
        print(f"\nTerraform files generated successfully in '{output_dir}/'")
        print("  - main.tf")
        print("  - variables.tf")
        print("  - outputs.tf")


# Integration with Step 2.3
if __name__ == "__main__":
    # Import the prompter from Step 2.3
    try:
        from prompts import test_complete_wizard
        
        print("Running Step 2.3 (Interactive Prompts)...")
        config = test_complete_wizard()
        
        if config:
            print("\nRunning Step 2.4 (Terraform Generation)...")
            generator = TerraformGenerator(config)
            generator.generate_all_files(output_dir="./terraform")
            
            print("\nNext steps:")
            print("  1. cd terraform")
            print("  2. terraform init")
            print("  3. terraform plan")
            print("  4. terraform apply")
        else:
            print("\nConfiguration was cancelled. No files generated.")
            
    except ImportError:
        print("Error: Could not import from prompts.py")
        print("Make sure prompts.py exists and contains test_complete_wizard()")