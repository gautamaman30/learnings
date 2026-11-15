"""
Creational Design Patterns Demonstration File

Contains:
1. Factory Method
2. Abstract Factory
3. Builder 
4. Singleton 
5. Prototype (ACTIVE)
"""

# =====================================================================
# 1. FACTORY METHOD
# =====================================================================
"""
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending Email: {message}")

class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")

class NotificationFactory(ABC):
    @abstractmethod
    def create_notification(self) -> Notification:
        pass

class EmailNotificationFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return EmailNotification()

class SMSNotificationFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return SMSNotification()
"""


# =====================================================================
# 2. ABSTRACT FACTORY
# =====================================================================
"""
from abc import ABC, abstractmethod

class Instance(ABC): pass
class Bucket(ABC): pass
class Storage(ABC): pass

class CloudFactory(ABC):
    @abstractmethod
    def createInstance(self, details: str) -> Instance: pass
    @abstractmethod
    def createBucket(self, details: str) -> Bucket: pass
    @abstractmethod
    def createStorage(self, details: str) -> Storage: pass

class Ec2Instance(Instance):
    def __init__(self, details: str): print('Ec2 created:', details)

class S3Bucket(Bucket):
    def __init__(self, details: str): print('S3 created:', details)

class RdsStorage(Storage):
    def __init__(self, details: str): print('Rds created:', details)

class AWSFactory(CloudFactory):
    def createInstance(self, instanceDetails: str) -> Instance:
        return Ec2Instance(instanceDetails)
    def createBucket(self, bucketDetails: str) -> Bucket:
        return S3Bucket(bucketDetails)
    def createStorage(self, storageDetails: str) -> Storage:
        return RdsStorage(storageDetails)
"""


# =====================================================================
# 3. BUILDER (Fluent Interface Variant)
# =====================================================================
"""
class HttpRequest:
    def __init__(self):
        self.url = ''
        self.method = ''
        self.params = {}
        self.headers = {}
        self.body = {}
        self.timeout_sec = 30
        
    def set_method(self, method: str):
        self.method = method
        return self
    
    def set_url(self, url: str):
        self.url = url
        return self
    
    def set_header(self, key: str, val: str):
        self.headers[key] = val
        return self
    
    def set_params(self, key: str, val: str):
        self.params[key] = val
        return self
        
    def set_body(self, key: str, val: str):
        self.body[key] = val
        return self
        
    def set_timeout(self, timeout: int):
        self.timeout_sec = timeout
        return self

    def __str__(self):
        return f"[{self.method}] {self.url} | Headers: {self.headers} | Timeout: {self.timeout_sec}s"
"""


# =====================================================================
# 4. SINGLETON
# =====================================================================
"""
class DatabaseConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, connection_string: str = "localhost:5432"):
        self.connection_string = connection_string
"""


# =====================================================================
# 5. PROTOTYPE (ACTIVE)
# =====================================================================
import copy

class Pipeline:
    def __init__(self, name: str):
        self.name = name
        # Heavy setup simulating DB lookups or config parsing
        self.stages = ["lint", "unit_test", "security_scan"]
        self.notifications = {"slack": "#dev-alerts", "email": "dev@company.com"}
        self.timeout_minutes = 60

    def clone(self):
        """Creates a deep copy of the object so nested structures remain independent."""
        return copy.deepcopy(self)

    def __str__(self):
        return f"[{self.name}] Stages: {self.stages} | Slack: {self.notifications['slack']}"


if __name__ == "__main__":
    print("--- Executing Active Pattern: Prototype ---")
    
    # 1. Create the base master prototype
    master_template = Pipeline("Enterprise-Master-Template")
    master_template.stages.append("docker_build")
    master_template.stages.append("deploy_to_k8s")

    # 2. Clone for Auth Service
    auth_service_pipeline = master_template.clone()
    auth_service_pipeline.name = "Auth-Service-Pipeline"
    auth_service_pipeline.notifications["slack"] = "#auth-team-alerts"

    # 3. Clone for Payment Service
    payment_service_pipeline = master_template.clone()
    payment_service_pipeline.name = "Payment-Service-Pipeline"
    payment_service_pipeline.notifications["slack"] = "#payments-team-alerts"

    print(master_template)
    print(auth_service_pipeline)
    print(payment_service_pipeline)