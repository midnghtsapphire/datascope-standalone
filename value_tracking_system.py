#!/usr/bin/env python3
"""
DataScope Enhanced - Value Tracking & Affiliate Integration System
Measures cost savings, environmental impact, and ROI while promoting affiliate products
"""

import json
import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
import sqlite3
import requests
from geopy.geocoders import Nominatim
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SavingsMetric:
    """Track various types of savings and their calculations"""
    category: str
    description: str
    amount_saved: float
    currency: str = "USD"
    time_period: str = "monthly"
    calculation_method: str = ""
    confidence_level: float = 0.85

@dataclass
class EnvironmentalImpact:
    """Track environmental benefits and green savings"""
    metric_type: str  # co2_reduced, o2_generated, waste_diverted, etc.
    amount: float
    unit: str  # kg, tons, liters, etc.
    description: str
    calculation_basis: str
    equivalent_description: str  # "Equal to planting 5 trees"

@dataclass
class AffiliateProduct:
    """Affiliate product recommendations based on user needs"""
    product_id: str
    name: str
    category: str
    description: str
    price: float
    affiliate_url: str
    commission_rate: float
    relevance_score: float
    location_specific: bool = False
    target_regions: List[str] = None

class ValueTrackingSystem:
    """Comprehensive system for tracking value, savings, and environmental impact"""
    
    def __init__(self, db_path: str = "value_tracking.db"):
        self.db_path = db_path
        self.geolocator = Nominatim(user_agent="datascope-enhanced")
        self.init_database()
        self.load_affiliate_products()
        
    def init_database(self):
        """Initialize SQLite database for tracking metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Savings tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                category TEXT,
                description TEXT,
                amount_saved REAL,
                currency TEXT DEFAULT 'USD',
                time_period TEXT,
                calculation_method TEXT,
                confidence_level REAL,
                domain TEXT,
                location TEXT
            )
        ''')
        
        # Environmental impact table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS environmental_impact (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                metric_type TEXT,
                amount REAL,
                unit TEXT,
                description TEXT,
                calculation_basis TEXT,
                equivalent_description TEXT,
                domain TEXT,
                location TEXT
            )
        ''')
        
        # Affiliate tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS affiliate_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                product_id TEXT,
                action TEXT,  -- view, click, purchase
                location TEXT,
                savings_context TEXT,
                commission_earned REAL DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def load_affiliate_products(self):
        """Load affiliate product catalog (your coffee and wellness products)"""
        self.affiliate_products = {
            # Qahwa Mythical Coffee Line
            "qahwa_falak_focus": AffiliateProduct(
                product_id="qahwa_falak_focus",
                name="Falak Focus Blend - Lion's Mane Coffee",
                category="functional_coffee",
                description="Bold Arabic dark roast + Lion's Mane mushroom for focus and memory",
                price=24.99,
                affiliate_url="https://qahwacoffeebeans.com/falak-focus?ref=datascope",
                commission_rate=0.30,  # 30% commission
                relevance_score=0.95,
                location_specific=False
            ),
            
            "qahwa_miraj_mind": AffiliateProduct(
                product_id="qahwa_miraj_mind",
                name="Mi'raj Mind Roast - Cordyceps Energy",
                category="functional_coffee",
                description="Light roast + Cordyceps mushroom for natural stamina and clarity",
                price=26.99,
                affiliate_url="https://qahwacoffeebeans.com/miraj-mind?ref=datascope",
                commission_rate=0.30,
                relevance_score=0.90,
                location_specific=False
            ),
            
            "qahwa_anqa_immune": AffiliateProduct(
                product_id="qahwa_anqa_immune",
                name="Anqa Immune Shield - Reishi Coffee",
                category="functional_coffee",
                description="Medium roast + Reishi & Turkey Tail for immune support",
                price=28.99,
                affiliate_url="https://qahwacoffeebeans.com/anqa-immune?ref=datascope",
                commission_rate=0.30,
                relevance_score=0.88,
                location_specific=False
            ),
            
            # Organic/Sustainable Products
            "organic_packaging_kit": AffiliateProduct(
                product_id="organic_packaging_kit",
                name="Eco-Friendly Office Packaging Kit",
                category="sustainable_office",
                description="Biodegradable packaging materials for small businesses",
                price=89.99,
                affiliate_url="https://qahwacoffeebeans.com/eco-packaging?ref=datascope",
                commission_rate=0.25,
                relevance_score=0.75,
                location_specific=True,
                target_regions=["US", "CA", "EU"]
            ),
            
            # Cybersecurity Tools
            "security_audit_service": AffiliateProduct(
                product_id="security_audit_service",
                name="Small Business Security Audit",
                category="cybersecurity",
                description="Professional cybersecurity assessment for small businesses",
                price=299.99,
                affiliate_url="https://qahwacoffeebeans.com/security-audit?ref=datascope",
                commission_rate=0.20,
                relevance_score=0.85,
                location_specific=True,
                target_regions=["US", "CA", "UK", "AU"]
            )
        }
    
    def calculate_cybersecurity_savings(self, threats_prevented: int, 
                                      avg_breach_cost: float = 4.45e6) -> SavingsMetric:
        """Calculate savings from prevented cybersecurity incidents"""
        # Conservative estimate: each threat prevented saves 0.1% of average breach cost
        estimated_savings = threats_prevented * (avg_breach_cost * 0.001)
        
        return SavingsMetric(
            category="cybersecurity",
            description=f"Estimated savings from preventing {threats_prevented} potential security incidents",
            amount_saved=estimated_savings,
            time_period="annual",
            calculation_method=f"Conservative estimate: {threats_prevented} threats × $4,450 avg prevention value",
            confidence_level=0.75
        )
    
    def calculate_time_savings(self, hours_saved: float, hourly_rate: float = 75) -> SavingsMetric:
        """Calculate monetary value of time saved through automation"""
        monetary_value = hours_saved * hourly_rate
        
        return SavingsMetric(
            category="time_efficiency",
            description=f"Time saved through automated data collection and analysis",
            amount_saved=monetary_value,
            time_period="monthly",
            calculation_method=f"{hours_saved} hours × ${hourly_rate}/hour professional rate",
            confidence_level=0.90
        )
    
    def calculate_research_cost_savings(self, reports_generated: int,
                                      avg_research_cost: float = 2500) -> SavingsMetric:
        """Calculate savings from automated research vs hiring analysts"""
        total_savings = reports_generated * avg_research_cost
        
        return SavingsMetric(
            category="research_automation",
            description=f"Cost savings vs hiring analysts for {reports_generated} research reports",
            amount_saved=total_savings,
            time_period="monthly",
            calculation_method=f"{reports_generated} reports × ${avg_research_cost} avg analyst cost",
            confidence_level=0.85
        )
    
    def calculate_environmental_impact(self, digital_reports: int,
                                     paper_saved_per_report: float = 50) -> List[EnvironmentalImpact]:
        """Calculate environmental benefits from digital-first approach"""
        impacts = []
        
        # Paper savings
        total_paper_saved = digital_reports * paper_saved_per_report  # sheets
        paper_weight_kg = total_paper_saved * 0.005  # 5g per sheet
        
        impacts.append(EnvironmentalImpact(
            metric_type="paper_saved",
            amount=paper_weight_kg,
            unit="kg",
            description=f"Paper saved through digital reports",
            calculation_basis=f"{digital_reports} reports × {paper_saved_per_report} sheets × 5g/sheet",
            equivalent_description=f"Equivalent to saving {int(paper_weight_kg/0.5)} magazines"
        ))
        
        # CO2 reduction from paper savings
        co2_saved = paper_weight_kg * 1.8  # 1.8kg CO2 per kg of paper
        impacts.append(EnvironmentalImpact(
            metric_type="co2_reduced",
            amount=co2_saved,
            unit="kg",
            description="CO2 emissions prevented through digital-first approach",
            calculation_basis=f"{paper_weight_kg}kg paper × 1.8kg CO2/kg paper",
            equivalent_description=f"Equal to {int(co2_saved/21.77)} trees planted"
        ))
        
        # Water savings
        water_saved = paper_weight_kg * 20  # 20L water per kg paper
        impacts.append(EnvironmentalImpact(
            metric_type="water_saved",
            amount=water_saved,
            unit="liters",
            description="Water saved in paper production",
            calculation_basis=f"{paper_weight_kg}kg paper × 20L/kg",
            equivalent_description=f"Equal to {int(water_saved/8)} days of drinking water"
        ))
        
        return impacts
    
    def calculate_organic_packaging_impact(self, packages_used: int) -> List[EnvironmentalImpact]:
        """Calculate environmental benefits from using organic packaging"""
        impacts = []
        
        # Plastic waste diverted
        plastic_diverted = packages_used * 0.05  # 50g plastic per package
        impacts.append(EnvironmentalImpact(
            metric_type="plastic_diverted",
            amount=plastic_diverted,
            unit="kg",
            description="Plastic waste diverted through biodegradable packaging",
            calculation_basis=f"{packages_used} packages × 50g plastic/package",
            equivalent_description=f"Equal to {int(plastic_diverted*20)} plastic bottles diverted"
        ))
        
        # Microplastic reduction
        microplastic_prevented = plastic_diverted * 0.1  # 10% becomes microplastic
        impacts.append(EnvironmentalImpact(
            metric_type="microplastic_prevented",
            amount=microplastic_prevented,
            unit="kg",
            description="Microplastic pollution prevented",
            calculation_basis=f"{plastic_diverted}kg plastic × 10% microplastic rate",
            equivalent_description=f"Protecting marine ecosystems from {int(microplastic_prevented*1000)}g microplastics"
        ))
        
        return impacts
    
    def get_location_based_recommendations(self, user_location: str) -> List[AffiliateProduct]:
        """Get affiliate product recommendations based on user location"""
        try:
            location = self.geolocator.geocode(user_location)
            if not location:
                return []
            
            # Determine region
            country_code = self.get_country_code(location.address)
            
            recommendations = []
            for product in self.affiliate_products.values():
                if not product.location_specific:
                    recommendations.append(product)
                elif product.target_regions and country_code in product.target_regions:
                    recommendations.append(product)
            
            # Sort by relevance score
            recommendations.sort(key=lambda x: x.relevance_score, reverse=True)
            return recommendations[:5]  # Top 5 recommendations
            
        except Exception as e:
            logger.error(f"Error getting location recommendations: {e}")
            return list(self.affiliate_products.values())[:3]  # Fallback to top 3
    
    def get_country_code(self, address: str) -> str:
        """Extract country code from geocoded address"""
        # Simple mapping - in production, use a proper geocoding service
        if "United States" in address or "USA" in address:
            return "US"
        elif "Canada" in address:
            return "CA"
        elif "United Kingdom" in address or "UK" in address:
            return "UK"
        elif "Australia" in address:
            return "AU"
        else:
            return "US"  # Default
    
    def generate_savings_report(self, user_id: str, domain: str, 
                              time_period: str = "monthly") -> Dict:
        """Generate comprehensive savings and impact report"""
        
        # Mock data for demonstration - in production, pull from actual usage
        mock_usage = {
            "threats_analyzed": 1417,
            "reports_generated": 12,
            "hours_saved": 45,
            "digital_reports": 12,
            "organic_packages": 25
        }
        
        # Calculate savings
        cyber_savings = self.calculate_cybersecurity_savings(mock_usage["threats_analyzed"])
        time_savings = self.calculate_time_savings(mock_usage["hours_saved"])
        research_savings = self.calculate_research_cost_savings(mock_usage["reports_generated"])
        
        total_savings = cyber_savings.amount_saved + time_savings.amount_saved + research_savings.amount_saved
        
        # Calculate environmental impact
        digital_impacts = self.calculate_environmental_impact(mock_usage["digital_reports"])
        packaging_impacts = self.calculate_organic_packaging_impact(mock_usage["organic_packages"])
        
        # Get product recommendations
        recommendations = self.get_location_based_recommendations("New York, NY")
        
        # Calculate potential affiliate revenue
        potential_revenue = sum(p.price * p.commission_rate for p in recommendations)
        
        report = {
            "user_id": user_id,
            "domain": domain,
            "time_period": time_period,
            "generated_at": datetime.datetime.now().isoformat(),
            
            "financial_savings": {
                "total_saved": total_savings,
                "currency": "USD",
                "breakdown": [
                    asdict(cyber_savings),
                    asdict(time_savings),
                    asdict(research_savings)
                ]
            },
            
            "environmental_impact": {
                "digital_benefits": [asdict(impact) for impact in digital_impacts],
                "packaging_benefits": [asdict(impact) for impact in packaging_impacts],
                "total_co2_saved": sum(i.amount for i in digital_impacts + packaging_impacts if i.metric_type == "co2_reduced"),
                "total_waste_diverted": sum(i.amount for i in digital_impacts + packaging_impacts if "diverted" in i.metric_type or "saved" in i.metric_type)
            },
            
            "roi_analysis": {
                "platform_cost": 99.0,  # Monthly platform cost
                "total_value_delivered": total_savings,
                "roi_percentage": ((total_savings - 99.0) / 99.0) * 100,
                "payback_period_days": (99.0 / total_savings) * 30 if total_savings > 0 else 999
            },
            
            "affiliate_recommendations": [asdict(product) for product in recommendations],
            "potential_affiliate_revenue": potential_revenue,
            
            "usage_metrics": mock_usage,
            
            "green_score": self.calculate_green_score(digital_impacts + packaging_impacts),
            
            "next_steps": self.generate_next_steps(total_savings, recommendations)
        }
        
        # Store in database
        self.store_report(report)
        
        return report
    
    def calculate_green_score(self, impacts: List[EnvironmentalImpact]) -> Dict:
        """Calculate overall green impact score"""
        co2_saved = sum(i.amount for i in impacts if i.metric_type == "co2_reduced")
        waste_diverted = sum(i.amount for i in impacts if "diverted" in i.metric_type or "saved" in i.metric_type)
        
        # Normalize to 0-100 scale
        co2_score = min(co2_saved * 10, 100)  # 10kg CO2 = 100 points
        waste_score = min(waste_diverted * 5, 100)  # 20kg waste = 100 points
        
        overall_score = (co2_score + waste_score) / 2
        
        return {
            "overall_score": round(overall_score, 1),
            "co2_score": round(co2_score, 1),
            "waste_score": round(waste_score, 1),
            "rating": self.get_green_rating(overall_score),
            "trees_equivalent": round(co2_saved / 21.77, 1)  # 21.77kg CO2 per tree per year
        }
    
    def get_green_rating(self, score: float) -> str:
        """Convert green score to rating"""
        if score >= 80:
            return "Eco Champion 🌟"
        elif score >= 60:
            return "Green Leader 🌱"
        elif score >= 40:
            return "Eco Conscious 🌿"
        elif score >= 20:
            return "Getting Greener 🌾"
        else:
            return "Starting Journey 🌱"
    
    def generate_next_steps(self, total_savings: float, 
                          recommendations: List[AffiliateProduct]) -> List[str]:
        """Generate actionable next steps for users"""
        steps = []
        
        if total_savings > 1000:
            steps.append("🎉 Excellent! You're saving over $1,000/month. Consider upgrading to our Enterprise plan for even more features.")
        
        steps.append("☕ Boost your productivity with our Falak Focus Blend - Lion's Mane coffee for enhanced concentration during data analysis.")
        
        if len(recommendations) > 0:
            top_product = recommendations[0]
            steps.append(f"🛍️ Recommended: {top_product.name} - Perfect for your current needs and location.")
        
        steps.append("📊 Share your green impact on social media to inspire others!")
        steps.append("🔄 Set up automated monthly reports to track your continued savings.")
        
        return steps
    
    def store_report(self, report: Dict):
        """Store report data in database for historical tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Store main metrics
        for saving in report["financial_savings"]["breakdown"]:
            cursor.execute('''
                INSERT INTO savings_metrics 
                (user_id, category, description, amount_saved, currency, time_period, 
                 calculation_method, confidence_level, domain)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                report["user_id"], saving["category"], saving["description"],
                saving["amount_saved"], saving["currency"], saving["time_period"],
                saving["calculation_method"], saving["confidence_level"], report["domain"]
            ))
        
        conn.commit()
        conn.close()
    
    def track_affiliate_interaction(self, user_id: str, product_id: str, 
                                  action: str, location: str = None):
        """Track affiliate product interactions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO affiliate_interactions 
            (user_id, product_id, action, location)
            VALUES (?, ?, ?, ?)
        ''', (user_id, product_id, action, location))
        
        conn.commit()
        conn.close()

def main():
    """Demo the value tracking system"""
    vts = ValueTrackingSystem()
    
    # Generate sample report
    report = vts.generate_savings_report(
        user_id="demo_user_001",
        domain="cybersecurity",
        time_period="monthly"
    )
    
    print("=== DataScope Enhanced - Value Tracking Report ===")
    print(f"Total Monthly Savings: ${report['financial_savings']['total_saved']:,.2f}")
    print(f"ROI: {report['roi_analysis']['roi_percentage']:.1f}%")
    print(f"Green Score: {report['green_score']['overall_score']}/100 ({report['green_score']['rating']})")
    print(f"CO2 Saved: {report['environmental_impact']['total_co2_saved']:.1f} kg")
    print(f"Trees Equivalent: {report['green_score']['trees_equivalent']} trees")
    
    print("\n=== Recommended Products ===")
    for product in report['affiliate_recommendations'][:3]:
        print(f"• {product['name']} - ${product['price']} (Commission: {product['commission_rate']*100}%)")
    
    print(f"\nPotential Affiliate Revenue: ${report['potential_affiliate_revenue']:.2f}")
    
    return report

if __name__ == "__main__":
    main()

