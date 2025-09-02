from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from app.models.pydantic_models import ProcessingResult, ValidationResult
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, agent_id: Optional[str] = None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.name = self.__class__.__name__
        self.created_at = datetime.utcnow()
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> ProcessingResult:
        """Process input data and return results"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        pass
    
    def log_action(self, action: str, details: Dict[str, Any]):
        """Log agent actions for audit purposes"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": self.agent_id,
            "agent_name": self.name,
            "action": action,
            "details": details
        }
        self.logger.info(f"Agent action: {log_entry}")
        return log_entry
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data format"""
        if not isinstance(input_data, dict):
            self.logger.error("Input data must be a dictionary")
            return False
        return True
    
    def create_error_result(self, error_message: str) -> ProcessingResult:
        """Create a standardized error result"""
        return ProcessingResult(
            success=False,
            error=error_message,
            confidence_score=0.0
        )
    
    def create_success_result(self, data: Dict[str, Any], confidence: float = 1.0) -> ProcessingResult:
        """Create a standardized success result"""
        return ProcessingResult(
            success=True,
            data=data,
            confidence_score=confidence
        )
    
    def __str__(self):
        return f"{self.name}(id={self.agent_id})"
    
    def __repr__(self):
        return self.__str__() 