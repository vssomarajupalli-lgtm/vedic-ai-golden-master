// @ts-nocheck
import React, { useMemo } from 'react';
import { 
  ChevronDown, ChevronRight,
  Calendar, CheckCircle, Zap,
  Users, Sun, Moon, AlertCircle,
  Shield, Target, TrendingUp, TrendingDown,
  ArrowUpRight, Saturn, AlertTriangle, Target as TargetIcon,
  MapPin, Crown, Sparkles, BookOpen
} from 'lucide-react';

interface GocharaPresentationProps {
  rawOutputs: any;
  questionResults?: any[];
  mode: 'standard' | 'professional' | 'expert' | 'study';
  className?: string;
}

export const GocharaPresentation: React.FC<GocharaPresentationProps> = ({
  rawOutputs,
  questionResults = [],
  mode = 'standard',
  className = ''
}) => {
  const gocharaData = useMemo(() => {
    if (!rawOutputs?.breakdown?.engine_outputs?.transit) return null;
    
    const transit = rawOutputs.breakdown.engine_outputs.transit;
    const planets = rawOutputs.breakdown.engine_outputs.planets || {};
    const houses = rawOutputs.breakdown.engine_outputs.houses || {};
    const dashas = rawOutputs.breakdown.engine_outputs.dashas?.synthesis || {};
    const natalPromise = rawOutputs.breakdown.engine_outputs.natal_promise || {};
    
    return {
      transit,
      planets,
      houses,
      dashas,
      natalPromise,
      currentTransits: buildCurrentTransits(transit, planets, dashas),
      mandaliPositions: buildMandaliPositions(transit),
      affectedDomains: buildAffectedDomains(transit, natalPromise),
      sadeSati: buildSadeSati(transit, planets),
      ashtamaShani: buildAshtamaShani(transit, planets),
      ardhaAshtamaShani: buildArdhaAshtamaShani(transit, planets),
      jupiterTransits: buildJupiterTransits(transit, planets),
      rahuKetuAxis: buildRahuKetuAxis(transit, planets),
      nextMajorEvent: buildNextMajorEvent(transit),
    };
  }, [rawOutputs]);

  if (!gocharaData) {
    return (
      <div className={`bg-gray-50 rounded-lg p-8 text-center ${className}`}>
        <MapPin className="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Gochara Presentation</h3>
        <p className="text-gray-500">Calculate a chart to view deterministic transit analysis.</p>
      </div>
    );
  }

  const { 
    transit, 
    planets, 
    dashas, 
    natalPromise,
    currentTransits, 
    mandaliPositions,
    affectedDomains,
    sadeSati,
    ashtamaShani,
    ardhaAshtamaShani,
    jupiterTransits,
    rahuKetuAxis,
    nextMajorEvent
  } = gocharaData;

  const activationScore = transit.activation_score || 0;
  const mdLord = dashas.active_md || '';
  const adLord = dashas.active_ad || '';

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden ${className}`}>
      <div className="bg-gradient-to-r from-purple-600 to-indigo-700 p-6 text-white">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold">Gochara (Transit) Presentation</h2>
            <p className="text-purple-100 text-sm">Deterministic Transit Analysis · Classical Parashari Gochara</p>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-medium ${mode === 'expert' ? 'bg-yellow-200 text-yellow-900' : mode === 'professional' ? 'bg-blue-200 text-blue-900' : mode === 'study' ? 'bg-green-200 text-green-900' : 'bg-gray-200 text-gray-900'}`}>
            {mode.toUpperCase()} MODE
          </span>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <GocharaMetric label="TRANSIT ACTIVATION" value={`${activationScore}%`} icon={Zap} grade={getGrade(activationScore)} />
          <GocharaMetric label="OVERALL STRENGTH" value={`${averageDomainStrength(transit.activated_domains)}%`} icon={TrendingUp} grade={getGrade(averageDomainStrength(transit.activated_domains))} />
          <GocharaMetric label="MD LORD TRANSIT" value={transit.breakdown?.dasha_sync ? `${transit.breakdown.dasha_sync}%` : '—'} icon={Sun} grade={transit.breakdown?.dasha_sync ? getGrade(transit.breakdown.dasha_sync) : '—'} />
          <GocharaMetric label="DASHA SYNC" value={`${transit.breakdown?.dasha_sync || 0}%`} icon={Target} grade={getGrade(transit.breakdown?.dasha_sync || 0)} />
          <GocharaMetric label="TIMING CONFIDENCE" value={getTimingConfidence(transit)} icon={Shield} grade={getTimingConfidence(transit)} />
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* SECTION A: CURRENT GOCHARA MANDALI */}
        <CurrentGocharaMandali 
          transit={transit} 
          planets={planets} 
          dashas={dashas}
          mdLord={mdLord}
          adLord={adLord}
          mode={mode}
        />

        {/* SECTION B: MAJOR SATURN TRANSIT CYCLES */}
        <SaturnTransitCycles 
          transit={transit} 
          planets={planets} 
          mode={mode}
        />

        {/* SECTION C: JUPITER MAJOR TRANSITS */}
        <JupiterMajorTransits 
          transit={transit} 
          planets={planets} 
          mode={mode}
        />

        {/* SECTION D: RAHU-KETU TRANSIT */}
        <RahuKetuTransit 
          transit={transit} 
          planets={planets} 
          mode={mode}
        />

        {/* SECTION E: CURRENT TRANSIT SUMMARY */}
        <TransitSummaryDashboard 
          transit={transit} 
          natalPromise={rawOutputs?.breakdown?.engine_outputs?.natal_promise || {}}
          mode={mode}
        />

        {/* SECTION F: QUESTION SPECIFIC GOCHARA */}
        {questionResults.length > 0 && (
          <QuestionSpecificGochara 
            transit={rawOutputs.breakdown.engine_outputs.transit} 
            natalPromise={rawOutputs.breakdown.engine_outputs.natal_promise || {}}
            dashas={dashas}
            questionResults={questionResults}
            mode={mode}
          />
        )}

        {/* SECTION G: DETERMINISTIC TRANSIT EVIDENCE */}
        {mode === 'expert' && (
          <ExpertTransitDetails transit={transit} planets={planets} houses={rawOutputs.breakdown.engine_outputs.houses || {}} dashas={dashas} />
        )}

        {mode === 'study' && (
          <StudyTransitSection transit={transit} dashas={dashas} questionResults={questionResults} />
        )}
      </div>
    </div>
  );
};

