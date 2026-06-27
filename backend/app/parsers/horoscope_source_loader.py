import json
import os
from pathlib import Path
from typing import Any, Dict, List

class HoroscopeSourceLoader:
    """
    Loads structured horoscope data produced by HoroscopeCleaner_Final.

    Reads two source files:
      - machine_index.json  : Navigation brain (section titles, page ranges)
      - canonical_content.json : Knowledge brain (planets, dashas, vargas, etc.)

    Produces a raw_input_data dict that is passed directly to JsonNormalizer.normalize().

    Architecture Rules:
      - This class never reads PDFs. (Rule 13)
      - This class contains zero astrological calculations. (Rule 4)
      - All type coercion and schema enforcement is deferred to JsonNormalizer. (Rule 6)
      - Uses stdlib only: json, os, pathlib, typing. (Rule 14)
    """

    def __init__(self, index_path: str, content_path: str):
        """
        Initializes the loader with paths to both required source files.

        Args:
            index_path (str): Absolute or relative path to machine_index.json
            content_path (str): Absolute or relative path to canonical_content.json

        Raises:
            FileNotFoundError: If either file does not exist on disk.
        """
        self.index_path = Path(index_path)
        self.content_path = Path(content_path)

        # Fail fast on missing files - do not silently continue with empty data.
        if not self.index_path.exists():
            raise FileNotFoundError(
                f"[HoroscopeSourceLoader] machine_index.json not found: {self.index_path}"
            )
        if not self.content_path.exists():
            raise FileNotFoundError(
                f"[HoroscopeSourceLoader] canonical_content.json not found: {self.content_path}"
            )

        # Internal diagnostic log populated during load()
        self._warnings: List[str] = []
        self._sections_found: List[str] = []
        self._sections_missing: List[str] = []

    def load(self) -> dict:
        """
        Main entry point. Loads both source files and returns a raw_input_data dict
        ready for JsonNormalizer.normalize().

        Returns:
            dict: A raw_input_data payload containing:
                - raw_metadata   : Birth details (name, lagna, degree)
                - raw_planets    : Raw planet data keyed by planet name
                - raw_vargas     : Raw varga chart data (D9, D10, etc.)
                - raw_dashas     : Active dasha lords (MD, AD, PD)
                - raw_houses     : Raw house data (passed through for future normalizer use)
                - _load_report   : Diagnostic summary (warnings, sections found/missing)
        """
        self._warnings = []
        self._sections_found = []
        self._sections_missing = []

        # 1. Load both JSON files defensively
        machine_index = self._load_json(self.index_path)
        canonical_content = self._load_json(self.content_path)

        # 2. Build the section navigation map from machine_index.json
        #    Used for diagnostics and future routing, not gating data extraction.
        section_map = self._build_section_map(machine_index)

        # 3. Extract all astrology data from canonical_content.json
        raw_metadata       = self._extract_metadata(canonical_content)
        raw_planets        = self._extract_planets(canonical_content)
        raw_vargas         = self._extract_vargas(canonical_content)
        raw_dashas         = self._extract_dashas(canonical_content)
        raw_houses         = self._extract_houses(canonical_content)
        raw_ashtakavarga   = self._extract_ashtakavarga(canonical_content)
        raw_doshas         = self._extract_doshas(canonical_content)

        # 4. Assemble the final raw_input_data payload
        return {
            "raw_metadata":     raw_metadata,
            "raw_planets":      raw_planets,
            "raw_vargas":       raw_vargas,
            "raw_dashas":       raw_dashas,
            "raw_houses":       raw_houses,
            "raw_ashtakavarga": raw_ashtakavarga,
            "raw_doshas":       raw_doshas,
            "_load_report":     self._build_load_report(section_map)
        }

    # -------------------------------------------------------------------------
    # File Loading
    # -------------------------------------------------------------------------

    def _load_json(self, path: Path) -> dict:
        """
        Loads and parses a JSON file. Raises a clear, path-specific error on failure.

        Args:
            path (Path): Path to the JSON file.

        Returns:
            dict: Parsed JSON content.

        Raises:
            ValueError: If the file content is not valid JSON.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"[HoroscopeSourceLoader] Invalid JSON in {path}: {e}"
            ) from e

    # -------------------------------------------------------------------------
    # Section Map (machine_index.json)
    # -------------------------------------------------------------------------

    def _build_section_map(self, machine_index: dict) -> Dict[str, Dict[str, Any]]:
        """
        Builds a normalized section navigation map from machine_index.json.

        Accepts two common shapes:
          Shape A (list):
            [{"title": "Planetary Positions", "from_page": 4, "to_page": 11}, ...]
          Shape B (dict):
            {"planetary_positions": {"from": 4, "to": 11}, ...}

        Args:
            machine_index (dict or list): Loaded machine_index.json content.

        Returns:
            dict: Normalized section map keyed by lowercase section title.
        """
        section_map = {}

        if isinstance(machine_index, list):
            # Shape A: list of section objects
            for entry in machine_index:
                if not isinstance(entry, dict):
                    continue
                title = str(entry.get("title", "")).strip().lower()
                if not title:
                    continue
                section_map[title] = {
                    "from_page": int(entry.get("from_page", entry.get("from", 0))),
                    "to_page":   int(entry.get("to_page",   entry.get("to",   0)))
                }

        elif isinstance(machine_index, dict):
            # Shape B: dict of section_key -> {from, to} or {from_page, to_page}
            for key, value in machine_index.items():
                if not isinstance(value, dict):
                    continue
                from_page = value.get("from_page", value.get("from", 0))
                to_page   = value.get("to_page",   value.get("to",   0))
                section_map[key.lower()] = {
                    "from_page": int(from_page),
                    "to_page":   int(to_page)
                }

        else:
            self._warnings.append(
                f"machine_index.json has unexpected root type: {type(machine_index).__name__}. "
                f"Expected dict or list. Section map will be empty."
            )

        return section_map

    # -------------------------------------------------------------------------
    # Data Extractors (canonical_content.json)
    # -------------------------------------------------------------------------

    def _extract_metadata(self, content: dict) -> dict:
        """
        Extracts birth/native metadata from canonical_content.json.

        Looks for data under these common section keys (in priority order):
          - "birth_data"
          - "metadata"
          - "native"
          - top-level keys (name, lagna, etc.)

        Args:
            content (dict): Loaded canonical_content.json.

        Returns:
            dict: raw_metadata dict with name, lagna, lagna_degree fields.
        """
        section_keys = ["birth_data", "metadata", "native"]
        source = {}

        for key in section_keys:
            if key in content:
                source = content[key]
                self._sections_found.append(key)
                break

        if not source:
            # Fall back to reading top-level keys directly
            self._sections_missing.append("birth_data / metadata")
            self._warnings.append(
                "No birth_data or metadata section found in canonical_content.json. "
                "Attempting top-level key extraction for name/lagna."
            )
            source = content

        return {
            "name":         source.get("name", ""),
            "lagna":        source.get("lagna", source.get("ascendant", source.get("lagna_sign", ""))),
            "lagna_degree": source.get("lagna_degree", source.get("ascendant_degree", 0.0))
        }

    def _extract_planets(self, content: dict) -> dict:
        """
        Extracts raw planet data from canonical_content.json.

        Expected section key: "planets"

        The full planet dict is passed through without modification.
        JsonNormalizer is responsible for all type coercion and defaults.

        Args:
            content (dict): Loaded canonical_content.json.

        Returns:
            dict: Raw planets dict keyed by planet name (as in source).
                  Returns {} if section is missing.
        """
        if "planets" not in content:
            self._sections_missing.append("planets")
            self._warnings.append(
                "No 'planets' section found in canonical_content.json. "
                "Planet engine will receive empty input."
            )
            return {}

        self._sections_found.append("planets")
        planets_raw = content["planets"]

        if not isinstance(planets_raw, dict):
            self._warnings.append(
                f"'planets' section has unexpected type: {type(planets_raw).__name__}. "
                f"Expected dict. Returning empty."
            )
            return {}

        return planets_raw

    def _extract_vargas(self, content: dict) -> dict:
        """
        Extracts raw Varga chart data from canonical_content.json.

        Expected section key: "vargas" or "shodasha_vargas"

        Args:
            content (dict): Loaded canonical_content.json.

        Returns:
            dict: Raw vargas dict (e.g. {"D9": {"planets": {...}}, "D10": {...}}).
                  Returns {} if section is missing.
        """
        for key in ("vargas", "shodasha_vargas", "divisional_charts"):
            if key in content:
                self._sections_found.append(key)
                vargas_raw = content[key]
                if isinstance(vargas_raw, dict):
                    return vargas_raw
                else:
                    self._warnings.append(
                        f"'{key}' section has unexpected type: {type(vargas_raw).__name__}. "
                        f"Expected dict. Returning empty."
                    )
                    return {}

        self._sections_missing.append("vargas")
        self._warnings.append(
            "No 'vargas' section found in canonical_content.json. "
            "Varga engine will receive empty input."
        )
        return {}

    def _extract_dashas(self, content: dict) -> dict:
        """
        Extracts the active Vimshottari Dasha lords from canonical_content.json.

        Expected section key: "dashas" or "dasha"

        Handles two common shapes:
          Shape A (flat):
            {"mahadasha": "Shani", "antardasha": "Budha", "pratyantardasha": "Guru"}
          Shape B (nested):
            {"mahadasha": {"lord": "Shani"}, "antardasha": {"lord": "Budha"}, ...}

        Args:
            content (dict): Loaded canonical_content.json.

        Returns:
            dict: raw_dashas with mahadasha, antardasha, pratyantardasha keys.
        """
        dasha_source = {}
        for key in ("dashas", "dasha", "vimshottari"):
            if key in content:
                self._sections_found.append(key)
                dasha_source = content[key]
                break

        if not dasha_source:
            self._sections_missing.append("dashas")
            self._warnings.append(
                "No 'dashas' section found in canonical_content.json. "
                "Dasha engine will receive empty input."
            )
            return {"mahadasha": "", "antardasha": "", "pratyantardasha": ""}

        def _extract_lord(value: Any) -> str:
            """Handles both flat string and nested {lord: ...} shapes."""
            if isinstance(value, str):
                return value
            if isinstance(value, dict):
                return str(value.get("lord", ""))
            return ""

        return {
            "mahadasha":       _extract_lord(dasha_source.get("mahadasha", "")),
            "antardasha":      _extract_lord(dasha_source.get("antardasha", "")),
            "pratyantardasha": _extract_lord(dasha_source.get("pratyantardasha", "")),
            "timeline":        dasha_source.get("timeline", []),
            "birth_balance":   dasha_source.get("birth_balance", {})
        }

    def _extract_houses(self, content: dict) -> dict:
        """
        Extracts raw house data from canonical_content.json.

        This data is passed through to the raw payload for future use.
        JsonNormalizer currently returns {} for houses — this will be consumed
        once the normalizer's _normalize_houses() method is implemented.

        Expected section key: "houses" or "bhavas"

        Args:
            content (dict): Loaded canonical_content.json.

        Returns:
            dict: Raw houses dict keyed by house number (as string).
                  Returns {} if section is missing.
        """
        for key in ("houses", "bhavas", "bhava"):
            if key in content:
                self._sections_found.append(key)
                houses_raw = content[key]
                if isinstance(houses_raw, dict):
                    return houses_raw
                else:
                    self._warnings.append(
                        f"'{key}' section has unexpected type: {type(houses_raw).__name__}. "
                        f"Expected dict. Returning empty."
                    )
                    return {}

        self._sections_missing.append("houses")
        # Houses missing is not yet a blocking warning since JsonNormalizer
        # doesn't consume them yet. Log for diagnostic purposes only.
        return {}

    def _extract_ashtakavarga(self, content: dict) -> dict:
        """
        Extracts Ashtakavarga data (SAV chart + BAV charts) from canonical_content.json.

        Expected section key: "ashtakavarga"

        Expected structure:
            {
                "sav_chart":  {"1": 26, "2": 25, ..., "12": 0},
                "bav_charts": {
                    "Surya":  {"1": 5, "2": 4, ..., "12": 1},
                    "Chandra": {...},
                    ...
                }
            }

        Both sav_chart and bav_charts are passed through without modification.
        All type coercion and key normalization is handled by JsonNormalizer.

        Args:
            content (dict): Loaded canonical_content.json.

        Returns:
            dict: Raw ashtakavarga dict with sav_chart and bav_charts keys.
                  Returns {"sav_chart": {}, "bav_charts": {}} if section is missing.
        """
        for key in ("ashtakavarga", "ashtaka_varga", "av"):
            if key in content:
                self._sections_found.append(key)
                av_raw = content[key]
                if not isinstance(av_raw, dict):
                    self._warnings.append(
                        f"'{key}' section has unexpected type: {type(av_raw).__name__}. "
                        f"Expected dict. Returning empty."
                    )
                    return {"sav_chart": {}, "bav_charts": {}}
                return {
                    "sav_chart":  av_raw.get("sav_chart",  {}),
                    "bav_charts": av_raw.get("bav_charts", {})
                }

        self._sections_missing.append("ashtakavarga")
        self._warnings.append(
            "No 'ashtakavarga' section found in canonical_content.json. "
            "AshtakavargaEngine will receive empty input."
        )
        return {"sav_chart": {}, "bav_charts": {}}

    def _extract_doshas(self, content: dict) -> dict:
        """
        Extracts raw Dosha data from canonical_content.json.
        """
        for key in ("doshas", "dosha"):
            if key in content:
                self._sections_found.append(key)
                doshas_raw = content[key]
                if isinstance(doshas_raw, dict):
                    return doshas_raw
                else:
                    self._warnings.append(
                        f"'{key}' section has unexpected type: {type(doshas_raw).__name__}. "
                        f"Expected dict. Returning empty."
                    )
                    return {}

        self._sections_missing.append("doshas")
        # Doshas missing is not a blocking warning as many charts have no doshas
        return {}

    # -------------------------------------------------------------------------
    # Diagnostic Report
    # -------------------------------------------------------------------------

    def _build_load_report(self, section_map: dict) -> dict:
        """
        Builds a diagnostic summary of the load operation.

        Provides visibility into what was found, what was missing, and any
        warnings raised during extraction — enabling explainable, auditable loads.

        Args:
            section_map (dict): The normalized section map from machine_index.json.

        Returns:
            dict: Load report with status, sections_found, sections_missing, warnings.
        """
        status = "success" if not self._warnings else "success_with_warnings"
        if self._sections_missing and not self._sections_found:
            status = "degraded"

        return {
            "status":           status,
            "index_path":       str(self.index_path),
            "content_path":     str(self.content_path),
            "sections_found":   sorted(self._sections_found),
            "sections_missing": sorted(self._sections_missing),
            "section_map":      section_map,
            "warnings":         list(self._warnings)
        }
