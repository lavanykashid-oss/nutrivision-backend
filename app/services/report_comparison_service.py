from app.models.health_report import HealthReport
from app.models.health_parameter import HealthParameter

class ReportComparisonService:

    @staticmethod
    def get_previous_report(current_report):

        return (
            HealthReport.query
            .filter(
                HealthReport.user_id == current_report.user_id,
                HealthReport.id < current_report.id
            )
            .order_by(HealthReport.id.desc())
            .first()
        )

    @staticmethod
    def compare(current_report):

        previous = ReportComparisonService.get_previous_report(current_report)

        if previous is None:

            return {
                "current_report": current_report.id,
                "previous_report": None,
                "comparison": []
            }

        current_params = {
            p.parameter.parameter_name: p
            for p in current_report.parameters
        }

        previous_params = {
            p.parameter.parameter_name: p
            for p in previous.parameters
        }

        comparison = []

        for name in current_params:

            if name not in previous_params:
                continue

            old = previous_params[name]
            new = current_params[name]

            change = new.value - old.value

            if change > 0:
                trend = "increase"
            elif change < 0:
                trend = "decrease"
            else:
                trend = "same"

            comparison.append({

                "parameter": name,

                "previous": old.value,

                "current": new.value,

                "difference": round(change, 2),

                "percent_change": round(
                    (change / old.value) * 100,
                    2
                ) if old.value else 0,

                "trend": trend,

                "old_flag": old.flag,

                "new_flag": new.flag

            })

        return {

            "current_report": current_report.id,

            "previous_report": previous.id,

            "comparison": comparison

        }


    @staticmethod
    def parameter_history(user_id, parameter_name):

        history = (
            HealthParameter.query
            .join(HealthReport)
            .join(HealthParameter.parameter)
            .filter(
                HealthReport.user_id == user_id
            )
            .order_by(HealthReport.id)
            .all()
        )

        trend = []

        for item in history:

            if item.parameter.parameter_name != parameter_name:
                continue

            trend.append({

                "report_id": item.report.id,

                "date": item.report.created_at.strftime("%d-%m-%Y"),

                "value": item.value,

                "flag": item.flag

            })

        return trend