// Helper functions
function buildCurrentTransits(transit: any, planets: any, dashas: any) {
  const factors = [...(transit.supporting_factors || []), ...(transit.obstructing_factors || [])];
  const mdLord = dashas.active_md || '';
  const adLord = dashas.active_ad || '';
  
  const planetMap = new Map<string, any>();
  factors.forEach(f => {
    const planet = f.planet?.toLowerCase();
    if (!planetMap.has(planet)) {
      planetMap.set(planet, {
        planet: planet.charAt(0).toUpperCase() + planet.slice(1),
        house: f.house || 0,
        mandali: f.mandali || `${f.house || 0}`,
        mandali_position: f.mandali_position || 0,
        status: f.score > 0 ? 'favorable' : f.score < 0 ? 'challenging' : 'neutral',
        intensity: Math.abs(f.score) > 10 ? 'high' : Math.abs(f.score) > 5 ? 'moderate' : 'low',
        affected_houses: [f.house].filter(h => h > 0 && h <= 12),
        affected_domains: getAffectedDomainsForHouse(f.house),
        dasha_sync: f.source === 'dasha_sync',
        description: f.factor
      });
    }
  });

  Object.keys(planets).forEach(p => {
    if (!planetMap.has(p.toLowerCase()) && p !== 'ascendant' && p !== 'lagna') {
      const planetData = planets[p];
      const house = planetData?.house || 0;
      if (house > 0 && house <= 12) {
        planetMap.set(p.toLowerCase(), {
          planet: p.charAt(0).toUpperCase() + p.slice(1),
          house,
          mandali: `${house}`,
          mandali_position: planetData?.longitude || 0,
          status: 'neutral',
          intensity: 'low',
          affected_houses: [house],
          affected_domains: getAffectedDomainsForHouse(house),
          dasha_sync: p.toLowerCase() === mdLord.toLowerCase() || p.toLowerCase() === adLord.toLowerCase(),
          description: `${p} transiting house ${house}`
        });
      }
    }
  });

  return Array.from(planetMap.values()).sort((a, b) => a.house - b.house);
}

function buildMandaliPositions(transit: any) {
  const factors = [...(transit.supporting_factors || []), ...(transit.obstructing_factors || [])];
  const map = new Map<string, any>();
  
  factors.forEach(f => {
    const key = `${f.planet}_${f.house}`;
    if (!map.has(key)) {
      map.set(key, {
        mandali: f.mandali || `${f.house || 0}`,
        planet: f.planet?.charAt(0).toUpperCase() + f.planet?.slice(1),
        position: f.mandali_position || f.house * 30,
        interpretation: getMandaliInterpretation(f.planet, f.house)
      });
    }
  });
  
  return Array.from(map.values());
}

function buildAffectedDomains(transit: any, natalPromise: any) {
  const domains = transit.activated_domains || {};
  return Object.entries(domains).map(([domain, score]) => ({
    domain_id: getDomainId(domain),
    domainId: getDomainId(domain),
    domain_name: domain,
    domainName: domain,
    net_influence: score >= 65 ? 'positive' : score >= 35 ? 'neutral' : 'negative',
    netInfluence: score >= 65 ? 'positive' : score >= 35 ? 'neutral' : 'negative',
    planets: getDomainPlanets(domain, transit),
    confidence: Math.min(95, Math.max(50, (score as number) + 10)),
    transit_strength: score
  }));
}

function buildSadeSati(transit: any, planets: any) {
  const moon = planets.moon || {};
  const saturn = planets.saturn || {};
  const saturnHouse = saturn?.house || 0;
  
  const isSadeSati = transit.confidence_flags?.includes('saturn_sadesati') || false;
  
  if (!isSadeSati) {
    return { is_active: false };
  }
  
  let phase = 2;
  if (saturnHouse === 12) phase = 1;
  else if (saturnHouse === 2) phase = 3;
  
  return {
    is_active: true,
    phase: phase === 1 ? 'first' : phase === 2 ? 'second' : 'third',
    start_date: 'Approximate - requires ephemeris',
    end_date: 'Approximate - requires ephemeris',
    current_phase: phase
  };
}

function buildAshtamaShani(transit: any, planets: any) {
  const moon = planets.moon || {};
  const saturn = planets.saturn || {};
  const moonSign = moon?.sign || 'taurus';
  const saturnSign = saturn?.sign || 'aquarius';
  
  // 8th from Moon
  const signs = ['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces'];
  const moonIdx = signs.indexOf(moonSign.toLowerCase());
  const ashtamaIdx = (moonIdx + 7) % 12;
  const ashtamaSign = signs[ashtamaIdx];
  const isActive = saturnSign.toLowerCase() === ashtamaSign.toLowerCase();
  
  return {
    is_active: isActive,
    occurrences: [
      { phase: 1, start_date: 'Requires ephemeris', end_date: 'Requires ephemeris' },
      { phase: 2, start_date: 'Requires ephemeris', end_date: 'Requires ephemeris' },
      { phase: 3, start_date: 'Requires ephemeris', end_date: 'Requires ephemeris' }
    ],
    current_occurrence: isActive ? 1 : null
  };
}

function buildArdhaAshtamaShani(transit: any, planets: any) {
  const moon = planets.moon || {};
  const saturn = planets.saturn || {};
  const moonSign = moon?.sign || 'taurus';
  const saturnSign = saturn?.sign || 'aquarius';
  
  const signs = ['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces'];
  const moonIdx = signs.indexOf(moonSign.toLowerCase());
  const ardhaIdx = (moonIdx + 3) % 12;
  const ardhaSign = signs[ardhaIdx];
  const isActive = saturnSign.toLowerCase() === ardhaSign.toLowerCase();
  
  return {
    is_active: isActive,
    occurrences: [
      { phase: 1, start_date: 'Requires ephemeris', end_date: 'Requires ephemeris' },
      { phase: 2, start_date: 'Requires ephemeris', end_date: 'Requires ephemeris' },
      { phase: 3, start_date: 'Requires ephemeris', end_date: 'Requires ephemeris' }
    ],
    current_occurrence: isActive ? 1 : null
  };
}

function buildJupiterTransits(transit: any, planets: any) {
  const jupiterFactors = (transit.supporting_factors || [])
    .filter(f => f.planet?.toLowerCase() === 'jupiter');
  
  const jupiter = planets.jupiter || {};
  const jupiterStrength = jupiter?.final_score || jupiter?.score || 50;
  
  const favourableHouses = [2, 5, 7, 9, 11]; // from Moon/Lagna
  
  return {
    planet_strength: Math.round(jupiterStrength),
    favourable_houses: favourableHouses.map(h => ({
      house: h,
      label: `${h}th from Moon`,
      areas: getAreasForHouse(h),
      status: jupiterFactors.some(f => f.house === h) ? 'active' : 'upcoming'
    }))
  };
}

