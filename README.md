# “Speak-to-Infrastructure: AI-Powered Natural Language to Terraform Generator”
AI-powered tool that turns natural language into Terraform projects. Supports AWS, Azure, GCP with interactive CLI, validation, and automated provisioning.

## Introduction

Infrastructure as Code (IaC) has transformed how organizations design, provision, and manage cloud resources. Tools like Terraform have become industry standards because they bring repeatability, version control, and automation into infrastructure management. However, Terraform comes with its own challenges: engineers must learn HashiCorp Configuration Language (HCL), remember countless resource attributes, and constantly cross-reference documentation. For beginners, this is intimidating; for experts, it is time-consuming.
In a world moving toward low-code and no-code solutions, there is a gap between the technical precision of Terraform and the simplicity modern teams expect. What if provisioning infrastructure was as easy as having a conversation? What if an engineer, a DevOps team lead, or even a non-technical manager could simply describe what they need; “Deploy a VPC with two subnets, one EC2 instance, and an RDS MySQL database”; and a system could automatically generate the complete Terraform project, with modules, variables, and outputs, ready to plan and apply?
This project, Speak-to-Infrastructure, bridges that gap. It is designed as a downloadable, standalone tool; similar to installing Python or MySQL; where users can open an interface, provide high-level instructions in natural language, and receive a fully structured Terraform codebase. The tool doesn’t just guess; it engages interactively by asking clarifying questions, validating inputs (like region, CIDR blocks, instance types), and scaffolding best-practice Terraform modules. The goal is to reduce setup time from hours to minutes, while keeping flexibility for advanced users.

## Statement of Problem
Despite the widespread adoption of Terraform and Infrastructure as Code practices, several key pain points persist across organizations:

- High Learning Curve: New engineers must spend weeks learning HCL syntax, terraform providers, and module structures before becoming productive. This slows onboarding and increases the barrier to entry for DevOps roles.

- Inefficient Workflow for Experts: Even experienced engineers waste time typing repetitive boilerplate (VPC blocks, subnet definitions, security groups). They often need to copy-paste from old projects or browse the Terraform Registry for modules.

- Error-Prone Configurations: Small mistakes like misconfigured CIDR blocks, wrong instance sizes, or missing IAM permissions frequently cause failed deployments. Debugging these errors consumes valuable engineering hours.

- Lack of Accessibility: Non-technical team members (e.g., project managers, architects) cannot directly experiment with infrastructure design. They must depend on DevOps engineers to translate requirements into code, creating bottlenecks.

- Slow Time-to-Deployment: Setting up production-ready infrastructure often takes hours or days, especially when projects require multiple components (networking, compute, databases, monitoring, security).

These problems highlight the need for a simpler, faster, and more intelligent way to generate Terraform configurations. The traditional manual approach is not aligned with the future of DevOps, where AI-driven tools can reduce complexity and accelerate delivery.

## Project Objectives

- To develop an AI-powered tool that converts natural language infrastructure requirements into structured Terraform code.

- To design an interactive prompt system that validates user inputs (e.g., region, instance type, security rules) before code generation.

- To automate the creation of production-ready Terraform modules with best practices for networking, compute, databases, and security.

- To reduce time-to-deployment by enabling users to generate and run Terraform projects in minutes instead of hours.

- To increase accessibility of Infrastructure as Code by allowing both technical and non-technical users to provision cloud resources without writing HCL manually.

- To package the system as a downloadable, standalone tool that can be installed and used directly by end users.


## Project Scope
The scope of this project defines what will be covered in the current implementation and what is planned for future expansion. The project is designed to deliver a working prototype that demonstrates the feasibility of using artificial intelligence to generate Terraform infrastructure code from natural language inputs.

### In-Scope (Current Version)
- Development of an AI-driven interface that accepts natural language or typed instructions for infrastructure provisioning.
- Interactive prompt system to gather required parameters (e.g., region, VPC, subnets, compute type, database engine, monitoring rules).
- Validation of user inputs to minimize errors in configurations.
- Automated generation of Terraform files, including main.tf, variables.tf, and outputs.tf.
- Multi-cloud support: initial focus on AWS, Azure, and GCP, with a unified experience so users can select their preferred provider at the start.
- Support for core infrastructure components across clouds (networking, compute, databases, and security).
- Option to run terraform plan directly after code generation.
- Packaging of the system as a standalone downloadable tool that can be installed and used locally by end users.

### Out-of-Scope (Future Enhancements)
- Advanced AI features such as predictive scaling, automated cost optimization, and self-healing recommendations.
- A full graphical user interface (GUI); initial releases will emphasize CLI/terminal-based interaction with potential extension to VS Code plugins or web dashboards.
- Enterprise-specific features like centralized governance, role-based access control (RBAC), and integrations with third-party ticketing or approval workflows.


## Project Significance (Why this project matters)
The Speak-to-Infrastructure project is significant because it addresses one of the most pressing challenges in modern DevOps: making Infrastructure as Code accessible, faster, and less error-prone. Traditional Terraform usage requires extensive knowledge of HCL syntax, resource attributes, and provider-specific configurations. This creates bottlenecks in onboarding, slows down project delivery, and limits participation to highly technical team members.

