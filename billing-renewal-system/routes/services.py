from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import db
from models.service import Service


services_bp = Blueprint("services", __name__, url_prefix="/services")


@services_bp.route("/", methods=["GET", "POST"])
def list_services():
    if request.method == "POST":
        service = Service(
            name=request.form["name"].strip(),
            description=request.form.get("description", "").strip(),
            monthly_price=float(request.form["monthly_price"]),
            quarterly_price=float(request.form["quarterly_price"]),
            yearly_price=float(request.form["yearly_price"]),
        )
        db.session.add(service)
        db.session.commit()
        flash("Service plan added.", "success")
        return redirect(url_for("services.list_services"))
    services = Service.query.order_by(Service.created_at.desc()).all()
    return render_template("services.html", services=services)


@services_bp.route("/<int:service_id>/toggle", methods=["POST"])
def toggle_service(service_id):
    service = Service.query.get_or_404(service_id)
    service.is_active = not service.is_active
    db.session.commit()
    flash("Service status changed.", "info")
    return redirect(url_for("services.list_services"))
