from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.models.pydantic_models import ProcessingResult
import logging
import random

logger = logging.getLogger(__name__)

class RecommenderAgent(BaseAgent):
    """Agent responsible for suggesting economic enablement options"""
    
    def __init__(self):
        super().__init__()
        self.recommendation_templates = {
            'soft_decline': {
                'credit_improvement': [
                    "Apply for a secured credit card to build credit history",
                    "Set up automatic bill payments to improve payment history",
                    "Request credit limit increases on existing cards",
                    "Monitor credit report regularly for errors"
                ],
                'debt_reduction': [
                    "Create a debt snowball plan to pay off debts systematically",
                    "Negotiate with creditors for lower interest rates",
                    "Consider debt consolidation loans",
                    "Set up automatic debt payments"
                ],
                'employment': [
                    "Obtain additional employment certifications",
                    "Seek career advancement opportunities",
                    "Consider part-time work to supplement income",
                    "Build emergency savings fund"
                ],
                'financial_education': [
                    "Attend financial literacy workshops",
                    "Work with a financial advisor",
                    "Use budgeting apps to track expenses",
                    "Learn about investment strategies"
                ]
            },
            'hard_decline': {
                'immediate_actions': [
                    "Focus on building emergency savings",
                    "Improve credit score through responsible credit use",
                    "Reduce monthly expenses and create budget",
                    "Seek financial counseling services"
                ],
                'long_term_goals': [
                    "Develop multiple income streams",
                    "Build professional network for career opportunities",
                    "Consider vocational training programs",
                    "Establish long-term financial planning"
                ]
            }
        }
        
    def get_capabilities(self) -> List[str]:
        return [
            "economic_recommendations",
            "personalized_suggestions",
            "resource_linking",
            "progress_tracking",
            "motivational_support"
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> ProcessingResult:
        """Generate personalized recommendations based on application data"""
        try:
            if not self.validate_input(input_data):
                return self.create_error_result("Invalid input data")
            
            # Extract decision information
            decision_data = input_data.get('eligibility_result', {}).get('decision', {})
            decision = decision_data.get('prediction', 'unknown')
            confidence = decision_data.get('confidence', 0.0)
            
            # Extract application context
            application_data = input_data.get('application_data', {})
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(
                decision, confidence, application_data
            )
            
            # Calculate recommendation confidence
            recommendation_confidence = self._calculate_recommendation_confidence(
                decision, confidence, application_data
            )
            
            self.log_action("recommendations_generated", {
                "decision": decision,
                "recommendations_count": len(recommendations),
                "confidence": recommendation_confidence
            })
            
            return self.create_success_result({
                'recommendations': recommendations,
                'decision_context': decision,
                'personalization_factors': self._identify_personalization_factors(application_data),
                'next_steps': self._suggest_next_steps(decision, recommendations)
            }, recommendation_confidence)
            
        except Exception as e:
            logger.error(f"Recommender agent error: {e}")
            return self.create_error_result(f"Recommendation generation failed: {str(e)}")
    
    async def _generate_recommendations(self, decision: str, confidence: float, 
                                      application_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized recommendations"""
        recommendations = []
        
        if decision == 'soft_decline':
            recommendations.extend(self._generate_soft_decline_recommendations(application_data))
        elif decision == 'hard_decline':
            recommendations.extend(self._generate_hard_decline_recommendations(application_data))
        elif decision == 'approve':
            recommendations.extend(self._generate_approval_recommendations(application_data))
        
        # Add general financial wellness recommendations
        recommendations.extend(self._generate_general_recommendations(application_data))
        
        # Personalize recommendations based on application data
        personalized_recommendations = self._personalize_recommendations(
            recommendations, application_data
        )
        
        return personalized_recommendations
    
    def _generate_soft_decline_recommendations(self, application_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations for soft decline cases"""
        recommendations = []
        
        # Credit improvement recommendations
        if self._should_recommend_credit_improvement(application_data):
            for rec in self.recommendation_templates['soft_decline']['credit_improvement']:
                recommendations.append({
                    'category': 'credit_improvement',
                    'recommendation': rec,
                    'priority': 'high',
                    'estimated_impact': 'medium',
                    'time_to_implement': '1-3 months'
                })
        
        # Debt reduction recommendations
        if self._should_recommend_debt_reduction(application_data):
            for rec in self.recommendation_templates['soft_decline']['debt_reduction']:
                recommendations.append({
                    'category': 'debt_reduction',
                    'recommendation': rec,
                    'priority': 'high',
                    'estimated_impact': 'high',
                    'time_to_implement': '3-6 months'
                })
        
        # Employment recommendations
        if self._should_recommend_employment_improvement(application_data):
            for rec in self.recommendation_templates['soft_decline']['employment']:
                recommendations.append({
                    'category': 'employment',
                    'recommendation': rec,
                    'priority': 'medium',
                    'estimated_impact': 'medium',
                    'time_to_implement': '6-12 months'
                })
        
        # Financial education
        for rec in self.recommendation_templates['soft_decline']['financial_education']:
            recommendations.append({
                'category': 'financial_education',
                'recommendation': rec,
                'priority': 'medium',
                'estimated_impact': 'long_term',
                'time_to_implement': 'ongoing'
            })
        
        return recommendations
    
    def _generate_hard_decline_recommendations(self, application_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations for hard decline cases"""
        recommendations = []
        
        # Immediate actions
        for rec in self.recommendation_templates['hard_decline']['immediate_actions']:
            recommendations.append({
                'category': 'immediate_actions',
                'recommendation': rec,
                'priority': 'critical',
                'estimated_impact': 'high',
                'time_to_implement': '1-2 months'
            })
        
        # Long-term goals
        for rec in self.recommendation_templates['hard_decline']['long_term_goals']:
            recommendations.append({
                'category': 'long_term_goals',
                'recommendation': rec,
                'priority': 'medium',
                'estimated_impact': 'long_term',
                'time_to_implement': '12+ months'
            })
        
        return recommendations
    
    def _generate_approval_recommendations(self, application_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations for approved applications"""
        recommendations = []
        
        recommendations.extend([
            {
                'category': 'financial_management',
                'recommendation': 'Maintain current positive financial practices',
                'priority': 'low',
                'estimated_impact': 'maintenance',
                'time_to_implement': 'ongoing'
            },
            {
                'category': 'credit_building',
                'recommendation': 'Continue building positive credit history',
                'priority': 'low',
                'estimated_impact': 'long_term',
                'time_to_implement': 'ongoing'
            },
            {
                'category': 'savings',
                'recommendation': 'Consider increasing emergency savings',
                'priority': 'medium',
                'estimated_impact': 'medium',
                'time_to_implement': '3-6 months'
            }
        ])
        
        return recommendations
    
    def _generate_general_recommendations(self, application_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate general financial wellness recommendations"""
        general_recommendations = [
            {
                'category': 'general_wellness',
                'recommendation': 'Create and maintain a monthly budget',
                'priority': 'medium',
                'estimated_impact': 'medium',
                'time_to_implement': '1 month'
            },
            {
                'category': 'general_wellness',
                'recommendation': 'Build an emergency fund covering 3-6 months of expenses',
                'priority': 'medium',
                'estimated_impact': 'high',
                'time_to_implement': '6-12 months'
            },
            {
                'category': 'general_wellness',
                'recommendation': 'Regularly review and update financial goals',
                'priority': 'low',
                'estimated_impact': 'long_term',
                'time_to_implement': 'ongoing'
            }
        ]
        
        return general_recommendations
    
    def _personalize_recommendations(self, recommendations: List[Dict[str, Any]], 
                                   application_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Personalize recommendations based on application data"""
        personalized = []
        
        for rec in recommendations:
            personalized_rec = rec.copy()
            
            # Add personalization based on family size
            family_size = application_data.get('family_size', 1)
            if family_size > 3 and rec['category'] in ['debt_reduction', 'savings']:
                personalized_rec['recommendation'] += f" (especially important for families of {family_size})"
            
            # Add personalization based on employment
            employment_length = application_data.get('employment_length_months', 0)
            if employment_length < 12 and rec['category'] == 'employment':
                personalized_rec['priority'] = 'high'
                personalized_rec['estimated_impact'] = 'high'
            
            # Add personalization based on income
            monthly_income = application_data.get('monthly_income', 0)
            if monthly_income < 2000 and rec['category'] in ['debt_reduction', 'savings']:
                personalized_rec['priority'] = 'high'
            
            personalized.append(personalized_rec)
        
        return personalized
    
    def _should_recommend_credit_improvement(self, application_data: Dict[str, Any]) -> bool:
        """Determine if credit improvement recommendations should be made"""
        # This would typically analyze credit score, payment history, etc.
        # For now, return True for demonstration
        return True
    
    def _should_recommend_debt_reduction(self, application_data: Dict[str, Any]) -> bool:
        """Determine if debt reduction recommendations should be made"""
        monthly_income = application_data.get('monthly_income', 0)
        family_size = application_data.get('family_size', 1)
        
        # Estimate debt burden
        estimated_debt = family_size * 200  # Simplified estimation
        debt_ratio = estimated_debt / monthly_income if monthly_income > 0 else 1.0
        
        return debt_ratio > 0.3
    
    def _should_recommend_employment_improvement(self, application_data: Dict[str, Any]) -> bool:
        """Determine if employment improvement recommendations should be made"""
        employment_length = application_data.get('employment_length_months', 0)
        return employment_length < 24
    
    def _identify_personalization_factors(self, application_data: Dict[str, Any]) -> List[str]:
        """Identify factors used for personalization"""
        factors = []
        
        if 'family_size' in application_data:
            factors.append('family_size')
        if 'employment_length_months' in application_data:
            factors.append('employment_stability')
        if 'monthly_income' in application_data:
            factors.append('income_level')
        
        return factors
    
    def _suggest_next_steps(self, decision: str, recommendations: List[Dict[str, Any]]) -> List[str]:
        """Suggest immediate next steps for the applicant"""
        next_steps = []
        
        if decision == 'soft_decline':
            next_steps = [
                "Review all recommendations and prioritize by impact",
                "Create a timeline for implementing high-priority recommendations",
                "Set up tracking for progress on key improvements",
                "Schedule follow-up review in 3-6 months"
            ]
        elif decision == 'hard_decline':
            next_steps = [
                "Focus on immediate action items first",
                "Seek professional financial counseling",
                "Create a detailed improvement plan",
                "Set up regular progress check-ins"
            ]
        else:
            next_steps = [
                "Continue current positive financial practices",
                "Implement suggested improvements gradually",
                "Monitor progress and adjust as needed"
            ]
        
        return next_steps
    
    def _calculate_recommendation_confidence(self, decision: str, confidence: float, 
                                          application_data: Dict[str, Any]) -> float:
        """Calculate confidence in the recommendations"""
        base_confidence = 0.8
        
        # Adjust based on decision confidence
        if confidence > 0.8:
            base_confidence += 0.1
        elif confidence < 0.6:
            base_confidence -= 0.1
        
        # Adjust based on data completeness
        required_fields = ['monthly_income', 'family_size', 'employment_length_months']
        data_completeness = sum(1 for field in required_fields if field in application_data) / len(required_fields)
        
        base_confidence += (data_completeness - 0.5) * 0.2
        
        return max(0.0, min(1.0, base_confidence)) 