By introducing an AI-powered, multi-cloud, natural language interface, this project:

- Democratizes Infrastructure as Code by lowering the barrier for entry and enabling both technical and non-technical users to generate Terraform projects collaboratively.
- Accelerates Deployment by reducing time-to-deployment from hours or days to minutes, speeding up prototyping, testing, and production rollouts.
- Minimizes Human Error through automated input validation and consistent application of security and best practices across projects.
- Promotes Multi-Cloud Readiness by offering a unified workflow for AWS, Azure, and GCP, allowing teams to adopt hybrid or multi-cloud strategies seamlessly.
- Drives Innovation in DevOps + AI by proving the integration of artificial intelligence into infrastructure automation and laying the groundwork for cost optimization, predictive scaling, and self-healing systems.
- Inspires Open-Source and Enterprise Adoption by being a downloadable standalone tool that organizations can use, adapt, and improve for real-world workflows.

## Project Stack / Tools & Technologies

| Category                | Tools / Technologies                                         | Purpose                                                                 |
|-------------------------|-------------------------------------------------------------|-------------------------------------------------------------------------|
| Artificial Intelligence & NLP | OpenAI / Hugging Face Transformers, Python (FastAPI / Flask) | Parse natural language input and generate Terraform code.               |
| Infrastructure as Code  | Terraform (AWS, Azure, GCP), Terraform Modules              | Provision multi-cloud infrastructure using reusable modules.            |
| DevOps & Cloud SDKs     | AWS SDK (Boto3), Azure SDK, Google Cloud SDK                | Validate inputs, fetch available resources, and support multi-cloud deployments. |
| CLI & User Interaction  | Python CLI frameworks (Click / Typer), Pydantic / Cerberus  | Provide interactive prompts, menus, and input validation.               |
| Automation Layer        | Terraform CLI Automation (`init`, `plan`, `apply`)          | Execute infrastructure provisioning after code generation.              |
| Packaging & Distribution| PyInstaller, Docker, Executable binaries (.exe, .deb, .pkg) | Package the system as a standalone downloadable tool for easy installation. |
| Future Extensions       | VS Code Extension, Web Dashboard (React + FastAPI)          | Enhance user experience with GUI-based or IDE-based interaction.        |


## End-to-End Flow 
The Speak-to-Infrastructure tool follows a clear end-to-end process that takes user input, validates it, generates Terraform code, and provisions cloud resources. This flow ensures the system is easy to understand and use, while keeping it flexible for multi-cloud environments.

i. **Intent** – User describes goal or chooses presets in CLI.  
ii. **Parse** – NLP extracts resources (VPC, subnets, EC2, DB, SGs, region).  
iii. **Q&A** – Prompt Engine asks only the missing/ambiguous items; each answer is validated instantly.  
iv. **Capabilities** – Provider Adapters fetch valid regions, AMIs/images, instance families, DB versions.  
v. **Codegen** – Template engine assembles `environments/<env>/*.tf` and `modules/*` from the Module Library.  
vi. **State** – Configure remote backend (S3 + DynamoDB / Azure Storage / GCS) based on cloud.  
vii. **Run** – Offer `terraform init → plan → apply`; stream logs; save artifacts to repo folder.  
viii. **Output** – Summary (resources, counts, cost estimation later), and next steps.  


## Functional Requirements (What the tool must do)
- The tool must accept natural language instructions and convert them into structured infrastructure intents.

- It must guide users through interactive prompts to capture missing details with minimal typing.

- All user inputs must be validated against schema rules and security best practices.

- The system must support multiple cloud providers (AWS, Azure, GCP) for provisioning resources.

- It must generate a complete, structured Terraform project with reusable modules.

- The tool must automate Terraform execution (init, plan, apply) with clear confirmations.

- It must handle PEM key pairs and credentials securely without exposing sensitive data.

- The system must be packaged as a standalone downloadable tool for cross-platform use.

- It must save generated Terraform code locally and provide resource summaries after deployment.

## Non-Functional Requirements (Performance, security, usability)

- Performance – The system must process and deliver speech input/output in real time with minimal latency.

- Scalability – The infrastructure must handle increasing numbers of users and workloads without performance degradation.
- Reliability – The system must ensure continuous availability with redundancy and failover mechanisms.
- Security – The platform must protect data using encryption, access control, and secure authentication.
- Usability – The interface must be intuitive, with simple navigation and clear error messages for both technical and non-technical users.
- Compliance – The system must meet relevant industry standards and data protection regulations.
- Maintainability – The infrastructure must allow easy updates, monitoring, and troubleshooting to reduce downtime.

## Assumptions & Limitations
### Assumptions