function buildRahuKetuAxis(transit: any, planets: any) {
  const rahu = planets.rahu || {};
  const ketu = planets.ketu || {};
  const rahuStrength = rahu?.final_score || rahu?.score || 50;
  const ketuStrength = ketu?.final_score || ketu?.score || 50;
  
  return {
    current_axis: `${rahu?.house || '?'} / ${ketu?.house || '?'} Axis`,
    rahu_strength: Math.round(rahuStrength),
    ketu_strength: Math.round(ketuStrength),
    affected_domains: getAffectedDomainsForHouse(rahu?.house || 0).concat(getAffectedDomainsForHouse(ketu?.house || 0)),
    previous_axis: 'Requires ephemeris',
    next_axis: 'Requires ephemeris'
  };
}

function buildNextMajorEvent(transit: any) {
  if (transit.confidence_flags?.includes('saturn_sadesati')) return 'Sade Sati Phase Transition';
  if (transit.confidence_flags?.includes('jupiter_transit_positive')) return 'Jupiter Favourable Transit';
  if (transit.confidence_flags?.includes('dasha_lord_transiting')) return 'Dasha Lord Transit';
  return 'Next Planetary Ingress';
}

function averageDomainStrength(domains: Record<string, number>): number {
  const values = Object.values(domains).filter(v => typeof v === 'number');
  if (values.length === 0) return 0;
  return Math.round(values.reduce((a, b) => a + b, 0) / values.length);
}

function getTimingConfidence(transit: any): string {
  if (transit.confidence_flags?.includes('jupiter_transit_positive')) return 'HIGH';
  if (transit.confidence_flags?.includes('saturn_transit_negative')) return 'LOW';
  if (transit.confidence_flags?.includes('dasha_lord_transiting')) return 'HIGH';
  if (transit.confidence_flags?.includes('saturn_sadesati')) return 'MODERATE';
  return 'MODERATE';
}

function getAffectedDomainsForHouse(house: number): number[] {
  const houseDomainMap: Record<number, number[]> = {
    1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 6: [6],
    7: [7], 8: [8], 9: [9], 10: [10], 11: [11], 12: [12]
  };
  return houseDomainMap[house] || [];
}

function getDomainId(domain: string): number {
  const domainIds: Record<string, number> = {
    'self': 1, 'wealth': 2, 'siblings': 3, 'home': 4, 'children': 5, 'health': 6,
    'marriage': 7, 'longevity': 8, 'fortune': 9, 'career': 10, 'income': 11, 'spirituality': 12
  };
  return domainIds[domain.toLowerCase()] || 1;
}

function getDomainPlanets(domain: string, transit: any): string[] {
  const factors = [...(transit.supporting_factors || []), ...(transit.obstructing_factors || [])];
  const planetSet = new Set<string>();
  factors.forEach(f => {
    if (f.planet) planetSet.add(f.planet.charAt(0).toUpperCase() + f.planet.slice(1));
  });
  return Array.from(planetSet);
}

function getMandaliInterpretation(planet: string, house: number): string {
  const interpretations: Record<string, Record<number, string>> = {
    sun: { 1: 'Self-expression', 10: 'Career peak', 11: 'Gains' },
    moon: { 4: 'Home comfort', 7: 'Relationships', 10: 'Public image' },
    mars: { 1: 'Energy', 3: 'Courage', 6: 'Competition', 10: 'Ambition' },
    mercury: { 1: 'Communication', 3: 'Learning', 7: 'Contracts', 10: 'Business' },
    jupiter: { 1: 'Wisdom', 5: 'Children', 9: 'Fortune', 11: 'Gains' },
    venus: { 1: 'Charm', 4: 'Home luxury', 7: 'Marriage', 11: 'Income' },
    saturn: { 1: 'Discipline', 3: 'Effort', 6: 'Service', 10: 'Authority', 11: 'Patience' },
    rahu: { 1: 'Obsession', 3: 'Desire', 7: 'Foreign', 10: 'Ambition', 11: 'Networks' },
    ketu: { 1: 'Detachment', 4: 'Roots', 8: 'Transformation', 12: 'Moksha' }
  };
  return interpretations[planet.toLowerCase()]?.[house] || `Transit in house ${house}`;
}

function getAreasForHouse(house: number): string {
  const areas: Record<number, string> = {
    2: 'Wealth, Family', 5: 'Children, Education', 7: 'Marriage, Partnership',
    9: 'Fortune, Dharma', 11: 'Income, Gains'
  };
  return areas[house] || '';
}

function getSupportedAreas(domains: Record<string, number>, natalPromise: any) {
  return Object.entries(domains)
    .filter(([_, score]) => score >= 65)
    .map(([name, score]) => ({ name: name.charAt(0).toUpperCase() + name.slice(1), score: Math.round(score) }));
}

function getCautionAreas(domains: Record<string, number>, natalPromise: any) {
  return Object.entries(domains)
    .filter(([_, score]) => score < 40)
    .map(([name, score]) => ({ name: name.charAt(0).toUpperCase() + name.slice(1), score: Math.round(score) }));
}

function getNextTransitEvent(transit: any): string {
  if (transit.confidence_flags?.includes('saturn_sadesati')) return 'Sade Sati Phase Transition';
  if (transit.confidence_flags?.includes('jupiter_transit_positive')) return 'Jupiter Favourable Transit';
  if (transit.confidence_flags?.includes('dasha_lord_transiting')) return 'Dasha Lord Transit';
  return 'Next Planetary Ingress';
}

function getPrimaryDomainForNextEvent(transit: any): string {
  const domains = transit.activated_domains || {};
  const maxEntry = Object.entries(domains).reduce((a, b) => a[1] > b[1] ? a : b, ['', 0]);
  return maxEntry[0] ? maxEntry[0].charAt(0).toUpperCase() + maxEntry[0].slice(1) : 'General';
}

function getSupportedHousesForDomain(domain: string, transit: any): string[] {
  const factors = [...(transit.supporting_factors || [])];
  const houses = new Set<number>();
  factors.forEach(f => {
    if (f.house && f.house > 0 && f.house <= 12) houses.add(f.house);
  });
  return Array.from(houses).map(h => `${h}H`).slice(0, 4);
}

function getGrade(value: number): string {
  if (value >= 80) return 'EXCELLENT';
  if (value >= 65) return 'VERY GOOD';
  if (value >= 50) return 'GOOD';
  if (value >= 35) return 'WEAK';
  return 'TOO WEAK';
}

function getGradeColor(grade: string): string {
  switch (grade) {
    case 'EXCELLENT': return 'bg-emerald-100 text-emerald-800';
    case 'VERY GOOD': return 'bg-blue-100 text-blue-800';
    case 'GOOD': return 'bg-green-100 text-green-800';
    case 'WEAK': return 'bg-yellow-100 text-yellow-800';
    case 'TOO WEAK': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
}

function formatDate(dateStr: string): string {
  if (!dateStr || dateStr === 'Unknown') return 'Unknown';
  try {
    return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  } catch {
    return dateStr;
  }
}

const ArrowUpRight = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M7 17L17 7M17 7h-10M17 7v10" />
  </svg>
);

