# invoice_controller.py

from dtos.invoice_models import InvoiceModel, UpdateInvoiceRequest
from models.invoices_table import CaseStatusHistories, InvoiceStatus
from models.users_table import User, UserRole
from models.lawyers_table import Lawyers
from helper.api_helper import APIHelper
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func


class InvoiceController:

    # ================= LAWYER CREATES INVOICE =================
    def create_invoice(create_invoice_request: InvoiceModel, user: User, db: Session):
        if user is None or user.role != UserRole.LAWYER:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        if not lawyer:
            raise HTTPException(status_code=404, detail="Lawyer not found")

        if lawyer.isBlocked:
            raise HTTPException(status_code=403, detail="You are blocked")

        invoice = CaseStatusHistories(
            totalAmount=create_invoice_request.totalAmount,
            totalHours=create_invoice_request.totalHours,
            status=InvoiceStatus.pending,
            caseId=int(create_invoice_request.caseId),
            clientId=int(create_invoice_request.clientId),
            lawyerId=lawyer.id,
            companyId=int(create_invoice_request.companyId)
        )

        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice

    # ================= READ INVOICES =================
    def read_all(user: User, db: Session, status: str = None):
        if user is None or user.role not in [UserRole.LAWYER, UserRole.CLIENT, UserRole.ADMIN]:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        # LAWYER sees only their invoices
        if user.role == UserRole.LAWYER:
            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
            if not lawyer:
                raise HTTPException(status_code=404, detail="Lawyer not found")
            if lawyer.isBlocked:
                raise HTTPException(status_code=403, detail="You are blocked")

            query = db.query(CaseStatusHistories).filter(CaseStatusHistories.lawyerId == lawyer.id)

        # CLIENT sees only their invoices
        elif user.role == UserRole.CLIENT:
            query = db.query(CaseStatusHistories).filter(CaseStatusHistories.clientId == user.id)

        # ADMIN sees all invoices
        elif user.role == UserRole.ADMIN:
            query = db.query(CaseStatusHistories)

        # Apply optional status filter
        if status:
            try:
                status_enum = InvoiceStatus(status)
                query = query.filter(CaseStatusHistories.status == status_enum)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid status value. Use 'pending' or 'paid'")

        invoices = query.all()
        return invoices

    # ================= UPDATE INVOICE =================
    def update_invoice(invoice_id: int, update_invoice_request: UpdateInvoiceRequest, user: User, db: Session):
        if user is None or user.role != UserRole.LAWYER:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        if not lawyer:
            raise HTTPException(status_code=404, detail="Lawyer not found")
        if lawyer.isBlocked:
            raise HTTPException(status_code=403, detail="You are blocked")

        invoice = db.query(CaseStatusHistories).filter(CaseStatusHistories.id == invoice_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        if invoice.lawyerId != lawyer.id:
            raise HTTPException(status_code=403, detail="Not your invoice")

        update_data = update_invoice_request.dict(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            if key == "status":
                setattr(invoice, key, InvoiceStatus(value))
            else:
                setattr(invoice, key, value)

        db.commit()
        db.refresh(invoice)
        return invoice

    # ================= DELETE INVOICE =================
    def delete_invoice(invoice_id: int, user: User, db: Session):
        if user is None or user.role != UserRole.LAWYER:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        if not lawyer:
            raise HTTPException(status_code=404, detail="Lawyer not found")
        if lawyer.isBlocked:
            raise HTTPException(status_code=403, detail="You are blocked")

        invoice = db.query(CaseStatusHistories).filter(CaseStatusHistories.id == invoice_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        if invoice.lawyerId != lawyer.id:
            raise HTTPException(status_code=403, detail="Not your invoice")

        db.delete(invoice)
        db.commit()
        return {"message": "Invoice deleted successfully"}

    # ================= CLIENT PAYS INVOICE =================
    def pay_invoice(invoice_id: int, user: User, db: Session):
        if user is None or user.role != UserRole.CLIENT:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        invoice = db.query(CaseStatusHistories).filter(
            CaseStatusHistories.id == invoice_id,
            CaseStatusHistories.clientId == user.id
        ).first()

        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        invoice.status = InvoiceStatus.paid
        db.commit()
        db.refresh(invoice)
        return invoice

    # ================= ADMIN TOTALS =================
    def get_admin_invoice_totals(user: User, db: Session):
        if user is None or user.role != UserRole.ADMIN:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        total_paid = db.query(func.sum(CaseStatusHistories.totalAmount)) \
            .filter(CaseStatusHistories.status == InvoiceStatus.paid).scalar() or 0

        total_pending = db.query(func.sum(CaseStatusHistories.totalAmount)) \
            .filter(CaseStatusHistories.status == InvoiceStatus.pending).scalar() or 0

        invoices = db.query(CaseStatusHistories).all()  # Admin sees all invoices

        return {
            "invoices": invoices,
            "total_paid": float(total_paid),
            "total_pending": float(total_pending)
        }