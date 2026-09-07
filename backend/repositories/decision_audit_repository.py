from models.decision_audit import DecisionAudit
from repositories.base import BaseRepository


class DecisionAuditRepository(BaseRepository[DecisionAudit]):
    model = DecisionAudit
