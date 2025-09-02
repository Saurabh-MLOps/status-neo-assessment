from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.models.pydantic_models import ProcessingResult, ValidationResult
import logging
import re
from datetime import datetime
import difflib

logger = logging.getLogger(__name__)

class ValidationAgent(BaseAgent):
    """Agent responsible for validating and reconciling information across documents"""
    
    def __init__(self):
        super().__init__()
        self.field_priorities = {
            'name': ['application_form', 'government_id', 'bank_statement'],
            'date_of_birth': ['government_id', 'application_form', 'bank_statement'],
            'income': ['bank_statement', 'pay_stub', 'tax_return', 'application_form'],
            'address': ['government_id', 'utility_bill', 'application_form'],
            'employment': ['pay_stub', 'application_form', 'bank_statement']
        }
        
    def get_capabilities(self) -> List[str]:
        return [
            "cross_document_validation",
            "conflict_resolution",
            "data_reconciliation",
            "confidence_scoring",
            "priority_based_resolution"
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> ProcessingResult:
        """Validate and reconcile information across documents"""
        try:
            if not self.validate_input(input_data):
                return self.create_error_result("Invalid input data")
            
            application_data = input_data.get('application_data', {})
            extracted_data = input_data.get('extracted_data', {})
            
            if not application_data or not extracted_data:
                return self.create_error_result("Missing application or extracted data")
            
            # Perform validation
            validation_result = await self._validate_information(application_data, extracted_data)
            
            # Resolve conflicts if any
            if validation_result.conflicts:
                resolved_data = await self._resolve_conflicts(validation_result.conflicts, extracted_data)
                validation_result.resolved_data.update(resolved_data)
            
            # Calculate overall confidence
            overall_confidence = self._calculate_overall_confidence(validation_result)
            validation_result.confidence_score = overall_confidence
            
            self.log_action("validation_completed", {
                "conflicts_found": len(validation_result.conflicts),
                "overall_confidence": overall_confidence,
                "fields_validated": len(self.field_priorities)
            })
            
            return self.create_success_result({
                'validation_result': validation_result.dict(),
                'is_valid': validation_result.is_valid,
                'confidence': overall_confidence
            }, overall_confidence)
            
        except Exception as e:
            logger.error(f"Validation agent error: {e}")
            return self.create_error_result(f"Validation failed: {str(e)}")
    
    async def _validate_information(self, application_data: Dict[str, Any], 
                                  extracted_data: Dict[str, Any]) -> ValidationResult:
        """Validate information across different sources"""
        conflicts = []
        validated_data = {}
        
        for field, priority_sources in self.field_priorities.items():
            field_conflicts = []
            field_values = {}
            
            # Get values from application form
            app_value = application_data.get(field)
            if app_value:
                field_values['application_form'] = app_value
            
            # Get values from extracted documents
            for doc_type in priority_sources:
                doc_value = self._extract_field_from_documents(field, doc_type, extracted_data)
                if doc_value:
                    field_values[doc_type] = doc_value
            
            # Check for conflicts
            if len(field_values) > 1:
                unique_values = set(str(v).lower().strip() for v in field_values.values() if v)
                if len(unique_values) > 1:
                    field_conflicts.append({
                        'field': field,
                        'values': field_values,
                        'priority_sources': priority_sources
                    })
            
            # Store validated data
            validated_data[field] = field_values
            
            if field_conflicts:
                conflicts.extend(field_conflicts)
        
        return ValidationResult(
            is_valid=len(conflicts) == 0,
            conflicts=conflicts,
            resolved_data=validated_data
        )
    
    def _extract_field_from_documents(self, field: str, doc_type: str, 
                                    extracted_data: Dict[str, Any]) -> Optional[Any]:
        """Extract specific field value from documents of given type"""
        try:
            # Look for documents of the specified type
            for doc in extracted_data.get('document_types', []):
                if doc_type.lower() in doc.lower():
                    # Extract field value based on field type
                    if field == 'name':
                        return self._extract_name_from_document(doc, extracted_data)
                    elif field == 'date_of_birth':
                        return self._extract_dob_from_document(doc, extracted_data)
                    elif field == 'income':
                        return self._extract_income_from_document(doc, extracted_data)
                    elif field == 'address':
                        return self._extract_address_from_document(doc, extracted_data)
                    elif field == 'employment':
                        return self._extract_employment_from_document(doc, extracted_data)
            
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting field {field} from {doc_type}: {e}")
            return None
    
    def _extract_name_from_document(self, doc_type: str, extracted_data: Dict[str, Any]) -> Optional[str]:
        """Extract name from document"""
        # Look for name patterns in text content
        text_content = extracted_data.get('all_text_content', [])
        for text in text_content:
            # Simple name extraction - look for common patterns
            name_patterns = [
                r'Name:\s*([A-Za-z\s]+)',
                r'Full Name:\s*([A-Za-z\s]+)',
                r'Applicant:\s*([A-Za-z\s]+)'
            ]
            
            for pattern in name_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        
        return None
    
    def _extract_dob_from_document(self, doc_type: str, extracted_data: Dict[str, Any]) -> Optional[str]:
        """Extract date of birth from document"""
        text_content = extracted_data.get('all_text_content', [])
        for text in text_content:
            # Look for DOB patterns
            dob_patterns = [
                r'Date of Birth:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'DOB:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'Birth Date:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
            ]
            
            for pattern in dob_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1)
        
        return None
    
    def _extract_income_from_document(self, doc_type: str, extracted_data: Dict[str, Any]) -> Optional[float]:
        """Extract income information from document"""
        text_content = extracted_data.get('all_text_content', [])
        for text in text_content:
            # Look for income patterns
            income_patterns = [
                r'Monthly Income:\s*\$?([\d,]+\.?\d*)',
                r'Income:\s*\$?([\d,]+\.?\d*)',
                r'Salary:\s*\$?([\d,]+\.?\d*)'
            ]
            
            for pattern in income_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        income_str = match.group(1).replace(',', '')
                        return float(income_str)
                    except ValueError:
                        continue
        
        return None
    
    def _extract_address_from_document(self, doc_type: str, extracted_data: Dict[str, Any]) -> Optional[str]:
        """Extract address information from document"""
        text_content = extracted_data.get('all_text_content', [])
        for text in text_content:
            # Look for address patterns
            address_patterns = [
                r'Address:\s*([^\n]+)',
                r'Street Address:\s*([^\n]+)',
                r'Residence:\s*([^\n]+)'
            ]
            
            for pattern in address_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        
        return None
    
    def _extract_employment_from_document(self, doc_type: str, extracted_data: Dict[str, Any]) -> Optional[str]:
        """Extract employment information from document"""
        text_content = extracted_data.get('all_text_content', [])
        for text in text_content:
            # Look for employment patterns
            employment_patterns = [
                r'Employer:\s*([^\n]+)',
                r'Company:\s*([^\n]+)',
                r'Workplace:\s*([^\n]+)'
            ]
            
            for pattern in employment_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        
        return None
    
    async def _resolve_conflicts(self, conflicts: List[Dict[str, Any]], 
                               extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflicts using priority-based rules"""
        resolved_data = {}
        
        for conflict in conflicts:
            field = conflict['field']
            values = conflict['values']
            priority_sources = conflict['priority_sources']
            
            # Use priority-based resolution
            resolved_value = self._resolve_field_conflict(field, values, priority_sources)
            resolved_data[field] = resolved_value
            
            logger.info(f"Resolved conflict for {field}: {resolved_value}")
        
        return resolved_data
    
    def _resolve_field_conflict(self, field: str, values: Dict[str, Any], 
                              priority_sources: List[str]) -> Any:
        """Resolve conflict for a specific field using priority rules"""
        # Find the highest priority source that has a value
        for source in priority_sources:
            if source in values and values[source]:
                return values[source]
        
        # If no priority source has a value, return the first available value
        for value in values.values():
            if value:
                return value
        
        return None
    
    def _calculate_overall_confidence(self, validation_result: ValidationResult) -> float:
        """Calculate overall confidence score based on validation results"""
        if not validation_result.conflicts:
            return 1.0
        
        # Base confidence
        base_confidence = 0.7
        
        # Reduce confidence based on number of conflicts
        conflict_penalty = min(len(validation_result.conflicts) * 0.1, 0.3)
        
        # Consider resolution success
        resolution_bonus = 0.1 if validation_result.resolved_data else 0.0
        
        final_confidence = base_confidence - conflict_penalty + resolution_bonus
        
        return max(0.0, min(1.0, final_confidence)) 