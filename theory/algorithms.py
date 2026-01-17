# algorithms.py

# ---------------- CPU Scheduling ---------------- #

def fcfs(processes):
    processes = sorted(processes, key=lambda x: x.get("arrival", 0))
    time = 0
    timeline = []
    completed = []

    for p in processes:
        start_time = max(time, p.get("arrival", 0))
        end_time = start_time + p["burst"]
        waiting_time = start_time - p.get("arrival", 0)
        turnaround_time = end_time - p.get("arrival", 0)

        timeline.extend([{"time": t, "pid": p["pid"]} for t in range(start_time, end_time)])

        completed.append({
            "pid": p["pid"],
            "arrival": p.get("arrival", 0),
            "burst": p["burst"],
            "start_time": start_time,
            "end_time": end_time,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time
        })
        time = end_time

    return {"timeline": timeline, "process_summary": completed}


def sjf_non_preemptive(processes):
    processes = [dict(p) for p in processes]
    completed = []
    timeline = []
    time = 0
    n = len(processes)
    remaining = processes.copy()

    while len(completed) < n:
        ready = [p for p in remaining if p.get("arrival", 0) <= time]
        if ready:
            ready.sort(key=lambda x: x["burst"])
            p = ready[0]
            start_time = max(time, p.get("arrival", 0))
            end_time = start_time + p["burst"]
            waiting_time = start_time - p.get("arrival", 0)
            turnaround_time = end_time - p.get("arrival", 0)

            timeline.extend([{"time": t, "pid": p["pid"]} for t in range(start_time, end_time)])

            completed.append({
                "pid": p["pid"],
                "arrival": p.get("arrival", 0),
                "burst": p["burst"],
                "start_time": start_time,
                "end_time": end_time,
                "waiting_time": waiting_time,
                "turnaround_time": turnaround_time
            })
            remaining.remove(p)
            time = end_time
        else:
            timeline.append({"time": time, "pid": "idle"})
            time += 1

    return {"timeline": timeline, "process_summary": completed}


