from flask import Blueprint, request, jsonify
from app.models.user import User

from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.report_upload_service import ReportUploadService

from app.services.dashboard_service import DashboardService

from app.services.health_report_service import HealthReportService


from app.services.report_comparison_service import ReportComparisonService

import os

from app.config.database import db

from app.models.health_report import HealthReport
from app.models.health_parameter import HealthParameter
from app.models.health_analysis import HealthAnalysis

health_report_bp = Blueprint(
    "health_report",
    __name__
)


@health_report_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_report():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if "report" not in request.files:
        return jsonify({"message": "No report uploaded"}), 400

    file = request.files["report"]

    report = ReportUploadService.upload(
        file=file,
        user_id=user.id
    )

    return jsonify({
        "report_id": report.id,
        "status": report.status,
        "report_name": report.report_name
    })

@health_report_bp.route(
    "/report/<int:report_id>",
    methods=["GET"]
)
@jwt_required()
def get_report(report_id):

    user_id = get_jwt_identity()

    report = HealthReportService.get_report(report_id)

    if not report:
        return jsonify({
            "message": "Report not found"
        }), 404

    if report.user_id != int(user_id):
        return jsonify({
            "message": "Unauthorized"
        }), 403

    return jsonify({
        "id": report.id,
        "report_name": report.report_name,
        "report_type": report.report_type,
        "patient_name": report.patient_name,
        "age": report.age,
        "gender": report.gender,
        "referred_by": report.referred_by,
        "report_date": (
            report.report_date.strftime("%d-%m-%y")
        if report.report_date
        else None),
        
        "laboratory": report.laboratory,
        "status": report.status,
        "created_at": report.created_at,
        "parameters": [
            {
                "name": p.parameter.parameter_name,
                "value": p.value,
                "unit": p.unit,
                "flag": p.flag,
                "reference_low": p.reference_low,
                "reference_high": p.reference_high
            }
            for p in report.parameters
        ],
        "analysis": {
            "score": report.analysis.health_score,
            "risk": report.analysis.risk_level,
            "summary": report.analysis.findings,
            "deficiencies": report.analysis.deficiencies,
            "recommendations": report.analysis.recommendations,
            "follow_up": report.analysis.follow_up
        } if report.analysis else None
    })





@health_report_bp.route(
    "/history",
    methods=["GET"]
)
@jwt_required()
def history():

    user_id = get_jwt_identity()

    reports = HealthReportService.get_user_report(
        int(user_id)
    )

    return jsonify([
        {
            "id": r.id,
            "report_name": r.report_name,
            "status": r.status,
            "date": r.created_at,
            "score": (
                r.analysis.health_score
                if r.analysis
                else None
            )
        }
        for r in reports
    ])




@health_report_bp.route(
    "/dashboard",
    methods=["GET"]
)
@jwt_required()
def dashboard():

    user_id = int(get_jwt_identity())

    data = DashboardService.get_dashboard(user_id)

    if not data:

        return jsonify({
            "message": "No reports found"
        }), 404

    report = data["latest_report"]
    analysis = data["analysis"]

    return jsonify({

        "health_score": analysis.health_score,

        "risk_level": analysis.risk_level,

        "latest_report": {

            "id": report.id,

            "report_name": report.report_name,

            "date": report.created_at

        },

        "findings": (
            analysis.deficiencies.split("\n")
            if analysis.deficiencies
            else[]
        ),

        "recommendations": (
            analysis.recommendations.split("\n")
            if analysis.recommendations
            else []
        )
    })



@health_report_bp.route(
    "/compare/<int:report_id>",
    methods=["GET"]
)
@jwt_required()
def compare_reports(report_id):

    user_id = int(get_jwt_identity())

    report = HealthReportService.get_report(report_id)

    if report is None:
        return jsonify({
            "message": "Report not found"
        }), 404

    if report.user_id != user_id:
        return jsonify({
            "message": "Unauthorized"
        }), 403

    comparison = ReportComparisonService.compare(report)

    return jsonify(comparison)



@health_report_bp.route(
    "/trend/<string:parameter_name>",
    methods=["GET"]
)
@jwt_required()
def parameter_trend(parameter_name):

    user_id = int(get_jwt_identity())

    trend = ReportComparisonService.parameter_history(
        user_id,
        parameter_name
    )

    return jsonify(trend)

@health_report_bp.route(
    "/reports",
    methods=["GET"]
)
@jwt_required()
def get_reports():

    user_id = int(get_jwt_identity())

    reports = HealthReportService.get_user_report(user_id)

    response = []

    for report in reports:

        abnormal = 0
        normal = 0

        for p in report.parameters:
            if p.flag in ["High", "Low"]:
                abnormal += 1
            else:
                normal += 1

        response.append({
            "id": report.id,
            "patient_name": report.patient_name,
            "report_type": report.report_type,
            "laboratory": report.laboratory,
            "report_name": report.report_name,
            "uploaded_date": report.created_at,
            "report_date": report.report_date,
            "referred_by": report.referred_by,
            "total_tests": len(report.parameters),
            "abnormal": abnormal,
            "normal": normal
        })

    return jsonify(response)

@health_report_bp.route("/report/<int:report_id>", methods=["DELETE"])
@jwt_required()
def delete_health_report(report_id):

    try:
        user_id = get_jwt_identity()

        report = HealthReport.query.filter_by(
            id=report_id,
            user_id=user_id
        ).first()

        if not report:
            return jsonify({
                "error": "Report not found"
            }), 404

        # --------------------------------------------------
        # Delete child records first
        # --------------------------------------------------

        HealthParameter.query.filter_by(
            report_id=report.id
        ).delete(synchronize_session=False)

        HealthAnalysis.query.filter_by(
            report_id=report.id
        ).delete(synchronize_session=False)

        # --------------------------------------------------
        # Delete physical uploaded file if it exists
        # --------------------------------------------------

        if report.file_path:
            try:
                if os.path.exists(report.file_path):
                    os.remove(report.file_path)
                    print("Deleted file:", report.file_path)
            except Exception as file_error:
                print("File deletion warning:", file_error)

        # --------------------------------------------------
        # Delete main report
        # --------------------------------------------------

        db.session.delete(report)

        db.session.commit()

        return jsonify({
            "message": "Report deleted successfully",
            "report_id": report_id
        }), 200

    except Exception as e:

        db.session.rollback()

        print("DELETE REPORT ERROR:", str(e))

        return jsonify({
            "error": "Failed to delete report",
            "details": str(e)
        }), 500