i. **Stable Internet** – The system assumes users have stable internet connectivity for real-time speech processing.  
ii. **Cloud Availability** – The infrastructure assumes cloud resources are available and scalable as needed.  
iii. **Compatible Devices** – It assumes users have compatible devices (microphones, speakers, browsers, or apps) to interact with the system.  
iv. **Third-Party Services** – The solution assumes third-party APIs and services used (e.g., speech-to-text, text-to-speech) remain available and reliable.

### Limitations
i. **Latency Under Load** – The system may experience latency under very high loads despite optimization.  
ii. **Speech Recognition Accuracy** – Accuracy may vary depending on background noise, accent, or language support.  
iii. **External Security Dependence** – Security depends partly on external service providers, which may limit full control.  
iv. **Limited Offline Functionality** – Most features require active internet access; offline support is restricted.  

## Project Steps 
**Step 1:** Set up the project environment and install dependencies.  

**Step 2:** Design the NLP engine to parse natural language into infrastructure intents.  

**Step 3:** Build the interactive prompt system for input validation.  

**Step 4:** Implement Terraform code generation with reusable modules.  

**Step 5:** Integrate automation for Terraform `init`, `plan`, and `apply`.  

**Step 6:** Package the system as a standalone downloadable tool.  

## Project Implementation 

### Step 1: Set up the Project Environment and Install Dependencies
Every successful project begins with a strong foundation. For Speak-to-Infrastructure, that foundation is the development environment. Before we can design NLP engines, generate Terraform code, or package executables, we need to make sure our system has the right tools installed and properly configured. If this step is skipped or done incorrectly, later stages (like running Terraform commands or calling cloud SDKs) will fail or behave unpredictably.
That’s why Step 1 is critical: it ensures consistency, reliability, and a clean workspace where all dependencies are isolated and managed. A well-prepared environment saves us hours of debugging later and allows us to focus on building features instead of fighting setup issues.

This includes:

i.	Installing Python (≥3.9) as our core programming language.

ii.	Setting up VS Code.

iii.	Creating a virtual environment to isolate project dependencies.

iv.	Installing the Python libraries we’ll need (NLP, SDKs, CLI tools).

v.	Installing the Terraform CLI, which is central to provisioning.


#### 1.1	Installing Python (≥3.9) as our core programming language

Python is the backbone of our Speak-to-Infrastructure tool. All the AI logic, NLP parsing, cloud SDK integrations, and even Terraform automation will be written in Python. That’s why installing Python correctly is the very first thing we must do.

- Go to the official Python download page: https://www.python.org/downloads/
- Download the latest stable release ≥3.9 (preferably 3.10 or 3.11 for best compatibility).
- Run the installer:
    - ✅ Check the box “Add Python to PATH” before clicking Install Now.
    - This ensures you can use python from the command line.
- After installation, open Command Prompt and check:
```
  Py --version
```
<img width="975" height="80" alt="image" src="https://github.com/user-attachments/assets/75863506-30ad-4c03-a292-bfade4f4a164" />

#### 1.2	Setting up VS Code

We’ll need a powerful code editor to write and organize our Python code, Terraform templates, and configuration files. Visual Studio Code (VS Code) is the most recommended because it’s lightweight, cross-platform, and has excellent extensions for Python, Terraform, and GitHub integration.

- Go to the official download page: https://code.visualstudio.com/
- Download the installer for your OS (Windows, macOS, or Linux).
- Run the installer and accept defaults. On Windows, ensure you check:
    - ✅ Add to PATH
    - ✅ Register Code as editor for supported file types
    - ✅ Add "Open with Code" action to Windows Explorer
- After installation, open VS Code.

  
Inside VS Code, go to Extensions (Ctrl+Shift+X) and install:

- Python (Microsoft) → for Python linting, IntelliSense, debugging.
<img width="975" height="284" alt="image" src="https://github.com/user-attachments/assets/e075d5c6-1f79-4abc-ab0b-b09c116f373f" />

- Terraform (HashiCorp) → syntax highlighting, validation, and auto-complete.
  <img width="975" height="227" alt="image" src="https://github.com/user-attachments/assets/bb0bb7aa-fc76-4116-844c-5008e6135b04" />

- GitHub Pull Requests & Issues → integrates GitHub directly into VS Code.
  
With VS Code ready, we’ll have a smooth workflow for writing Python scripts, testing the CLI tool, and generating Terraform projects.


#### 1.3 Creating a virtual environment to isolate project dependencies
A virtual environment isolates project dependencies so they don’t conflict with global Python packages or other projects on your machine. This ensures our Speak-to-Infrastructure tool runs consistently across setups.

- Inside your project folder (speak-to-infrastructure), run;
```
py -m venv venv
```
This creates a folder named venv containing the isolated Python environment.
<img width="570" height="260" alt="image" src="https://github.com/user-attachments/assets/726b20ba-a0f7-40e5-9f83-2d79b94c1632" />


- Activate the folder by running;
```
venv\Scripts\activate
```

#### 1.4	Installing the Python libraries we’ll need (NLP, SDKs, CLI tools)
Now that our virtual environment is active, we’ll install the core Python libraries that power our Speak-to-Infrastructure tool. These libraries cover AI/NLP, CLI interaction, validation, and cloud SDKs.

