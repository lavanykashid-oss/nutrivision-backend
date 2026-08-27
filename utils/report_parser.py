import json

from app.providers.claude_provider import ClaudeProvider
from app.services.parameter_matcher import ParameterMatcher
from app.services.report_chunker import ReportChunker
from app.services.evidence_extractor import EvidenceExtractor
from app.services.local_result_extractor import LocalResultExtractor


class ReportParser:

    # ============================================================
    # MAIN REPORT PARSER
    # ============================================================

    @staticmethod
    def parse_report(text: str):

        if not text:
            return {
                "metadata": {},
                "parameters": {}
            }

        print("=" * 80)
        print("REPORT PARSER STARTED")
        print("=" * 80)

        # --------------------------------------------------------
        # Split OCR into pages / chunks
        # --------------------------------------------------------

        chunks = ReportChunker.split_text(
            text,
            max_chars=12000
        )

        print(
            f"Total OCR chunks: {len(chunks)}"
        )

        provider = ClaudeProvider()

        merged_parameters = {}
        metadata = {}

        # ========================================================
        # PROCESS EACH CHUNK
        # ========================================================

        for index, chunk in enumerate(
            chunks,
            start=1
        ):

            print("=" * 80)
            print(
                f"PROCESSING CHUNK "
                f"{index}/{len(chunks)}"
            )
            print(
                f"Chunk characters: "
                f"{len(chunk)}"
            )

            # ----------------------------------------------------
            # 1. FIND LOCAL CANDIDATES
            # ----------------------------------------------------

            candidates = (
                ParameterMatcher.get_candidates(
                    chunk
                )
            )

            print(
                f"Local candidates found: "
                f"{len(candidates)}"
            )

            if not candidates:

                print(
                    "No candidates. "
                    "Skipping chunk."
                )

                continue

            # ----------------------------------------------------
            # 2. BUILD SMALL EVIDENCE SECTION
            # ----------------------------------------------------

            evidence = (
                EvidenceExtractor.extract(
                    chunk,
                    candidates
                )
            )

            print(
                f"Evidence characters: "
                f"{len(evidence)}"
            )

            if not evidence:

                print(
                    "No useful evidence. "
                    "Skipping chunk."
                )

                continue

            # ----------------------------------------------------
            # 3. EXTRACT EASY RESULTS LOCALLY
            # ----------------------------------------------------

            (
                local_results,
                unresolved
            ) = LocalResultExtractor.extract(
                evidence,
                candidates
            )

            print(
                f"Local extracted: "
                f"{len(local_results)}"
            )

            print(
                f"Claude unresolved: "
                f"{len(unresolved)}"
            )

            # ----------------------------------------------------
            # 4. MERGE LOCAL RESULTS
            # ----------------------------------------------------

            for (
                parameter_id,
                data
            ) in local_results.items():

                # Keep first trusted result.
                if (
                    parameter_id
                    not in merged_parameters
                ):

                    merged_parameters[
                        parameter_id
                    ] = data

            # ----------------------------------------------------
            # 5. NOTHING LEFT FOR CLAUDE
            # ----------------------------------------------------

            if not unresolved:

                print(
                    "All candidates extracted "
                    "locally. Skipping Claude."
                )

                continue

            # ----------------------------------------------------
            # 6. REMOVE ALREADY RESOLVED PARAMETERS
            #
            # Important:
            # If parameter was extracted correctly on an earlier
            # page, do not waste Claude tokens asking again.
            # ----------------------------------------------------

            unresolved = [
                candidate
                for candidate in unresolved
                if int(candidate["id"])
                not in merged_parameters
            ]

            print(
                f"Claude unresolved after "
                f"deduplication: "
                f"{len(unresolved)}"
            )

            if not unresolved:

                print(
                    "All unresolved candidates "
                    "already found on earlier pages. "
                    "Skipping Claude."
                )

                continue

            # ----------------------------------------------------
            # 7. BUILD SMALL CLAUDE PROMPT
            # ----------------------------------------------------

            prompt = (
                ReportParser.build_prompt(
                    evidence,
                    unresolved
                )
            )

            print(
                f"Claude prompt characters: "
                f"{len(prompt)}"
            )

            # ----------------------------------------------------
            # 8. CALL CLAUDE
            # ----------------------------------------------------

            try:

                result = (
                    provider.generate_json(
                        prompt
                    )
                )

            except Exception as e:

                print("=" * 80)
                print(
                    f"CLAUDE ERROR ON "
                    f"CHUNK {index}"
                )
                print(e)
                print("=" * 80)

                # Do not kill whole report
                # because one chunk failed.
                continue

            # ----------------------------------------------------
            # 9. VALIDATE CLAUDE RESPONSE
            # ----------------------------------------------------

            if not isinstance(
                result,
                dict
            ):

                print(
                    f"Invalid Claude result "
                    f"for chunk {index}"
                )

                continue

            # ----------------------------------------------------
            # 10. VALIDATION MAP
            #
            # Claude may ONLY return unresolved candidates
            # supplied in this prompt.
            # ----------------------------------------------------

            candidate_map = {

                int(candidate["id"]):
                    candidate

                for candidate in unresolved
            }

            claude_parameters = (
                result.get(
                    "parameters",
                    []
                )
            )

            # ----------------------------------------------------
            # 11. PROCESS CLAUDE RESULTS
            # ----------------------------------------------------

            for item in claude_parameters:

                try:

                    parameter_id = int(
                        item.get(
                            "parameter_id"
                        )
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    continue

                # Claude returned something
                # not supplied to it.
                candidate = (
                    candidate_map.get(
                        parameter_id
                    )
                )

                if not candidate:
                    continue

                # Already resolved locally/
                # by earlier chunk.
                if (
                    parameter_id
                    in merged_parameters
                ):
                    continue

                value = item.get(
                    "value"
                )

                if value is None:
                    continue

                # ------------------------------------------------
                # Numeric strings
                # ------------------------------------------------

                if isinstance(
                    value,
                    str
                ):

                    value = (
                        value.strip()
                    )

                    if not value:
                        continue

                    value = (
                        value.replace(
                            ",",
                            ""
                        )
                    )

                    try:

                        value = float(
                            value
                        )

                    except ValueError:

                        print(
                            "Skipping "
                            "non-numeric value:",
                            value
                        )

                        continue

                if not isinstance(
                    value,
                    (int, float)
                ):
                    continue

                # ------------------------------------------------
                # MERGE CLAUDE RESULT
                # ------------------------------------------------

                merged_parameters[
                    parameter_id
                ] = {

                    "parameter_name":
                        candidate["name"],

                    "parameter_id":
                        parameter_id,

                    "value":
                        float(value),

                    "matched_alias":
                        candidate.get(
                            "matched_alias"
                        ),

                    "unit":
                        item.get(
                            "unit"
                        )
                        or candidate.get(
                            "unit"
                        ),

                    "source":
                        "claude"
                }

        # ========================================================
        # FINAL RESULT
        # ========================================================

        print("=" * 80)
        print(
            "REPORT PARSER COMPLETED"
        )
        print(
            "Total unique parameters:",
            len(merged_parameters)
        )
        print("=" * 80)

        for (
            parameter_id,
            data
        ) in merged_parameters.items():

            print(
                f"{data['parameter_name']} "
                f"-> {data['value']} "
                f"(ID: {parameter_id}, "
                f"source: "
                f"{data.get('source', 'unknown')})"
            )

        return {
            "metadata": metadata,
            "parameters": merged_parameters
        }

    # ============================================================
    # COMPACT CLAUDE PROMPT
    # ============================================================

    @staticmethod
    def build_prompt(
        text,
        candidates
    ):

        # --------------------------------------------------------
        # Only send fields Claude actually needs.
        #
        # Do NOT send:
        # normal_min
        # normal_max
        # matched_alias
        # category
        #
        # This saves tokens.
        # --------------------------------------------------------

        compact_candidates = [

            {
                "id":
                    candidate["id"],

                "name":
                    candidate["name"],

                "unit":
                    candidate.get(
                        "unit"
                    )
            }

            for candidate
            in candidates
        ]

        candidate_json = json.dumps(
            compact_candidates,
            separators=(",", ":"),
            ensure_ascii=False
        )

        # --------------------------------------------------------
        # Compact prompt
        # --------------------------------------------------------

        return f"""Extract explicit laboratory results.

Rules:
- Use only candidate IDs below.
- Value must belong to the test row.
- Ignore reference ranges, dates, IDs, methods and notes.
- Do not calculate or infer.
- If uncertain, omit.
- Return JSON only.

Format:
{{"parameters":[{{"parameter_id":1,"value":13.5,"unit":"g/dL"}}]}}

Candidates:
{candidate_json}

Text:
{text}
"""