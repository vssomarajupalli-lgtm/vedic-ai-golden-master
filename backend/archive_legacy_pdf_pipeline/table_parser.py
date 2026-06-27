class TableParser:
    """
    Parses raw 2D list grids from PDF table extractions into a structured
    dictionary. This class is designed to be deterministic and fault-tolerant,
    rejecting malformed rows instead of crashing.
    """
    def parse(self, raw_grid: list[list[str]]) -> dict:
        """
        Parses the planetary positions table.

        Args:
            raw_grid: A list of lists representing the raw table data.

        Returns:
            A dictionary containing structured planet data and extraction metadata.
        """
        planets = {}
        rejected_rows = []
        parsed_count = 0

        for idx, row in enumerate(raw_grid):
            if not row:
                rejected_rows.append({"row_index": idx, "raw_data": row, "reason": "empty_row"})
                continue
            
            if len(row) < 6:
                rejected_rows.append({"row_index": idx, "raw_data": row, "reason": "malformed_row"})
                continue
                
            planet_name = row[0].strip()
            if not planet_name:
                rejected_rows.append({"row_index": idx, "raw_data": row, "reason": "empty_first_column"})
                continue
                
            if planet_name.lower() == "planet":
                rejected_rows.append({"row_index": idx, "raw_data": row, "reason": "header_row"})
                continue
                
            planets[planet_name] = {
                "sign": row[1],
                "longitude": row[2],
                "nakshatra": row[3],
                "pada": row[4],
                "retrograde": row[5]
            }
            parsed_count += 1

        return {
            "planets": planets,
            "extraction_metadata": {
                "status": "success", "total_parsed": parsed_count, "rejected_rows": rejected_rows
            },
        }