- Upgrade pip first. This makes sure pip can handle new packages smoothly. Run;
```
py -m pip install --upgrade pip
```

- Run this inside your activated virtual environment ((venv) should show in your terminal);
```
pip install transformers torch fastapi click typer pydantic boto3 azure-mgmt-resource google-cloud
``` 
<img width="975" height="217" alt="image" src="https://github.com/user-attachments/assets/09af0ea1-113f-402e-bb71-4a031f4fb02b" />

Breakdown of Libraries
  - transformers → Hugging Face library for NLP models (understands natural language).
  - torch → PyTorch backend for running AI models. (If you prefer TensorFlow, you can swap later, but PyTorch is more common.)
  - fastapi → Lightweight framework for APIs (we’ll use it if we expose the tool as an API).
  - click / typer → Frameworks for building nice CLI (command line interfaces) with prompts.
  - pydantic → For validating and structuring user inputs (e.g., regions, instance types).
  - boto3 → AWS SDK for Python, lets us validate regions/instances in AWS.
  - azure-mgmt-resource → Azure SDK to fetch regions/resources in Azure.
  - google-cloud → Google Cloud SDK for resource validation in GCP.

- After pip finishes, verify installation by running;
```
pip list
```
<img width="559" height="556" alt="image" src="https://github.com/user-attachments/assets/39d3322d-1bed-4712-8806-eb4b681ec563" />


#### 1.5	Installing the Terraform CLI, which is central to provisioning
Terraform CLI is the heart of this project — it’s what will take the AI-generated .tf files and actually provision cloud infrastructure. Without it, our tool can only generate code but not apply it.

Open your PowerShell as administrator and run these command

- Create a Directory for Terraform
```
mkdir "$HOME\terraform"
cd "$HOME\terraform"
```
- Download Terraform v1.13.3
```
Invoke-WebRequest -Uri "https://releases.hashicorp.com/terraform/1.13.3/terraform_1.13.3_windows_amd64.zip" -OutFile "terraform_1.13.3_windows_amd64.zip"
``` 
<img width="975" height="181" alt="image" src="https://github.com/user-attachments/assets/2268d3f7-3c5d-4349-a3d1-bddc2d0d5f1f" />

- Extract the ZIP File
```
Expand-Archive -Path "terraform_1.13.3_windows_amd64.zip" -DestinationPath "$HOME\terraform"
```

- Add Terraform to PATH (User-level)
```
$oldPath = [Environment]::GetEnvironmentVariable("Path", "User")
$newPath = "$oldPath;$HOME\terraform"
[Environment]::SetEnvironmentVariable("Path", $newPath, "User")
```
- Restart your PowerShell terminal for the PATH update to apply, then verify Installation
```
terraform -version
``` 
<img width="975" height="84" alt="image" src="https://github.com/user-attachments/assets/11d29aec-0842-4a28-be84-630d992e52d0" />

We have successfully set up a complete development environment with Python, VS Code, a virtual environment, essential libraries, Terraform CLI, and GitHub. This foundation ensures our project has the right tools, isolation, and automation capability to run smoothly. With this groundwork in place, we’re now ready to move into building the actual intelligence of the system in Step 2.

### Step 2: Design the Natural Language Processing NLP engine to parse Natural Language into Infrastructure Intents
The intelligence of Speak-to-Infrastructure begins with its ability to understand human instructions and convert them into structured infrastructure intents. This is made possible through Natural Language Processing (NLP) — a field of artificial intelligence that enables computers to understand, interpret, and generate human language. Without this layer, the tool would only be a code generator with no sense of context. By designing an NLP engine, we bridge the gap between natural language and Terraform-ready definitions, ensuring that user requests like “create a VPC with two subnets and an EC2 instance” can be parsed into actionable components. This step is critical because it lays the foundation for accuracy, flexibility, and reliability in the way infrastructure requests are interpreted.

This includes:

i. Loading a pre-trained NLP model.

ii. Defining intent categories: networking, compute, database, security, monitoring.

iii. Writing a parser that extracts entities: resource type, counts, configurations.

iv. Building a mapping layer to translate entities into Terraform resource blocks.

v. Testing the NLP engine with sample sentences.


##### 2.1 Loading a pre-trained NLP model

The first step in designing the NLP engine is giving our system the ability to understand human language. Instead of training a language model from scratch (which requires huge datasets and computing power), we can leverage pre-trained NLP models that are already trained on vast amounts of text. These models can recognize patterns in sentences, identify entities, and understand intent.
For this project, a pre-trained model (e.g., from Hugging Face Transformers such as BERT, DistilBERT, or GPT-based models) will serve as the foundation. Once loaded into our tool, we’ll customize it by adding rules, mappings, or fine-tuning so it can interpret DevOps-specific instructions like:

 - “Create a VPC with two subnets.”
 - “Deploy an EC2 instance with a MySQL database.”

