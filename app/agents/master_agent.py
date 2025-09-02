from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.extraction_agent import ExtractionAgent
from app.agents.validation_agent import ValidationAgent
from app.agents.eligibility_agent import EligibilityAgent
from app.models.pydantic_models import ProcessingResult, ApplicationStatus
import logging
import asyncio
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class MasterAgent(BaseAgent):
    """Master agent that orchestrates the entire application processing workflow"""
    
    def __init__(self):
        super().__init__()
        self.agents = {
            'extraction': ExtractionAgent(),
            'validation': ValidationAgent(),
            'eligibility': EligibilityAgent()
        }
        self.workflow_steps = [
            'extraction',
            'validation', 
            'eligibility'
        ]
        
    def get_capabilities(self) -> List[str]:
        return [
            "workflow_orchestration",
            "agent_coordination",
            "error_handling",
            "progress_tracking",
            "result_aggregation"
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> ProcessingResult:
        """Orchestrate the complete application processing workflow"""
        try:
            if not self.validate_input(input_data):
                return self.create_error_result("Invalid input data")
            
            # Initialize workflow state
            workflow_id = str(uuid.uuid4())
            workflow_state = {
                'workflow_id': workflow_id,
                'start_time': datetime.utcnow(),
                'current_step': 0,
                'total_steps': len(self.workflow_steps),
                'results': {},
                'errors': [],
                'status': 'processing'
            }
            
            self.log_action("workflow_started", {
                'workflow_id': workflow_id,
                'input_data_keys': list(input_data.keys())
            })
            
            # Execute workflow steps
            for step_idx, step_name in enumerate(self.workflow_steps):
                try:
                    workflow_state['current_step'] = step_idx + 1
                    workflow_state['status'] = f'processing_{step_name}'
                    
                    logger.info(f"Executing step {step_idx + 1}/{len(self.workflow_steps)}: {step_name}")
                    
                    # Execute agent
                    step_result = await self._execute_agent_step(step_name, input_data, workflow_state)
                    
                    if step_result.success:
                        workflow_state['results'][step_name] = step_result.data
                        logger.info(f"Step {step_name} completed successfully")
                    else:
                        workflow_state['errors'].append({
                            'step': step_name,
                            'error': step_result.error,
                            'timestamp': datetime.utcnow().isoformat()
                        })
                        logger.error(f"Step {step_name} failed: {step_result.error}")
                        
                        # Decide whether to continue or fail fast
                        if not self._should_continue_after_error(step_name, step_result.error):
                            workflow_state['status'] = 'failed'
                            break
                    
                    # Update input data for next step
                    input_data = self._prepare_input_for_next_step(step_name, step_result, input_data)
                    
                except Exception as e:
                    error_msg = f"Unexpected error in step {step_name}: {str(e)}"
                    workflow_state['errors'].append({
                        'step': step_name,
                        'error': error_msg,
                        'timestamp': datetime.utcnow().isoformat()
                    })
                    logger.error(error_msg)
                    
                    if not self._should_continue_after_error(step_name, error_msg):
                        workflow_state['status'] = 'failed'
                        break
            
            # Finalize workflow
            workflow_state['end_time'] = datetime.utcnow()
            workflow_state['status'] = self._determine_final_status(workflow_state)
            
            # Aggregate results
            final_result = await self._aggregate_workflow_results(workflow_state)
            
            self.log_action("workflow_completed", {
                'workflow_id': workflow_id,
                'final_status': workflow_state['status'],
                'total_errors': len(workflow_state['errors']),
                'duration_seconds': (workflow_state['end_time'] - workflow_state['start_time']).total_seconds()
            })
            
            # Check if workflow has errors and should be treated as failed
            if workflow_state['status'] in ['failed', 'completed_with_errors']:
                return self.create_error_result(f"Workflow completed with errors: {workflow_state['status']}")
            else:
                return self.create_success_result(final_result, self._calculate_workflow_confidence(workflow_state))
            
        except Exception as e:
            logger.error(f"Master agent workflow error: {e}")
            return self.create_error_result(f"Workflow execution failed: {str(e)}")
    
    async def _execute_agent_step(self, step_name: str, input_data: Dict[str, Any], 
                                 workflow_state: Dict[str, Any]) -> ProcessingResult:
        """Execute a single agent step"""
        try:
            agent = self.agents.get(step_name)
            if not agent:
                return self.create_error_result(f"Agent {step_name} not found")
            
            # Prepare step-specific input
            step_input = self._prepare_step_input(step_name, input_data, workflow_state)
            
            # Execute agent
            step_result = await agent.process(step_input)
            
            # Log step execution
            self.log_action(f"step_executed", {
                'step_name': step_name,
                'agent_id': agent.agent_id,
                'success': step_result.success,
                'confidence': step_result.confidence_score
            })
            
            return step_result
            
        except Exception as e:
            logger.error(f"Error executing step {step_name}: {e}")
            return self.create_error_result(f"Step execution failed: {str(e)}")
    
    def _prepare_step_input(self, step_name: str, input_data: Dict[str, Any], 
                           workflow_state: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input data for a specific step"""
        step_input = input_data.copy()
        
        # Add results from previous steps
        for prev_step, result in workflow_state['results'].items():
            if prev_step in step_input:
                step_input[f'{prev_step}_result'] = result
            else:
                step_input[prev_step] = result
        
        # Add workflow context
        step_input['workflow_context'] = {
            'workflow_id': workflow_state['workflow_id'],
            'current_step': step_name,
            'previous_results': workflow_state['results']
        }
        
        return step_input
    
    def _prepare_input_for_next_step(self, step_name: str, step_result: ProcessingResult, 
                                   current_input: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input data for the next step"""
        next_input = current_input.copy()
        
        # Add current step result
        next_input[f'{step_name}_result'] = step_result.data
        
        # Update application data if available
        if step_name == 'extraction' and step_result.success:
            next_input['extracted_data'] = step_result.data
        
        elif step_name == 'validation' and step_result.success:
            next_input['validation_result'] = step_result.data
            # Update application data with validated information
            if 'resolved_data' in step_result.data:
                next_input['validated_application_data'] = step_result.data['resolved_data']
        
        elif step_name == 'eligibility' and step_result.success:
            next_input['eligibility_result'] = step_result.data
        
        return next_input
    
    def _should_continue_after_error(self, step_name: str, error: str) -> bool:
        """Determine if workflow should continue after an error"""
        # Critical steps that should fail fast
        critical_steps = ['extraction']
        
        if step_name in critical_steps:
            return False
        
        # For other steps, continue but log the error
        return True
    
    def _determine_final_status(self, workflow_state: Dict[str, Any]) -> str:
        """Determine the final status of the workflow"""
        if workflow_state['status'] == 'failed':
            return 'failed'
        
        if workflow_state['errors']:
            return 'completed_with_errors'
        
        if len(workflow_state['results']) == len(self.workflow_steps):
            return 'completed_successfully'
        
        return 'incomplete'
    
    async def _aggregate_workflow_results(self, workflow_state: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate results from all workflow steps"""
        aggregated_result = {
            'workflow_id': workflow_state['workflow_id'],
            'status': workflow_state['status'],
            'start_time': workflow_state['start_time'].isoformat(),
            'end_time': workflow_state['end_time'].isoformat(),
            'total_steps': workflow_state['total_steps'],
            'completed_steps': len(workflow_state['results']),
            'errors': workflow_state['errors']
        }
        
        # Add step results
        for step_name, result in workflow_state['results'].items():
            aggregated_result[f'{step_name}_result'] = result
        
        # Create final application status
        if 'eligibility_result' in workflow_state['results']:
            eligibility_data = workflow_state['results']['eligibility_result']
            if 'decision' in eligibility_data:
                decision_data = eligibility_data['decision']
                aggregated_result['final_decision'] = {
                    'decision': decision_data['prediction'],
                    'confidence': decision_data['confidence'],
                    'explanation': self._generate_decision_explanation(decision_data),
                    'recommendations': self._generate_recommendations(decision_data)
                }
        
        return aggregated_result
    
    def _generate_decision_explanation(self, decision_data: Dict[str, Any]) -> str:
        """Generate human-readable explanation of the decision"""
        prediction = decision_data.get('prediction', 'unknown')
        confidence = decision_data.get('confidence', 0.0)
        shap_values = decision_data.get('shap_values', {})
        
        explanation = f"Based on the analysis, the application has been {prediction} "
        explanation += f"with {confidence:.1%} confidence. "
        
        if shap_values:
            # Get top 3 contributing factors
            sorted_factors = sorted(shap_values.items(), key=lambda x: x[1], reverse=True)[:3]
            explanation += "The top contributing factors are: "
            factor_descriptions = []
            
            for factor, importance in sorted_factors:
                factor_desc = self._describe_factor(factor)
                factor_descriptions.append(f"{factor_desc} ({importance:.1%})")
            
            explanation += ", ".join(factor_descriptions) + "."
        
        return explanation
    
    def _describe_factor(self, factor: str) -> str:
        """Convert factor name to human-readable description"""
        factor_descriptions = {
            'monthly_income': 'monthly income level',
            'employment_length_months': 'employment stability',
            'family_size': 'family size',
            'dependents': 'number of dependents',
            'income_stability': 'income stability',
            'employment_stability': 'employment stability',
            'debt_to_income_ratio': 'debt-to-income ratio',
            'credit_score': 'credit score',
            'monthly_balance_consistency': 'financial consistency'
        }
        
        return factor_descriptions.get(factor, factor.replace('_', ' '))
    
    def _generate_recommendations(self, decision_data: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on the decision"""
        prediction = decision_data.get('prediction', 'unknown')
        recommendations = []
        
        if prediction == 'soft_decline':
            recommendations = [
                "Consider improving credit score through timely bill payments",
                "Reduce existing debt to improve debt-to-income ratio",
                "Provide additional employment verification documents",
                "Consider applying for smaller loan amounts initially"
            ]
        elif prediction == 'hard_decline':
            recommendations = [
                "Focus on building credit history",
                "Improve employment stability",
                "Reduce monthly expenses",
                "Consider financial counseling services"
            ]
        elif prediction == 'approve':
            recommendations = [
                "Maintain current financial practices",
                "Continue building positive credit history",
                "Consider setting up automatic payments"
            ]
        
        return recommendations
    
    def _calculate_workflow_confidence(self, workflow_state: Dict[str, Any]) -> float:
        """Calculate overall confidence for the workflow"""
        if not workflow_state['results']:
            return 0.0
        
        # Calculate confidence based on completed steps
        total_confidence = 0.0
        step_count = 0
        
        for step_name, result in workflow_state['results'].items():
            if 'confidence' in result:
                total_confidence += result['confidence']
                step_count += 1
        
        if step_count == 0:
            return 0.0
        
        # Reduce confidence for errors
        error_penalty = min(len(workflow_state['errors']) * 0.1, 0.3)
        
        avg_confidence = total_confidence / step_count
        final_confidence = avg_confidence - error_penalty
        
        return max(0.0, min(1.0, final_confidence))
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific workflow (for monitoring)"""
        # This would typically query a database or cache
        # For now, return None as this is a simplified implementation
        return None
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a running workflow"""
        # This would implement workflow cancellation logic
        # For now, return False as this is a simplified implementation
        return False 