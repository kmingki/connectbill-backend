from datetime import datetime

from grpc import Status
from client_commission.models import Commission

def changeStatus() :
    objects = Commission.objecs.all()
    for obj in objects :
        if obj.Status == 0 and datetime.strptime(obj.deadline , "%Y-%m-%d") - datetime.now() < 0: 
            obj.Status = 1
            obj.messageFlag = 1
            obj.save()
    return

            
        