def srtf_preemptive(processes):
    processes = [dict(p) for p in processes]
    n = len(processes)
    remaining = {p["pid"]: p["burst"] for p in processes}
    completed = []
    timeline = []
    time = 0

    while len(completed) < n:
        ready = [p for p in processes if p.get("arrival", 0) <= time and p["pid"] in remaining]
        if ready:
            ready.sort(key=lambda x: remaining[x["pid"]])
            p = ready[0]
            pid = p["pid"]
            timeline.append({"time": time, "pid": pid})
            remaining[pid] -= 1
            if remaining[pid] == 0:
                end_time = time + 1
                start_time = end_time - p["burst"]
                waiting_time = end_time - p.get("arrival", 0) - p["burst"]
                turnaround_time = end_time - p.get("arrival", 0)
                completed.append({
                    "pid": pid,
                    "arrival": p.get("arrival", 0),
                    "burst": p["burst"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "waiting_time": waiting_time,
                    "turnaround_time": turnaround_time
                })
                del remaining[pid]
        else:
            timeline.append({"time": time, "pid": "idle"})
        time += 1

    return {"timeline": timeline, "process_summary": completed}


def round_robin(processes, quantum=1):
    processes = [dict(p) for p in processes]
    n = len(processes)
    remaining = {p["pid"]: p["burst"] for p in processes}
    timeline = []
    completed = []
    time = 0
    queue = []

    while len(completed) < n:
        for p in processes:
            if p.get("arrival", 0) <= time and p["pid"] not in queue and p["pid"] in remaining:
                queue.append(p["pid"])
        if queue:
            pid = queue.pop(0)
            exec_time = min(quantum, remaining[pid])
            timeline.extend([{"time": t, "pid": pid} for t in range(time, time + exec_time)])
            remaining[pid] -= exec_time
            if remaining[pid] == 0:
                end_time = time + exec_time
                p = next(x for x in processes if x["pid"] == pid)
                start_time = end_time - p["burst"]
                waiting_time = end_time - p.get("arrival", 0) - p["burst"]
                turnaround_time = end_time - p.get("arrival", 0)
                completed.append({
                    "pid": pid,
                    "arrival": p.get("arrival", 0),
                    "burst": p["burst"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "waiting_time": waiting_time,
                    "turnaround_time": turnaround_time
                })
            else:
                queue.append(pid)
            time += exec_time
        else:
            timeline.append({"time": time, "pid": "idle"})
            time += 1

    return {"timeline": timeline, "process_summary": completed}


def priority_preemptive(processes):
    processes = [dict(p) for p in processes]
    remaining = {p["pid"]: p["burst"] for p in processes}
    completed = []
    timeline = []
    time = 0
    n = len(processes)

    while len(completed) < n:
        ready = [p for p in processes if p.get("arrival", 0) <= time and p["pid"] in remaining]
        if ready:
            ready.sort(key=lambda x: x.get("priority", 1))
            p = ready[0]
            pid = p["pid"]
            timeline.append({"time": time, "pid": pid})
            remaining[pid] -= 1
            if remaining[pid] == 0:
                end_time = time + 1
                start_time = end_time - p["burst"]
                waiting_time = end_time - p.get("arrival", 0) - p["burst"]
                turnaround_time = end_time - p.get("arrival", 0)
                completed.append({
                    "pid": pid,
                    "arrival": p.get("arrival", 0),
                    "burst": p["burst"],
                    "priority": p.get("priority", 1),
                    "start_time": start_time,
                    "end_time": end_time,
                    "waiting_time": waiting_time,
                    "turnaround_time": turnaround_time
                })
                del remaining[pid]
        else:
            timeline.append({"time": time, "pid": "idle"})
        time += 1

    return {"timeline": timeline, "process_summary": completed}

# ---------------- Banker’s Algorithm ---------------- #

def bankers_algorithm(processes, alloc, max_req, avail):
    n = len(processes)
    m = len(avail)
    need = [[max_req[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
    finish = [False]*n
    safe_seq = []
    timeline = []

    while len(safe_seq) < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= avail[j] for j in range(m)):
                for j in range(m):
                    avail[j] += alloc[i][j]
                safe_seq.append(processes[i])
                finish[i] = True
                timeline.append({"pid": processes[i], "time": len(safe_seq)})
                found = True
        if not found:
            break

    return {
        "timeline": timeline,
        "safe_sequence": safe_seq,
        "unsafe_processes": [p for i, p in enumerate(processes) if not finish[i]]
    }

# ---------------- Memory Allocation ---------------- #

def first_fit(processes, blocks):
    allocation = [-1]*len(processes)
    timeline = []

    for i, psize in enumerate(processes):
        for j, bsize in enumerate(blocks):
            if bsize >= psize:
                allocation[i] = j
                blocks[j] -= psize
                timeline.append({"process": i, "block": j})
                break

    return {"timeline": timeline, "allocation": allocation, "remaining_blocks": blocks}


def best_fit(processes, blocks):
    allocation = [-1]*len(processes)
    timeline = []

    for i, psize in enumerate(processes):
        best_index = -1
        for j, bsize in enumerate(blocks):
            if bsize >= psize and (best_index == -1 or bsize < blocks[best_index]):
                best_index = j
        if best_index != -1:
            allocation[i] = best_index
            blocks[best_index] -= psize
            timeline.append({"process": i, "block": best_index})

    return {"timeline": timeline, "allocation": allocation, "remaining_blocks": blocks}

# ---------------- Page Replacement ---------------- #

def fifo_page_replacement(ref, frames):
    frame_list = [-1]*frames
    timeline = []
    faults = 0
    index = 0

    for t, page in enumerate(ref):
        hit = page in frame_list
        if not hit:
            frame_list[index] = page
            index = (index + 1) % frames
            faults += 1
        timeline.append({"time": t, "page": page, "frame": frame_list.copy(), "hit": hit})

    return {"timeline": timeline, "page_faults": faults}


def lru_page_replacement(ref, frames):
    frame_list = [-1]*frames
    time_list = [0]*frames
    timeline = []
    faults = 0
    counter = 0

    for t, page in enumerate(ref):
        hit = False
        if page in frame_list:
            hit = True
            idx = frame_list.index(page)
            counter += 1
            time_list[idx] = counter
        else:
            counter += 1
            if -1 in frame_list:
                idx = frame_list.index(-1)
            else:
                idx = time_list.index(min(time_list))
            frame_list[idx] = page
            time_list[idx] = counter
            faults += 1
        timeline.append({"time": t, "page": page, "frame": frame_list.copy(), "hit": hit})

    return {"timeline": timeline, "page_faults": faults}


def optimal_page_replacement(ref, frames):
    frame_list = [-1]*frames
    timeline = []
    faults = 0

    for t, page in enumerate(ref):
        hit = page in frame_list
        if not hit:
            if -1 in frame_list:
                idx = frame_list.index(-1)
            else:
                farthest = -1
                idx = 0
                for i, f in enumerate(frame_list):
                    try:
                        next_use = ref[t+1:].index(f)
                    except ValueError:
                        next_use = float('inf')
                    if next_use > farthest:
                        farthest = next_use
                        idx = i
            frame_list[idx] = page
            faults += 1
        timeline.append({"time": t, "page": page, "frame": frame_list.copy(), "hit": hit})

    return {"timeline": timeline, "page_faults": faults}
