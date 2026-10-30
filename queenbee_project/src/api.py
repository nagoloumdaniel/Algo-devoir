"""
API REST QueenBee — routage d'urgence (T-W5, T-W6, T-W7).

    POST /api/v1/routing/emergency-path

Lancement :
    uvicorn src.api:app --reload
    Documentation interactive : http://127.0.0.1:8000/docs
"""

import logging
from enum import Enum
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from src.routing_service import (
    InvalidIdentifierError,
    UnknownResourceError,
    compute_emergency_path,
)

logger = logging.getLogger("queenbee.routing")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


# ====================================================================== #
# T-W6 : schéma d'entrée
# ====================================================================== #
class UrgencyLevel(str, Enum):
    critique = "critique"
    haute = "haute"
    moyenne = "moyenne"


class EmergencyPathRequest(BaseModel):
    coordinator_id: str = Field(
        ..., pattern=r"^C\d{2}$",
        description="Identifiant du coordinateur régional (point de départ), format CXX.",
        examples=["C01"],
    )
    target_hive_id: str = Field(
        ..., pattern=r"^H\d{2}$",
        description="Identifiant de la ruche en alerte critique, format HXX.",
        examples=["H07"],
    )
    urgence_niveau: Optional[UrgencyLevel] = Field(
        None, description="Niveau d'urgence de l'alerte (optionnel).")
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Informations libres sur l'alerte (optionnel).",
        examples=[{"alerte": "chute_de_poids"}])

    @field_validator("coordinator_id", "target_hive_id", mode="before")
    @classmethod
    def normalize(cls, value):
        """Insensible à la casse et aux espaces : ' h07' -> 'H07'.
        Les valeurs non textuelles sont laissées telles quelles et rejetées par Pydantic."""
        if isinstance(value, str):
            return value.strip().upper()
        return value

    model_config = {
        "json_schema_extra": {
            "examples": [{"coordinator_id": "C01", "target_hive_id": "H07",
                          "urgence_niveau": "critique"}]
        }
    }


# ====================================================================== #
# T-W7 : schéma de sortie
# ====================================================================== #
class EmergencyPathResponse(BaseModel):
    status: str = Field(..., description='"success" ou "error" (ruche inaccessible).')
    message: Optional[str] = Field(None, description="Détail en cas d'erreur.")
    coordinator_id: str
    target_hive_id: str
    start_node: str = Field(..., description="Noeud de départ du coordinateur dans le graphe.")
    total_cost: Optional[float] = Field(
        None, description="Temps de trajet total en minutes (2 décimales), null si inaccessible.")
    total_cost_formatted: Optional[str] = Field(None, description='Ex. "12 min 30 sec".')
    path: List[str] = Field(..., description="Points de passage ordonnés, de la base à la ruche.")
    hop_count: int = Field(..., description="Nombre de tronçons parcourus.")
    calculation_time_ms: float = Field(..., description="Temps de calcul de l'algorithme (ms).")
    algorithm_version: str

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "status": "success", "message": None,
                "coordinator_id": "C01", "target_hive_id": "H07", "start_node": "BASE_NORD",
                "total_cost": 17.5, "total_cost_formatted": "17 min 30 sec",
                "path": ["BASE_NORD", "J1", "J2", "J3", "J4", "H07"], "hop_count": 5,
                "calculation_time_ms": 0.042, "algorithm_version": "dijkstra-minheap-1.0",
            }]
        }
    }


class ErrorResponse(BaseModel):
    detail: str


# ====================================================================== #
# T-W5 : endpoint
# ====================================================================== #
router = APIRouter(prefix="/api/v1/routing", tags=["routing"])


@router.post(
    "/emergency-path",
    response_model=EmergencyPathResponse,
    summary="Itinéraire d'urgence vers une ruche en alerte (Dijkstra)",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def emergency_path(request: EmergencyPathRequest) -> EmergencyPathResponse:
    """Calcule le plus court chemin entre la base du coordinateur et la ruche cible.

    - **200** : calcul effectué (`status` = `success`, ou `error` si la ruche est inaccessible)
    - **400** : identifiant invalide
    - **404** : coordinateur ou ruche inconnu
    - **422** : corps de requête invalide (champ manquant, mauvais type, mauvais format)
    """
    logger.info("emergency-path coordinator=%s hive=%s urgence=%s",
                request.coordinator_id, request.target_hive_id, request.urgence_niveau)
    try:
        result = compute_emergency_path(request.coordinator_id, request.target_hive_id)
    except InvalidIdentifierError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except UnknownResourceError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    logger.info("-> status=%s cost=%s time=%sms", result["status"],
                result["total_cost"], result["calculation_time_ms"])
    return EmergencyPathResponse(**result)


app = FastAPI(
    title="QueenBee API",
    version="1.0.0",
    description="Backend QueenBee — calcul d'itinéraires d'urgence (UC-C01).",
)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api:app", host="127.0.0.1", port=8000, reload=True)