const Saturn = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="5" />
    <path d="M12 2a10 10 0 0 1 0 20M12 2a10 10 0 0 0 0 20" />
    <ellipse cx="12" cy="12" rx="14" ry="3" />
  </svg>
);

const Crown = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
  </svg>
);

const Sparkles = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M12 3v2m0 14v2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41M3 12h2m14 0h2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41" />
  </svg>
);

const BookOpen = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
  </svg>
);

// ============================================
// SECTION COMPONENTS
// ============================================

interface SectionCardProps {
  title: string;
  icon: React.ComponentType<{ className?: string }>;
  color?: string;
  children: React.ReactNode;
}

const SectionCard: React.FC<SectionCardProps> = ({ title, icon: Icon, color = 'blue', children }) => (
  <section className="bg-white border border-gray-200 rounded-xl overflow-hidden">
    <div className={`bg-${color}-600 text-white p-4`}>
      <h3 className="text-lg font-bold flex items-center gap-2">
        <Icon className="w-5 h-5" />
        {title}
      </h3>
    </div>
    <div className="p-6">
      {children}
    </div>
  </section>
);

interface GocharaMetricProps {
  label: string;
  value: string;
  icon: React.ComponentType<{ className?: string }>;
  grade: string;
}

const GocharaMetric: React.FC<GocharaMetricProps> = ({ label, value, icon: Icon, grade }) => (
  <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
    <div className="flex items-center justify-between mb-2">
      <Icon className="w-5 h-5 text-purple-200" />
      <span className={`text-xs font-medium px-2 py-0.5 rounded ${getGradeColor(grade)}`}>
        {grade}
      </span>
    </div>
    <div className="text-2xl font-bold mb-1">{value}</div>
    <div className="flex items-center gap-1 text-sm text-purple-200">
      <span className="text-xs uppercase tracking-wider">{label}</span>
    </div>
  </div>
);

