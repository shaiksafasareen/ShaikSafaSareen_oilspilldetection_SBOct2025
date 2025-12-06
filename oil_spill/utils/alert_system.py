"""
Alert system for oil spill detections
"""
from typing import Dict, List
from datetime import datetime

class AlertSystem:
    """Alert system for managing detection alerts"""
    
    def __init__(self):
        self.alerts = []
        self.alert_thresholds = {
            "critical": 10,  # Number of detections
            "high": 5,
            "medium": 2,
            "low": 1
        }
    
    def check_detection(self, stats: Dict) -> Dict:
        """
        Check if detection requires an alert
        
        Args:
            stats: Detection statistics dictionary
            
        Returns:
            Alert dictionary with severity and message
        """
        detections = stats.get("total_detections", 0)
        avg_confidence = stats.get("avg_confidence", 0)
        coverage = stats.get("coverage_percentage", 0)
        
        # Determine severity
        severity = "info"
        if detections >= self.alert_thresholds["critical"]:
            severity = "critical"
        elif detections >= self.alert_thresholds["high"]:
            severity = "high"
        elif detections >= self.alert_thresholds["medium"]:
            severity = "medium"
        elif detections >= self.alert_thresholds["low"]:
            severity = "low"
        
        # Create alert message
        message = self._generate_message(detections, avg_confidence, coverage, severity)
        
        alert = {
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "message": message,
            "detections": detections,
            "confidence": avg_confidence,
            "coverage": coverage
        }
        
        self.alerts.append(alert)
        return alert
    
    def _generate_message(self, detections: int, confidence: float, 
                         coverage: float, severity: str) -> str:
        """Generate alert message based on detection parameters"""
        if severity == "critical":
            return f"🚨 CRITICAL: {detections} oil spills detected! Immediate action required. Coverage: {coverage:.2f}%"
        elif severity == "high":
            return f"⚠️ HIGH ALERT: {detections} oil spills detected. Coverage: {coverage:.2f}%"
        elif severity == "medium":
            return f"⚡ MEDIUM: {detections} oil spills detected. Coverage: {coverage:.2f}%"
        elif severity == "low":
            return f"ℹ️ LOW: {detections} oil spill(s) detected. Coverage: {coverage:.2f}%"
        else:
            return f"✅ No significant oil spills detected."
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Get recent alerts"""
        return self.alerts[-limit:] if len(self.alerts) > limit else self.alerts
    
    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts = []
    
    def get_alert_summary(self) -> Dict:
        """Get summary of alerts"""
        if not self.alerts:
            return {"total": 0, "by_severity": {}}
        
        by_severity = {}
        for alert in self.alerts:
            severity = alert["severity"]
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        return {
            "total": len(self.alerts),
            "by_severity": by_severity
        }

