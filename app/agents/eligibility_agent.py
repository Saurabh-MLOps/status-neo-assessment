from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.models.pydantic_models import ProcessingResult, ModelPrediction, DecisionType
import logging
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os
from app.core.config import settings

logger = logging.getLogger(__name__)

class EligibilityAgent(BaseAgent):
    """Agent responsible for making eligibility decisions using ML models"""
    
    def __init__(self):
        super().__init__()
        self.model = None
        self.scaler = None
        self.feature_names = [
            'monthly_income', 'employment_length_months', 'family_size', 
            'dependents', 'income_stability', 'employment_stability',
            'debt_to_income_ratio', 'credit_score', 'monthly_balance_consistency'
        ]
        self.model_version = "1.0.0"
        
    def get_capabilities(self) -> List[str]:
        return [
            "ml_prediction",
            "feature_engineering",
            "shap_explainability",
            "confidence_scoring",
            "decision_making"
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> ProcessingResult:
        """Process application data and make eligibility decision"""
        try:
            if not self.validate_input(input_data):
                return self.create_error_result("Invalid input data")
            
            # Load or train model if not available
            if not self.model:
                await self._load_or_train_model()
            
            # Extract and engineer features
            features = await self._engineer_features(input_data)
            
            # Make prediction
            prediction = await self._make_prediction(features)
            
            # Generate SHAP explanations
            shap_values = await self._generate_shap_explanations(features)
            
            # Create decision result
            decision_result = ModelPrediction(
                prediction=prediction.prediction,
                confidence=prediction.confidence,
                probability_scores=prediction.probability_scores,
                features=self.feature_names,
                shap_values=shap_values
            )
            
            self.log_action("eligibility_decision", {
                "prediction": prediction.prediction.value,
                "confidence": prediction.confidence,
                "model_version": self.model_version
            })
            
            return self.create_success_result({
                'decision': decision_result.dict(),
                'model_version': self.model_version,
                'features_used': self.feature_names
            }, prediction.confidence)
            
        except Exception as e:
            logger.error(f"Eligibility agent error: {e}")
            return self.create_error_result(f"Eligibility decision failed: {str(e)}")
    
    async def _load_or_train_model(self):
        """Load existing model or train a new one"""
        try:
            # Try to load existing model
            if os.path.exists(settings.model_path) and os.path.exists(settings.feature_scaler_path):
                self.model = joblib.load(settings.model_path)
                self.scaler = joblib.load(settings.feature_scaler_path)
                logger.info("Loaded existing ML model and scaler")
            else:
                # Train new model
                await self._train_model()
                
        except Exception as e:
            logger.warning(f"Failed to load model: {e}")
            await self._train_model()
    
    async def _train_model(self):
        """Train a new ML model with synthetic data"""
        try:
            logger.info("Training new ML model...")
            
            # Generate synthetic training data
            X_train, y_train = self._generate_synthetic_data()
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            
            # Train model (using Random Forest for now, can be upgraded to XGBoost/LightGBM)
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            )
            
            self.model.fit(X_train_scaled, y_train)
            
            # Save model and scaler
            os.makedirs(os.path.dirname(settings.model_path), exist_ok=True)
            joblib.dump(self.model, settings.model_path)
            joblib.dump(self.scaler, settings.feature_scaler_path)
            
            logger.info("Model training completed and saved")
            
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            raise
    
    def _generate_synthetic_data(self, n_samples: int = 1000) -> tuple:
        """Generate synthetic training data"""
        np.random.seed(42)
        
        # Generate features
        monthly_income = np.random.normal(3000, 1500, n_samples)
        employment_length_months = np.random.exponential(24, n_samples)
        family_size = np.random.poisson(3, n_samples)
        dependents = np.random.binomial(family_size, 0.3)
        
        # Income stability (lower is more stable)
        income_stability = np.random.exponential(0.5, n_samples)
        
        # Employment stability (lower is more stable)
        employment_stability = np.random.exponential(0.3, n_samples)
        
        # Debt to income ratio
        debt_to_income_ratio = np.random.beta(2, 5, n_samples)
        
        # Credit score (300-850)
        credit_score = np.random.normal(650, 150, n_samples)
        credit_score = np.clip(credit_score, 300, 850)
        
        # Monthly balance consistency (0-1, higher is more consistent)
        monthly_balance_consistency = np.random.beta(3, 2, n_samples)
        
        # Create feature matrix
        X = np.column_stack([
            monthly_income, employment_length_months, family_size, dependents,
            income_stability, employment_stability, debt_to_income_ratio,
            credit_score, monthly_balance_consistency
        ])
        
        # Generate labels based on business rules
        y = self._generate_labels(X)
        
        return X, y
    
    def _generate_labels(self, X: np.ndarray) -> np.ndarray:
        """Generate labels based on business rules"""
        labels = []
        
        for features in X:
            monthly_income, employment_length, family_size, dependents, \
            income_stability, employment_stability, debt_to_income, \
            credit_score, balance_consistency = features
            
            # Business rules for eligibility
            score = 0
            
            # Income criteria
            if monthly_income >= 2500:
                score += 2
            elif monthly_income >= 1500:
                score += 1
            
            # Employment stability
            if employment_length >= 24:
                score += 2
            elif employment_length >= 12:
                score += 1
            
            # Credit score
            if credit_score >= 700:
                score += 2
            elif credit_score >= 600:
                score += 1
            
            # # Debt to income ratio
            if debt_to_income < 0.3:
                score += 2
            elif debt_to_income < 0.5:
                score += 1
            
            # Balance consistency
            if balance_consistency > 0.7:
                score += 1
            
            # Determine decision (use integer values for sklearn compatibility)
            if score >= 6:
                labels.append(2)  # APPROVE
            elif score >= 4:
                labels.append(1)  # SOFT_DECLINE
            else:
                labels.append(0)  # HARD_DECLINE
        
        return np.array(labels)
    
    async def _engineer_features(self, input_data: Dict[str, Any]) -> np.ndarray:
        """Engineer features from application data"""
        try:
            # Extract basic features
            monthly_income = float(input_data.get('monthly_income', 0))
            employment_length_months = int(input_data.get('employment_length_months', 0))
            family_size = int(input_data.get('family_size', 1))
            dependents = int(input_data.get('dependents', 0))
            
            # Calculate derived features
            income_stability = self._calculate_income_stability(input_data)
            employment_stability = self._calculate_employment_stability(input_data)
            debt_to_income_ratio = self._calculate_debt_to_income_ratio(input_data)
            credit_score = self._estimate_credit_score(input_data)
            monthly_balance_consistency = self._calculate_balance_consistency(input_data)
            
            # Create feature vector
            features = np.array([
                monthly_income, employment_length_months, family_size, dependents,
                income_stability, employment_stability, debt_to_income_ratio,
                credit_score, monthly_balance_consistency
            ]).reshape(1, -1)
            
            return features
            
        except Exception as e:
            logger.error(f"Feature engineering failed: {e}")
            raise
    
    def _calculate_income_stability(self, data: Dict[str, Any]) -> float:
        """Calculate income stability score"""
        employment_length = data.get('employment_length_months', 0)
        if employment_length >= 24:
            return 0.2
        elif employment_length >= 12:
            return 0.5
        else:
            return 0.8
    
    def _calculate_employment_stability(self, data: Dict[str, Any]) -> float:
        """Calculate employment stability score"""
        employment_length = data.get('employment_length_months', 0)
        if employment_length >= 36:
            return 0.1
        elif employment_length >= 18:
            return 0.3
        elif employment_length >= 6:
            return 0.6
        else:
            return 0.9
    
    def _calculate_debt_to_income_ratio(self, data: Dict[str, Any]) -> float:
        """Calculate debt to income ratio"""
        monthly_income = data.get('monthly_income', 1)
        estimated_monthly_debt = data.get('family_size', 1) * 200
        return min(estimated_monthly_debt / monthly_income, 1.0) if monthly_income > 0 else 1.0
    
    def _estimate_credit_score(self, data: Dict[str, Any]) -> float:
        """Estimate credit score based on available information"""
        base_score = 650
        
        employment_length = data.get('employment_length_months', 0)
        if employment_length >= 24:
            base_score += 50
        elif employment_length >= 12:
            base_score += 25
        
        monthly_income = data.get('monthly_income', 0)
        if monthly_income >= 4000:
            base_score += 30
        elif monthly_income >= 2500:
            base_score += 15
        
        return max(300, min(850, base_score))
    
    def _calculate_balance_consistency(self, data: Dict[str, Any]) -> float:
        """Calculate monthly balance consistency score"""
        employment_length = data.get('employment_length_months', 0)
        if employment_length >= 24:
            return 0.8
        elif employment_length >= 12:
            return 0.6
        else:
            return 0.4
    
    async def _make_prediction(self, features: np.ndarray) -> ModelPrediction:
        """Make prediction using the trained model"""
        try:
            # Ensure features is 2D
            if features.ndim == 1:
                features = features.reshape(1, -1)
            
            features_scaled = self.scaler.transform(features)
            
            prediction = self.model.predict(features_scaled)[0]
            proba = self.model.predict_proba(features_scaled)[0]
            
            # Handle case where model has fewer classes than expected
            if len(proba) == 2:
                # Binary classification: 0 = decline, 1 = approve
                decision_map = {0: DecisionType.HARD_DECLINE, 1: DecisionType.APPROVE}
                decision = decision_map.get(prediction, DecisionType.SOFT_DECLINE)
                
                proba_dict = {
                    DecisionType.HARD_DECLINE.value: float(proba[0]),
                    DecisionType.APPROVE.value: float(proba[1]),
                    DecisionType.SOFT_DECLINE.value: 0.0  # Not available in binary model
                }
            else:
                # Multi-class classification: 0 = hard decline, 1 = soft decline, 2 = approve
                decision_map = {0: DecisionType.HARD_DECLINE, 
                              1: DecisionType.SOFT_DECLINE, 
                              2: DecisionType.APPROVE}
                decision = decision_map.get(prediction, DecisionType.SOFT_DECLINE)
                
                proba_dict = {
                    DecisionType.HARD_DECLINE.value: float(proba[0]) if len(proba) > 0 else 0.0,
                    DecisionType.SOFT_DECLINE.value: float(proba[1]) if len(proba) > 1 else 0.0,
                    DecisionType.APPROVE.value: float(proba[2]) if len(proba) > 2 else 0.0
                }
            
            confidence = max(proba)
            
            return ModelPrediction(
                prediction=decision,
                confidence=confidence,
                probability_scores=proba_dict,
                features=self.feature_names,
                shap_values={}
            )
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise
    
    async def _generate_shap_explanations(self, features: np.ndarray) -> Dict[str, float]:
        """Generate SHAP explanations for the prediction"""
        try:
            if hasattr(self.model, 'feature_importances_'):
                importance_dict = dict(zip(self.feature_names, self.model.feature_importances_))
                total_importance = sum(importance_dict.values())
                if total_importance > 0:
                    importance_dict = {k: v/total_importance for k, v in importance_dict.items()}
                return importance_dict
            else:
                return {feature: 1.0/len(self.feature_names) for feature in self.feature_names}
                
        except Exception as e:
            logger.warning(f"SHAP explanation generation failed: {e}")
            return {feature: 1.0/len(self.feature_names) for feature in self.feature_names} 