// SECTION A: CURRENT GOCHARA MANDALI
const CurrentGocharaMandali: React.FC<{ 
  transit: any; planets: any; dashas: any; 
  mdLord: string; adLord: string; mode: string 
}> = ({ transit, planets, dashas, mdLord, adLord, mode }) => {
  const currentTransits = buildCurrentTransits(transit, planets, dashas);
  
  if (!currentTransits.length) return null;

  return (
    <SectionCard title="Current Gochara Mandali" icon={MapPin} color="indigo">
      <div className="space-y-4">
        <p className="text-sm text-gray-600 mb-4">
          Moon-centered Mandali showing all 9 planets with current Rasi, Mandali position, House, and Transit Strength.
        </p>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Planet</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Current Rasi</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Degree</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Mandali</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Mandali Pos</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">House</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Strength</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Nature</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Dasha Sync</th>
                {mode === 'expert' && <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Interpretation</th>}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {currentTransits.map((t: any, idx: number) => {
                const isMdLord = t.planet?.toLowerCase() === mdLord.toLowerCase();
                const isAdLord = t.planet?.toLowerCase() === adLord.toLowerCase;
                const planetStrength = planets[t.planet?.toLowerCase()]?.final_score || planets[t.planet?.toLowerCase()]?.score || 50;
                
                return (
                  <tr key={idx} className={`hover:bg-gray-50 ${isMdLord ? 'bg-amber-50' : isAdLord ? 'bg-blue-50' : ''}`}>
                    <td className="px-4 py-3 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <span className="capitalize font-medium text-gray-900">{t.planet}</span>
                        {isMdLord && <span className="px-1.5 py-0.5 bg-amber-100 text-amber-800 text-xs font-bold rounded">MD LORD</span>}
                        {isAdLord && <span className="px-1.5 py-0.5 bg-blue-100 text-blue-800 text-xs font-bold rounded">AD LORD</span>}
                      </div>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 capitalize">
                      {getSignForHouse(t.house)}
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm font-mono text-gray-600">
                      {planets[t.planet?.toLowerCase()]?.longitude?.toFixed(2) || '—'}°
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap">
                      <span className="px-2 py-0.5 bg-purple-100 text-purple-800 text-xs font-bold rounded">{t.mandali}</span>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm font-mono text-gray-600">{t.mandali_position || '—'}</td>
                    <td className="px-4 py-3 whitespace-nowrap">
                      <span className="px-2 py-0.5 bg-indigo-100 text-indigo-800 text-xs font-bold rounded">{t.house}H</span>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap">
                      <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                        planetStrength >= 70 ? 'bg-emerald-100 text-emerald-800' :
                        planetStrength >= 40 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {Math.round(planetStrength)}%
                      </span>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap">
                      <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                        t.status === 'favorable' ? 'bg-emerald-100 text-emerald-800' :
                        t.status === 'challenging' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {t.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap">
                      {t.dasha_sync ? (
                        <span className="px-2 py-0.5 bg-emerald-100 text-emerald-800 text-xs font-bold rounded flex items-center gap-1">
                          <CheckCircle className="w-3 h-3" /> Synced
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">No sync</span>
                      )}
                    </td>
                    {mode === 'expert' && (
                      <td className="px-4 py-3 text-sm text-gray-500 max-w-xs truncate">{t.description}</td>
                    )}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Mandali Grid Visualization */}
        <div className="mt-6">
          <h4 className="font-bold text-gray-900 mb-3">Mandali Grid (Moon-Centered)</h4>
          <MandaliGridView currentTransits={currentTransits} />
        </div>
      </div>
    </SectionCard>
  );
};

const MandaliGridView: React.FC<{ currentTransits: any[] }> = ({ currentTransits }) => (
  <div className="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-12 gap-2">
    {Array.from({ length: 12 }, (_, i) => i + 1).map(house => {
      const planet = currentTransits.find(t => t.house === house);
      return (
        <div key={house} className={`p-3 rounded-lg text-center ${planet ? 'bg-indigo-50 border border-indigo-200' : 'bg-gray-50 border border-gray-200'}`}>
          <div className="text-xs font-bold text-gray-500">{house}H</div>
          <div className={`text-sm font-medium ${planet ? 'text-indigo-700' : 'text-gray-400'}`}>
            {planet ? planet.planet : '—'}
          </div>
          {planet && (
            <div className="text-xs text-gray-500 mt-1">
              Str: {planets[planet.planet?.toLowerCase()]?.final_score || 50}%
            </div>
          )}
        </div>
      );
    })}
  </div>
);

// SECTION B: SATURN TRANSIT CYCLES
const SaturnTransitCycles: React.FC<{ transit: any; planets: any; mode: string }> = ({ transit, planets, mode }) => {
  const sadeSati = buildSadeSati(transit, planets);
  const ashtamaShani = buildAshtamaShani(transit, planets);
  const ardhaAshtamaShani = buildArdhaAshtamaShani(transit, planets);
  
  return (
    <SectionCard title="Major Saturn Transit Cycles" icon={Saturn} color="amber">
      <div className="space-y-4">
        {/* SADE SATI */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-4">
            <h4 className="font-bold text-gray-900 flex items-center gap-2">
              <Saturn className="w-5 h-5 text-orange-600" />
              Sade Sati (Elinati Shani)
            </h4>
            <span className={`px-3 py-1 rounded-full text-xs font-bold ${sadeSati.is_active ? 'bg-amber-100 text-amber-800' : 'bg-gray-100 text-gray-600'}`}>
              {sadeSati.is_active ? 'ACTIVE' : 'INACTIVE'}
            </span>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <PhaseCard 
              title="Phase 1: 12th from Moon" 
              phase={1}
              active={sadeSati.current_phase === 1}
              start={sadeSati.start_date}
              end={sadeSati.end_date}
              description="Saturn transiting 12th house from natal Moon. Beginning of 7.5-year cycle. Mental preparation, detachment, spiritual growth."
            />
            <PhaseCard 
              title="Phase 2: Janma Shani" 
              phase={2}
              active={sadeSati.current_phase === 2}
              start={sadeSati.start_date}
              end={sadeSati.end_date}
              description="Saturn over natal Moon. Peak intensity. Major life restructuring, emotional pressure, karmic fruition."
            />
            <PhaseCard 
              title="Phase 3: 2nd from Moon" 
              phase={3}
              active={sadeSati.current_phase === 3}
              start={sadeSati.start_date}
              end={sadeSati.end_date}
              description="Saturn transiting 2nd house from Moon. Consolidation, financial pressure, family responsibilities, final lessons."
            />
          </div>
          
          {sadeSati.is_active && (
            <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
              <p className="text-amber-800 font-medium">Currently in Phase {sadeSati.current_phase} of Sade Sati.</p>
            </div>
          )}
        </div>

        {/* ASHTAMA SHANI */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Saturn className="w-5 h-5 text-purple-600" />
            Ashtama Shani (8th House Transit)
          </h4>
          <p className="text-gray-600 mb-4">Saturn transiting the 8th house from Moon. Occurs every ~29.5 years. 3 occurrences per cycle.</p>
          <div className="space-y-2">
            <AshtamaOccurrence occurrence={1} />
            <AshtamaOccurrence occurrence={2} />
            <AshtamaOccurrence occurrence={3} />
          </div>
        </div>

        {/* ARDHA ASHTAMA SHANI */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Saturn className="w-5 h-5 text-blue-600" />
            Ardha Ashtama Shani (4th House Transit)
          </h4>
          <p className="text-gray-600 mb-4">Saturn transiting the 4th house from Moon. Home, mother, emotional foundation challenges.</p>
          <div className="space-y-2">
            <AshtamaOccurrence occurrence={1} title="Ardha Ashtama 1" />
            <AshtamaOccurrence occurrence={2} title="Ardha Ashtama 2" />
            <AshtamaOccurrence occurrence={3} title="Ardha Ashtama 3" />
          </div>
        </div>

        {/* KANTAKA SHANI */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Saturn className="w-5 h-5 text-gray-600" />
            Kantaka Shani (Dashama Shani / 10th House)
          </h4>
          <p className="text-gray-600">Not available in deterministic engine.</p>
        </div>
      </div>
    </SectionCard>
  );
};

const PhaseCard: React.FC<{ title: string; phase: number; active: boolean; start: string; end: string; description: string }> = ({ 
  title, phase, active, start, end, description 
}) => (
  <div className={`p-4 rounded-lg border-2 ${active ? 'border-amber-400 bg-amber-50' : 'border-gray-200'}`}>
    <h5 className="font-bold text-gray-900 mb-2">{title}</h5>
    <p className="text-sm text-gray-600 mb-2">{description}</p>
    <div className="text-xs text-gray-500">
      {active ? '● CURRENT PHASE' : '○'}
      <br />
      {start !== 'Approximate - requires ephemeris' ? `From ${formatDate(start)} to ${formatDate(end)}` : 'Dates require ephemeris'}
    </div>
  </div>
);

const AshtamaOccurrence: React.FC<{ occurrence: number; title?: string }> = ({ occurrence, title }) => (
  <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
    <div className="flex items-center justify-between">
      <span className="font-medium text-gray-900">{title || `Occurrence ${occurrence}`}</span>
      <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">Dates require ephemeris</span>
    </div>
  </div>
);

// SECTION C: JUPITER MAJOR TRANSITS
const JupiterMajorTransits: React.FC<{ transit: any; planets: any; mode: string }> = ({ transit, planets, mode }) => {
  const jupiterFactors = (transit.supporting_factors || [])
    .filter(f => f.planet?.toLowerCase() === 'jupiter');
  
  const jupiter = planets.jupiter || {};
  const jupiterStrength = jupiter?.final_score || jupiter?.score || 50;
  
  return (
    <SectionCard title="Jupiter Major Transits" icon={TrendingUp} color="emerald">
      <div className="space-y-4">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 bg-emerald-100 text-emerald-800 text-sm font-bold rounded-full">JUPITER</span>
            <span className={`px-2 py-0.5 rounded text-xs font-bold ${
              jupiterStrength >= 70 ? 'bg-emerald-100 text-emerald-800' :
              jupiterStrength >= 40 ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800'
            }`}>
              {Math.round(jupiterStrength)}%
            </span>
          </div>
        </div>
        
        <p className="text-gray-600 mb-4">
          Major favourable periods when Jupiter transits favourable houses (2nd, 5th, 7th, 9th, 11th from Moon/Lagna).
        </p>
        
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-bold text-gray-900 mb-3">Favourable Transit Windows</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FavourableWindow house={2} label="2nd from Moon" areas="Wealth, Family" />
            <FavourableWindow house={5} label="5th from Moon" areas="Children, Education" />
            <FavourableWindow house={7} label="7th from Moon" areas="Marriage, Partnership" />
            <FavourableWindow house={9} label="9th from Moon" areas="Fortune, Dharma" />
            <FavourableWindow house={11} label="11th from Moon" areas="Income, Gains" />
          </div>
        </div>
      </div>
    </SectionCard>
  );
};

const FavourableWindow: React.FC<{ house: number; label: string; areas: string }> = ({ house, label, areas }) => (
  <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4">
    <div className="font-bold text-emerald-800 mb-1">{label} ({house}H)</div>
    <div className="text-sm text-emerald-700 mb-2">{areas}</div>
    <div className="text-xs text-gray-500">Requires ephemeris for dates</div>
  </div>
);

// SECTION D: RAHU-KETU TRANSIT
const RahuKetuTransit: React.FC<{ transit: any; planets: any; mode: string }> = ({ transit, planets, mode }) => {
  const rahu = planets.rahu || {};
  const ketu = planets.ketu || {};
  const rahuStrength = rahu?.final_score || rahu?.score || 50;
  const ketuStrength = ketu?.final_score || ketu?.score || 50;
  
  return (
    <SectionCard title="Rahu-Ketu Transit Axis" icon={Target} color="purple">
      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <h4 className="font-bold text-purple-900 mb-2 flex items-center gap-2">
              <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs font-bold rounded">RAHU</span>
            </h4>
            <div className="space-y-1 text-sm">
              <div>Current House: {rahu?.house || '—'}H</div>
              <div>Strength: <span className={`font-bold ${rahuStrength >= 70 ? 'text-emerald-600' : rahuStrength >= 40 ? 'text-yellow-600' : 'text-red-600'}`}>{Math.round(rahuStrength)}%</span></div>
              <div>Affected Domains: {getAffectedDomainsForHouse(rahu?.house || 0).map(d => getDomainName(d)).join(', ')}</div>
            </div>
          </div>
          
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h4 className="font-bold text-gray-900 mb-2 flex items-center gap-2">
              <span className="px-2 py-1 bg-gray-100 text-gray-800 text-xs font-bold rounded">KETU</span>
            </h4>
            <div className="space-y-1 text-sm">
              <div>Current House: {ketu?.house || '—'}H</div>
              <div>Strength: <span className={`font-bold ${ketuStrength >= 70 ? 'text-emerald-600' : ketuStrength >= 40 ? 'text-yellow-600' : 'text-red-600'}`}>{Math.round(ketuStrength)}%</span></div>
              <div>Affected Domains: {getAffectedDomainsForHouse(ketu?.house || 0).map(d => getDomainName(d)).join(', ')}</div>
            </div>
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-bold text-gray-900 mb-3">Axis Timeline</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="p-3 bg-gray-50 rounded">
              <div className="text-gray-500 text-xs uppercase">Previous Axis</div>
              <div className="font-medium">Requires ephemeris</div>
            </div>
            <div className="p-3 bg-purple-50 border border-purple-200 rounded">
              <div className="text-gray-500 text-xs uppercase">Current Axis</div>
              <div className="font-medium text-purple-700">{rahu?.house || '?'} / {ketu?.house || '?'} Axis</div>
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <div className="text-gray-500 text-xs uppercase">Next Axis</div>
              <div className="font-medium">Requires ephemeris</div>
            </div>
          </div>
        </div>
      </div>
    </SectionCard>
  );
};

// SECTION E: TRANSIT SUMMARY DASHBOARD
const TransitSummaryDashboard: React.FC<{ transit: any; natalPromise: any; mode: string }> = ({ transit, natalPromise, mode }) => {
  const domains = transit.activated_domains || {};
  
  return (
    <SectionCard title="Current Transit Summary" icon={Target} color="blue">
      <div className="space-y-6">
        {/* Overall Strength */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <SummaryCard label="Overall Transit Strength" value={`${averageDomainStrength(domains)}%`} grade={getGrade(averageDomainStrength(domains))} icon={Zap} />
          <SummaryCard label="Transit Grade" value={transit.grade || 'UNKNOWN'} grade={transit.grade || 'UNKNOWN'} icon={Shield} />
          <SummaryCard label="Activation Score" value={`${transit.activation_score || 0}%`} grade={getGrade(transit.activation_score || 0)} icon={TrendingUp} />
          <SummaryCard label="Timing Confidence" value={getTimingConfidence(transit)} grade={getTimingConfidence(transit)} icon={Calendar} />
        </div>

        {/* Most Supported Areas */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-bold text-gray-900 mb-4">Most Supported Life Areas</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {getSupportedAreas(domains, natalPromise).map((area, idx) => (
              <SupportedAreaCard key={idx} area={area} />
            ))}
          </div>
        </div>

        {/* Areas Requiring Caution */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-bold text-gray-900 mb-4">Areas Requiring Caution</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {getCautionAreas(domains, natalPromise).map((area, idx) => (
              <CautionAreaCard key={idx} area={area} />
            ))}
          </div>
        </div>

        {/* Next Major Transit Event */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg p-6">
          <h4 className="font-bold text-lg mb-2">Next Major Transit Event</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <div className="text-purple-100 text-xs uppercase">Event</div>
              <div className="font-bold">{getNextTransitEvent(transit)}</div>
            </div>
            <div>
              <div className="text-purple-100 text-xs uppercase">Approximate Timing</div>
              <div className="font-bold">Requires ephemeris</div>
            </div>
            <div>
              <div className="text-purple-100 text-xs uppercase">Primary Domain</div>
              <div className="font-bold">{getPrimaryDomainForNextEvent(transit)}</div>
            </div>
          </div>
        </div>
      </div>
    </SectionCard>
  );
};

const SummaryCard: React.FC<{ label: string; value: string; grade: string; icon: React.ComponentType<{ className?: string }> }> = ({ 
  label, value, grade, icon: Icon 
}) => (
  <div className="bg-white border border-gray-200 rounded-lg p-4">
    <div className="flex items-center justify-between mb-2">
      <Icon className="w-5 h-5 text-indigo-600" />
      <span className={`text-xs font-medium px-2 py-0.5 rounded ${getGradeColor(grade)}`}>{grade}</span>
    </div>
    <div className="text-2xl font-bold text-gray-900">{value}</div>
    <div className="text-xs text-gray-500 uppercase tracking-wider">{label}</div>
  </div>
);

const SupportedAreaCard: React.FC<{ area: { name: string; score: number } }> = ({ area }) => (
  <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-3">
    <div className="font-medium text-emerald-800">{area.name}</div>
    <div className="text-2xl font-bold text-emerald-600">{area.score}%</div>
    <div className="text-xs text-emerald-600">Supported</div>
  </div>
);

const CautionAreaCard: React.FC<{ area: { name: string; score: number } }> = ({ area }) => (
  <div className="bg-red-50 border border-red-200 rounded-lg p-3">
    <div className="font-medium text-red-800">{area.name}</div>
    <div className="text-2xl font-bold text-red-600">{area.score}%</div>
    <div className="text-xs text-red-600">Caution advised</div>
  </div>
);

// SECTION F: QUESTION SPECIFIC GOCHARA
const QuestionSpecificGochara: React.FC<{ 
  transit: any; natalPromise: any; dashas: any; 
  questionResults: any[]; mode: string 
}> = ({ transit, natalPromise, dashas, questionResults, mode }) => (
  <SectionCard title="Question-Specific Gochara" icon={CheckCircle} color="green">
    <div className="space-y-4">
      {questionResults.map((qr: any, idx: number) => (
        <QuestionGocharaCard key={idx} question={qr} transit={transit} natalPromise={natalPromise} dashas={dashas} />
      ))}
    </div>
  </SectionCard>
);

const QuestionGocharaCard: React.FC<{ 
  question: any; transit: any; natalPromise: any; dashas: any 
}> = ({ question, transit, natalPromise, dashas }) => {
  const domain = question.domain || '';
  const domainTransitScore = transit.activated_domains?.[domain] || 0;
  const domainPromise = natalPromise[domain]?.score || 50;
  
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <h4 className="font-bold text-gray-900 mb-3 capitalize">{domain} - Transit Analysis</h4>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
        <div className="p-3 bg-indigo-50 rounded">
          <div className="text-xs text-indigo-600 uppercase">Transit Support</div>
          <div className="font-bold text-indigo-800">{domainTransitScore}%</div>
        </div>
        <div className="p-3 bg-emerald-50 rounded">
          <div className="text-xs text-emerald-600 uppercase">Natal Promise</div>
          <div className="font-bold text-emerald-800">{domainPromise}%</div>
        </div>
        <div className="p-3 bg-amber-50 rounded">
          <div className="text-xs text-amber-600 uppercase">Dasha Sync</div>
          <div className="font-bold text-amber-800">{transit.breakdown?.dasha_sync || 0}%</div>
        </div>
        <div className="p-3 bg-purple-50 rounded">
          <div className="text-xs text-purple-600 uppercase">Timing</div>
          <div className="font-bold text-purple-800">{dashas.active_md} / {dashas.active_ad}</div>
        </div>
      </div>
      <div className="space-y-2 text-sm">
        <div className="flex items-center gap-2">
          <span className="text-gray-500">Supporting Planets:</span>
          <span>{getDomainPlanets(domain, transit).join(', ') || '—'}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-gray-500">Supporting Houses:</span>
          <span>{getSupportedHousesForDomain(domain, transit).join(', ')}</span>
        </div>
      </div>
    </div>
  );

// SECTION G: DETERMINISTIC TRANSIT EVIDENCE
const ExpertTransitDetails: React.FC<{ transit: any; planets: any; houses: any; dashas: any }> = ({ 
  transit, planets, houses, dashas 
}) => (
  <details className="group border border-gray-200 rounded-lg bg-gray-50 mt-6">
    <summary className="flex items-center justify-between p-4 cursor-pointer bg-white border-b border-gray-200">
      <div className="flex items-center gap-3">
        <AlertTriangle className="w-5 h-5 text-yellow-600" />
        <span className="font-bold text-gray-900">Expert Mode: Full Transit Deterministic Details</span>
      </div>
      <ChevronDown className="w-5 h-5 text-gray-400 group-open:rotate-180 transition-transform" />
    </summary>
    <div className="p-6 space-y-6">
      {/* Breakdown Scores */}
      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h4 className="font-bold text-gray-900 mb-4">Transit Activation Breakdown</h4>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <ExpertMetric label="Activation Score" value={`${transit.activation_score || 0}%`} />
          <ExpertMetric label="House Activation" value={`${transit.breakdown?.house_activation || 0}%`} />
          <ExpertMetric label="BAV Support" value={`${transit.breakdown?.bav_support || 0}%`} />
          <ExpertMetric label="Planet Activation" value={`${transit.breakdown?.planet_activation || 0}%`} />
          <ExpertMetric label="Dasha Sync" value={`${transit.breakdown?.dasha_sync || 0}%`} />
          <ExpertMetric label="Vedha Obstruction" value={`${transit.breakdown?.vedha_layer || 0}%`} />
        </div>
      </div>

      {/* Supporting Factors */}
      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h4 className="font-bold text-gray-900 mb-4">Supporting Factors</h4>
        <div className="space-y-2">
          {(transit.supporting_factors || []).map((f: any, idx: number) => (
            <div key={idx} className="flex items-center gap-3 p-2 bg-emerald-50 rounded">
              <span className="w-2 h-2 rounded bg-emerald-500" />
              <span className="text-sm font-medium text-emerald-800">{f.factor}</span>
              <span className="text-sm text-emerald-600 ml-auto">+{f.score}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Obstructing Factors */}
      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h4 className="font-bold text-gray-900 mb-4">Obstructing Factors</h4>
        <div className="space-y-2">
          {(transit.obstructing_factors || []).map((f: any, idx: number) => (
            <div key={idx} className="flex items-center gap-3 p-2 bg-red-50 rounded">
              <span className="w-2 h-2 rounded bg-red-500" />
              <span className="text-sm font-medium text-red-800">{f.factor}</span>
              <span className="text-sm text-red-600 ml-auto">{f.score}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Activated Domains */}
      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h4 className="font-bold text-gray-900 mb-4">Activated Domains</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {Object.entries(transit.activated_domains || {}).map(([domain, score]) => (
            <div key={domain} className="p-3 bg-gray-50 rounded">
              <div className="font-medium capitalize text-gray-900">{domain}</div>
              <div className="text-2xl font-bold text-indigo-600">{Math.round(score)}%</div>
            </div>
          ))}
        </div>
      </div>

      {/* Confidence Flags */}
      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h4 className="font-bold text-gray-900 mb-4">Confidence Flags</h4>
        <div className="flex flex-wrap gap-2">
          {(transit.confidence_flags || []).map((flag: string, idx: number) => (
            <span key={idx} className="px-3 py-1 bg-indigo-100 text-indigo-800 text-xs font-medium rounded-full">
              {flag.replace(/_/g, ' ')}
            </span>
          ))}
        </div>
      </div>
    </div>
  </details>
);

const StudyTransitSection: React.FC<{ transit: any; dashas: any; questionResults: any[] }> = ({ 
  transit, dashas, questionResults 
}) => (
  <details className="group border border-green-200 rounded-lg bg-green-50 mt-6">
    <summary className="flex items-center justify-between p-4 cursor-pointer bg-white border-b border-green-200">
      <div className="flex items-center gap-3">
        <CheckCircle className="w-5 h-5 text-green-600" />
        <span className="font-bold text-gray-900">Study Mode: Transit Learning & Verification</span>
      </div>
      <ChevronDown className="w-5 h-5 text-gray-400 group-open:rotate-180 transition-transform" />
    </summary>
    <div className="p-6 space-y-6">
      {/* Formula Breakdown */}
      <div className="bg-white rounded-lg p-4 border border-green-200">
        <h4 className="font-bold text-green-800 mb-4">How Transit Activation is Calculated</h4>
        <div className="space-y-3 text-sm font-mono">
          <FormulaRow label="House Activation (30%)" value={`${transit.breakdown?.house_activation || 0}%`} weight="0.30" />
          <FormulaRow label="BAV Support (20%)" value={`${transit.breakdown?.bav_support || 0}%`} weight="0.20" />
          <FormulaRow label="Planet Activation (20%)" value={`${transit.breakdown?.planet_activation || 0}%`} weight="0.20" />
          <FormulaRow label="Dasha Sync (20%)" value={`${transit.breakdown?.dasha_sync || 0}%`} weight="0.20" />
          <FormulaRow label="Vedha Layer (10%)" value={`${transit.breakdown?.vedha_layer || 0}%`} weight="0.10" isDeduction />
          <FormulaRow label="Transit Activation = " value={`${transit.activation_score || 0}%`} isTotal />
        </div>
      </div>

      {/* Dasha-Transit Synchronization */}
      <div className="bg-white rounded-lg p-4 border border-green-200">
        <h4 className="font-bold text-green-800 mb-4">Dasha-Transit Synchronization</h4>
        <div className="space-y-3 text-sm">
          <SyncRow label="MD Lord" planet={dashas.active_md} strength={`${transit.breakdown?.dasha_sync || 0}%`} />
          <SyncRow label="AD Lord" planet={dashas.active_ad} strength={`${transit.breakdown?.dasha_sync || 0}%`} />
          <SyncRow label="Sync Bonus" planet="—" strength={`+${transit.breakdown?.dasha_sync || 0}%`} isBonus />
        </div>
      </div>

      {/* Question-Level Transit Evidence */}
      {questionResults.length > 0 && (
        <div className="bg-white rounded-lg p-4 border border-green-200">
          <h4 className="font-bold text-green-800 mb-4">Question-Level Transit Evidence</h4>
          <div className="space-y-3">
            {questionResults.map((qr: any, idx: number) => (
              <div key={idx} className="p-3 bg-green-50 rounded">
                <div className="font-bold text-green-700">{qr.question_title || qr.question}</div>
                <div className="flex gap-4 text-xs text-gray-600 mt-1">
                  <span>Transit: {qr.transit?.activation_score || '—'}</span>
                  <span>Dasha: {qr.timing?.dasha_strength || '—'}</span>
                  <span className="font-bold text-indigo-600">Final: {qr.probability?.score || '—'}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  </details>
);

const FormulaRow: React.FC<{ 
  label: string; value: string; weight?: string; isDeduction?: boolean; isTotal?: boolean 
}> = ({ label, value, weight, isDeduction, isTotal }) => (
  <div className={`flex justify-between p-2 rounded ${isTotal ? 'bg-green-100 font-bold border border-green-300' : isDeduction ? 'bg-red-50' : 'bg-green-50'}`}>
    <span>{label}</span>
    <span className="font-mono">{value} {weight ? `× ${weight}` : ''}</span>
  </div>
);

const SyncRow: React.FC<{ label: string; planet: string; strength: string; isBonus?: boolean }> = ({ 
  label, planet, strength, isBonus 
}) => (
  <div className={`flex justify-between p-2 rounded ${isBonus ? 'bg-emerald-100 border border-emerald-300' : 'bg-gray-50'}`}>
    <span className="font-medium">{label} ({planet})</span>
    <span className={`font-bold ${isBonus ? 'text-emerald-600' : 'text-gray-900'}`}>{strength}</span>
  </div>
);

// ============================================
// UTILITY FUNCTIONS & SMALL COMPONENTS
// ============================================

function getSignForHouse(house: number): string {
  const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
  return signs[(house - 1) % 12];
}

function getSupportedAreas(domains: Record<string, number>, natalPromise: any) {
  return Object.entries(domains)
    .filter(([_, score]) => score >= 65)
    .map(([name, score]) => ({ name: name.charAt(0).toUpperCase() + name.slice(1), score: Math.round(score) }));
}

function getCautionAreas(domains: Record<string, number>, natalPromise: any) {
  return Object.entries(domains)
    .filter(([_, score]) => score < 40)
    .map(([name, score]) => ({ name: name.charAt(0).toUpperCase() + name.slice(1), score: Math.round(score) }));
}

function getNextTransitEvent(transit: any): string {
  if (transit.confidence_flags?.includes('saturn_sadesati')) return 'Sade Sati Phase Transition';
  if (transit.confidence_flags?.includes('jupiter_transit_positive')) return 'Jupiter Favourable Transit';
  if (transit.confidence_flags?.includes('dasha_lord_transiting')) return 'Dasha Lord Transit';
  return 'Next Planetary Ingress';
}

function getPrimaryDomainForNextEvent(transit: any): string {
  const domains = transit.activated_domains || {};
  const maxEntry = Object.entries(domains).reduce((a, b) => a[1] > b[1] ? a : b, ['', 0]);
  return maxEntry[0] ? maxEntry[0].charAt(0).toUpperCase() + maxEntry[0].slice(1) : 'General';
}

function getSupportedHousesForDomain(domain: string, transit: any): string[] {
  const factors = [...(transit.supporting_factors || [])];
  const houses = new Set<number>();
  factors.forEach(f => {
    if (f.house && f.house > 0 && f.house <= 12) houses.add(f.house);
  });
  return Array.from(houses).map(h => `${h}H`).slice(0, 4);
}

const ExpertMetric: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="bg-white rounded-lg p-3 border border-gray-200">
    <div className="text-xs text-gray-500 uppercase tracking-wider">{label}</div>
    <div className="font-bold text-gray-900">{value}</div>
  </div>
);

function getGrade(value: number): string {
  if (value >= 80) return 'EXCELLENT';
  if (value >= 65) return 'VERY GOOD';
  if (value >= 50) return 'GOOD';
  if (value >= 35) return 'WEAK';
  return 'TOO WEAK';
}

function getGradeColor(grade: string): string {
  switch (grade) {
    case 'EXCELLENT': return 'bg-emerald-100 text-emerald-800';
    case 'VERY GOOD': return 'bg-blue-100 text-blue-800';
    case 'GOOD': return 'bg-green-100 text-green-800';
    case 'WEAK': return 'bg-yellow-100 text-yellow-800';
    case 'TOO WEAK': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
}

function formatDate(dateStr: string): string {
  if (!dateStr || dateStr === 'Unknown') return 'Unknown';
  try {
    return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  } catch {
    return dateStr;
  }
}}
