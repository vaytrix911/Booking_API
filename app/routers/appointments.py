from fastapi import APIRouter,Depends,HTTPException
from app.schemas import AppointmentCreate,AppointmentResponse,AppointmentUpdate
from app.models import User
from app.dependencies import get_current_user,get_db
from sqlalchemy.orm import Session
from app.models import Appointment

router = APIRouter()

@router.post("/appointments",response_model=AppointmentResponse)
def add_appointments(
                    appointment:AppointmentCreate,
                    db:Session = Depends(get_db),
                    current_user:User = Depends(get_current_user)):
    existing_appointments = db.query(Appointment).filter(Appointment.owner_id == current_user.id).all()
    for existing in existing_appointments:
        if appointment.start_time < existing.end_time and appointment.end_time > existing.start_time:
            raise HTTPException(status_code=409,detail="time conflict with an existing appointment")
    new_appointment = Appointment(title= appointment.title,
                                description = appointment.description,
                                start_time = appointment.start_time,
                                end_time = appointment.end_time,
                                owner = current_user)
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

@router.get("/appointments", response_model=list[AppointmentResponse])
def get_appointments(db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    appointment = db.query(Appointment).filter(Appointment.owner_id == current_user.id).all()
    return appointment

@router.get("/appointments/{appointment_id}",response_model=AppointmentResponse)
def get_appointment(appointment_id:int,db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404,detail="appointment not found")
    if appointment.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="you don't have permission to this appointment")
    return appointment

@router.patch("/appointments/{appointment_id}")
def update_appointments(updates:AppointmentUpdate,appointment_id:int,db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404,detail="appointment not found")
    if appointment.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="you don't have permission to this appointment")
    update_data = updates.model_dump(exclude_unset=True)
    for field,value in update_data.items():
        setattr(appointment,field,value)

    existing_appointments = db.query(Appointment).filter(Appointment.owner_id == current_user.id).all()
    for existing in existing_appointments:
        if existing.id == appointment_id:
            continue
        if appointment.start_time < existing.end_time and appointment.end_time > existing.start_time:
            raise HTTPException(status_code=409,detail="time conflict with an existing appointment")

    db.commit()
    db.refresh(appointment)
    return appointment

@router.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id:int,db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404,detail="appointment not found")
    if appointment.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="you don't have permission to this appointment")
    db.delete(appointment)
    db.commit()
    return {"message":"appointment deleted successfully"}