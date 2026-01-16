# theory/algorithms.py

def fcfs(processes):
    processes = sorted(processes, key=lambda x: x["arrival"])
    time = 0
    timeline = []
    completed = []

    for p in processes:
        start_time = max(time, p["arrival"])
        end_time = start_time + p["burst"]
        waiting_time = start_time - p["arrival"]
        turnaround_time = end_time - p["arrival"]

        timeline.extend([{"time": t, "pid": p["pid"]} for t in range(start_time, end_time)])

        completed.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
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
        ready = [p for p in remaining if p["arrival"] <= time]
        if ready:
            ready.sort(key=lambda x: x["burst"])
            p = ready[0]
            start_time = max(time, p["arrival"])
            end_time = start_time + p["burst"]
            waiting_time = start_time - p["arrival"]
            turnaround_time = end_time - p["arrival"]

            timeline.extend([{"time": t, "pid": p["pid"]} for t in range(start_time, end_time)])

            completed.append({
                "pid": p["pid"],
                "arrival": p["arrival"],
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
        ready = [p for p in processes if p["arrival"] <= time and p["pid"] in remaining]
        if ready:
            ready.sort(key=lambda x: remaining[x["pid"]])
            p = ready[0]
            pid = p["pid"]
            timeline.append({"time": time, "pid": pid})
            remaining[pid] -= 1
            if remaining[pid] == 0:
                end_time = time + 1
                start_time = end_time - p["burst"]
                waiting_time = end_time - p["arrival"] - p["burst"]
                turnaround_time = end_time - p["arrival"]
                completed.append({
                    "pid": pid,
                    "arrival": p["arrival"],
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


def round_robin(processes, quantum):
    processes = [dict(p) for p in processes]
    n = len(processes)
    remaining = {p["pid"]: p["burst"] for p in processes}
    timeline = []
    completed = []
    time = 0
    queue = []

    while len(completed) < n:
        for p in processes:
            if p["arrival"] <= time and p["pid"] not in queue and p["pid"] in remaining:
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
                waiting_time = end_time - p["arrival"] - p["burst"]
                turnaround_time = end_time - p["arrival"]
                completed.append({
                    "pid": pid,
                    "arrival": p["arrival"],
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
        ready = [p for p in processes if p["arrival"] <= time and p["pid"] in remaining]
        if ready:
            ready.sort(key=lambda x: x["priority"])
            p = ready[0]
            pid = p["pid"]
            timeline.append({"time": time, "pid": pid})
            remaining[pid] -= 1
            if remaining[pid] == 0:
                end_time = time + 1
                start_time = end_time - p["burst"]
                waiting_time = end_time - p["arrival"] - p["burst"]
                turnaround_time = end_time - p["arrival"]
                completed.append({
                    "pid": pid,
                    "arrival": p["arrival"],
                    "burst": p["burst"],
                    "priority": p["priority"],
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