This way, the model isn’t starting from zero — it already understands English structure — we just adapt it to map natural sentences into infrastructure intents.


- We need the transformers library from Hugging Face because it contains many pre-trained NLP models (like BERT, DistilBERT, GPT, etc.). run;
```
pip install transformers
```
<img width="975" height="231" alt="image" src="https://github.com/user-attachments/assets/dd6b650c-205e-4222-93b9-5bc3988a7728" />

- Install PyTorch (backend for running the model). Most Hugging Face models run on PyTorch by default (unless you choose TensorFlow). We’ll go with PyTorch for this project because it’s more widely supported. Run;
```
pip install torch
```
<img width="975" height="267" alt="image" src="https://github.com/user-attachments/assets/a0654cfb-883d-4c31-bd90-19ab8bc25931" />

- Create a new Python file in your project folder, call it: test_nlp.py
  <img width="850" height="231" alt="image" src="https://github.com/user-attachments/assets/88b33c5b-4708-403a-b5fe-6568af155ac4" />

- Open test_nlp.py and paste this code;
  
  [test_nlp.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/test_nlp.py)

  <img width="975" height="297" alt="image" src="https://github.com/user-attachments/assets/7b408f46-1032-48d6-916a-d777f1497d75" />

#### What this does:
- Loads DistilBERT, a smaller version of BERT.
- Runs a test by filling in the word [MASK] in a sentence.
- Prints the model’s predictions (e.g., it might say “powerful,” “useful,” etc.).


- Run the script with;
```
py test_nlp.py
```
<img width="975" height="325" alt="image" src="https://github.com/user-attachments/assets/f403bfe9-a61d-4938-9064-5f2fc2fdc56a" />

We successfully loaded a pre-trained NLP model (DistilBERT), tested it with a sample sentence, and confirmed it can understand natural language — giving us the foundation to map human instructions into infrastructure intents.


##### 2.2 Defining intent categories: networking, compute, database, security, monitoring

In order for our NLP engine to correctly interpret infrastructure instructions, we need to organize user requests into clear categories. These categories represent the major building blocks of cloud infrastructure.

For example:
- Networking → VPCs, Subnets, Gateways, Load Balancers
- Compute → EC2 instances, Auto Scaling, Containers
- Database → RDS, DynamoDB, Cloud SQL
- Security → IAM roles, Security Groups, Policies
- Monitoring → CloudWatch, Alerts, Logging
  
By defining these intent categories, we’re creating a framework that the model can map text onto. So, when a user says “create a VPC with two subnets”, the system immediately knows this falls under Networking, and can then parse details like VPC name or CIDR block.
This step is important because it gives our tool a structured vocabulary for infrastructure; without it, the AI would generate outputs too loosely.

- We’ll create a new Python file where we define the categories that our AI will use. The python file would be named intents.py

- Open intents.py and paste the below code.

  [intents.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/intents.py)

- Run it to confirm;
```
py intents.py
```
<img width="975" height="819" alt="image" src="https://github.com/user-attachments/assets/4fe63071-7a3a-4826-8e6f-c4fccfaa971f" />

We successfully defined intent categories (networking, compute, database, security, monitoring) and built a simple function that detects which category a user’s request belongs to. This gives our AI a basic ability to classify infrastructure instructions into the right “box,” making it easier to map them to Terraform resources later.

##### 2.3 Writing a parser that extracts entities: resource type, counts, configurations
Now that our AI can recognize what type of request a user makes, the next step is to make it more interactive.

Think of it like a conversation:

- If the user says “Create a server”, the tool should ask:
  
👉 “What size of server do you want?”

👉 “Which region should I deploy it in?”

- If the user says “Set up a database”, it should ask:
  
👉 “Which database engine (MySQL, Postgres, etc.)?”

👉 “What storage size do you need?”

This prompt system ensures we don’t guess blindly. Instead, we ask for missing details, validate inputs, and store them for Terraform code generation.

- Create a new file in the project folder named prompts.py

- Paste the below code inside;

  [prompts.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/prompts.py)

- Run this in your terminal;
```
pip install typer
```
<img width="975" height="225" alt="image" src="https://github.com/user-attachments/assets/8ef59428-33bc-445e-9314-2833e30934ac" />

- Run the program;
```
py prompts.py 
```
<img width="928" height="842" alt="image" src="https://github.com/user-attachments/assets/85faa527-3b36-46b4-b27d-045fe77f406d" />

We successfully built an interactive prompt system that guides the user step by step in selecting infrastructure options. Instead of typing technical commands, the user chooses from simple menus covering server size, operating system, database engine, networking, security, and monitoring. At the end, the tool generates a clear summary of all selections.
This makes the system beginner-friendly, reduces errors, and prepares structured input that will later be translated into Terraform code.

#### 2.4 Building a mapping layer to translate entities into Terraform resource blocks
Now that our system can collect structured user inputs (like server size, OS, database, networking, etc.), we need a way to map those choices into real Terraform resource definitions.

Think of it like this:

