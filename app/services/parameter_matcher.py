import re

from app.models.parameter_alias import ParameterAlias


class ParameterMatcher:

    @staticmethod
    def normalize(text):
        """
        Normalize text for simple matching.
        """

        if not text:
            return ""

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9]+",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    @staticmethod
    def get_candidates(text):
        """
        Find possible laboratory parameters locally.

        Claude will only receive parameters that appear
        relevant to this OCR text.
        """

        normalized_text = ParameterMatcher.normalize(
            text
        )

        aliases = ParameterAlias.query.all()

        candidates = {}

        for alias_obj in aliases:

            parameter = alias_obj.parameter

            if not parameter:
                continue

            alias = alias_obj.alias

            if not alias:
                continue

            normalized_alias = (
                ParameterMatcher.normalize(alias)
            )

            if not normalized_alias:
                continue

            # Avoid dangerous one/two-character aliases
            if len(normalized_alias) < 3:
                continue

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(normalized_alias)
                + r"(?![a-z0-9])"
            )
            if re.search(
                pattern,
                normalized_text
            ):

            # Exact normalized phrase presence
            # if normalized_alias in normalized_text:

                candidates[parameter.id] = {
                    "id": parameter.id,
                    "name": parameter.parameter_name,
                    "unit": parameter.unit,
                    # "normal_min": parameter.normal_min,
                    # "normal_max": parameter.normal_max,
                    "matched_alias": alias
                }

        return list(candidates.values())