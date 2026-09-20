from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import h3
import h3.api.basic_int as h3_int


app = FastAPI(
    title="H3-API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

class H3Data(BaseModel):
    reqLat: str = ""
    reqLng: str = ""
    reqRes: str = ""
    reqOrigin: str = ""
    reqK: str = ""
    reqCell: str = ""

    resLat: str = ""
    resLng: str = ""
    resCount: str = "0"
    resCell: str = ""

class H3Request(BaseModel):
    items: list[H3Data]

def create_response(req: H3Data) -> dict:
    return {
        "reqLat": req.reqLat,
        "reqLng": req.reqLng,
        "reqRes": req.reqRes,
        "reqOrigin": req.reqOrigin,
        "reqK": req.reqK,
        "reqCell": req.reqCell,

        "resLat": req.reqLat,
        "resLng": req.reqLng,
        "resCount": "0",
        "resCell": req.reqCell
    }

@app.post("/health")
def health():
    return {
        "status": "ok",
        "h3_version": h3.versions()
    }


@app.post("/latLngToCell")
def latLngToCell(request: H3Request):
    results = []

    for req in request.items:
        try:
            lat = float(req.reqLat)
            lng = float(req.reqLng)
            res = int(req.reqRes)

            cell = h3_int.latlng_to_cell(
                lat,
                lng,
                res
            )

            result = create_response(req)
            result["resCell"] = str(cell)
            results.append(result)

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    return {
        "items": results
    }

@app.post("/latLngToCellAddress")
def latLngToCellAddress(request: H3Request):
    results = []

    for req in request.items:
        try:
            lat = float(req.reqLat)
            lng = float(req.reqLng)
            res = int(req.reqRes)

            cell = h3_int.latlng_to_cell(
                lat,
                lng,
                res
            )

            result = create_response(req)
            result["resCell"] = h3.int_to_str(cell)
            results.append(result)

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    return {
        "items": results
    }


def parse_h3_cell(cell: str) -> tuple[int, str]:
    if cell.isdigit():
        value = int(cell)

        if not h3_int.is_valid_cell(value):
            raise ValueError("Invalid H3 decimal cell")

        return value, "decimal"

    value = h3.str_to_int(cell)

    if not h3_int.is_valid_cell(value):
        raise ValueError("Invalid H3 cell")

    return value, "address"


@app.post("/gridDisk")
def gridDisk(request: H3Request):
    results = []

    for req in request.items:
        try:
            origin_int, input_type = parse_h3_cell(
                req.reqOrigin
            )

            k = int(req.reqK)

            cells = h3_int.grid_disk(
                origin_int,
                k
            )

            count = len(cells)

            for cell in cells:
                result = create_response(req)
                result["resCount"] = str(count)

                if input_type == "decimal":
                    result["resCell"] = str(cell)
                else:
                    result["resCell"] = h3.int_to_str(cell)

                results.append(result)

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    return {
        "items": results
    }

@app.post("/cellToLatLng")
def cellToLatLng(request: H3Request):
    results = []

    for req in request.items:
        try:
            cell_int, _ = parse_h3_cell(
                req.reqCell
            )

            lat, lng = h3_int.cell_to_latlng(
                cell_int
            )

            result = create_response(req)

            result["resLat"] = str(lat)
            result["resLng"] = str(lng)

            results.append(result)

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    return {
        "items": results
    }