- The user’s choice is the idea → e.g., “Medium server, Ubuntu OS, MySQL database.”
- The mapping layer is the translator → it takes those ideas and turns them into actual Terraform code blocks.
- The Terraform files (main.tf, variables.tf, outputs.tf) are the final language that the cloud understands.
- 
Example:

- If the user picks Medium (t3.medium) → the mapping layer generates a Terraform block for an AWS EC2 instance (or Azure VM / GCP Compute Engine depending on provider).
- If the user picks MySQL → it generates a Terraform block for an RDS MySQL database.
- If the user picks Custom VPC with Subnet → it creates Terraform code for a VPC and subnet.


This step is critical because it connects the interactive wizard (Step 2.3) with the infrastructure-as-Code automation. Without it, the tool would just collect choices but never build the infrastructure.

- Create a script named infrastructure_wizard.py and paste the below script inside
  
  [infrastructure_wizard.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/infrastructure_wizard.py)

##### What This Script Does

This script is a multi-cloud interactive wizard that helps users design infrastructure without needing to know Terraform syntax. Instead of writing code manually, the user goes through a guided step-by-step process where they choose options from menus.

i. Asks the user to choose a cloud provider (AWS, Azure, or GCP).

ii.	Guides the user through prompts to select server size, operating system, database, networking, security, and monitoring options.

iii. Maps each user choice to the correct Terraform resource block for the chosen provider.

iv.	Generates a main.tf file containing Terraform code for compute, database, networking, security, and monitoring.

v.	Generates a variables.tf file to define reusable variables like region.

vi.	Generates an outputs.tf file to show important values like server ID or public IP.

vii.	Prints a final summary of all the user’s choices at the end.

viii.	Overall, it transforms simple menu-driven inputs into a ready-to-run Terraform project.


- Run the program;
```
py infrastructure_wizard.py 
```
<img width="975" height="656" alt="image" src="https://github.com/user-attachments/assets/7838625a-f841-4c16-b083-6478834a9ffd" />

#### 2.5 Testing the NLP engine with sample sentences
The goal here is to test whether our NLP engine can interpret natural language requests and map them into infrastructure intents (like compute, database, networking, etc.).
What we’ll do in 2.5:

i.	Take sample sentences (e.g., “Deploy a small Ubuntu server on AWS with MySQL”).

ii.	Run them through the NLP intent parser (the script we built in Step 2.2).

iii.	Verify that the parser correctly identifies:

  - Cloud Provider (AWS, Azure, GCP)
  - Server Size (Small, Medium, Large)
  - Operating System (Ubuntu, Windows, etc.)
  - Database (MySQL, PostgreSQL, MongoDB)
  - Networking (Default VPC, Custom VPC, etc.)
  - Security & Monitoring

- Create a new file called test_nlp_infra.py and paste the below code in it;
  
  [test_nlp_infra.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/test_nlp_infra.py)

##### What this script does

i.	Loads the DistilBERT NLP model.

ii.	Runs a few sample infrastructure requests through it.

iii. Just tests whether the model understands context (this is the warm-up before linking directly with intents.py). 

iv.	Prints the results (so you’ll see what the AI thinks fits into the sentence).

- Run the script:
```
py test_nlp_infra.py
```
<img width="952" height="963" alt="image" src="https://github.com/user-attachments/assets/9cdefa26-c7ad-441c-8109-8ec32db15330" />

In this Step, we successfully designed and implemented the Natural Language Processing (NLP) engine for the Speak-to-Infrastructure project. The goal of this step was to ensure our system could understand plain English instructions and convert them into structured infrastructure intents that later translate into Terraform code.

Here’s what was achieved:

i.	Loaded a Pre-trained NLP Model → We used Hugging Face’s DistilBERT model to give the tool an immediate ability to interpret natural language without training from scratch.

ii.	Defined Intent Categories → We organized all cloud-related tasks into key categories: networking, compute, database, security, monitoring, provider, and operating system.

iii.	Built an Intent Parser → A rule-based parser was created to extract entities (e.g., “server,” “MySQL,” “Ubuntu”) from user sentences.

iv.	Added Interactive Prompts → The system asks clarifying questions (e.g., “Which server size do you want?”) so the user selects from clear options instead of typing complex inputs.

v.	Developed a Mapping Layer → User choices are translated into real Terraform resource blocks for AWS, Azure, and GCP.

vi.	Tested with Sample Sentences → Sentences like “Deploy a small Ubuntu server on AWS with MySQL” were parsed successfully into intents such as provider=AWS, compute=small, os=Ubuntu, database=MySQL.

##### Overall Result:
Step 2 gave our tool its intelligence layer. Instead of blindly generating Terraform code, the system now understands user requests, classifies them into intents, asks follow-up questions when needed, and maps everything into structured infrastructure definitions. This provides the foundation for seamless automation in later steps.


### Step 3: Build the interactive prompt system for input validation

After successfully building the Natural Language Processing (NLP) engine in Step 2, the next critical milestone is giving the system a voice and a face, a way for users to actually interact with it.

