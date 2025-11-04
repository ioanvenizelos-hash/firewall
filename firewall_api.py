from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class firewall_rules(BaseModel):
    enabled: bool = True
    action: str
    chain: str
    source: str
    source_port: str
    dest: str
    dest_port: str
    protocol: str
    description: Optional[str] = None
    order_index: int
    user_defined: bool = True
    visible: bool = True
    group_id: Optional[int]
    extra: Optional[str] = None

def db_connection():
    con = psycopg2.connect(
        host='127.0.0.1',
        database='mydb',
        user='pi',
        password='j741995'
    )
    return con

@app.get("/firewall_rules/")
def get_firewall_rules():
    con = db_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from firewall_rules; ")
    rows = cur.fetchall()
    cur.close
    con.close
    return {"firewall":rows}

@app.get("/firewall_rules/rules")
def get_firewall_rules_by_field(
    id: Optional[int] = None,
    enabled: Optional[bool] = None,
    action: Optional[str] = None,
    chain: Optional[str] = None,
    source: Optional[str] = None,
    source_port: Optional[str] = None,
    dest: Optional[str] = None,
    dest_port: Optional[str] = None,
    protocol: Optional[str] = None,
    description: Optional[str] = None,
    order_index: Optional[int] = None,
    user_defined: Optional[bool] = None,
    visible: Optional[bool] = None,
    group_id: Optional[int] = None,
    extra: Optional[str] = None
    ):

    con = db_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)

    query ="select * from firewall_rules WHERE 1=1"

    if id is not None:
        query+= f" AND id = '{id}'"
    
    if enabled is not None:
        query+= f" AND enabled = '{enabled}'"
        
    if action is not None:
        query+= f" AND action = '{action}'"

    if chain is not None:
        query+= f" AND chain = '{chain}'"

    if source is not None:
        query+= f" AND id = '{source}'"
    
    if source_port is not None:
        query+= f" AND source_port = '{source_port}'"
        
    if dest is not None:
        query+= f" AND dest = '{dest}'"

    if dest_port is not None:
        query+= f" AND dest_port = '{dest_port}'"

    if protocol is not None:
        query+= f" AND protocol = '{protocol}'"

    query+= f";"

    cur.execute(query)
    rows = cur.fetchall()
    cur.close
    con.close

    return {"firewall":rows}

@app.delete("/firewall_rules/delete/{id}")
def delete_firewall_rule(id: int):
    try:
        con = db_connection()
        cur = con.cursor(cursor_factory=RealDictCursor) 
        cur.execute("DELETE from firewall_rules WHERE ID=%s RETURNING id;", (id,))
        deleted = cur.fetchone()
        con.commit()
        cur.close()
        con.close()
        if not deleted:
            raise HTTPException(status_code=404, detail="Alert not found") 
        return {"message": "Alert deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error: {str(e)}")

@app.post("/firewall_rules/add")
def add_firewall_rule(frule: firewall_rules):
    con = db_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute("""
                    INSERT INTO firewall_rules
                    (enabled,action,chain,source,source_port,dest,dest_port,protocol,description,order_index,user_defined,visible,group_id,extra)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING id
                    """,(
                        frule.enabled, frule.action, frule.chain, frule.source, frule.source_port,
                        frule.dest, frule.dest_port, frule.protocol, frule.description,
                        frule.order_index, frule.user_defined, frule.visible, frule.group_id, frule.extra
        ))
        new_id = cur.fetchone()['id']
        con.commit()
        return {"message": "New alert created", "id": new_id}
    
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=500,detail=f"Error: {str(e)}")
    
    finally:
        cur.close()
        con.close()

@app.patch("/firewall_rules/edit")
def edit_firewall_rule(id: int, frule: dict):

    try:
        con = db_connection()
        cur = con.cursor(cursor_factory=RealDictCursor)
        keys=[]
        values=[]

        for key,value in frule.items():
            keys.append(f"{key} = %s")
            values.append(value)

        if not keys:
            return {"message": "No Change"}

        values.append(id)
        query =  f"UPDATE firewall_rules SET {', '.join(keys)} WHERE id = %s RETURNING id"

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