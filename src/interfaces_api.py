from fastapi import FastAPI, HTTPException
import psycopg2
import os
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class interfaces(BaseModel):
    vlan_id: int
    ip_address: str 
    interface_netmask: str
    network: str
    network_start: Optional[str]
    network_finish: Optional[str]
    gw : str
    enabled: bool = True
    created_at: Optional[str]
    updated_at: Optional[str]

def db_connection():
    con = psycopg2.connect(
        host='my_postgres',
        database='firewalldb',
        user='pi',
        password=os.getenv("POSTGRES_PASSWORD"),
        port=5432
    )
    return con


@app.get("/interfaces/")
def get_interfaces_by_field(
    vlan_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    network: Optional[str] = None,
    gw: Optional[str] = None,
    enabled: Optional[bool] = None
):
    con = db_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)

    query = "select * from interfaces WHERE 1=1"

    if vlan_id is not None:
        query+= f" AND vlan_id = '{vlan_id}'"
    if ip_address is not None:
        query+= f" AND ip_address = '{ip_address}'"
    if network is not None:
        query+= f" AND network = '{network}'"
    if gw is not None:
        query+= f" AND gw = '{gw}'"
    if enabled is not None:
        query+= f" AND enabled = '{enabled}'"
    
    query+= f";"
    cur.execute(query)
    rows = cur.fetchall()
    cur.close
    con.close
    return {"interfaces":rows}

@app.delete("/interfaces/delete/{id}")
def delete_interfaces(id:int):
    try:
        con = db_connection()
        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE from interfaces WHERE ID=%s RETURNING id;", (id,))
        deleted = cur.fetchone()
        con.commit()
        cur.close()
        con.close()

        if not deleted:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"message:" "Interface deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error: {str(e)}")

@app.post("/interfaces/add")
def add_interface(iface: interfaces):
    con = db_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute("""
        INSERT INTO interfaces
        (vlan_id, ip_address, interface_netmask, network,
         network_start, network_finish, gw, enabled)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
        """, (
        iface.vlan_id,
        iface.ip_address,
        iface.interface_netmask,
        iface.network,
        iface.network_start,
        iface.network_finish,
        iface.gw,
        iface.enabled
        ))
        new_id = cur.fetchone()['id']
        con.commit()
        return {"message": "New interface created", "id": new_id}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=500,detail=f"Error: {str(e)}")
    
    finally:
        cur.close()
        con.close()

@app.patch("/interfaces/edit")
def edit_finterfaces(id: int, iface: dict):

    try:
        con = db_connection()
        cur = con.cursor(cursor_factory=RealDictCursor)
        keys=[]
        values=[]

        for key,value in iface.items():
            keys.append(f"{key} = %s")
            values.append(value)

        if not keys:
            return {"message": "No Change"}

        values.append(id)
        query =  f"UPDATE interfaces SET {', '.join(keys)} WHERE id = %s RETURNING id"

        cur.execute(query,values)
        updated = cur.fetchone()
        con.commit()
        cur.close()
        con.close()

        if not updated:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"message": "Alert updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error: {str(e)}")
    
        