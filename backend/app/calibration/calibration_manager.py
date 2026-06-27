import dataclasses
from .calibration_registry import CalibrationRegistry
from .calibration_types import CalibrationProfile

def _restore_int_keys(data):
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            new_key = k
            if isinstance(k, str) and k.isdigit() and not k.startswith('0') or (k.startswith('-') and k[1:].isdigit()):
                try:
                    new_key = int(k)
                except ValueError:
                    pass
            # Specifically handle '0' since isdigit() handles it but we excluded startswith('0')
            elif k == '0':
                new_key = 0
                
            new_dict[new_key] = _restore_int_keys(v)
        return new_dict
    elif isinstance(data, list):
        return [_restore_int_keys(item) for item in data]
    else:
        return data

class CalibrationManager:
    """
    Central orchestrator for all mathematical tuning values.
    Injects configuration slices directly into astrology calculation engines.
    """
    
    def __init__(self, profile_id: str = "v1.0.0_base", registry: CalibrationRegistry = None):
        self.registry = registry or CalibrationRegistry()
        raw_profile = self.registry.get_profile(profile_id)
        
        # Deep restore integer keys that JSON serialization converted to strings
        for field in dataclasses.fields(raw_profile):
            val = getattr(raw_profile, field.name)
            setattr(raw_profile, field.name, _restore_int_keys(val))
            
        # Specifically restore tuple keys for transit matrices
        if hasattr(raw_profile, 'transit'):
            tp = raw_profile.transit
            if 'TRANSIT_CONJUNCTION_MATRIX' in tp:
                tp['TRANSIT_CONJUNCTION_MATRIX'] = {
                    tuple(k.split('_')): v for k, v in tp['TRANSIT_CONJUNCTION_MATRIX'].items()
                }
            if 'TRANSIT_ASPECT_WEIGHTS' in tp:
                tp['TRANSIT_ASPECT_WEIGHTS'] = {
                    tuple(k.split('_')): v for k, v in tp['TRANSIT_ASPECT_WEIGHTS'].items()
                }

        self.active_profile = raw_profile

    # Exposed namespaces for direct engine access
    @property
    def master_probability(self):
        return self.active_profile.master_probability

    @property
    def planet_strength(self):
        return self.active_profile.planet_strength

    @property
    def house_strength(self):
        return self.active_profile.house_strength

    @property
    def rasi_strength(self):
        return self.active_profile.rasi_strength

    @property
    def varga(self):
        return self.active_profile.varga

    @property
    def dasha(self):
        return self.active_profile.dasha

    @property
    def ashtakavarga(self):
        return self.active_profile.ashtakavarga

    @property
    def natal_promise(self):
        return self.active_profile.natal_promise

    @property
    def transit(self):
        return self.active_profile.transit
