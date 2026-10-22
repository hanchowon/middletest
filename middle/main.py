from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueueSystem:
    def __init__(self, capacity: int = 20):
        self.capacity = capacity
        self.queue = []

    def clear(self):
        self.queue = []

    def push(self, value: int) -> bool:
        if len(self.queue) >= self.capacity:
            return False
        self.queue.append(value)
        return True

    def pop(self) -> Optional[int]:
        if not self.queue:
            return None
        return self.queue.pop(0)

    def size(self) -> int:
        return len(self.queue)

    def is_full(self) -> bool:
        return len(self.queue) == self.capacity

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def peek(self) -> Optional[int]:
        if not self.queue:
            return None
        return self.queue[0]

    def search_index(self, value: int) -> List[int]:
        return [idx for idx, val in enumerate(self.queue) if val == value]

    def count_value(self, value: int) -> int:
        return self.queue.count(value)

    def contains(self, value: int) -> bool:
        return value in self.queue

    def get_all(self) -> List[int]:
        return list(self.queue)

q = QueueSystem(capacity=20)

class InitReq(BaseModel):
    capacity: int = 20

class PushReq(BaseModel):
    value: int

class PushArrayReq(BaseModel):
    values: List[int]

class SearchReq(BaseModel):
    value: int

@app.post("/init")
def init_queue(req: InitReq):
    global q
    q = QueueSystem(capacity=req.capacity)
    return {"message": "Initialized", "capacity": q.capacity, "size": q.size()}

@app.post("/push")
def push_item(req: PushReq):
    success = q.push(req.value)
    return {"success": success, "size": q.size(), "is_full": q.is_full()}

@app.post("/push_array")
def push_array(req: PushArrayReq):
    pushed = []
    failed = []
    for val in req.values:
        if q.push(val):
            pushed.append(val)
        else:
            failed.append(val)
    return {"pushed": pushed, "failed": failed, "size": q.size()}

@app.post("/pop")
def pop_item():
    val = q.pop()
    return {"popped": val, "size": q.size(), "is_empty": q.is_empty()}

@app.get("/size")
def get_size():
    return {"size": q.size(), "capacity": q.capacity}

@app.get("/status")
def get_status():
    return {"is_full": q.is_full(), "is_empty": q.is_empty()}

@app.get("/front")
def get_front():
    return {"front": q.peek()}

@app.delete("/clear")
def clear_queue():
    q.clear()
    return {"message": "Cleared", "size": q.size()}

@app.post("/search_index")
def search_index(req: SearchReq):
    indices = q.search_index(req.value)
    return {"value": req.value, "indices": indices}

@app.post("/count_value")
def count_value(req: SearchReq):
    cnt = q.count_value(req.value)
    return {"value": req.value, "count": cnt}

@app.post("/contains")
def contains_value(req: SearchReq):
    exists = q.contains(req.value)
    return {"value": req.value, "exists": exists}

@app.get("/print_all")
def print_all():
    return {"data": q.get_all()}

@app.post("/run_test")
def run_test():
    global q
    q = QueueSystem(capacity=20)
    
    initial_array = [19, 15, 29, 25, 33, 35, 49, 42, 50, 65, 62, 66, 77, 80]
    for v in initial_array:
        q.push(v)
        
    curr_size = q.size()
    status = {"is_full": q.is_full(), "is_empty": q.is_empty()}
    front_val = q.peek()
    
    val_42_indices = q.search_index(42)
    val_42_count = q.count_value(42)
    
    val_88_exists = q.contains(88)
    all_data = q.get_all()
    
    return {
        "step1_capacity": 20,
        "step2_pushed_array": initial_array,
        "step3_current_size": curr_size,
        "step4_status": status,
        "step5_front_data": front_val,
        "step6_value_42": {
            "indices": val_42_indices,
            "count": val_42_count
        },
        "step7_value_88_exists": val_88_exists,
        "step8_all_data": all_data
    }