Step 3 transforms Speak-to-Infrastructure from a background intelligence tool into a truly interactive assistant that can communicate with users through both voice and text.
The goal of this step is to design a dual-mode interaction framework that allows users to either speak or type their infrastructure requests and to receive confirmations, clarifications, and validations through the same channels. This is the stage where our project evolves from “AI that understands infrastructure” to “AI that converses about infrastructure.”

Through this interactive prompt system, we will:
- Create an intuitive command-line interface (CLI) for text users.
- Integrate speech-to-text (STT) and text-to-speech (TTS) libraries for voice interaction.
- Build real-time validation using cloud SDKs (AWS, Azure, GCP).
- Implement context-aware question flows that ask for only missing or ambiguous details.
- Introduce error handling, mode switching, and final configuration summaries that work in both voice and text.

Below is the project workflow for thus step
3.1 Design Dual-Mode Interaction Framework (Voice + Text)

3.2 Implement Voice Interaction System

3.3 Implement Text Interaction System

3.4 Create Hybrid Mode Functionality

3.5 Build Intelligent Prompt Logic for Missing Infrastructure Details

3.6 Integrate Cloud SDK Validation with Dual Feedback

3.7 Build Input Validation Rules with Pydantic Schemas

3.8 Create Comprehensive Error Handling and Re-Prompt Mechanisms

3.9 Store Validated Configuration with Dual-Mode Summary

3.10 Test Prompt System Comprehensively


#### 3.1 Design Dual-Mode Interaction Framework (Voice + Text)

Right now, our tool is a smart brain that works through a text-based wizard (infrastructure_wizard.py). It's powerful, but it only has one way to talk: typing.

Our goal is to give our brain (the app) two new faces and one new voice.

- A Text Face: A more polished and professional Command-Line Interface (CLI).
- A Voice Face: The ability to listen through the microphone and talk through the speakers.
- A Mode Selector: A simple menu at the very start that lets the user choose how they want to talk to the tool.

Think of it like this: Our project is a car. Until now, it only had a manual transmission (the text wizard). We are now adding an automatic transmission (voice mode) and a little switch on the dashboard to let the driver choose which one they prefer.
	
- We will create a simple, clear menu that asks the user how they want to interact. Create a new file in your project folder and name it orchestrator.py and paste the below code

     [orchestrator.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/orchestrator.py)



- Run the file from your terminal to make sure it works perfectly.
py orchestrator.py

<img width="852" height="301" alt="image" src="https://github.com/user-attachments/assets/d42c428b-cf77-45d4-96c5-1f0bf0d4e67f" />

Now that the user can choose voice mode, we need to give our program the ability to hear. We do this by installing a library that can turn microphone input into text.
We will install the SpeechRecognition library. It's the easiest and most popular one for this job. It acts as a universal wrapper for many different speech-to-text engines.

- Run this command to install SpeechRecognition.
```
pip install SpeechRecognition
```
<img width="975" height="323" alt="image" src="https://github.com/user-attachments/assets/b4d6545b-7cc6-4633-b92f-857ef121da15" />

 
- SpeechRecognition is just a manager. It needs a worker to do the actual sound processing. The most common and reliable one is PyAudio. Install it with this command:
```
pip install PyAudio
```
<img width="888" height="239" alt="image" src="https://github.com/user-attachments/assets/547a00c6-b4b8-41cc-b076-8b4e9fbb2f77" />


- Let's make sure everything installed correctly and do a hearing test. Create a new file called test_hearing.py and paste this code:

  [test_hearing.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/test_hearing.py)

- Run the file and speak into your microphone when it says "Listening...".
py test_hearing.py
<img width="975" height="847" alt="image" src="https://github.com/user-attachments/assets/719632f0-a923-4998-827a-a820ba97c971" />
 

Now that our program can hear the user, we need to teach it how to speak back. We do this by installing a Text-to-Speech (TTS) library.

- Run this command to install;
```
pip install pyttsx3
```
<img width="930" height="495" alt="image" src="https://github.com/user-attachments/assets/91d82305-c872-4317-ade7-e220ce7959c0" />


- Do a Super Simple "Speaking Test". Let's make sure it works. Create a new file called test_speaking.py and paste this code:

 [test_speaking.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/test_speaking.py)

  
- Run the file. You should hear the computer speak the test message.
```
py test_speaking.py
```
<img width="975" height="829" alt="image" src="https://github.com/user-attachments/assets/0a4e4919-db31-4f3e-8de8-6d6322005ee9" />

 

Right now, our text mode uses simple input() and print() statements. This works, but we can make it more professional, easier to use, and less error-prone. We will use Typer because it's modern, intuitive, and perfect for building CLIs.



- Let’s install typer by running the command;
```
pip install typer
```
<img width="975" height="393" alt="image" src="https://github.com/user-attachments/assets/e9e26e00-be5a-41c7-b035-f85991a26fed" />
 

- Let’s do a Simple Typer Test. Let's learn the basics. Create a new file called test_typer.py and paste this code:

   [test_typer.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/test_typer.py)

