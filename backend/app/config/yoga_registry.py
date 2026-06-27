"""
Yoga Registry Configuration.
Maps classical yogas to their primary houses and domains.
"""

YOGA_REGISTRY = {
    "Gaja Kesari Yoga": {"houses": ["universal"], "category": "universal"},
    "Neecha Bhanga Raja Yoga": {"houses": ["universal"], "category": "universal"},
    "Adhi Yoga": {"houses": ["universal"], "category": "universal"},
    
    "Ruchaka Yoga": {"houses": ["universal"], "category": "pancha_mahapurusha"},
    "Bhadra Yoga": {"houses": ["universal"], "category": "pancha_mahapurusha"},
    "Hamsa Yoga": {"houses": ["universal"], "category": "pancha_mahapurusha"},
    "Malavya Yoga": {"houses": ["universal"], "category": "pancha_mahapurusha"},
    "Sasa Yoga": {"houses": ["universal"], "category": "pancha_mahapurusha"},
    
    "Dhana Yoga": {"houses": [2, 11], "category": "wealth"},
    "Lakshmi Yoga": {"houses": [2, 5, 9], "category": "wealth"},
    "Vasumathi Yoga": {"houses": [2, 11], "category": "wealth"}, # Example, can vary
    
    "Raja Yoga": {"houses": [9, 10], "category": "career"},
    "Dharma Karma Adhipati Yoga": {"houses": [9, 10], "category": "career"},
    "Amala Yoga": {"houses": [10], "category": "career"},
    
    "Saraswati Yoga": {"houses": [5], "category": "education"},
    "Vidya Yoga": {"houses": [5], "category": "education"},
    
    "Kalatra Yoga": {"houses": [7], "category": "marriage"},
    "Saubhagya Yoga": {"houses": [7], "category": "marriage"},
    
    "Putra Yoga": {"houses": [5], "category": "children"},
    "Santana Yoga": {"houses": [5], "category": "children"},
    
    "Moksha Yoga": {"houses": [12], "category": "spirituality"},
    "Sanyasa Yoga": {"houses": [12], "category": "spirituality"},
    "Parivraja Yoga": {"houses": [12], "category": "spirituality"},
}
