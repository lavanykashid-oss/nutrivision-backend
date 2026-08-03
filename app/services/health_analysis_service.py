from app.config.database import db

from app.models.health_parameter import HealthParameter
from app.models.health_analysis import HealthAnalysis


class HealthAnalysisService:

    @staticmethod
    def analyze(report):

        parameters = HealthParameter.query.filter_by(
            report_id=report.id
        ).all()

        HealthAnalysis.query.filter_by(
    report_id=report.id
).delete()

        findings = []
        recommendations = []

        score = 100

        risk = "Low"

        for p in parameters:

            print(
                p.parameter.parameter_name,
                p.value,
                p.flag
            )

            if p.flag == "Low":

                score -= 5

                findings.append(
                    f"{p.parameter.parameter_name} is Low"
                )

                if p.parameter.deficiency_message:
                    findings.append(
                        p.parameter.deficiency_message
                    )

                if p.parameter.recommendation:
                    recommendations.append(
                        p.parameter.recommendation
                    )

            elif p.flag == "High":

                score -= 5

                findings.append(
                    f"{p.parameter.parameter_name} is High"
                )

                if p.parameter.excess_message:
                    findings.append(
                        p.parameter.excess_message
                    )

                if p.parameter.recommendation:
                    recommendations.append(
                        p.parameter.recommendation
                    )

        if score < 80:
            risk = "Moderate"

        if score < 60:
            risk = "High"

        analysis = HealthAnalysis(

            user_id=report.user_id,

            report_id=report.id,

             health_score=score,

             risk_level=risk,

             findings="\n".join(findings),

             deficiencies="\n".join(findings),

             recommendations="\n".join(recommendations),

             follow_up="Consult a physician if abnormalities",

             ai_model="Rule Based v1"

           )

        db.session.add(analysis)

        db.session.commit()

        return True