- Now, try running the file in different ways to see how Typer works: Test 1 - Get Help:
```
py test_typer.py –help
```
<img width="975" height="272" alt="image" src="https://github.com/user-attachments/assets/24d34202-7bd6-43ce-89d1-c786b342b3b4" />




- Test 2 - Run the hello command:
```
py test_typer.py hello Dave
```
<img width="752" height="119" alt="image" src="https://github.com/user-attachments/assets/6403cdb1-7a28-45e1-8820-d49afb5160dc" />


- Test 3 - Run the menu command:
```
py test_typer.py menu
```
<img width="672" height="806" alt="image" src="https://github.com/user-attachments/assets/bf72210a-6f42-4118-a027-2eea50c8067d" />


Now, we need to create a reusable function that we can call whenever we want to listen to the user in voice mode.

- Create a new file called voice_engine.py in your project folder. Write the Core Listening Function. Code below

 [voice_engine.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/voice_engine.py)


- Run the voice engine test to make sure everything works together:
```
py voice_engine.py
``` 
<img width="975" height="776" alt="image" src="https://github.com/user-attachments/assets/6b28f223-3d3b-44dd-b4f0-63cd9bbe69eb" />

We're going to create a simple test that brings everything together and lets us test both input methods (Voice and Text).

- Create a new file called test_modes.py and paste this code:

   [test_modes.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/test_modes.py)


- Run the Comprehensive Test;
```
py test_modes.py
``` 
<img width="966" height="548" alt="image" src="https://github.com/user-attachments/assets/2dd8a317-aa60-4953-8f22-131c00f4a900" />

#### 3.2 Implement voice interaction system

We've successfully given your application the basic ability to hear and speak. It can detect speech through the microphone and respond with synthesized voice. However, this is comparable to teaching someone the alphabet without yet showing them how to form sentences or hold conversations.

Now, we are about moving from those raw capabilities to creating a fluid and reliable conversational experience. We will transform the simple voice functions into an interactive system that feels intelligent and responsive. This involves making the tool more robust against errors, allowing it to confirm its understanding with you, and providing clear feedback so you always know what it's processing.

The goal is to build trust in the voice interface. You should feel confident that when you speak a command, the system has understood you correctly before it takes any action. We will add layers of verification and clarity to ensure the conversation between you and the tool is as smooth and error-free as possible.

- Right now, our listen_to_speech() function works, but it's basic. We're going to make it much more robust and user-friendly. Create a new file enhanced_voice_engine.py and paste the below

   [enhanced_voice_engine.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/enhanced_voice_engine.py)

- Test the new enhanced system by running;
```
py enhanced_voice_engine.py
```
<img width="975" height="726" alt="image" src="https://github.com/user-attachments/assets/cd137130-48a0-47b4-b168-2edd6ed6f343" />


Now we'll enhance the text-to-speech system to make the computer's voice more natural and appropriate for an infrastructure assistant.

- Create a new file advanced_tts_engine.py and paste the below;

   [advanced_tts_engine.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/advanced_tts_engine.py)


- Test the advanced TTS system by running this command;
```
py advanced_tts_engine.py
```
 <img width="975" height="576" alt="image" src="https://github.com/user-attachments/assets/7d93860a-235a-499f-9b90-1be760cb1dce" />


The next is a cool feature that makes the voice interaction feel more natural. Instead of always listening, the system will wait for a wake word like "Hey Assistant" before it starts processing commands.

- Create a new file wake_word_detector.py and paste the below code

   [wake_word_detector.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/wake_word_detector.py)

- Test the wake word detection
```
py wake_word_detector.py
``` 
<img width="975" height="438" alt="image" src="https://github.com/user-attachments/assets/c64b549a-504f-4215-8a3a-6eb4156b9ea0" />

We would now build a voice confirmation system. This feature makes the interaction much more reliable. 

- Create a new file voice_confirmation_system.py and paste the below code

   [voice_confirmation_system.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/voice_confirmation_system.py)

- Test the confirmation system. Run;
```
py voice_confirmation_system.py
``` 
<img width="975" height="361" alt="image" src="https://github.com/user-attachments/assets/c43489dc-d727-41c4-bbf9-de67792a5fe2" />

Now, we would implement voice-to-text transcription display for verification. This feature gives users visual confirmation of what the system understood by displaying the transcribed text on screen. This provides dual verification - both hearing the confirmation and seeing the text. 

- Create a new file voice_transcription_display.py and paste the below code

   [voice_transcription_display.py](https://github.com/Ogbunugafor-Philip/-Speak-to-Infrastructure-AI-Powered-Natural-Language-to-Terraform-Generator-/blob/main/voice_transcription_display.py)

- Test the transcription display system by running the command;
```
py voice_transcription_display.py
``` 
<img width="975" height="691" alt="image" src="https://github.com/user-attachments/assets/bd463700-4ecf-4385-8ff0-c23e4c0e4e91" />

#### 3.3 Implement text interaction system















  






